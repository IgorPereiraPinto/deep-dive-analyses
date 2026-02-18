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
    df = pd.read_csv(REPO_ROOT / "data/base_vendas_historica.csv")
    assert df["receita"].ge(0).all(), "Receita inválida para pareto."

    det = df.groupby("cliente_id", as_index=False)["receita"].sum().sort_values("receita", ascending=False)
    det["pct_receita"] = det["receita"] / det["receita"].sum()
    det["pct_acumulado"] = det["pct_receita"].cumsum()
    det["classe_abc"] = pd.cut(det["pct_acumulado"], bins=[-0.001, 0.8, 0.95, 1.0], labels=["A", "B", "C"])

    resumo = pd.DataFrame(
        {
            "kpi": ["clientes_total", "receita_total", "top_10_participacao", "classe_A_participacao"],
            "valor": [
                int(det["cliente_id"].nunique()),
                float(det["receita"].sum()),
                float(det.head(10)["receita"].sum() / det["receita"].sum()),
                float(det[det["classe_abc"] == "A"]["receita"].sum() / det["receita"].sum()),
            ],
        }
    )
    parametros = pd.DataFrame(
        {
            "parametro": ["regra_abc", "data_geracao"],
            "valor": ["A até 80%, B até 95%, C restante", datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        }
    )

    out_dir = REPO_ROOT / "02_analise_pareto_abc/outputs"
    save_portfolio_table(out_dir, "02_tabela_resultados.xlsx", resumo=resumo, detalhe=det, parametros=parametros)

    plot_df = det.head(50).copy()
    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax1.bar(plot_df.index.astype(str), plot_df["receita"], color="#4E79A7")
    ax1.set_ylabel("Receita")
    ax1.set_xticks([])
    ax2 = ax1.twinx()
    ax2.plot(plot_df.index.astype(str), (plot_df["pct_acumulado"] * 100), color="#E15759", linewidth=2)
    ax2.axhline(80, color="gray", linestyle="--", linewidth=1)
    ax2.axhline(95, color="gray", linestyle=":", linewidth=1)
    ax2.set_ylabel("% acumulado")
    ax1.set_title("Pareto de Receita por Cliente (Top 50)")
    fig.tight_layout()
    fig.savefig(out_dir / "03_grafico_principal.png", dpi=180)
    plt.close(fig)

    txt = [
        "- A concentração de receita está elevada nos clientes classe A.",
        "- Risco: dependência de poucos clientes para sustentar o faturamento.",
        "- Ação: estratégia de retenção premium para A e desenvolvimento de carteira B.",
        "- Ação: campanhas de upsell para migrar clientes C para B.",
    ]
    (out_dir / "01_resumo_executivo.txt").write_text("\n".join(txt), encoding="utf-8")
    print("[OK] Análise 02 Pareto/ABC concluída.")


if __name__ == "__main__":
    main()
