from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class DataGenConfig:
    """Configuração da geração de dados sintéticos."""

    seed: int = 42
    start_date: str = "2023-01-01"
    end_date: str = "2024-12-31"
    n_rows: int = 90000
    n_clients: int = 4500


REPO_ROOT = Path(__file__).resolve().parent
DATA_DIR = REPO_ROOT / "data"


def _validate_sales_schema(df: pd.DataFrame) -> None:
    expected = {
        "data",
        "mes_ref",
        "cliente_id",
        "produto",
        "canal",
        "regional",
        "quantidade",
        "receita",
        "custo",
        "desconto_pct",
    }
    missing = expected - set(df.columns)
    if missing:
        raise ValueError(f"Schema incompleto em vendas: {sorted(missing)}")

    if df.isna().sum().sum() > 0:
        raise ValueError("Há nulos na base de vendas.")

    dup = df.duplicated().sum()
    if dup > 0:
        raise ValueError(f"Há {dup} linhas duplicadas na base de vendas.")

    if not df["desconto_pct"].between(0, 0.25).all():
        raise ValueError("desconto_pct fora do range [0, 0.25].")

    if (df[["quantidade", "receita", "custo"]] <= 0).any().any():
        raise ValueError("quantidade/receita/custo devem ser positivos.")


def _validate_forecast_schema(df: pd.DataFrame) -> None:
    expected = {"mes_ref", "canal", "regional", "produto", "meta_receita", "forecast_receita"}
    missing = expected - set(df.columns)
    if missing:
        raise ValueError(f"Schema incompleto em forecast: {sorted(missing)}")

    if df.isna().sum().sum() > 0:
        raise ValueError("Há nulos na base de forecast.")

    if df.duplicated(["mes_ref", "canal", "regional", "produto"]).sum() > 0:
        raise ValueError("Há duplicidades na chave mes_ref/canal/regional/produto.")


def generate_sample_data(config: DataGenConfig) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Gera dados sintéticos determinísticos para vendas históricas e forecast."""

    rng = np.random.default_rng(config.seed)
    dates = pd.date_range(config.start_date, config.end_date, freq="D")

    produtos = np.array(["Notebook", "Smartphone", "Tablet", "Monitor", "Acessorios", "Software"])
    canais = np.array(["Online", "Loja", "Marketplace", "Inside Sales"])
    regionais = np.array(["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"])

    sampled_dates = rng.choice(dates, size=config.n_rows, replace=True)
    cliente_id = rng.integers(10000, 10000 + config.n_clients, size=config.n_rows)
    produto = rng.choice(produtos, size=config.n_rows, p=[0.2, 0.26, 0.1, 0.14, 0.18, 0.12])
    canal = rng.choice(canais, size=config.n_rows, p=[0.38, 0.28, 0.22, 0.12])
    regional = rng.choice(regionais, size=config.n_rows)

    quantidade = rng.integers(1, 8, size=config.n_rows)
    preco_base = pd.Series(produto).map(
        {
            "Notebook": 4200,
            "Smartphone": 2600,
            "Tablet": 1800,
            "Monitor": 1400,
            "Acessorios": 420,
            "Software": 900,
        }
    ).to_numpy(dtype=float)

    sazonal = 1 + (pd.DatetimeIndex(sampled_dates).month.to_numpy() - 6) * 0.01
    desconto_pct = rng.uniform(0, 0.25, size=config.n_rows).round(4)
    receita = (quantidade * preco_base * sazonal * (1 - desconto_pct) * rng.normal(1.0, 0.08, size=config.n_rows)).clip(min=30)
    custo = (receita * rng.uniform(0.55, 0.82, size=config.n_rows)).clip(min=10)

    sales = pd.DataFrame(
        {
            "data": pd.to_datetime(sampled_dates),
            "cliente_id": cliente_id,
            "produto": produto,
            "canal": canal,
            "regional": regional,
            "quantidade": quantidade,
            "receita": receita.round(2),
            "custo": custo.round(2),
            "desconto_pct": desconto_pct,
        }
    ).sort_values("data", ignore_index=True)
    sales["mes_ref"] = sales["data"].dt.to_period("M").astype(str)
    sales = sales[
        [
            "data",
            "mes_ref",
            "cliente_id",
            "produto",
            "canal",
            "regional",
            "quantidade",
            "receita",
            "custo",
            "desconto_pct",
        ]
    ]

    monthly = (
        sales.groupby(["mes_ref", "canal", "regional", "produto"], as_index=False)["receita"].sum().rename(columns={"receita": "realizado"})
    )
    monthly["meta_receita"] = (monthly["realizado"] * rng.uniform(0.95, 1.08, size=len(monthly))).round(2)
    monthly["forecast_receita"] = (monthly["meta_receita"] * rng.uniform(0.96, 1.04, size=len(monthly))).round(2)
    forecast = monthly[["mes_ref", "canal", "regional", "produto", "meta_receita", "forecast_receita"]].copy()

    _validate_sales_schema(sales)
    _validate_forecast_schema(forecast)

    return sales, forecast


def main() -> None:
    config = DataGenConfig()
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    sales, forecast = generate_sample_data(config)

    sales_path = DATA_DIR / "base_vendas_historica.csv"
    forecast_path = DATA_DIR / "forecast_mensal.csv"

    sales.to_csv(sales_path, index=False, encoding="utf-8")
    forecast.to_csv(forecast_path, index=False, encoding="utf-8")

    print("[OK] Dados sintéticos gerados com seed=42")
    print(f"- vendas: {sales_path} | linhas={len(sales)} | receita_total={sales['receita'].sum():,.2f}")
    print(f"- forecast: {forecast_path} | linhas={len(forecast)} | meta_total={forecast['meta_receita'].sum():,.2f}")


if __name__ == "__main__":
    main()
