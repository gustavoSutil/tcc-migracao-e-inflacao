import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def aplicar_correcao(datasus, censo_2010, censo_2022):
    """
    Aplica a correção nas estimativas do DATASUS usando os censos de 2010 e 2022 como âncoras.
    """
    # 🔗 Merge das bases
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


def gerar_grafico_erro(pop, path_save=None):
    """
    Gera gráfico da distribuição do erro relativo entre DATASUS e População Corrigida.
    """
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

def interpolar_mensal(pop):
    """
    Interpola a população mensalmente entre os anos.
    """
    pop['data'] = pd.to_datetime(pop['ano'].astype(str) + '-01-01')

    out = []
    for mun, g in pop.groupby('municipio'):
        g = g.set_index('data').sort_index()
        g = g[['pop_corrigida']].resample('MS').interpolate()
        g['municipio'] = mun
        out.append(g)

    df_out = pd.concat(out).reset_index().rename(columns={'index': 'data'})
    return df_out


def grafico_populacao_floripa(pop, df_mensal=None, path_save=None):
    cod_floripa = '4205407'
    df = pop[pop['municipio'] == cod_floripa].sort_values('ano')

    plt.figure(figsize=(10, 6))
    plt.plot(df['ano'], df['pop_datasus'], label='DATASUS (Estimativa)', marker='o')
    plt.plot(df['ano'], df['pop_corrigida'], label='Corrigida/Interpolada', marker='x')

    # Pontos dos censos
    if 'pop_censo_2010' in df.columns and not df[df['ano'] == 2010]['pop_censo_2010'].isna().all():
        plt.scatter([2010], df.loc[df['ano'] == 2010, 'pop_censo_2010'], color='red', label='Censo 2010', s=100, zorder=5)
    if 'pop_censo_2022' in df.columns and not df[df['ano'] == 2022]['pop_censo_2022'].isna().all():
        plt.scatter([2022], df.loc[df['ano'] == 2022, 'pop_censo_2022'], color='violet', label='Censo 2022', s=100, zorder=5)

    # Interpolação mensal: use o ano da data
    if df_mensal is not None:
        df_mensal_floripa = df_mensal[df_mensal['municipio'] == cod_floripa]
        plt.plot(
            df_mensal_floripa['data'].dt.year + (df_mensal_floripa['data'].dt.month - 1)/12,
            df_mensal_floripa['pop_corrigida'],
            label='Interpolação Mensal',
            color='green',
            alpha=0.6,
            linewidth=2
        )

    plt.title('População de Florianópolis (4205407) — DATASUS, Censo, Interpolação')
    plt.xlabel('Ano')
    plt.ylabel('População')
    plt.legend()
    plt.grid(True)
    if path_save:
        plt.savefig(path_save)
    plt.show()