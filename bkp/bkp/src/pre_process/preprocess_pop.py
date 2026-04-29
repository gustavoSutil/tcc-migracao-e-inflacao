import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def preparar_base_anual(pop):
    df = pop.copy()


    # Selecionar colunas relevantes
    df = df[['municipio', 'nome_municipio', 'ano', 'pop_corrigida']]

    # Renomeiar
    df = df.rename(columns={
        'municipio': 'codigo_ibge',
        'pop_corrigida': 'populacao'
    })

    #Apenas até 2022
    df = df[(df['ano'] >= 2010) & (df['ano'] <= 2022)]

    # Ordenar
    df = df.sort_values(['codigo_ibge', 'ano'])

    # Crescimento populacional anual
    df['crescimento_pop'] = (
        df.groupby('codigo_ibge')['populacao']
        .pct_change()
    )

    return df

#Aplica a correção nas estimativas do DATASUS usando os censos de 2010 e 2022 como âncoras.
def aplicar_correcao(datasus, censo_2010, censo_2022):

    pop = datasus.merge(censo_2010, on=['municipio', 'ano'], how='left')
    pop = pop.merge(censo_2022, on=['municipio', 'ano'], how='left')

    pop['fator_corr'] = np.nan

    # Fator para 2010 (Censo)
    pop.loc[pop['ano'] == 2010, 'fator_corr'] = (
            pop.loc[pop['ano'] == 2010, 'pop_censo_2010'] / pop.loc[pop['ano'] == 2010, 'pop_datasus']
    )

    # Fator para 2022 (Censo)
    pop.loc[pop['ano'] == 2022, 'fator_corr'] = (
            pop.loc[pop['ano'] == 2022, 'pop_censo_2022'] / pop.loc[pop['ano'] == 2022, 'pop_datasus']
    )

    # Interpolação linear do fator de correção
    pop['fator_corr'] = pop.groupby('municipio')['fator_corr'].transform(
        lambda x: x.interpolate().ffill().bfill()
    )

    # População corrigida
    pop['pop_corrigida'] = pop['pop_datasus'] * pop['fator_corr']

    return pop

# Gera gráfico da distribuição do erro relativo entre DATASUS e População Corrigida.
def gerar_grafico_erro(pop, path_save=None):
    pop['erro_relativo'] = (
        (pop['pop_corrigida'] - pop['pop_datasus']) / pop['pop_datasus']
    )

    plt.figure(figsize=(10, 6))
    sns.histplot(pop['erro_relativo'], bins=50, kde=True)
    plt.title('Distribuição do Erro Relativo - População Corrigida vs DATASUS')
    plt.xlim(-0.01, 0.01)
    plt.xlabel('Erro Relativo')
    plt.ylabel('Frequência')

    if path_save:
        plt.savefig(path_save)

    plt.show()

def gerar_populacao_geom_censos(censo_2010, censo_2022):
    """
    Gera população anual 2010–2022 usando crescimento geométrico
    entre os censos.
    """

    # Merge dos dois censos
    df = censo_2010.merge(
        censo_2022[['municipio', 'pop_censo_2022', 'nome_municipio']],
        on='municipio',
        how='inner'
    )

    df = df.rename(columns={
        'pop_censo_2010': 'pop_2010',
        'pop_censo_2022': 'pop_2022'
    })

    resultados = []

    for _, row in df.iterrows():
        cod = row['municipio']
        nome = row['nome_municipio']
        pop_2010 = row['pop_2010']
        pop_2022 = row['pop_2022']

        if pop_2010 > 0 and pop_2022 > 0:

            # taxa geométrica anual
            g = (pop_2022 / pop_2010) ** (1/12) - 1

            for ano in range(2010, 2023):
                pop_t = pop_2010 * ((1 + g) ** (ano - 2010))

                resultados.append({
                    'codigo_ibge': cod,
                    'nome_municipio': nome,
                    'ano': ano,
                    'populacao': pop_t,
                    'crescimento_pop': g
                })

    df_final = pd.DataFrame(resultados)

    return df_final

def grafico_populacao_municipio(pop, codigo_ibge, path_save=None):
    # Filtra município e período intercensitário
    df = pop[
        (pop['municipio'] == codigo_ibge) &
        (pop['ano'] >= 2010) &
        (pop['ano'] <= 2022)
    ].sort_values('ano')

    if df.empty:
        print(f"Nenhum dado encontrado para o município {codigo_ibge}")
        return

    nome = (
        df['nome_municipio'].dropna().iloc[0]
        if df['nome_municipio'].notna().any()
        else "Município"
    )

    plt.figure(figsize=(10, 6))

    # Série DATASUS
    if 'pop_datasus' in df.columns:
        plt.plot(
            df['ano'],
            df['pop_datasus'],
            label='DATASUS (Estimativa)',
            marker='o'
        )

    # Série Corrigida
    if 'pop_corrigida' in df.columns:
        plt.plot(
            df['ano'],
            df['pop_corrigida'],
            label='População Corrigida',
            marker='x'
        )

    # Censo 2010
    if 'pop_censo_2010' in df.columns:
        df_2010 = df[df['ano'] == 2010]
        if not df_2010.empty and not df_2010['pop_censo_2010'].isna().all():
            plt.scatter(
                2010,
                df_2010['pop_censo_2010'].values[0],
                label='Censo 2010',
                s=120,
                zorder=5
            )

    # Censo 2022
    if 'pop_censo_2022' in df.columns:
        df_2022 = df[df['ano'] == 2022]
        if not df_2022.empty and not df_2022['pop_censo_2022'].isna().all():
            plt.scatter(
                2022,
                df_2022['pop_censo_2022'].values[0],
                label='Censo 2022',
                s=120,
                zorder=5
            )

    plt.title(f'População — {nome} ({codigo_ibge})')
    plt.xlabel('Ano')
    plt.ylabel('População')
    plt.legend()
    plt.grid(True)

    if path_save:
        plt.savefig(path_save)

    plt.show()


def grafico_populacao_geom(df_geom, codigo_ibge, path_save=None):
    """
    Plota a população estimada por crescimento geométrico
    (2010–2022) para um município específico.

    df_geom: dataframe gerado por gerar_populacao_geom_censos()
    codigo_ibge: código do município
    """

    # Filtra município
    df = df_geom[df_geom['codigo_ibge'] == codigo_ibge].sort_values('ano')

    if df.empty:
        print(f"Nenhum dado encontrado para o município {codigo_ibge}")
        return

    nome = df['nome_municipio'].iloc[0]

    plt.figure(figsize=(10, 6))

    # Curva geométrica
    plt.plot(
        df['ano'],
        df['populacao'],
        label='População (Crescimento Geométrico)',
        marker='o'
    )

    # Pontos Censo 2010
    pop_2010 = df[df['ano'] == 2010]['populacao'].values[0]
    plt.scatter(
        2010,
        pop_2010,
        label='Censo 2010',
        s=120,
        zorder=5
    )

    # Pontos Censo 2022
    pop_2022 = df[df['ano'] == 2022]['populacao'].values[0]
    plt.scatter(
        2022,
        pop_2022,
        label='Censo 2022',
        s=120,
        zorder=5
    )

    plt.title(f'População — {nome} ({codigo_ibge})')
    plt.xlabel('Ano')
    plt.ylabel('População')
    plt.legend()
    plt.grid(True)

    if path_save:
        plt.savefig(path_save, bbox_inches='tight')

    plt.show()



def construir_populacao_corrigida(df_est, df_censo):

    df = df_est.copy()
    df = df.sort_values(["codigo_ibge", "ano"])

    # =========================
    # 1. PADRONIZAR CENSO
    # =========================
    df_censo = df_censo.rename(columns={
        "municipio": "codigo_ibge",
        "pop_censo_2022": "pop_real_2022"
    })

    df_censo["codigo_ibge"] = df_censo["codigo_ibge"].astype(int)

    # =========================
    # 2. POP 2021 (BASE)
    # =========================
    pop_2021 = df[df["ano"] == 2021][
        ["codigo_ibge", "populacao"]
    ].rename(columns={"populacao": "pop_est_2021"})

    # =========================
    # 3. MERGES
    # =========================
    df = df.merge(pop_2021, on="codigo_ibge", how="left")

    df = df.merge(
        df_censo[["codigo_ibge", "pop_real_2022"]],
        on="codigo_ibge",
        how="left"
    )

    # =========================
    # 4. ERRO
    # =========================
    df["erro_total"] = df["pop_real_2022"] / df["pop_est_2021"]

    # =========================
    # 5. CORREÇÃO PROGRESSIVA
    # =========================
    ano_base = 2010
    ano_final = 2022

    df["peso_tempo"] = (df["ano"] - ano_base) / (ano_final - ano_base)
    df["peso_tempo"] = df["peso_tempo"].clip(0, 1)

    df["fator_correcao"] = df["erro_total"] ** df["peso_tempo"]

    df["pop_corrigida"] = np.where(
        df["ano"] < 2022,
        df["populacao"] * df["fator_correcao"],
        df["populacao"]
    )

    # FORÇAR 2022 = CENSO REAL
    df["pop_corrigida"] = np.where(
        df["ano"] == 2022,
        df["pop_real_2022"],
        df["pop_corrigida"]
    )

    df = df[df["ano"] <= 2022]

    # =========================
    # 6. LOGS
    # =========================
    df["log_pop_corr"] = np.log(df["pop_corrigida"])

    df["dlog_pop_corr"] = (
        df.groupby("codigo_ibge")["log_pop_corr"]
        .diff()
    )

    # =========================
    # 7. OUTPUT
    # =========================
    return df[[
        "codigo_ibge",
        "ano",
        "pop_corrigida",
        "log_pop_corr",
        "dlog_pop_corr"
    ]]