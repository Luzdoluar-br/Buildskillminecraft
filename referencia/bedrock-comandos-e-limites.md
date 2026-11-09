# Bedrock: comandos, funções, limites, luz, névoa

> Status: parte OFICIAL (Microsoft Learn / Mojang bedrock-samples), parte comunidade (wiki), parte TESTADA no jogo do dono | Última revisão: 2026-11-09

Legenda: **[OFICIAL]** página aberta de Microsoft Learn ou arquivo do repositório Mojang/bedrock-samples · **[WIKI]** minecraft.wiki / wiki.bedrock.dev (comunidade) · **[TESTADO]** observado no jogo do dono · **[NV]** não verificado.
As páginas foram lidas por uma ferramenta que **resume** o texto (não é leitura bruta); números oficiais abaixo vêm desses resumos.

## Estruturas e comandos
| Item | Valor | Fonte |
|---|---|---|
| Tamanho máximo de `/structure save` | **64 × 384 × 64** | [OFICIAL] tutorial de blocos de estrutura |
| `/structure load` | `rotation` 0/90/180/270_degrees; `mirror` x, z, xz, none; `animation` block_by_block ou layer_by_layer + segundos; `includeEntities`, `includeBlocks`, `waterlogged`, `integrity` 0–100, `seed`, `saveMode` disk/memory (o texto oficial de Mirror/Rotation tem erro de redação: use os valores acima) | [OFICIAL] |
| `/fill` (modos) | replace, destroy, hollow, keep, outline | [OFICIAL] |
| **Limite de volume do `/fill` e do `/clone`** | **Nenhuma página oficial publica limite.** A wiki cita 32.768 (fill) e 655.360 (clone); a gamerule `max_block_modifications` é marcada como Java-only (bug MCPE-182123) | [NV] — por precaução dividir em ≤ 32.768 e checar o resultado |
| `/clone` modos | replace/masked/filtered; normal/force/move | [OFICIAL] |
| `/setblock`, `/execute` | sintaxe nova do `execute` (`as … at … run`, `if/unless block|blocks|entity|score`) | [OFICIAL] |
| `/kill` | — | [NV] (página não aberta) |
| `/tickingarea` | até **10 áreas** por mundo; círculo com raio **0–4** chunks; coluna cheia (altura inteira); `preload` carrega antes na abertura do mundo (padrão false) | [OFICIAL] |
| `/tickingarea` retangular | máx. 100 chunks | [WIKI] |
| `/schedule on_area_loaded add …` | espera os chunks carregarem antes de rodar uma função (útil para colocar estruturas em área não gerada) | [OFICIAL] |
| `/structure load` em chunk não carregado | falha; solução usual: ticking area + aguardar | [WIKI]; **[TESTADO]** que `preparar` (tickingarea) seguido de `colocar` funcionou no jogo do dono |

## Funções (`.mcfunction`) e add-on
- Arquivo em `functions/` do behavior pack, **sem `/` inicial**, um comando por linha; subpasta vira `/function pasta/arquivo`. [OFICIAL] (a página oficial lida não cita o `#` de comentário: só a wiki). Máximo **10.000 comandos por chamada**. [OFICIAL]
- Arquivo `.mcfunction` NOVO exige reiniciar o jogo (`/reload` só recarrega os existentes). [WIKI]
- Manifest do BP: `format_version` 2, `header` com `name`, `description`, `uuid`, `version`, `min_engine_version` (obrigatório), `modules[]` com `type: "data"` e outro `uuid`. [OFICIAL] O exemplo oficial do repositório usa `min_engine_version [1,26,60]`.
- Estruturas do BP ficam em `structures/<namespace>/*.mcstructure` e carregam com `/structure load <namespace>:<nome>`. [WIKI] + **[TESTADO]** (add-on VULPUS Vila).
- Add-on embutido num mundo: copiar para `<mundo>/behavior_packs/<nome>` e listar em `world_behavior_packs.json`. **[TESTADO]**

## Blocos, estados e formato
- IDs e estados: `blocos-bedrock.md` (lista oficial, 1.466 blocos). Significado e rotação: `estados-e-rotacao.md`. Formato do arquivo: `mcstructure-formato.md`.
- Porta de carvalho é `minecraft:wooden_door`; **não existe `oak_door`**. [OFICIAL]
- 91 blocos ainda usam `facing_direction` (int 0–5): barril, escada de mão, placa de parede, bandeira de parede, end_rod, para-raios, cabeças, botões, funil, êmbolo… Já `chest, smoker, lectern, campfire, stonecutter, wooden_door` usam `minecraft:cardinal_direction`. [OFICIAL]
- Mapeamento número→direção de `weirdo_direction` e `facing_direction` **não está no arquivo oficial**: [NV] oficialmente; o uso do projeto (0 leste, 1 oeste, 2 sul, 3 norte para escadas) foi **[TESTADO]** por telhados e escadas que renderizam e carregam corretamente no jogo.
- Cobre: base `copper_block`, `exposed_copper`, `weathered_copper`, `oxidized_copper`; encerados `waxed_copper` (**não** `waxed_copper_block`), `waxed_exposed_copper`, `waxed_weathered_copper`, `waxed_oxidized_copper`; `*_cut_copper`, `*_cut_copper_stairs`, `*_cut_copper_slab`. [OFICIAL] Em construções use as versões `waxed_` (sem oxidação por tempo).
- Luz invisível: `minecraft:light_block_0` … `minecraft:light_block_15` (16 IDs, sem estados). O ID antigo `light_block` + estado não existe nesta versão. [OFICIAL]

## Luz e nascimento de monstros (comunidade, NÃO testado no jogo)
- Níveis: farol, glowstone, sea_lantern, lantern, lava, fogo = 15; tocha, end_rod = 14; soul_torch/soul_lantern = 10; velas 3 a 12 conforme a quantidade. [WIKI]
- Monstros hostis nascem com luz de bloco **0** (e luz do céu ≤ 7 em ambientes abertos); superfície precisa de topo sólido cheio (tapete, laje inferior, cerca, escada comum e escada invertida não servem). [WIKI]
- Uso prático [INT]: para impedir nascimento numa praça ou ruína, garantir luz de bloco ≥ 1 em todo bloco de superfície, ou usar lajes/blocos não sólidos, ou `light_block_1` invisível. **Teste no jogo pendente.**

## Névoa, partículas e atmosfera
- Fog é **do cliente/resource pack e do bioma/jogador**, não do bloco: JSON em `fogs/` + `fog_identifier` em `biomes_client.json`; pilha de prioridade comando (`/fog push|pop|remove`) > bioma > padrão. [OFICIAL]
- Partículas: JSON em `particles/` do resource pack; disparo por `/particle`, animação de entidade ou controlador. [OFICIAL]
- **Nada disso pode ser parte de um `.mcstructure`.** Atmosfera dentro da estrutura = só blocos (vidro tingido, teia, luz) ou, com add-on, entidades/funções em `tick.json`.

## Altura do mundo
Overworld y de −64 a 319 (384 camadas); End 0–255; Nether ~0–127 (a wiki é ambígua). [WIKI]

## Pendências de teste no jogo (para o dono, quando puder)
1. Limite real do `/fill` (a função `limpar` da vila usa fatias de 30.208 blocos).
2. Se `block_entity_data` de `Bed` no `.mcstructure` gerado pelo nosso exportador faz a cama aparecer (`ferramentas/construcao/exemplos/exemplo_minimo.py`).
3. Nascimento de monstros com luz de bloco 0 vs 1 em superfície de pedra.
4. Direção do alçapão aberto (`direction` 0–3) para persianas.
