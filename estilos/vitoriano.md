# Vitoriano (Gothic Revival, Queen Anne, Italianate)

> Status: só pesquisa em Wikipédia, nenhum teste de construção deste estilo | Confiança: baixa | Última revisão: 2026-11-09

## Resumo
O vitoriano é um conjunto de estilos: Gothic Revival/Carpenter Gothic (empenas íngremes, ogivas), Queen Anne (assimétrico, torres, varandas, bay windows) e Italianate (telhado baixo, mísulas, cúpula). Em comum: silhueta recortada e ornamento denso. Proporções e paletas históricas NÃO foram verificadas; tudo de cor é hipótese.

## Conceito
- [DOC, aberta (Wikipédia, resumo)] Gothic Revival: estilo romântico do início do séc. XIX, reação à simetria paladiana; usou ferro fundido e forjado (ex.: Victoria Building, Liverpool, 1893, tijolo vermelho).
- [DOC] Queen Anne (EUA, 1880-1910; Carson Mansion, Eureka, 1884-86): fachada assimétrica; torres redondas, quadradas ou poligonais; janelas oriel e bay; varanda frontal envolvente (muitas vezes em L); beirais salientes, telhados piramidais ou de quatro águas; telhas de madeira com padrão (escama de peixe); madeira, tijolo, terracota, ardósia.
- [DOC] Italianate: telhado baixo ou plano, em geral de quatro águas, às vezes oculto por parapeito; beirais salientes sobre mísulas e cornijas pesadas; torres belvedere/cúpula/campanário; janelas arqueadas, com frontão ou serlianas, mais altas no piano nobile; cantoneiras (quoins), loggias, balaustradas.
- [DOC] Carpenter Gothic: empena central íngreme, bargeboards (gingerbread), janelas ogivais, board-and-batten.
- [DOC] "Painted Ladies" é um termo para casas coloridas, não um estilo.
- [DOC, só busca] Policromia construtiva: tijolo/pedra coloridos para mostrar a estrutura, ligada a Ruskin; Neil Jackson (Architectural History) argumenta que o interesse começou antes de Ruskin (página da Cambridge não aberta).

## Características / regras
| Item | Valor | Rótulo |
|---|---|---|
| Proporções numéricas (altura/largura, inclinação) | nenhuma verificada | [NV] |
| Silhueta assimétrica e recortada: torre de canto, várias empenas, varanda larga, chaminés altas | | [INT] |
| Paleta: verde-oliva, bordô, ocre, creme; tijolo vermelho com faixas pretas ou cremes; telhado de ardósia escura; 3+ cores por fachada | **paleta por estilo [NV]**; Historic England/V&A/Victorian Society não achados | [NV] + [INT] |
| Janelas altas e verticais, vidros divididos | | [INT] |
| Queen Anne = telhado íngreme e varanda; Italianate = telhado baixo e mísulas: não misturar | [DOC] nos elementos, [INT] na regra | [INT] |

## Como construir no Bedrock
Nada abaixo foi construído nem renderizado [NÃO TESTADO]; usa-se apenas técnicas testadas em outros estilos como base (avanço de andar, planos de profundidade, janela com moldura).

**Receita A - casa Queen Anne, volume ~11x9, 2 andares + sótão [NÃO TESTADO]**
1. Corpo em `spruce_planks`/`dark_oak_planks` ou tijolo (`brick_block`, `brick_stairs`, `brick_slab`), 4 de altura por andar.
2. Telhado de empenas cruzadas íngreme: 1:1 (testado em X01-a, 131 blocos na caixa 9x7) com uma empena transversal; Queen Anne com telhado raso é erro.
3. Torre de canto: diâmetro >= 15 só para círculo de verdade [TESTADO X03]; para 5x5, assuma torre **octogonal/quadrada de cantos chanfrados** com cone de `*_stairs`.
4. Bay window: 3 faces salientes 1 bloco com `glass_pane` e laje de teto: é o "avanço de 1 bloco" que mais ajuda fachada [TESTADO X02 F1 para avanço de andar].
5. Varanda envolvente em L: laje + `spruce_fence` + escadas; 2 de largura.
6. Ornamento: `*_trapdoor`, botões, cercas como gingerbread; shingles alternando escadas e lajes de tom levemente diferente.

**Receita B - casa Italianate [NÃO TESTADO]**: telhado baixo (use `telhado_suave_x` 1:2 ou plano com platibanda: X01-b e X01-g leem bem); mísulas = `*_stairs` invertidas + alçapões em fileira sob o beiral largo; cúpula quadrada no topo; janelas altas 1x3 com verga em escada invertida (moldura = melhor custo-efeito em X02); quoins alternando bloco de tom diferente nos cantos.

**Receita C - Carpenter Gothic/Gothic Revival [NÃO TESTADO]**: empena íngreme com bargeboard de alçapões/cercas; janela ogival só com >= 3 de largura e >= 6 de altura [TESTADO X02]; janela ogival 1x3 como na rodada 1 **não lê** e não deve ser usada.

**Policromia [NÃO TESTADO]**: banda horizontal de tijolo de cor diferente (ex.: `brick_block` com faixa de `stone_bricks` ou `white_terracotta`) a cada 2-3 fiadas.

## Combina com
- `gotico.md`, `medieval-europeu-e-fantasia.md`
- `../estruturas/casas-e-edificios-residenciais.md`, `../estruturas/vilas-e-cidades.md`
- `../materiais/paletas-e-combinacoes.md`, `../fundamentos/composicao-hierarquia-silhueta.md`, `../tecnicas/telhados-e-beirais.md`

## Erros comuns
- Casa simétrica e monocromática; Queen Anne com telhado raso; torre sem cone; sem varanda.
- Misturar Italianate (telhado baixo) com empenas íngremes [INT].
- Janela ogival estreita 1 bloco: não lê.
- Tratar "Painted Ladies" como estilo arquitetônico.

## Limitações e dúvidas
- Filigrana (gingerbread) real é impossível; aproximar com cercas, alçapões e botões.
- Paletas históricas e proporções: [NV]; qualquer cor sugerida é hipótese.
- Doc quase todo [INT]: valide com um teste (render) antes de tratar como regra.
- Sem teste, sem experimento próprio; confiança baixa.

## Fontes e evidências
- Wikipédia EN, abertas via resumo: Victorian architecture, Queen Anne style architecture in the United States, Italianate architecture, Carpenter Gothic.
- Cambridge (Architectural History, Neil Jackson): só busca, não aberta. Historic England, V&A, Victorian Society: não retornaram na busca.
- `../experimentos/X01-telhados/RESULTADO.md`, `X02-fachadas-e-janelas/RESULTADO.md`, `X03-curvas-e-diagonais/RESULTADO.md`.
