import pandas as pd

def process_cesta_basica(input_path: str, output_path: str, cidade_ibge):

    df = pd.read_csv(
        input_path,
        sep=";",
        encoding="utf-8"
    )

    df = df.rename(columns={df.columns[0]: "date"})

    df_long = df.melt(
        id_vars="date",
        var_name="cidade",
        value_name="cesta_basica"
    )

    df_long["date"] = pd.to_datetime(df_long["date"], format="%m-%Y")

    df_long["ano"] = df_long["date"].dt.year

    df_long["cesta_basica"] = (
        df_long["cesta_basica"]
        .astype(str)
        .str.replace(",", ".", regex=False)
    )

    df_long["cesta_basica"] = pd.to_numeric(df_long["cesta_basica"], errors="coerce")

    df_long = df_long.dropna(subset=["cesta_basica"])

    df_year = (
        df_long
        .groupby(["cidade", "ano"], as_index=False)
        ["cesta_basica"]
        .mean()
    )

    # adicionar codigo ibge
    df_year["codigo_ibge"] = df_year["cidade"].map(cidade_ibge)

    # verificar cidades sem código
    missing = df_year[df_year["codigo_ibge"].isna()]["cidade"].unique()

    if len(missing) > 0:
        print("⚠️ Cidades sem código IBGE:")
        for c in missing:
            print(c)

    df_year.to_csv(output_path, index=False)

    return df_year