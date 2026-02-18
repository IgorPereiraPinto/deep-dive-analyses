from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional, Union

import pandas as pd


def ensure_parent_dir(filepath: Union[str, Path]) -> Path:
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def save_excel_with_sheets(
    filepath: Union[str, Path],
    sheets: Dict[str, pd.DataFrame],
    *,
    index: bool = False,
    engine: str = "openpyxl",
    freeze_panes: Optional[tuple] = (1, 0),
) -> Path:
    out_path = ensure_parent_dir(filepath)

    normalized_sheets = {}
    for name, df in sheets.items():
        normalized_sheets[str(name)[:31]] = df.copy()

    with pd.ExcelWriter(out_path, engine=engine) as writer:
        for sheet_name, df in normalized_sheets.items():
            df.to_excel(writer, sheet_name=sheet_name, index=index)

        try:
            workbook = writer.book
            for sheet_name in normalized_sheets.keys():
                ws = workbook[sheet_name]
                if freeze_panes is not None:
                    row, col = freeze_panes
                    ws.freeze_panes = ws.cell(row=row + 1, column=col + 1)
        except Exception:
            pass

    return out_path


def save_portfolio_table(
    outputs_dir: Union[str, Path],
    filename: str,
    resumo: pd.DataFrame,
    detalhe: pd.DataFrame,
    parametros: Optional[pd.DataFrame] = None,
    *,
    index: bool = False,
) -> Path:
    outputs_dir = Path(outputs_dir)
    outputs_dir.mkdir(parents=True, exist_ok=True)

    sheets = {"resumo": resumo, "detalhe": detalhe}
    if parametros is not None:
        sheets["parametros"] = parametros

    return save_excel_with_sheets(outputs_dir / filename, sheets, index=index)
