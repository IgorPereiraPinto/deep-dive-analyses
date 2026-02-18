from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(REPO_ROOT))

from src.utils.excel import save_portfolio_table


def main() -> None:
    vendas = pd.read_csv(REPO_ROOT / "data/base_vendas_historica.csv", parse_dates=["data"])
    forecast = pd.read_csv(REPO_ROOT / "data/forecast_mensal.csv")

    vendas["mes_ref"] = vendas["data"].dt.to_period("M").astype(str)
    real_mensal = vendas.groupby("mes_ref", as_index=False)["receita"].sum().rename(columns={"receita": "realizado"})
    meta_mensal = forecast.groupby("mes_ref", as_index=False)["meta_receita"].sum().rename(columns={"meta_receita": "meta"})

    resumo = real_mensal.merge(meta_mensal, on="mes_ref", how="inner")
    resumo["gap"] = resumo["realizado"] - resumo["meta"]
    resumo["gap_pct"] = (resumo["gap"] / resumo["meta"]).round(4)

    real_det = vendas.groupby(["mes_ref", "canal", "regional", "produto"], as_index=False)["receita"].sum().rename(columns={"receita": "realizado"})
    detalhe = real_det.merge(forecast, on=["mes_ref", "canal", "regional", "produto"], how="left")
    detalhe["gap"] = detalhe["realizado"] - detalhe["meta_receita"]
    detalhe["gap_pct"] = (detalhe["gap"] / detalhe["meta_receita"]).replace([float("inf"), -float("inf")], 0).fillna(0)

    assert resumo["meta"].gt(0).all() and detalhe["meta_receita"].notna().all(), "Sanity check de metas falhou."

    parametros = pd.DataFrame(
        {
            "parametro": ["granularidade", "fonte_meta", "data_geracao"],
            "valor": ["mes_ref e decomposição por canal/regional/produto", "data/forecast_mensal.csv", datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        }
    )

    out_dir = REPO_ROOT / "04_indicadores_vendas_mensal/outputs"
    save_portfolio_table(out_dir, "02_tabela_resultados.xlsx", resumo=resumo, detalhe=detalhe, parametros=parametros)

    fig, ax = plt.subplots(figsize=(12, 6))
    x = range(len(resumo))
    ax.plot(x, resumo["realizado"], marker="o", label="Realizado")
    ax.plot(x, resumo["meta"], marker="o", label="Meta")
    for i, g in enumerate(resumo["gap"]):
        ax.vlines(i, resumo.loc[i, "meta"], resumo.loc[i, "realizado"], colors="#E15759" if g < 0 else "#59A14F", linewidth=2)
    ax.set_xticks(list(x))
    ax.set_xticklabels(resumo["mes_ref"], rotation=45)
    ax.set_title("Realizado vs Meta por Mês")
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_dir / "03_grafico_principal.png", dpi=180)
    plt.close(fig)

    top_drivers = detalhe.groupby("produto", as_index=False)["gap"].sum().sort_values("gap")
    txt = [
        "- Driver principal do gap negativo: " + str(top_drivers.iloc[0]["produto"]),
        "- Driver principal do gap positivo: " + str(top_drivers.iloc[-1]["produto"]),
        "- Plano de ação: atacar gaps negativos com revisão de mix, preço e execução comercial por canal/regional.",
        "- Plano de ação: capturar oportunidades de produtos acima da meta com expansão tática.",
    ]
    (out_dir / "01_resumo_executivo.txt").write_text("\n".join(txt), encoding="utf-8")
    print("[OK] Análise 04 Indicadores concluída.")


if __name__ == "__main__":
    main()
