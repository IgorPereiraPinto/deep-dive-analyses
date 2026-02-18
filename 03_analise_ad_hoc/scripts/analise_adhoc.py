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
    df = pd.read_csv(REPO_ROOT / "data/base_vendas_historica.csv", parse_dates=["data"])
    df["mes_ref"] = df["data"].dt.to_period("M").astype(str)

    receita_prod_mes = df.groupby(["produto", "mes_ref"], as_index=False)["receita"].sum()
    meses = sorted(receita_prod_mes["mes_ref"].unique())
    ultimos2 = meses[-2:]
    prev3 = meses[-5:-2]

    ult = receita_prod_mes[receita_prod_mes["mes_ref"].isin(ultimos2)].groupby("produto", as_index=False)["receita"].mean().rename(columns={"receita": "media_ultimos_2m"})
    ant = receita_prod_mes[receita_prod_mes["mes_ref"].isin(prev3)].groupby("produto", as_index=False)["receita"].mean().rename(columns={"receita": "media_3m_anteriores"})

    queda = ult.merge(ant, on="produto", how="inner")
    queda["delta_receita"] = queda["media_ultimos_2m"] - queda["media_3m_anteriores"]
    queda["delta_pct"] = (queda["delta_receita"] / queda["media_3m_anteriores"]).replace([float("inf"), -float("inf")], 0).fillna(0)
    queda = queda.sort_values("delta_receita")

    ticket_cliente = df.groupby("cliente_id", as_index=False).agg(ticket_medio=("receita", "mean"), desconto_medio=("desconto_pct", "mean"))
    corr = ticket_cliente[["ticket_medio", "desconto_medio"]].corr().iloc[0, 1]

    resumo = queda.head(10).copy()
    resumo["insight"] = "Produtos com maior queda de receita versus média histórica recente"

    detalhe = receita_prod_mes.merge(queda[["produto", "delta_receita", "delta_pct"]], on="produto", how="left")
    parametros = pd.DataFrame(
        {
            "parametro": ["janela_comparacao", "correlacao_desconto_ticket", "data_geracao"],
            "valor": [f"{ultimos2} vs {prev3}", round(float(corr), 4), datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        }
    )

    out_dir = REPO_ROOT / "03_analise_ad_hoc/outputs"
    save_portfolio_table(out_dir, "02_tabela_resultados.xlsx", resumo=resumo, detalhe=detalhe, parametros=parametros)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(queda["produto"], queda["delta_receita"], color=["#E15759" if x < 0 else "#59A14F" for x in queda["delta_receita"]])
    ax.axhline(0, color="black", linewidth=1)
    ax.set_title("Queda de Receita por Produto (2M recentes vs 3M anteriores)")
    ax.set_ylabel("Delta de Receita")
    fig.tight_layout()
    fig.savefig(out_dir / "03_grafico_principal.png", dpi=180)
    plt.close(fig)

    fig2, ax2 = plt.subplots(figsize=(8, 5))
    ax2.scatter(ticket_cliente["desconto_medio"], ticket_cliente["ticket_medio"], alpha=0.35, s=12)
    ax2.set_title("Desconto médio vs Ticket médio por cliente")
    ax2.set_xlabel("Desconto médio")
    ax2.set_ylabel("Ticket médio")
    fig2.tight_layout()
    fig2.savefig(out_dir / "04_scatter_desconto_ticket.png", dpi=180)
    plt.close(fig2)

    txt = [
        "- Investigação (a): produtos no topo da queda exigem revisão de preço, sortimento e campanhas.",
        f"- Investigação (b): correlação desconto vs ticket médio = {corr:.4f}.",
        "- Recomendação: testar elasticidade por produto e canal com desenho de experimento A/B.",
        "- Próximos testes: segmentar por regional e faixa de desconto para encontrar limiares ótimos.",
    ]
    (out_dir / "01_resumo_executivo.txt").write_text("\n".join(txt), encoding="utf-8")
    print("[OK] Análise 03 Ad hoc concluída.")


if __name__ == "__main__":
    main()
