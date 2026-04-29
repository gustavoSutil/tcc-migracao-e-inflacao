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


def load_datasus(path, censo_2022):
    df = pd.read_csv(path, sep=';', encoding='utf-8')
    df.columns = df.columns.str.replace('"', '').str.strip()
    df = df.melt(id_vars='Municipio', var_name='ano', value_name='pop_datasus')
    df['codigo6'] = df['Municipio'].astype(str).str.extract(r'^(\d{6})')
    df['ano'] = df['ano'].astype(int)
    df['pop_datasus'] = pd.to_numeric(df['pop_datasus'], errors='coerce')
    # Merge para pegar o código IBGE correto
    censo_2022['codigo6'] = censo_2022['municipio'].astype(str).str[:6]
    df = df.merge(censo_2022[['codigo6', 'municipio']], on='codigo6', how='left')
    df = df.drop(columns=['Municipio', 'codigo6'])
    return df

def load_censo_2010_2012(path, censo_2022):
    df = pd.read_csv(path, sep=';', encoding='latin1')
    df.columns = df.columns.str.replace('"', '').str.strip()
    df = df.melt(id_vars='Municipio', var_name='ano', value_name='pop_censo')
    df['codigo6'] = df['Municipio'].astype(str).str.extract(r'^(\d{6})')
    df['ano'] = df['ano'].astype(int)
    df['pop_censo'] = pd.to_numeric(df['pop_censo'], errors='coerce')
    df = df[df['ano'] == 2010].copy()
    df = df.rename(columns={'pop_censo': 'pop_censo_2010'})
    # Merge pelo código6 para pegar o IBGE correto
    censo_2022['codigo6'] = censo_2022['municipio'].astype(str).str[:6]
    df = df.merge(censo_2022[['codigo6', 'municipio']], on='codigo6', how='left')
    df = df.drop(columns=['Municipio', 'codigo6'])
    return df[['municipio', 'ano', 'pop_censo_2010']]

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