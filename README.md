# Deep Dive Analyses — Python + SQL Server (Análises Avançadas de Vendas)

Portfólio executável com dados sintéticos determinísticos para demonstrar análises avançadas de vendas em Python, com estrutura pronta para integração futura com SQL Server.

## 1) Visão executiva

### Contexto
Empresas com alta complexidade comercial precisam entender retenção de clientes, concentração de receita, anomalias de performance e aderência a metas.

### Achados esperados
- Coortes com maior e menor retenção para orientar CRM e lifecycle.
- Nível de concentração de receita por cliente (Pareto/ABC) para avaliar risco.
- Produtos com queda recente de receita e relação desconto vs ticket médio.
- Meses e dimensões com gap entre realizado e meta/forecast.

### Impacto
As análises fornecem priorização objetiva de ações comerciais e reduzem tempo de diagnóstico em reuniões executivas.

### Decisão
Com os outputs, o negócio pode definir foco tático por coorte, por carteira, por produto e por dimensão comercial (canal/regional).

### Próximos passos
- Conectar com SQL Server para leitura direta de fatos e dimensões.
- Incluir testes estatísticos e monitoramento contínuo dos indicadores.
- Evoluir para dashboard Power BI com refresh automatizado.

## 2) Estrutura do repositório

```text
/
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example
├── generate_sample_data.py
├── validate_outputs.py
├── src/
│   └── utils/
│       ├── __init__.py
│       └── excel.py
├── data/
├── 01_analise_safra/
├── 02_analise_pareto_abc/
├── 03_analise_ad_hoc/
└── 04_indicadores_vendas_mensal/
```

## 3) Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 4) Execução (ordem obrigatória)

```bash
python generate_sample_data.py
python 01_analise_safra/scripts/analise_safra.py
python 02_analise_pareto_abc/scripts/analise_pareto.py
python 03_analise_ad_hoc/scripts/analise_adhoc.py
python 04_indicadores_vendas_mensal/scripts/analise_indicadores.py
python validate_outputs.py
```

## 5) Checklist de aderência

- [x] Estrutura de pastas e arquivos conforme especificação
- [x] Dependências mínimas declaradas em `requirements.txt`
- [x] Geração de dados sintéticos determinísticos (`seed=42`)
- [x] Volume da base dentro de faixa moderada (60k–120k)
- [x] Quatro análises implementadas (01–04)
- [x] Cada análise gera TXT + XLSX + PNG em `outputs/`
- [x] XLSX de cada análise com abas `resumo`, `detalhe`, `parametros`
- [x] Quality gate `validate_outputs.py` em execução PASS
- [x] Documentação executiva e técnica em PT-BR

## 6) Como interpretar outputs

Cada análise salva 3 artefatos obrigatórios em `<analise>/outputs/`:

1. **01_resumo_executivo.txt**
   - Leitura rápida para decisão (insights, risco, ação e próximos passos).
2. **02_tabela_resultados.xlsx**
   - **resumo:** principais KPIs para priorização.
   - **detalhe:** granularidade analítica para investigação.
   - **parametros:** rastreabilidade (regras, janelas, data de geração).
3. **03_grafico_principal.png**
   - Visual principal para comunicação executiva.

## Observações de implementação
- Dados sempre são gerados em runtime (sem dependências externas).
- Scripts usam backend `Agg` do matplotlib para execução headless.
- Caso algum erro de caminho/import ocorra, aplique apenas correção mínima e reexecute o pipeline.
