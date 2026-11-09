# Vidro, luz e metal

> Status: rascunho de biblioteca | Confiança: média (níveis de luz de wiki, IDs oficiais; nada testado no jogo) | Última revisão: 2026-11-09

## Resumo
- Vidro em bloco dá superfície; vidraça (pane) dá moldura fina e conecta sozinha; `tinted_glass` escurece.
- Metais usáveis: `iron_bars`, `iron_chain`, família de cobre (oxida e pode ser encerada).
- Luz: lanterna, sea_lantern e glowstone = 15; tocha = 14; soul = 10; `light_block_0..15` sem estados. Hostis exigem luz de bloco 0: DOC de comunidade, não testado no jogo.

## Conceito
Vidro, metal e luz definem leitura de noite e de perto: o vidro mostra o interior, o metal dá linha fina (grade, corrente) e a luz marca entradas e cantos. O render por raycast mostra vidro e cor só aproximados (X02), então a decisão final precisa de conferência no jogo.

## Características / regras

### Vidro (IDs conferidos)
| Bloco | ID | Nota |
|---|---|---|
| Vidro | `glass` | bloco cheio |
| Vidro escurecido | `tinted_glass` | bloco |
| Vidro tingido | `white_stained_glass`, `cyan_stained_glass_pane` etc. | uma versão por cor |
| Vidraça | `glass_pane`, `white_stained_glass_pane` | fina |
- Vidraças têm estados `minecraft:connection_north/south/east/west` (0/1) calculados pelo jogo: não definir à mão, as conexões são automáticas (`../referencia/estados-e-rotacao.md`).
- T5: bloco de vidro -> vidraça; branco suaviza reflexo [TESTADO-AULA02, interpretação de confiança média].
- Vidro e folhas não servem de superfície para spawn (wiki Mob_spawning, só busca) [DOC comunidade].

### Metal
| Bloco | ID | Uso |
|---|---|---|
| Grade | `iron_bars` | seteira, gradil; conecta com `minecraft:connection_*`. Seteira com `iron_bars` "funciona muito bem" [TESTADO X02] |
| Corrente | `iron_chain` | `pillar_axis` y/x/z (estado) |
| Cobre | `copper_block`, `exposed_copper`, `weathered_copper`, `oxidized_copper`, `waxed_copper` | ver `envelhecimento-e-deterioracao.md` |
| Peças de cobre | `copper_lantern`, `copper_chain`, `copper_bars`, `copper_door` | variantes de oxidação e cera |

### Luz e emissivos [DOC comunidade, minecraft.wiki Light, só busca]
| Nível | Fontes |
|---|---|
| 15 | `lantern`, `sea_lantern`, `glowstone`, `lit_pumpkin`, lava, fogo, beacon |
| 14 | `torch`, `copper_torch`, `end_rod` |
| 13 | fornalhas/defumador/alto-forno acesos |
| 10 | `soul_torch`, `soul_lantern`, `soul_campfire`, `crying_obsidian` |
| velas | 1 vela = 3; 3 velas = 9; 4 velas = 12; 2 velas e fogueira comum: [NV] |
| 7 | enchanting table, ender chest, tocha de redstone |
`light_block_0` a `light_block_15`: 16 IDs sem estados, existem na lista oficial (A6_r2 #23). Só aparecem com item de luz na mão; inquebráveis por explosão [DOC wiki]. O ID antigo `light_block` + `block_light_level` NÃO está nos blocos de v1.26.60.5.
Nota de redação: em fonte da wiki o item "12 vault ativo, 4 velas acesas" vem em linha única; a leitura de "4 velas = 12" é [INT] pela progressão 3/9/12.

### Spawn de hostis [DOC comunidade, não testado no jogo]
Hostis precisam de luz de bloco 0 em muitos casos (e luz do céu interna <= 7); superfícies sem topo sólido cheio (tapete, laje inferior, cerca, escada, escada invertida, vidro, folhas) não geram spawn. Portanto `light_block_1` invisível sob uma superfície ou lajes superiores impedem spawn [INT sobre wiki].

## Como construir no Bedrock
1. Janela: `glass_pane` em moldura de pedra/madeira; deixar o jogo conectar. [TESTADO-AULA02 para panes; conexões: estado oficial]
2. Fachada moderna: `glass` ou `tinted_glass` com montantes a cada 3 blocos para evitar "caixa de vidro". [TESTADO X02 (render)]
3. Seteira: coluna 1x2 de `iron_bars` na parede de pedra. [TESTADO X02]
4. Luz de acesso: poste/lanterna dos dois lados da porta (`lantern`, `hanging=1` quando pendurada). [INT; canto com lanterna: TESTADO-AULA02]
5. Luz quente (tocha 14/lanterna 15) para interiores; `soul_lantern` (10) para clima frio. [INT]
6. Segurança de spawn: nenhuma superfície válida abaixo do nível 1; use `light_block_1` onde luz visível estraga o clima. [NÃO TESTADO]
7. Em `.mcstructure`, `light_block_N` com `states: {}` e `name: minecraft:light_block_N`. [A6_r2]

## Combina com
- [paletas-e-combinacoes.md](paletas-e-combinacoes.md)
- [envelhecimento-e-deterioracao.md](envelhecimento-e-deterioracao.md)
- [../ambientacao/iluminacao-e-atmosfera.md](../ambientacao/iluminacao-e-atmosfera.md)
- [../tecnicas/postes-de-luz.md](../tecnicas/postes-de-luz.md)
- [../tecnicas/cantos-e-vigas.md](../tecnicas/cantos-e-vigas.md)
- [../experimentos/X02-fachadas-e-janelas/RESULTADO.md](../experimentos/X02-fachadas-e-janelas/RESULTADO.md)
- [../estilos/futurista-cyberpunk-solarpunk.md](../estilos/futurista-cyberpunk-solarpunk.md)

## Erros comuns
- Vidro e cores avaliados pelo render: só aproximado (X02).
- ID de vidraça sem o sufixo `_pane`; `light_block` sem número.
- Alçapão de persiana com direção não conferida (X02).
- Excesso de luz 15 sem hierarquia; todas as lâmpadas iguais.
- `waxed_copper_block` (não existe).
- Confiar em spawn sem checar luz 0 e superfície válida.

## Limitações e dúvidas
- Níveis de luz e regras de spawn: wiki, só busca; "dois velas" e "campfire comum" [NV].
- Nada foi testado no jogo (transparência real, brilho real, spawn).
- Cor e brilho de cobre/vidro tingido no jogo não aparecem no render.
- O mapeamento de `pillar_axis` da corrente não foi validado no jogo.

## Fontes e evidências
- A6_tecnico_bedrock (níveis de luz e Mob_spawning, minecraft.wiki, só busca) e A6_r2 #23, #29 (bedrock-samples, aberto).
- X02 (render): seteira e janelas; `../tecnicas/materiais-e-paletas.md` T5.
- IDs conferidos em `../referencia/blocos-bedrock.md`.
