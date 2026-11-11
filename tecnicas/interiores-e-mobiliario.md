# Interiores e mobiliário

## I1. Mobiliar com blocos de função (recorrente: casas 01, 02, 03, 04)
**Evidência**: em todas as casas o interior, antes vazio, recebeu: cama (2–4), `barrel` (6–9), `smoker`/`blast_furnace`/`furnace`, `crafting_table`, `bookshelf`/`chiseled_bookshelf`, `lectern`, `flower_pot` (1–14), carpete cinza (8–26), `fletching/cartography_table`, `anvil`.
**Decisão**: cada casa tem "zona de dormir" + "zona de trabalho" + decoração.
**Por que funciona** (interpretação): blocos funcionais têm textura rica e comunicam uso; carpete cobre o piso e agrupa a zona.
**Reuso**: sempre que a casa tiver interior visível.
**Dado a registrar**: cada interior usa ~5–7 tipos de blocos de função, 0–1 de luz.

## I2. Chão com carpete como "tapete"
**Evidência**: `light_gray_carpet` 9 (01), 26 (04), 8 (03); `orange_carpet` 7 (02).
**Interpretação**: marca zona central. Confiança média.

## Não determinado
Iluminação interna: poucos dados (1 soul_lantern em 02, 2 lanternas em 22). A rotina de luz não foi alterada em quantidade suficiente.

## I3. Lobby de minigame de terror (Hunter): moldura, forro, cerca e luz (correções do dono, 2026-11-11) [TESTADO no jogo]
- **Pé e capitel nos postes**: escada de madeira encostada na base do pilar/tronco (e na cabeça, sob a viga) integra o poste ao bloco de madeira de trás e dá moldura. Pilar liso do chão ao teto parece cano.
- **Forro com volume**: `slab` + `trapdoor` sob o teto/telhado (beiral e caixotão) em vez de teto de tábuas lisas.
- **Nunca meio bloco onde se fica em pé**: cerca/guarda-corpo baixo deixa o jogador parar em cima e no canto. **Cobrir a cerca com slab** (ou usar parede alta/barreira) em volta de qualquer pad, porta ou ponto de interação do jogo. Em minigame, isso já impediu a partida de começar (a pessoa ficou fora do pad).
- **Luz escondida e orgânica**: trocar `sea_lantern`/lâmpada visível atrás de vitral por `shroomlight` (ou luz escondida atrás de vigas). Vitral + luz atrás continua válido, mas a fonte não deve aparecer como "lâmpada".
- **Tema manda**: terror de fuga na floresta = casa/cabana abandonada (madeira escura, musgo, ardósia), não salão ritual. Conferir sempre se a arquitetura conta a mesma história do jogo.
- **Confira de DENTRO**: portais e saídas devem ser vistos do ponto de chegada (E-39).
