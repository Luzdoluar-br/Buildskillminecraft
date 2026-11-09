# Vegetação e ambientação

## V1. Cobertura de solo em camadas (recorrente: 03, 04, 11, 12, 13, 23, 24)
**Evidência** (números por estrutura): `short_grass` 18–98; `tall_grass` 12–36; samambaia/`large_fern` 8–34; flores variadas (tulipas, dandelion, poppy, cornflower, azure bluet, oxeye) 6–20; `sweet_berry_bush` 9–10; `moss_carpet` 1–9; `moss_block` 7–32 no lugar de `grass_block`.
**Decisão**: o chão nunca fica só grama; mistura de altura baixa (grama), média (flores/samambaia) e alta (tall_grass).
**Por que funciona** (interpretação, confiança alta pela recorrência): quebra o plano do chão e dá "vida" sem alterar a estrutura.
**Reuso**: raio de 3–5 blocos ao redor de qualquer construção.

## V2. Musgo como transição
**Evidência**: `grass_block → moss_block` em árvores (11: 32, 12: 7, 13: 24, 24: 17, 03: 11) + `moss_carpet`.
**Interpretação**: tom mais escuro e úmido ao pé de troncos e bordas de pedra. Confiança média.

## V3. Árvore: galhos em tronco no meio da copa
**Evidência**: 13 (9 `birch_leaves → birch_log`), 14 (40 `dark_oak_leaves → dark_oak_log`), 11/12 (6–7).
**Interpretação**: troncos internos dão estrutura e galhos visíveis. Confiança média-alta.
**Limite**: remoção de folhas (`→ air`, 100–292) ficou inconclusiva (poda vs decaimento natural no Bedrock).

## V4. Detalhes de luz/vida em árvore
**Evidência**: 14 `azalea_leaves_flowered` (5), 11/13 `azalea` e `flowering_azalea`; 12 `vine` (6).
**Interpretação**: pontos de cor numa copa uniforme.

## V5. Horta e canteiro
**Evidência**: 03 `farmland` (10) + `carrots` (10); 04 14 `flower_pot`.
