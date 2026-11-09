# Futurista, cyberpunk e solarpunk

> Status: rascunho; nenhuma receita deste documento foi testada em render | Confiança: média nas definições, baixa nas receitas | Última revisão: 2026-11-09

## Resumo
Três linguagens DIFERENTES de "futuro": futurista/ficção científica (formas aerodinâmicas e módulos, otimista), cyberpunk (denso, vertical, sujo, neon) e solarpunk (verde, madeira e vidro, luz). As definições têm fonte; as receitas em blocos são todas [INT, NÃO TESTADO], apoiadas só em achados de X02/X03/X05 sobre curvas e verticalidade.

## Conceito
Legenda de honestidade: **consenso** = fonte aberta confirma; **especulação** = lista de traços sem fonte; **interpretação própria** = [INT].
| Linguagem | Consenso (fonte) | Especulação / não verificado | Interpretação própria |
|---|---|---|---|
| Streamline Moderne | linhas horizontais, cantos arredondados, janelas redondas/em faixa, branco e pastéis [DOC Wikipedia] | fonte institucional (Britannica 403) | bandas brancas/azuis |
| Googie | telhados inclinados para cima, bumerangues, starbursts, letreiros grandes; nome de Googie's Coffee Shop (1949, Lautner), Haskell 1952 [DOC Wikipedia] | -- | letreiro em `glowstone` |
| Metabolismo | movimento japonês dos anos 1960 (Kikutake, Kurokawa, Maki, Tange), cidade como organismo [DOC ArchDaily + Wikipedia] | Nakagin 2,5 x 2,5 x 4,0 m, janela ~1,3 m: [NV] fonte única | cápsula 3x3x4 |
| Cyberpunk | Blade Runner (1982): Syd Mead e Lawrence G. Paull confirmados; Scott: "Hong Kong on a very bad day" [DOC] | influência de Hong Kong só Wikipedia | camadas e neon |
| Kowloon | ver abaixo | letreiros e poços de luz: sem fonte | ruelas, passarelas |
| Solarpunk | termo de 2008; manifesto de Adam Flynn (2014, Project Hieroglyph) aberto [DOC] | lista fixa de traços (curvas, madeira+vidro) como regra do gênero | tudo o que está em "Como construir" |
- **Kowloon Walled City** [DOC, Wikipedia + Far Out, lidos]: 2,6 ha (~210 x 120 m), ~33.000 moradores em 1987, 13-14 andares por limite do aeroporto Kai Tak, becos de 1-2 m, construções empilhadas sobre as antigas. Altura em metros: não informada; 3 m por andar é [INT].
- Flynn: cita "art nouveau Edwardian-garden aesthetic" só como uma visão de fãs, e rejeita visões modernistas "lisas, limpas e brancas". "Vitral" NÃO aparece no manifesto [REFUTADO]. Solarpunk não tem arquitetura canônica [INT].
- Cuidado: cyberpunk tem crítica de "tecno-orientalismo" [DOC Wikipedia]; evite caricatura da Ásia.

## Características / regras
| | Futurista | Cyberpunk | Solarpunk |
|---|---|---|---|
| Humor | otimista, aerodinâmico | opressivo, saturado | calmo, abundante |
| Forma [INT] | discos, arcos, cápsulas, balanços | torres estreitas empilhadas e anexadas | madeira e vidro com curvas, jardins |
| Cor [INT] | branco, azul-claro, vermelho/laranja (Googie) | cinza/preto sujos + 2-3 neons por quadra | verde, creme, madeira clara, cobre oxidado |
| Luz [INT] | faixas brancas/ciano | neon sobre superfície molhada | luz natural, vidro claro |
- Cuidados do Bedrock vindos de teste: círculo de blocos só lê como círculo a partir de diâmetro ~15; janela redonda 3x3 NÃO lê [TESTADO X03, X02]. Abóbada de raio 4 parece caixa chanfrada [TESTADO X01].

## Como construir no Bedrock
**F1 — Streamline [NÃO TESTADO]**: caixa horizontal 21 x 9 x 6; cantos arredondados com escada + laje (raio de canto 3-4, aceitar polígono); bandas alternadas `white_concrete` / `light_blue_concrete` a cada 2 blocos de altura; janela em faixa contínua de 2 de altura (a faixa lê [TESTADO X02]); janelas redondas só se o diâmetro for grande, senão use quadradas.
**F2 — Googie [NÃO TESTADO]**: telhado em diagonal com escadas invertidas em "V" (diagonal 45° exige espessura 2 [TESTADO X03]); letreiro alto com `red_concrete`/`orange_concrete` e `glowstone`.
**F3 — Metabolista [NÃO TESTADO]**: núcleo de concreto 3x3 (cinza); cápsulas 3x3x4 ancoradas a ele (cápsula real é 2,5x2,5x4 [NV]); alternar posições e deixar 1-2 vagas. Janela: 1x1 ou 2x2 quadrada.
**C1 — Cyberpunk [NÃO TESTADO]**: lote 12x12 a 16x16; torre de 13 andares de 3 blocos (~39, [INT] coerente com 13-14 andares de Kowloon).
1. Térreo: ruelas de 2-3 blocos de largura (reais eram 1-2 m; 2 dá passagem confortável) cobertas por passarelas.
2. Meio: andares superiores avançam 1-2 blocos sobre a rua; varandas de `iron_bars`; anexos em material diferente [INT, em linha com a estratigrafia de X04/A5].
3. Topo: antenas (`lightning_rod`; rotacione o estado), caixas d'água, letreiros.
4. Parede: `gray_concrete`, `black_concrete`, `deepslate`, `tuff`, `cracked_deepslate_bricks` misturados (sujeira). Piso molhado: lajes escuras.
5. Neon: vidro tingido (`magenta_stained_glass`, `cyan_stained_glass`) com `sea_lantern` ou `glowstone` atrás; máximo 2-3 cores por quadra [heurística INT].
**S1 — Solarpunk [NÃO TESTADO]**: estrutura de `stripped_birch_log`/`birch_planks`, panos largos de `glass`; telhado em duas águas suave 1:2 [TESTADO X01-b] com `daylight_detector` como painéis solares; floreiras (alçapão + terra) com `vine`, `moss_carpet`, `azalea`, `flowering_azalea`, `hanging_roots`; cobre oxidado (`oxidized_copper`, `cut_copper`) em detalhes. Referência real de "floresta vertical": Bosco Verticale (torres de 80 e 112 m, ~800 árvores, dados do estúdio; fontes divergem), que NÃO é "solarpunk por definição" [INT].

## Combina com
- [Modernista](modernista-e-contemporaneo.md), [Industrial/brutalista](industrial-e-brutalista.md), [Pós-apocalíptico](pos-apocaliptico-subterraneo-liminal.md) (contraste distópico).
- [Arranha-céus](../estruturas/arranha-ceus.md), [Vilas e cidades](../estruturas/vilas-e-cidades.md), [Iluminação](../ambientacao/iluminacao-e-atmosfera.md), [Vidro, luz e metal](../materiais/vidro-luz-e-metal.md), [Paletas](../materiais/paletas-e-combinacoes.md).

## Erros comuns
- Misturar Googie colorido com Streamline branco sem intenção; só branco sem acento [INT].
- Cyberpunk: neon demais com parede limpa; rua larga e vazia; sem camadas [INT].
- Solarpunk: "verde em tudo", sem desenho nem tecnologia visível (água, solar, vento); formas retas e duras [INT].
- Metabolismo como "blobs": é estrutura + módulo [INT].
- Círculos pequenos fingindo curva [TESTADO X03].

## Limitações e dúvidas
- Todas as receitas deste documento são [NÃO TESTADO]; nenhum render.
- Medidas Nakagin e Villa Savoye: fonte única. Poços de luz/letreiros de Kowloon: sem fonte.
- Solarpunk arquitetônico é definido pela comunidade; tratar como convenção e não como norma.
- `daylight_detector` como painel solar e as cores de neon são escolhas visuais minhas.

## Fontes e evidências
- Wikipedia: Streamline Moderne, Googie, Metabolism, Nakagin Capsule Tower, Retrofuturism, Cyberpunk, Blade Runner, Solarpunk, Art Nouveau (resumos, rodada 1).
- Abertas (rodada 2): ArchDaily tag Metabolism; hieroglyph.asu.edu (Flynn 2014); AV Club (Mead); página do estúdio Boeri (Bosco Verticale); Wikipedia + Far Out Magazine (Kowloon, rodada 2 de A5). MoMA: só busca.
- Não abriram: Britannica, Domus, e-flux (404).
- `../experimentos/X01-telhados/RESULTADO.md`, `../experimentos/X02-fachadas-e-janelas/RESULTADO.md`, `../experimentos/X03-curvas-e-diagonais/RESULTADO.md`.
