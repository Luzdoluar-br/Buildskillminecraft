# Telhados, beirais e topos

## R1. Teto não pode ser só um anel
**Evidência**: 03, y=7 — no original só havia o perímetro de `dark_oak_stairs`; o dono preencheu o interior com `dark_oak_planks` (camada sólida).
**Interpretação**: telhado oco deixa o céu visível por dentro; fechar o plano é pré-requisito. Confiança alta (diferença objetiva); motivo exato é inferência.
**Regra**: conferir cada camada do telhado em planta — o centro tem que ter fechamento.

## R2. Beiral projetado com escada + laje
**Evidência**: 04, y=11 — ring de `stone_brick_stairs`/`stone_brick_slab` avança ~2 blocos além da parede, cantos em `stone_bricks`.
**Interpretação**: beiral largo dá sombra e estilo oriental; lajes suavizam o degrau.
**Reuso**: casas de estilo japonês/asiático; reduzir para 1 bloco em casas europeias.

## R3. Lajes invertidas (`vertical_half=top`) como forro
**Evidência**: 03 (45 lajes de carvalho-negro invertidas) e 04 (stone_brick_slab top 48).
**Interpretação**: forro por baixo do beiral esconde o "dente" das escadas. Confiança média.
**Limite Bedrock**: o estado correto é `minecraft:vertical_half=top` (não `upside_down_bit`, que é de escadas).

## Dúvida
Inclinação do telhado (pitch) e quebra de cumeeira não foram claramente alteradas nos dados — sem material.
