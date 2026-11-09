# Gótico

> Status: geometria calculada, janelas e contrafortes testados por render (X02) | Confiança: média-baixa (uma fonte terciária por tema) | Última revisão: 2026-11-09

## Resumo
Gótico = verticalidade: ogiva, contrafortes que absorvem o empuxo, janelas altas e rosácea. Em Minecraft a ogiva só lê com largura >= 3 e altura >= 6; contrafortes salientes dão o ritmo. Curvas finas de tracery não existem no Bedrock: aproximar.

## Conceito
- [DOC, aberta (Wikipédia, resumo)] Nasce no norte da França no fim do séc. XII (coro de Saint-Denis, 1140-1144, tido como o primeiro); origem debatida porque arcos ogivais já aparecem no românico tardio.
- [DOC] Abóbada de nervuras + contrafortes + arcobotantes permitem paredes mais altas e janelas maiores; rosácea, pináculos, tracery, vitrais.
- [DOC] Ogiva de dois centros (Wikipédia, Arch): equilátera = centros nos pontos de arranque opostos, formando triângulo equilátero com o ápice; lanceta = centros mais afastados (mais estreita); arco "drop" = centros mais próximos (mais largo).

## Características / regras
| Item | Valor | Rótulo |
|---|---|---|
| Chartres, nave | ~37 m de altura; 16,4 m de largura; torres 105 m e 113 m | [DOC] Wikipédia (resumo parcial). 38 m foi refutado |
| Beauvais, coro | ~47,5 m (a mesma página cita também 48,5 m); colapso da abóbada em **1284** | [DOC] Wikipédia |
| Saint-Eustache | 105 x 44 x 35 m (híbrido gótico-renascentista) | [DOC] Wikipédia (rodada 1) |
| Altura da ogiva equilátera | altura = vão x 0,87 (lado x raiz(3)/2). Vão 5 = ~4,3; vão 7 = ~6 | [INT] cálculo próprio a partir da geometria documentada |
| Razões nave 1:2 a 1:3, janelas 1:4 | | [NV] / [INT] (nenhuma razão confirmada nas fontes) |
| Paleta: calcário claro, telhado cinza-azulado | | [INT] |

Nota: "vão x 0,87" é altura **do arco acima do arranque**; em blocos inteiros arredonde e confira em render.

## Como construir no Bedrock
**Receita A - fachada gótica 17 x 12 [TESTADO X02 F4, parcialmente]**
1. Paredão de 2 de espessura (`stone_bricks`, `andesite`, `polished_andesite` misturados), 11 de altura.
2. Contrafortes salientes 2 blocos para fora, a cada 4 blocos (x = 0, 4, 8, 12, 16), do chão até y=9; capa em `stone_brick_stairs` + `stone_bricks`.
3. Cornija de `polished_andesite` no topo (2 de profundidade).
4. Medido: 4 planos; "boa verticalidade", contrafortes dão ritmo.
5. **Alerta**: a janela usada na F4 foi 1 de largura x 5. O teste das janelas (abaixo) mostra que ogival 1 de largura **não lê**. Na fachada, o efeito veio dos contrafortes, não das janelas.

**Receita B - janela ogival que lê [TESTADO X02: mínimo; geometria em [INT]]**
- Mínimo para ler: **>= 3 de largura e >= 6 de altura**. Com 1 de largura parece entalhe.
- Vão 3: duas colunas de ombro (altura ~3), depois escadas invertidas cortando os cantos e laje/bloco no vértice. Altura total alvo 6+ (lanceta: vão menor, ápice mais alto).
- Vão 5 equilátero: ápice ~4,3 acima do arranque; some 3-4 blocos de ombreira reta para chegar a 8 de altura total.
- Moldura (ombreira `polished_andesite`, verga em escada invertida, soleira em laje) foi a janela de melhor custo-efeito [TESTADO X02 para janela retangular].
- Vidro: `*_stained_glass_pane` coloridos em moldura de pedra [NÃO TESTADO]; tracery fina com `iron_bars` e `stone_brick_wall` [NÃO TESTADO].

**Receita C - nave interior** [NÃO TESTADO]: >= 12-16 blocos livres de altura (heurística [INT]); pilares `quartz_pillar` ou `polished_andesite` com `stone_brick_wall` nas faces; nervuras com escadas e lajes invertidas no forro.

**Receita D - telhado e flechas**: telhado muito íngreme, >= 60 graus [INT]; 1:1 (45 graus) é o mais íngreme testado [TESTADO X01]; mais íngreme (2:1 vertical) [NÃO TESTADO]. Pináculos: `stone_brick_wall`, `end_rod`, `lightning_rod`, `calcite`.

**Receita E - rosácea** [NÃO TESTADO e provavelmente não lê]: círculo só lê a partir de diâmetro ~15 [TESTADO X03]. Rosácea de raio 5-7 (diâmetro 11-15) fica no limite; trate como octógono se menor.

**Arcobotante** [NÃO TESTADO]: escadas e lajes subindo em diagonal da nave ao contraforte.

## Combina com
- `medieval-europeu-e-fantasia.md`, `vitoriano.md` (Gothic Revival), `../estruturas/templos-e-monumentos.md`
- `../fundamentos/escala-e-proporcao.md`, `../fundamentos/composicao-hierarquia-silhueta.md`
- `../materiais/vidro-luz-e-metal.md`, `../ambientacao/iluminacao-e-atmosfera.md`

## Erros comuns
- Janela larga e quadrada, ou ogiva feita como triângulo (cantos retos).
- Ogiva de 1 de largura: não lê [TESTADO X02]. Arco pleno de 3 de largura vira trapézio: não use em "românico" pequeno.
- Sem contrafortes; cornija ausente; paleta toda cinza sem variação de pedra.
- Usar 38 m (Chartres) ou 1248 (Beauvais) em texto: ambos refutados.

## Limitações e dúvidas
- Curvas finas de tracery, nervuras e arcobotantes reais: só aproximados.
- O render não mostra transparência de vidro nem cor final.
- Nenhuma razão geométrica (nave, torre) confirmada; altura = vão x 0,87 vale só para ogiva equilátera ideal.
- Nada testado andando no jogo.

## Fontes e evidências
- Wikipédia EN, abertas via resumo: Gothic architecture (primeiros 100 mil caracteres), Chartres Cathedral (100 mil de 206 mil), Beauvais Cathedral, Arch.
- Britannica: 403, não lida. Smarthistory: 404.
- `../experimentos/X02-fachadas-e-janelas/RESULTADO.md`, `X03-curvas-e-diagonais/RESULTADO.md`, `X01-telhados/RESULTADO.md`.
