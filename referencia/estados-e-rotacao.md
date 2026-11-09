# Estados e rotação de blocos (Bedrock)

**Evidência**: os estados abaixo foram observados em dados que o próprio jogo gravou num mundo real (ver a coluna "Estados observados" em `blocos-bedrock.md`). Onde marcado *(a confirmar)* é interpretação.

## Regra de ouro
1. O ID tem de estar em `blocos-bedrock.md`. **Não existe lá → não usar** (ex.: `rooted_dirt`, `lily_pad`, `dirt_path`).
2. Bloco com orientação: **sempre** informar o estado de rotação; o padrão do jogo costuma ser errado para o que eu quero (ex.: `lightning_rod` padrão = 0, para baixo).
3. Depois de gerar: rodar `aulas/aula-02/codigo/auditoria.py` (valida IDs, apoio, rotação).

## Tabela de rotação
| Tipo | Estado | Valores | Observação |
|---|---|---|---|
| Troncos (`*_log`, `stripped_*_log`, `*_wood`), `hay_block`, `iron_chain` | `pillar_axis` | `x`, `y`, `z` | `y` = em pé. Tronco horizontal mostra a **ponta (anéis)** nas duas extremidades: só deixar ponta exposta de propósito |
| Escadas | `weirdo_direction` | 0 leste, 1 oeste, 2 sul, 3 norte | direção em que a escada **sobe** (as costas ficam desse lado). Invertida: `upside_down_bit=1`. `minecraft:corner` é calculado pelo jogo, não definir |
| Lajes | `minecraft:vertical_half` | `bottom`, `top` | laje dupla = bloco `*_double_slab` |
| Portas | `minecraft:cardinal_direction` + `door_hinge_bit` + `open_bit` + `upper_block_bit` | north/south/east/west; 0/1 | metade de baixo e de cima são 2 blocos; verga acima (E-10) |
| Alçapões | `direction` (0-3), `open_bit`, `upside_down_bit` | | *(a confirmar: qual direção é qual lado)* |
| Forno, defumador, alto-forno, atril, bigorna, abóbora, fogueira | `minecraft:cardinal_direction` | north/south/east/west | = lado para onde a **frente** olha. NÃO usar `facing_direction` nesses (o jogo converte) |
| Barril, para-raios, moldura | `facing_direction` | 0 baixo, 1 cima, 2 norte, 3 sul, 4 oeste, 5 leste | barril em pé = 1; para-raios para cima = 1 |
| Lanterna | `hanging` | 0/1 | pendurada precisa de bloco acima (senão o jogo remove) |
| Cercas, vidraças, muros | `minecraft:connection_*`, `wall_connection_type_*` | | calculados pelo jogo |
| Folhas | `persistent_bit`, `update_bit` | | `persistent_bit=1` evita decair |
| Água | `liquid_depth` | 0 = fonte | |
| Plantas altas | `upper_block_bit` | 0/1 | metade de cima = 1 |
| Cultura / terra arada | `growth` / `moisturized_amount` | | |
| Cama | `direction`, `head_piece_bit` | | **o jogo descarta** sem entidade de bloco (E-04) |

## Girar uma construção 180° (flip)
Trocar leste↔oeste e sul↔norte em: escadas, `cardinal_direction` de portas e máquinas. Troncos `x`/`z` e `y` não mudam. No código: `Molde.dirm()` e `Molde.maq()`.

## Nomes Java → Bedrock (verificados contra a lista de IDs)
| Java / de memória | Bedrock |
|---|---|
| `rooted_dirt` | `dirt_with_roots` |
| `lily_pad` | `waterlily` |
| `sugar_cane` | `reeds` |
| `dirt_path` | `grass_path` |
| `cobweb` | `web` |
| `terracotta` | `hardened_clay` |
| `grass` (planta) | `short_grass` |
| `melon` | `melon_block` |
| `chain` | `iron_chain` (e `copper_chain`...) |
| `nether_bricks` | `nether_brick` |
| `spawner` | `mob_spawner` |
| `jack_o_lantern` | `lit_pumpkin` |
| `bricks` | `brick_block` |
| `end_stone_bricks` | `end_bricks` |
| `snow_block` | `snow` |
| `beetroots` | `beetroot` |
