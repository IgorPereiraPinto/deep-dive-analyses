# 01 — Análise de Safra (Cohort)

## Objetivo e perguntas de negócio
Avaliar retenção por coorte mensal de primeira compra.
Perguntas: quais coortes retêm melhor nos meses M1, M2 e M3? Onde há queda acelerada?

## KPIs / medidas principais
- Clientes por coorte
- Retenção M1/M2/M3
- Receita total por coorte

## Como o código funciona
O script lê a base de vendas sintética, identifica o mês da primeira compra por cliente e monta a matriz coorte x período. Em seguida calcula retenção relativa à base inicial de cada coorte. Gera três saídas: TXT com leitura executiva, XLSX com resumo/detalhe/parâmetros e PNG com heatmap de retenção. Também inclui sanity checks de consistência para cliente e receita. Usa utilitário comum de Excel para manter padrão de entrega.

## Como interpretar outputs
No TXT, priorize coortes fortes e fracas e ações sugeridas de retenção. No XLSX, use a aba resumo para comparação rápida entre coortes e a aba detalhe para análise por período. No PNG, observe gradientes de cor para detectar deterioração de retenção.

Setup e execução: ver README na raiz.
