from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple


REPO_ROOT = Path(__file__).resolve().parent

ANALYSES = [
    "01_analise_safra",
    "02_analise_pareto_abc",
    "03_analise_ad_hoc",
    "04_indicadores_vendas_mensal",
]

REQUIRED_OUTPUT_FILES = [
    "01_resumo_executivo.txt",
    "02_tabela_resultados.xlsx",
    "03_grafico_principal.png",
]


@dataclass
class ValidationIssue:
    analysis: str
    missing_files: List[str]
    outputs_dir: Path


def _check_analysis_outputs(analysis_dir: Path) -> Tuple[bool, List[str]]:
    outputs_dir = analysis_dir / "outputs"
    missing: List[str] = []

    if not outputs_dir.exists() or not outputs_dir.is_dir():
        return False, REQUIRED_OUTPUT_FILES.copy()

    for fname in REQUIRED_OUTPUT_FILES:
        if not (outputs_dir / fname).exists():
            missing.append(fname)

    return (len(missing) == 0), missing


def main() -> int:
    issues: List[ValidationIssue] = []

    for analysis in ANALYSES:
        analysis_dir = REPO_ROOT / analysis
        ok, missing = _check_analysis_outputs(analysis_dir)
        if not ok:
            issues.append(
                ValidationIssue(
                    analysis=analysis,
                    missing_files=missing,
                    outputs_dir=analysis_dir / "outputs",
                )
            )

    if issues:
        print("\n❌ Quality Gate FAILED — outputs obrigatórios ausentes.\n")
        for issue in issues:
            print(f"- {issue.analysis}")
            print(f"  outputs/: {issue.outputs_dir}")
            for mf in issue.missing_files:
                print(f"   • faltando: {mf}")
            print()
        print("Ação: gere os outputs faltantes e execute novamente: python validate_outputs.py\n")
        return 1

    print("\n✅ Quality Gate PASSED — todos os outputs obrigatórios estão presentes.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
