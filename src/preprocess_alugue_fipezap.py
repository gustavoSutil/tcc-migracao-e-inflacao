import pandas as pd
import numpy as np

def preprocessar_fipezap(path_xlsx, path_save, cidade_ibge):
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

        # Numeric
        df_out['preco_aluguel_m2'] = pd.to_numeric(df_out['preco_aluguel_m2'], errors='coerce')
        df_out['variacao_mensal'] = df_out['variacao_mensal'].astype(str).str.replace('%', '').str.replace(',', '.').astype(float)

        df_out['cidade'] = cidade
        df_out['codigo_ibge'] = cidade_ibge.get(cidade)
        resultados.append(df_out)
        df_out.dropna(subset=['data', 'preco_aluguel_m2', 'codigo_ibge'])

    df_final = pd.concat(resultados, ignore_index=True)
    df_final.to_csv(path_save, index=False)
    print(f"Arquivo salvo em: {path_save}")


cidade_ibge = {
    "São Paulo": "3550308",
    "Barueri": "3505708",
    "Campinas": "3509502",
    "Diadema": "3513801",
    "Guarujá": "3518702",
    "Guarulhos": "3518801",
    "Osasco": "3534401",
    "Praia Grande": "3541007",
    "Ribeirão Preto": "3543409",
    "Santo André": "3547809",
    "Santos": "3548500",
    "São Bernardo do Campo": "3548708",
    "São Caetano do Sul": "3548807",
    "São José do Rio Preto": "3549805",
    "São José dos Campos": "3549904",
    "São Vicente": "3551009",
    "Rio de Janeiro": "3304557",
    "Niterói": "3303302",
    "Belo Horizonte": "3106200",
    "Betim": "3106705",
    "Contagem": "3118601",
    "Porto Alegre": "4314902",
    "Canoas": "4304606",
    "Caxias do Sul": "4305108",
    "Novo Hamburgo": "4313400",
    "Pelotas": "4314408",
    "Santa Maria": "4316908",
    "São Leopoldo": "4318706",
    "Curitiba": "4106902",
    "Londrina": "4113700",
    "São José dos Pinhais": "4125506",
    "Florianópolis": "4205407",
    "Balneário Camboriú": "4202008",
    "Blumenau": "4202404",
    "Itajaí": "4208203",
    "Itapema": "4208302",
    "Joinville": "4209102",
    "São José": "4216602",   # São José (SC)
    "Vitória": "3205309",
    "Vila Velha": "3205200",
    "Brasília": "5300108",
    "Goiânia": "5208707",
    "Campo Grande": "5002704",
    "Cuiabá": "5103403",
    "Aracaju": "2800308",
    "Fortaleza": "2304400",
    "João Pessoa": "2507507",
    "Maceió": "2704302",
    "Natal": "2408102",
    "Recife": "2611606",
    "Salvador": "2927408",
    "São Luís": "2111300",
    "Teresina": "2211001",
    "Jaboatão dos Guararapes": "2607901",
    "Belém": "1501402",
    "Manaus": "1302603"
}

mes_map = {
    'jan': '01',
    'fev': '02',
    'mar': '03',
    'abr': '04',
    'mai': '05',
    'jun': '06',
    'jul': '07',
    'ago': '08',
    'set': '09',
    'out': '10',
    'nov': '11',
    'dez': '12'
}

preprocessar_fipezap('../data/raw/aluguel_por_cidade_fipezap.xlsx', '../data/processed/aluguel_fipezap.csv', cidade_ibge)
