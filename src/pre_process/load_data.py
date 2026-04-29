import pandas as pd



def diagnostico_csv(path, nrows=5, encoding='utf-8', sep=','):
    print(f'\n---- Diagnóstico do arquivo: {path} ----')
    # Usa o pandas para ler só as primeiras linhas do arquivo
    try:
        df = pd.read_csv(path, nrows=nrows, encoding=encoding, sep=sep)
    except Exception as e:
        print(f"Erro ao ler CSV: {e}")
        return
    print('Tipos detectados:')
    print(df.dtypes)
    print('\nAmostra de dados:')
    print(df.head(nrows))
    print('----------------------------\n')

def load_censo_2022(path):
    df = pd.read_csv(path, encoding='utf-8')
    df.columns = df.columns.str.strip()

    # Código IBGE
    df['municipio'] = df['id_municipio'].astype(str).str.zfill(7)

    # Nome do município
    df['nome_municipio'] = df['id_municipio_nome'].astype(str).str.strip()

    # Ano fixo
    df['ano'] = 2022

    # População
    df['pop_censo_2022'] = pd.to_numeric(df['populacao'], errors='coerce')

    df_final = df[['municipio', 'nome_municipio', 'ano', 'pop_censo_2022']].copy()

    return df_final


def load_ibge(path):
    return  pd.read_csv(path, encoding='utf-8', sep=',')