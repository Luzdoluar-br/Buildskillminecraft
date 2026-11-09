# X03 — Curvas e diagonais

**Perguntas**: (A) a partir de que tamanho um círculo de blocos "lê" como círculo? (B) cúpula de blocos x cúpula com lajes; (C) rampas 1:1, 1:2, 1:3 e muro diagonal. **Script**: `experimento.py`. **Imagens**: `imagens/montagem.png`.

## A) Torres circulares (anel de 1 bloco, altura 7)
Métrica: **maior trecho reto** do anel (o que faz um círculo parecer octógono/quadrado arredondado) e sua razão ao diâmetro.

| Raio | Diâmetro (blocos) | Células no anel | Maior trecho reto | Reto / diâmetro |
|---|---|---|---|---|
| 2,5 | 6 | 16 | 5 | 0,83 |
| 3,5 | 8 | 20 | 5 | 0,62 |
| 5 | 11 | 28 | 5 | 0,45 |
| 7 | 15 | 40 | 5 | 0,33 |
| 10 | 21 | 56 | 7 | 0,33 |

**Conclusão (TESTADO)**: com razão > 0,5 (diâmetro ≤ 8) o "círculo" é um quadrado arredondado; **só a partir de diâmetro ~15** o trecho reto cai para ~1/3 do diâmetro e o contorno lê como curva. Torres menores devem ser assumidas como **octógonos** ou quadradas com cantos chanfrados, sem fingir círculo.

(Obs.: a primeira métrica que escrevi, "erro de circularidade", era ≤ 0,5 por construção e **não discriminava nada**: descartada.)

## B) Cúpulas
| Raio | `Cena.cupula` (blocos) | Cúpula com lajes (meio bloco) | Diferença de custo |
|---|---|---|---|
| 5 | 153 | 163 | +7% |
| 8 | 395 | 491 | +24% |
| 12 | 998 | 1095 | +10% |
Lajes dão degraus de meio bloco e uma superfície mais suave no render; o ganho é visível a partir de raio 8. Em raio 5 a diferença é pouca.

## C) Rampas e diagonais
- Rampas 1:1 (escada), 1:2 e 1:3 (lajes) renderizam como inclinações distintas e legíveis; 1:3 já é "quase plana".
- Muro diagonal a 45° só com blocos: a escada irregular fica evidente; exige espessura 2 para fechar a diagonal. **Não testado**: suavizar com escadas de canto.

## Falhas e limites
- Ângulos de câmera ruins nas 1ªs imagens (estavam muito próximos): o resultado numérico é mais confiável que a foto.
- Não testei cúpula com escadas em anéis (técnica "octogonal escalonada" citada em manuais): NÃO VALIDADA.
