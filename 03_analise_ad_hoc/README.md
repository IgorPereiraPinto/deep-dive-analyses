# 03 — Análise Ad hoc

## Objetivo e perguntas de negócio
Responder duas investigações rápidas de performance comercial.
Perguntas: quais produtos perderam receita recentemente? Qual relação entre desconto e ticket médio?

## KPIs / medidas principais
- Delta de receita por produto (2 meses recentes vs 3 anteriores)
- Delta percentual por produto
- Correlação desconto médio x ticket médio

## Como o código funciona
O script consolida receita por produto e mês para comparar as janelas temporais definidas. Calcula os maiores deltas negativos de receita e registra os resultados em resumo executivo e planilha. Na segunda investigação, calcula ticket médio e desconto médio por cliente e estima correlação linear simples. Gera gráfico principal de queda por produto e um scatter complementar para apoio diagnóstico. Inclui parâmetros analíticos no XLSX para rastreabilidade.

## Como interpretar outputs
No TXT, leia a resposta direta para cada investigação e as recomendações de ação. No XLSX, confira quais produtos puxam a queda e a série mensal de suporte. No PNG principal, barras negativas indicam necessidade de intervenção prioritária.

Setup e execução: ver README na raiz.
