# Formato `.mcstructure` (Bedrock): o que foi TESTADO no jogo

Classificação de confiança usada nesta página:
- **TESTADO** = observado em arquivos que o próprio jogo gravou (`/structure save`, estruturas guardadas no mundo do dono) ou em carregamento real no jogo.
- **DOCUMENTADO** = consta em documentação de terceiros (wiki); fonte indicada.
- **NÃO VERIFICADO** = ainda sem teste nem fonte aberta.

Versão do jogo observada: a paleta das estruturas gravadas pelo jogo traz `version = 18168865` (coincide com o valor citado por wiki.bedrock.dev, que o associa a 1.21.60.33).

## Estrutura NBT (little-endian, sem compressão)
| Campo | Observado no arquivo gravado pelo jogo (TESTADO) |
|---|---|
| `format_version` | **2** no jogo atual; o jogo também **carrega** `1` (nosso exportador grava 1 e a vila carregou 100% idêntica) |
| `compression` | tag raiz presente em format 2, valor `0` (dados sem compressão) |
| `size` | lista de 3 ints `[X, Y, Z]` |
| `structure.block_indices` | lista de listas de int. O jogo grava **1 camada** quando não há água/waterlog; nosso exportador grava 2 (a 2ª toda `-1`) e carrega normalmente. `-1` = não alterar o bloco |
| `structure.palette.default.block_palette` | lista de `{name, states, version}` |
| `structure.palette.default.block_position_data` | compound indexado pelo **índice linear do bloco** (string), cada valor com `block_entity_data` |
| `structure.entities` | lista (vazia nas amostras) |
| `structure_world_origin` | 3 ints (onde foi salva) |

**Ordem dos índices (TESTADO, duas fontes: leitura de arquivos do jogo e carregamento real):**
`indice = x*(Y*Z) + y*Z + z` (z varia mais rápido, depois y, depois x), com x,y,z relativos ao canto mínimo.

**Tipos NBT dos estados (TESTADO):** booleano = **byte** (`open_bit`, `upside_down_bit`, `hanging`...), inteiro = **int** (`weirdo_direction`, `direction`...), texto = **string** (`pillar_axis`, `minecraft:cardinal_direction`, `minecraft:vertical_half`). Booleano gravado como int é erro.

## Entidades de bloco (`block_position_data`) (TESTADO a leitura; escrita ainda NÃO validada no jogo)
Amostras lidas de uma estrutura salva pelo jogo (chave = índice linear):
- `FlowerPot`: `{id:'FlowerPot', x,y,z, BlockEntityVersion:0, PlantBlock:{name,states,version}}`
- `Bed`: `{id:'Bed', x,y,z, color:0, BlockEntityVersion:0}`
- `Barrel`: `{id:'Barrel', x,y,z, Items:[], Findable:0, BlockEntityVersion:0}`
- Também apareceram `Furnace` e `ItemFrame`.
`x,y,z` dentro dos dados são coordenadas do mundo onde foi salva; o jogo as substitui ao carregar (DOCUMENTADO, wiki.bedrock.dev).

**Efeito de NÃO ter a entidade (TESTADO):** uma `bed` colocada via `/structure load` **sem** `block_entity_data` **desapareceu** (virou ar) no mundo do dono. Barris e fornos sem entidade carregaram normalmente (ganham a entidade padrão). Não presumir "cama vermelha": o teste mostrou ar.

## Estados que o jogo altera ao carregar (TESTADO)
- `facing_direction` em forno/defumador/alto-forno/atril → vira `minecraft:cardinal_direction` (o jogo converte; usar a chave nova direto).
- Escadas ganham `minecraft:corner` (`none`, `inner_left`, `outer_left`, `outer_right`...) calculado pelo jogo; não definir.
- Cercas, vidraças e muros ganham `minecraft:connection_*` / `wall_connection_type_*`.
- Fazenda e culturas, água `liquid_depth`: preservados.
- Nomes **inexistentes** (ex.: `rooted_dirt`, `minecraft:spruce`) são **gravados como estão** e mostram bloco de erro; o jogo não avisa. Validar sempre contra `referencia/blocos-bedrock.md`.
- O jogo remove `lantern[hanging=1]` sem bloco acima.

## Compatibilidade
O exportador `ferramentas/construcao/exportar.py` grava `format_version 1`, `version 18161159`, 2 camadas: carregado com sucesso no jogo atual (estrutura 62×33×59, 31 mil blocos, todos os blocos conferidos depois por leitura do mundo).
