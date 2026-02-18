# 02 — Análise Pareto / ABC

## Objetivo e perguntas de negócio
Mensurar concentração de receita por cliente e classificar carteira em A/B/C.
Perguntas: qual o nível de dependência de poucos clientes? Como está a distribuição de valor?

## KPIs / medidas principais
- Receita total e participação top 10
- % acumulado de receita
- Participação da classe A

## Como o código funciona
O script agrega receita por cliente, ordena do maior para o menor e calcula percentual acumulado. Com base nos thresholds padrão (80% e 95%), define classes A, B e C automaticamente. Produz TXT com riscos e ações, XLSX com tabela detalhada de clientes e resumo de concentração e PNG de Pareto (barras + linha acumulada). Inclui check de receita não negativa e padroniza exportação via utilitário compartilhado.

## Como interpretar outputs
No TXT, foque no risco de concentração e nas ações para reduzir dependência. No XLSX, verifique clientes que formam o bloco A e oportunidades de evolução B/C. No PNG, identifique visualmente o ponto onde a curva acumulada cruza 80% e 95%.

Setup e execução: ver README na raiz.
