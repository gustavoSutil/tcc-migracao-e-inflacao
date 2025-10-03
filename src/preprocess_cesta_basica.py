import pandas as pd
import re


def processar_cesta_basica(path_csv):
    # Lê o arquivo, atenção para decimal e separador!
    df = pd.read_csv(path_csv, sep=';', decimal=',')

    # Renomeia a primeira coluna para 'data'
    if df.columns[0] != 'data':
        df = df.rename(columns={df.columns[0]: 'data'})

    # Remove linhas sem data
    df = df[df['data'].notnull()]

    # De wide para long
    df_long = df.melt(id_vars='data', var_name='cidade', value_name='preco_cesta')

    df_long['data'] = df_long['data'].astype(str).str.extract(r'(\d{2}-\d{4})')

    # Remove linhas onde data ficou vazia após o regex
    df_long = df_long[df_long['data'].notnull()]

    # Agora converte para datetime
    df_long['data'] = pd.to_datetime(df_long['data'], format='%m-%Y')

    # Corrige para float
    df_long['preco_cesta'] = pd.to_numeric(df_long['preco_cesta'].replace(',', '.'), errors='coerce')

    # Remove NaN em preço
    df_long = df_long.dropna(subset=['preco_cesta'])

    return df_long


df_cesta = processar_cesta_basica('../data/raw/cesta_basica_cidade.csv')

cidade_ibge = {
    "Aracaju": "2800308",
    "Belém": "1501402",
    "Belo Horizonte": "3106200",
    "Boa Vista": "1400100",
    "Brasília": "5300108",
    "Campo Grande": "5002704",
    "Cuiabá": "5103403",
    "Curitiba": "4106902",
    "Florianópolis": "4205407",
    "Fortaleza": "2304400",
    "Goiânia": "5208707",
    "João Pessoa": "2507507",
    "Macapá": "1600303",
    "Maceió": "2704302",
    "Manaus": "1302603",
    "Natal": "2408102",
    "Palmas": "1721000",
    "Porto Alegre": "4314902",
    "Porto Velho": "1100205",
    "Recife": "2611606",
    "Rio Branco": "1200401",
    "Rio de Janeiro": "3304557",
    "Salvador": "2927408",
    "São Luís": "2111300",
    "São Paulo": "3550308",
    "Teresina": "2211001",
    "Vitória": "3205309",
    "Macaé": "3302403"
}

df_cesta['codigo_ibge'] = df_cesta['cidade'].map(cidade_ibge)

df_cesta.to_csv('../data/processed/cesta_basica_long.csv', index=False)
