import numpy as np


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