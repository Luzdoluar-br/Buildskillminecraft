# Paletas e combinações de blocos

> Status: rascunho de biblioteca | Confiança: média (IDs conferidos; combinações de estilo majoritariamente [INT], [NÃO TESTADO]) | Última revisão: 2026-11-09

## Resumo
- Paleta = 1 dominante + 1-2 de apoio + 1 acento; 60/30/10 é só heurística de decoração [INT] sem autor nem estudo.
- Misturar 2-3 tons próximos na massa dá textura de "pedra real"; contraste forte fica para moldura, estrutura e acento.
- IDs abaixo existem em `../referencia/blocos-bedrock.md`; o render não mostra cor final de folha, cobre ou lã (aparecem cinza), então paletas de cor são [NÃO TESTADO].

## Conceito
Paleta combina valor (claro/escuro), matiz e textura. Em Minecraft o desenho da textura pesa tanto quanto a cor: tijolo regular parece novo, mistura irregular parece usado (T6). A regra 60/30/10 é folclore de decoração: nenhuma fonte nomeia autor, data ou estudo (A1_r2 itens 5-6, só busca). Serve como ponto de partida rotulado [INT].

## Características / regras

### Estrutura da paleta [INT]
| Papel | Fatia aproximada | Função |
|---|---|---|
| Dominante | >= ~50-60% da área visível | massa/parede |
| Apoio (1-2) | ~25-30% | estrutura, base, telhado, moldura |
| Acento | < ~10-15% | portas, lanternas, detalhes, ênfase |
Teste (A1_r2): contar blocos no render; se 3+ materiais disputam o mesmo percentual, "não há dominante". No máximo ~4 materiais principais (heurística de guias, só busca).

### Esquemas de cor [INT, NÃO TESTADO]
- Monocromática: variações de um matiz (ex.: cinzas de pedra) com valores diferentes. Segura, coesa.
- Análoga: matizes vizinhos (madeira + terracota + tijolo). Quente e unificada.
- Complementar: matizes opostos só no acento (laranja/azul, magenta/ciano). Usar pouco.

### Lições já testadas (Aulas 01-02)
- T1: tirar o bloco de padrão forte da massa e distribuir 2-3 tons próximos (stone, tuff_bricks, polished_andesite, smooth_stone); dominante ~60%, 1-2 de apoio, sem contraste forte [TESTADO-AULA02, interpretação de confiança média].
- T2: tronco descascado = estrutura; tábua/concreto = preenchimento.
- T3: madeira clara contra pedra/concreto escuro destaca portas.
- T6: pavimento com 3-4 pedras (andesite 45, cobblestone 28, gravel 22, light_gray_wool 11 no exemplo da Aula 01).
- Imagem boa não é construção correta: listar os nomes únicos da paleta no `.mcstructure` e conferir (ver `../erros-e-licoes.md`).

### Mistura ponderada [INT sobre T1/T6]
Receita: dominante 60%, vizinho de tom próximo 25%, vizinho 2 de 10%, rachado/musgo 5%. Distribuição aleatória com semente fixa, sem agrupar por manchas grandes (a menos que seja desgaste proposital).

### Paletas por estilo (IDs conferidos; combinação [NÃO TESTADO] salvo indicação)
| Estilo/ambiente | Dominante | Apoio | Acento |
|---|---|---|---|
| Medieval pedra-musgo | `stone_bricks`, `cobblestone` | `mossy_stone_bricks`, `spruce_planks`, `stripped_spruce_log` | `lantern`, `dark_oak_planks` |
| Enxaimel | `white_terracotta` ou `white_concrete` | `stripped_dark_oak_log` | `spruce_planks` |
| Japonês | `white_concrete` ou `white_terracotta` | `dark_oak_log`, `stripped_dark_oak_log`, `spruce_planks` | `lantern`, `bamboo_planks` |
| Industrial | `gray_concrete`, `light_gray_concrete` | `iron_bars`, `polished_andesite`, `stone_bricks` | `orange_concrete`, `lantern` |
| Brutalista | `light_gray_concrete`, `smooth_stone` | `gray_concrete` | `glass_pane` em recesso |
| Moderno | `white_concrete`, `glass` | `stripped_oak_log` ou `pale_oak_planks`, `black_concrete` | `sea_lantern`, `lantern` |
| Cyberpunk neon sobre concreto sujo | `gray_concrete`, `black_concrete`, `cracked_stone_bricks` | `iron_bars`, `blackstone` | `magenta_concrete`, `cyan_concrete`, `sea_lantern`, panes tingidos |
| Solarpunk | `oak_planks`, `stripped_birch_log` | `glass`, `moss_block`, `azalea_leaves` | `flowering_azalea`, `copper_block` |
| Pântano futurista | `mud_bricks`, `mangrove_planks` | `moss_block`, `weathered_copper`, `oxidized_copper` | `sea_lantern`, `cyan_stained_glass_pane` |
| Ruína de pedra | `mossy_stone_bricks`, `mossy_cobblestone` | `cracked_stone_bricks`, `moss_block`, `vine` | `short_grass`, `fern` |
Notas: concreto não emite luz; "neon" em cyberpunk vem de `sea_lantern`, `shroomlight`, `glowstone` e vidros tingidos [INT]. Pedra-musgo, madeira dupla e mistura de cinzas vêm da Vila (Aula 02); o resto das linhas não foi construído nem renderizado.

## Como construir no Bedrock
1. Escolha o dominante e confirme o ID: `grep` em `../referencia/blocos-bedrock.md`. IDs de frequente erro: `normal_stone_slab` (não `stone_slab`); cerâmica = `hardened_clay`/`white_terracotta`.
2. Monte a mistura 60/25/10/5 com semente fixa; pavimento irregular com 3-4 pedras. [T1/T6 TESTADO-AULA02]
3. Reserve o acento para pontos de ênfase (porta, lanterna, canto). [INT]
4. Renderize para forma/silhueta, mas confira cor no jogo (folha, cobre, lã aparecem cinza). [TESTADO: limite do render, Aula 02]
5. Para neon: 1 cor de acento por quarteirão; luz branca/âmbar como base. [NÃO TESTADO]

## Combina com
- [../tecnicas/materiais-e-paletas.md](../tecnicas/materiais-e-paletas.md)
- [envelhecimento-e-deterioracao.md](envelhecimento-e-deterioracao.md)
- [vidro-luz-e-metal.md](vidro-luz-e-metal.md)
- [../fundamentos/profundidade-contraste-transicoes.md](../fundamentos/profundidade-contraste-transicoes.md)
- [../estilos/futurista-cyberpunk-solarpunk.md](../estilos/futurista-cyberpunk-solarpunk.md)
- [../estilos/industrial-e-brutalista.md](../estilos/industrial-e-brutalista.md)
- [../estilos/japones-tradicional.md](../estilos/japones-tradicional.md)
- [../estilos/medieval-europeu-e-fantasia.md](../estilos/medieval-europeu-e-fantasia.md)
- [../erros-e-licoes.md](../erros-e-licoes.md)

## Erros comuns
- IDs de memória (`stone_slab`, `waxed_copper_block`, `oak_door`): conferir sempre.
- 3+ materiais com o mesmo peso (sem dominante).
- Misturar tons distantes na massa (vira ruído).
- Manchas grandes de uma pedra só sem causa.
- Julgar paleta pelo render (cor de folha/cobre/lã errada).
- Acento em toda parte (Ching: se tudo é enfatizado, nada é).

## Limitações e dúvidas
- 60/30/10 e "4 materiais" são heurísticas sem fonte [INT/só busca].
- Matizes das paletas de estilo não foram renderizados nem testados no jogo.
- Cor real de vidro tingido, cobre e lã depende da textura do jogo, não do render.

## Fontes e evidências
- A1_r2 itens 5-6 (60/30/10, só busca); `../tecnicas/materiais-e-paletas.md` (Aulas 01-02); `../erros-e-licoes.md`.
- IDs conferidos em `../referencia/blocos-bedrock.md` (oficial, v1.26.60.5).
- `../experimentos/README.md` (limite do render sobre cor).
