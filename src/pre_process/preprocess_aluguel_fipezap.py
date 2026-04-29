import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def preprocessar_fipezap_anual(path_xlsx, path_save, cidade_ibge):

    all_sheets = pd.read_excel(path_xlsx, sheet_name=None, header=3)
    resultados = []

    for nome_aba, df in all_sheets.items():

        if nome_aba in ['Resumo', 'Aux', 'Índice FipeZAP']:
            continue

        cidade = nome_aba.strip()

        if df.shape[1] < 10:
            continue

        df = df.replace(".", np.nan)

        data_col = df.columns[1]
        preco_col = df.columns[37]
        variacao_col = df.columns[27]

        df_out = df[[data_col, preco_col, variacao_col]].copy()
        df_out.columns = ['data', 'preco_aluguel_m2', 'variacao_mensal']

        # Garantir datetime
        df_out['data'] = pd.to_datetime(df_out['data'], errors='coerce')

        # Converter numéricos
        df_out['preco_aluguel_m2'] = pd.to_numeric(df_out['preco_aluguel_m2'], errors='coerce')

        df_out['variacao_mensal'] = (
            df_out['variacao_mensal']
            .astype(str)
            .str.replace('%', '')
            .str.replace(',', '.')
        )
        df_out['variacao_mensal'] = pd.to_numeric(df_out['variacao_mensal'], errors='coerce')

        df_out['cidade'] = cidade
        df_out['codigo_ibge'] = cidade_ibge.get(cidade)

        df_out = df_out.dropna(subset=['data', 'preco_aluguel_m2', 'codigo_ibge'])

        resultados.append(df_out)

    # CONCATENA MENSAL
    df_mensal = pd.concat(resultados, ignore_index=True)

    # =========================
    # 🔹 TRANSFORMA PARA ANUAL
    # =========================

    df_mensal['ano'] = df_mensal['data'].dt.year

    df_anual = (
        df_mensal
        .groupby(['codigo_ibge', 'cidade', 'ano'])
        .agg({
            'preco_aluguel_m2': 'mean'
        })
        .reset_index()
    )

    # =========================
    # 🔹 CRIA LOG E VARIAÇÃO ANUAL
    # =========================

    df_anual = df_anual.sort_values(['codigo_ibge', 'ano'])

    df_anual['log_aluguel'] = np.log(df_anual['preco_aluguel_m2'])

    df_anual['dlog_aluguel'] = (
        df_anual
        .groupby('codigo_ibge')['log_aluguel']
        .diff()
    )

    # Remove primeiro ano de cada cidade (sem variação)
    df_anual = df_anual.dropna(subset=['dlog_aluguel'])

    df_anual.to_csv(path_save, index=False)

    print(f"Arquivo anual salvo em: {path_save}")


def plot_graph_prices(capital):

    df = pd.read_csv("../data/processed/dataset_painel.csv")

    df_capital = df[df["cidade"] == capital].sort_values("ano").copy()

    # índices base 100
    df_capital["indice_cesta"] = 100 * np.exp(df_capital["dlog_cesta"].cumsum())
    df_capital["indice_ipca"] = 100 * (1 + df_capital["ipca_12m"] / 100).cumprod()
    df_capital["indice_aluguel"] = 100 * np.exp(df_capital["dlog_aluguel"].cumsum())

    # população indexada
    df_capital["indice_pop"] = 100 * (df_capital["populacao"] / df_capital["populacao"].iloc[0])

    plt.figure(figsize=(11,6))

    plt.plot(df_capital["ano"], df_capital["indice_cesta"], label="Cesta Básica")
    plt.plot(df_capital["ano"], df_capital["indice_ipca"], label="IPCA")
    plt.plot(df_capital["ano"], df_capital["indice_aluguel"], label="Aluguel")
    plt.plot(df_capital["ano"], df_capital["indice_pop"], label="População")

    plt.title(f"Evolução de Preços e População - {capital}")
    plt.xlabel("Ano")
    plt.ylabel("Índice (Base = 100)")
    plt.legend()

    plt.show()