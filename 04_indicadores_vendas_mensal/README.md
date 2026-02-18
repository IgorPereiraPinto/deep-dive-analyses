# 04 — Indicadores de Vendas Mensal (Real vs Meta)

## Objetivo e perguntas de negócio
Comparar realizado e meta/forecast mensal para localizar gaps e drivers.
Perguntas: onde estamos abaixo/acima da meta? Quais dimensões explicam o gap?

## KPIs / medidas principais
- Realizado mensal
- Meta mensal
- Gap absoluto e gap percentual

## Como o código funciona
O script integra vendas históricas e tabela de meta/forecast sintética. Primeiro calcula o consolidado mensal (real, meta, gap e gap%) e depois detalha por canal, regional e produto. Cria TXT com drivers e plano de ação, XLSX com abas resumo/detalhe/parâmetros e PNG com comparação temporal Real vs Meta. Inclui sanity check para validar existência de meta positiva e aderência de chave na decomposição.

## Como interpretar outputs
No TXT, priorize drivers de gap negativo e ações recomendadas. No XLSX, use resumo para priorização mensal e detalhe para investigação dimensional. No PNG, observe distância entre linhas para detectar meses críticos.

Setup e execução: ver README na raiz.
