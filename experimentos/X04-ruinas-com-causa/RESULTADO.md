# X04 — Ruína com causa x dano aleatório

**Pergunta**: deteriorar a partir de uma causa física lê melhor (e é mais plausível) que remover blocos ao acaso? **Script**: `experimento.py` + módulo `ferramentas/construcao/ruina.py`. **Imagens**: `imagens/montagem.png`, `montagem_causas.png`.

Mesma casa de pedra (15×11, dois pisos, telhado de duas águas, chaminé) em 5 cópias.

| Variante | Blocos finais | Blocos flutuantes* | Leitura visual |
|---|---|---|---|
| R0 intacta | 1030 | 2 | referência |
| R1 aleatória (40% removido ao acaso) | 679 | **106** | "queijo suíço": buracos uniformes, telhado em pedaços soltos; **não conta nenhuma história** |
| R2 abandono (tempo e água) | 607 | 1 | topos de parede em dentes, musgo/rachaduras, janelas vazias, telhado quase todo perdido, vegetação nos topos |
| R3 impacto (explosão, raio 6) | 969 | 0 | cratera na fachada com gradiente de chamuscado (blackstone/rachado) e entulho no chão; **o telhado ficou intacto demais** |
| R4 incêndio | 613 | 3 | madeira some, pedra fica, fuligem acima das aberturas, chaminé em pé |
(*) Blocos sem ligação por face com o chão, excluindo vegetação, vidro e lanternas.

## Conclusões (TESTADO)
1. **Causa + gradiente + remoção de flutuantes** produz ruínas legíveis e fisicamente plausíveis; aleatório produz ruído e deixa ~100 blocos no ar.
2. Ordem de falha usada (INTERPRETAÇÃO PRÓPRIA apoiada em guia de conservação de ruínas de alvenaria): cobertura → topos de muro → madeiramento/pisos → esquadrias → cantos/empenas. Pedra sobrevive mais que madeira.
3. A métrica de flutuantes serve também como teste de qualidade de **construção**: ela revelou que minha casa de teste tinha o telhado a 1 bloco das paredes (erro corrigido no próprio experimento).

## Falhas / limites
- **Impacto não derruba o telhado** quando só um trecho de parede cai (o telhado ainda se apoia no resto): falta uma regra de "telhado sem apoio em um lado desmorona".
- Resíduo de madeira alta (poucos degraus do telhado presos à empena) continua visível no render; a regra `limitar_balancos_de_madeira` (máx. 3 células sem apoio de pedra) reduziu mas não eliminou.
- Vegetação ainda esparsa: densidade e espécies não calibradas.
- Não comparei com ruínas reais por foto; a plausibilidade é julgamento visual + física simples.
- **Bugs do próprio experimento** (registrados): chão em y=0 enquanto a casa começava em y=1 (tudo "flutuava"); paredes de 7 com telhado em y=9.
