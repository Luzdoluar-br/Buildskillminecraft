# Japonês tradicional

> Status: módulo e telhado de dois beirais testados por render (X01, X02); inclinações e termos de telhado NÃO verificados | Confiança: média | Última revisão: 2026-11-09

## Resumo
Silhueta baixa e horizontal, telhado maior que as paredes, beiral muito projetado, base de pedra, madeira, shoji. O módulo ken (~1,82 m) vira 2 blocos por arredondamento próprio. A fachada japonesa foi a que mais camadas teve no teste (7 contando dois níveis de beiral).

## Conceito
- [DOC, aberta (Wikipédia, resumo)] Quase tudo em madeira; pedra só em pódios, fundações de pagode, bases de casas Edo e muralhas de castelo. Telhas de cerâmica a partir do período Heian.
- [DOC] Beirais levemente curvos e muito projetados; templos usam mísulas; o beiral grande deixa o interior escuro. Shoji: painéis de madeira com papel (shoin-zukuri). A varanda sob o beiral é o espaço que o projeto chama de engawa (a fonte lida não usa o termo).
- [DOC] Irimoya: quatro águas com empena no topo; a empena cobre o moya (núcleo), as águas cobrem o hisashi (galeria); veio da China no séc. VI (também dita xieshan no lado chinês).
- [DOC] Castelo: tenshu de 3 a 5 andares (Azuchi até 7), base de pedra em talude (musha-gaeshi), reboco sobre madeira, muros de pedra e fossos. Pagode de cinco andares de Horyu-ji, séc. VII.
- [DOC] Torii: pilares, kasagi, shimaki, nuki; madeira natural ou vermelho vivo; preto só em kasagi e nemaki. Torii de Nakayama Jinja ~9 m.

## Características / regras
| Item | Valor | Rótulo |
|---|---|---|
| Ken | ~1,82 m padrão; varia no tempo; até 1,97 m em Kansai | [DOC] Wikipédia (confirmada) |
| Tatami | padronizado no Muromachi como 1 ken x meio ken; regional 1,91 / 1,82 / 1,76 m de comprimento (Kyoto, Nagoya, Edo) | [DOC] Wikipédia |
| Baias | número ímpar (3x3, 5x5); salão principal do Enryaku-ji 11x6 baias (37,60 x 23,92 m) | [DOC] Wikipédia (Ken) |
| 1 ken = 2 blocos; sala de 6 jo ~ 3x4 blocos | arredondamento (1,82 para 2 = erro de ~10%; Kansai 1,97 fica quase exato) | [DOC] base + [INT] conversão |
| Kirizuma, hogyo, yosemune: definições e inclinação | JAANUS deu 403 | [NV] |
| Inclinação típica dos telhados | não achada em fonte aberta | [NV] |
| Pagode de andares ímpares | tradição geral, fonte não aberta | [NV] |
| Paleta: madeira clara/escura, reboco branco, telhado cinza escuro, vermelho só em santuário/torii | preto edoguro é [DOC]; o resto [INT] | [INT] |

## Como construir no Bedrock
**Receita A - fachada com engawa (17 de largura) [TESTADO X02 F5]**
1. Plataforma de pedra `stone_bricks`+`andesite`, 1 de altura, de x=0 a 16, profundidade de z=-2 a 3.
2. Engawa: piso `pale_oak_planks` elevado sobre a plataforma, 2-3 blocos de largura sob o beiral.
3. Pilares `stripped_dark_oak_log` (`pillar_axis=y`) a cada 4 blocos, 6 de altura, na frente da engawa (módulo de 2 blocos por ken: um pilar a cada 2 kens).
4. Shoji **recuado** 3 planos atrás dos pilares: `white_stained_glass_pane` 1x4 com montantes `stripped_dark_oak_log` a cada 4.
5. Forro `dark_oak_planks` no topo dos pilares (y=7), de x=-1 a 17 e profundidade -3 a 3; beiral em 2 níveis de `spruce_stairs` (y=8 na ponta, y=9 um bloco para dentro); cobertura `spruce_planks` (y=10).
6. Medido: 7 planos distintos (inclui os dois níveis de beiral); silhueta marcante.

**Receita B - pagode de 2 beirais [TESTADO X01-f: 275 blocos, 2,1x o custo do quatro águas de 99]**
Sobre caixa de pedra 9x7 com paredes de 4:
1. Forro de `spruce_planks` em y=5 de x=-1..9, z=-1..7.
2. Primeira cobertura: `tenda` de `dark_oak_stairs` com beiral 2, só 2 fileiras (y=6).
3. Cantos levantados: `spruce_slab` na posição de canto a 2 blocos além da parede (-2,-2), (10,-2), (-2,8), (10,8), em y=6.
4. Forro invertido: `spruce_slab` com `vertical_half=top` em y=5 nas linhas z=-2 e z=8, de x=-2 a 10 (esconde o dente das escadas).
5. Segundo pavimento: bloco `spruce_planks` 7x5 (x=1..7, z=1..5) em y=8; segunda `tenda` menor (2..6 x 2..4, y=9), beiral 1.
6. Resultado: silhueta mais rica e reconhecível; pagoda real (5 andares) é [NÃO TESTADO]: repita o par "andar menor + beiral" com larguras decrescentes.

**Receita C - casa baixa com telhado 1:2** [TESTADO X01-b para forma]: `telhado_suave_x` dá casa baixa e longa; adicionar beiral de 2-3 blocos [INT].

**Receita D - castelo (tenshu)** [NÃO TESTADO]: base de pedra em talude por degraus escalonados (escada), 2-3 pisos de reboco `white_concrete`, telhados escalonados cinza escuro; karahafu e chidori-hafu não definidos nas fontes [NV].

**Receita E - torii** [NÃO TESTADO]: pilares 1x1 vermelhos (`red_concrete`), kasagi de 5-7 blocos com pontas levantadas, base preta `black_concrete`.

## Combina com
- `chines-tradicional.md` (não misturar), `../estruturas/templos-e-monumentos.md`, `../estruturas/casas-e-edificios-residenciais.md`
- `../fundamentos/escala-e-proporcao.md`, `../fundamentos/profundidade-contraste-transicoes.md`
- `../tecnicas/telhados-e-beirais.md`, `../tecnicas/cantos-e-vigas.md` (casa de chá da Vila), `../materiais/paletas-e-combinacoes.md`

## Erros comuns
- Beiral curto (1 bloco): perde o caráter; no Japão o beiral pode ser 2-3 [INT].
- Telhado vermelho/amarelo (chinês) em prédio japonês; torii de cor errada.
- Pilares sem base de pedra; telhado "casinha" sem hierarquia de andares.
- Torre/torii circular de diâmetro < 15: vira quadrado arredondado [TESTADO X03].
- Esquecer o forro de laje invertida sob o beiral (fica o "dente" de escadas).

## Limitações e dúvidas
- Curvatura suave do beiral e da cumeeira: impossível; aproximar com 1 bloco levantado no canto [DOC/INT].
- Inclinação de telhado e nomes kirizuma/hogyo/yosemune: NÃO VERIFICADOS (JAANUS 403). Sugestão: obter por navegador ou pelo livro de Nishi e Hozumi.
- Ken = 2 blocos tem erro de ~10% em relação a 1,82 m; aceito pela grade.
- Direção e abertura de alçapões/persianas não confirmadas no jogo.

## Fontes e evidências
- Wikipédia EN, abertas via resumo: Japanese architecture, Japanese castle, East Asian hip-and-gable roof, Torii, Ken (unit), Japanese units of measurement, Tatami.
- aanda.org/JAANUS: 403 (5 páginas).
- `../experimentos/X01-telhados/RESULTADO.md` (receita f), `X02-fachadas-e-janelas/RESULTADO.md` (F5), `X03-curvas-e-diagonais/RESULTADO.md`.
