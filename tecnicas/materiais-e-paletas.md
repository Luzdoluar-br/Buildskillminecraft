# Materiais e paletas

Fontes: estruturas 01–04, 24, 33, 43 (ver `aulas/aula-01/estruturas-analisadas.md`).

## T1. Trocar o material "base" por um mais neutro e variar com 2–3 vizinhos
**Evidência**: 02 `stone_bricks → stone` (77) + `tuff_bricks` (115) + `polished_tuff/andesite` + `smooth_stone`; 04 `white_concrete/stone_bricks → light_gray_concrete`.
**Decisão**: tirar o bloco com mais padrão/saturação da massa principal e distribuir 2–3 tons próximos de cinza.
**Por que funciona** (interpretação, confiança média): tons próximos criam textura sem ruído; o olho lê "pedra real" em vez de padrão repetido.
**Reuso**: paredes grandes. Regra prática: 1 material dominante (~60%), 1–2 de apoio, nenhum com contraste forte.

## T2. Madeira em dois "pesos": estrutura vs preenchimento
**Evidência**: 01 `oak_planks → stripped_oak_log` + pilares `stripped_spruce_log`; 03 `spruce_planks → stripped_spruce_log` alternando com tábuas; 04 pilares `stripped_dark_oak_log` sobre concreto.
**Decisão**: tronco descascado marca estrutura (pilares/vigas), tábua/concreto preenche.
**Por que funciona**: contraste de tom e de direção do veio separa "esqueleto" e "pele", dando profundidade.
**Reuso**: qualquer casa de madeira ou mista. Limite: texturas de tronco têm veio — usar `pillar_axis` coerente (x/z/y).

## T3. Madeira clara contra concreto/pedra escura (ou vice-versa)
**Evidência**: 04 `pale_oak` (porta, laje, escada, alçapão) + concreto cinza/branco.
**Interpretação** (confiança média): um terceiro material de cor quente/clara destaca portas e detalhes.

## T4. Substituir blocos "chamativos" por tom de apoio
**Evidência**: 33 `obsidian/crying_obsidian/end_rod → black_concrete` (60 + 32 escadas); 24 `polished_andesite → stone_bricks`.
**Interpretação**: reduzir brilho/textura marcante para o objeto principal (portal, fonte) dominar. Confiança baixa a média (decisão pode ser só estética pessoal).

## T5. Vidro em bloco → vidraça
**Evidência**: 33 `purple_stained_glass → magenta/purple pane` (35); 01/02/04 `glass_pane` → `white_stained_glass_pane`.
**Interpretação**: vidraça é mais fina, dá moldura visual; vidro colorido branco suaviza reflexo. Confiança média.

## T6. Pavimento irregular com 3–4 pedras
**Evidência**: 43 `andesite` 45, `cobblestone` 28, `gravel` 22, `light_gray_wool` 11 no lugar de `stone_bricks`.
**Por que funciona**: tijolo regular parece calçada nova; mistura irregular parece caminho usado.
