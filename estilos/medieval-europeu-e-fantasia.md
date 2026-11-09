# Medieval europeu e medieval fantástico

> Status: rascunho validado em parte por render (X01, X02, Vila) | Confiança: média (histórico, só Wikipédia EN) / baixa (fantasia) | Última revisão: 2026-11-09

## Resumo
Enxaimel, castelo e românico se reconhecem por massa pesada, telhado dominante e fachada com 3-4 planos de profundidade. O avanço do andar superior é o recurso mais barato e mais forte (testado). "Fantasia" aqui é estilização própria [INT] sobre esse histórico: nada nas fontes documenta torres tortas ou telhados exagerados.

## Conceito
- [DOC, aberta (Wikipédia, resumo)] Enxaimel: estrutura de madeira com preenchimento entre os montantes; o mais antigo é pau-a-pique (wattle and daub), depois tijolo e pedra, em geral rebocado. Visual "preto-e-branco" = madeira escura + reboco claro.
- [DOC] Românico: arcos de volta perfeita, paredes muito espessas, poucas janelas pequenas e geminadas, torres grandes.
- [DOC] Castelo: motte e bailey, torre de menagem, muralha cortina com torres e seteiras, ameias, matacães, gatehouse com grade levadiça, fosso.
- [DOC, só busca] Alan Lee e John Howe: entrevista (Lee, 2005, resumo) diz que o contexto histórico é "ponto de partida" e o resto é inventado; Howe cita paisagens suíças e redesenhou a casa de Beorn para ficar mais grandiosa. Isso é tudo que sustenta a ponte histórico-fantasia.

## Características / regras
| Item | Valor | Rótulo |
|---|---|---|
| Jettying (andar superior avança) | séc. XIII-XVI, vigas em balanço; exemplo The Shambles, York | [DOC] |
| Contraventamento | diagonais ~45 graus (espinha de peixe), cruzes de Santo André (Alemanha), montantes juntos (Inglaterra/França) | [DOC] |
| Muralha cortina | ~3 m de espessura, ~12 m de altura, "variando muito"; donjon do séc. XII com paredes de 3-4 m | [DOC] |
| Românico | planta quadrada do cruzamento como módulo | [DOC]; "naves em baias quadradas": [NV] |
| Paleta de castelo (cinza variado) e de enxaimel (madeira escura + claro) | só a ideia de preto-e-branco é [DOC]; as cores em blocos são [INT] | [INT] |
| Fantasia: torres 2-3x mais finas/altas, telhado 50-70% da altura visível, assimetria, escala de porta/janela alterada | tudo [INT] (não documentado) | [INT] |

Fantástico = [INT]: estilizar é escolher exagerar proporções do histórico, mantendo sempre referência humana (porta, janela, escada) para a escala ser lida.

## Como construir no Bedrock
Convenção: 1 bloco = 1 m. IDs conferidos em `../referencia/blocos-bedrock.md`.

**Receita A - fachada de enxaimel com avanço (17 de largura x 12 de altura) [TESTADO X02 F1; TESTADO-AULA02 no chalé da Vila]**
1. Soco de pedra (`stone_bricks`, `andesite`, `cobblestone` misturados), 3 de altura, **recuado** 1 plano.
2. Viga de respaldo `stripped_spruce_log` (eixo horizontal) acima do soco.
3. Piso do andar de cima (`spruce_planks`) **avançando 1 bloco** para fora do soco.
4. Parede do andar: reboco `calcite` (+ `diorite`), 4 de altura; pilares `stripped_spruce_log` (`pillar_axis=y`) a cada 4 blocos; viga no topo.
5. Janelas `glass_pane` 1x2 entre pilares; mãos-francesas sob o avanço: `spruce_stairs` invertida a cada 2 blocos.
6. Resultado medido: 4 planos distintos (soco, avanço, pilares, mãos-francesas). Fachada lisa de controle: 1 plano, "papelão".
7. Cantos: tronco vertical contínuo, com degrau de escada, lanterna e ponta de viga: ver `../tecnicas/cantos-e-vigas.md` [TESTADO-AULA02].
8. Diagonais de contraventamento: só aproximadas (escada invertida dá diagonal de 2 blocos) [NÃO TESTADO].

**Receita B - telhado** [TESTADO X01]
- 1:1 (`telhado_x`, 131 blocos na caixa 9x7): linguagem de casa europeia íngreme/chalé.
- 1:2 (`Molde.telhado_suave_x`, 155 blocos): alterna escada (nível k) e laje inferior (k+1) com enchimento sob a laje; empenas fechadas por coluna. Lê como casa rural baixa.
- Quatro águas (`tenda`, 99 blocos): torres e volumes compactos.
- Fechar o plano interno do telhado (nunca só um anel): `../tecnicas/telhados-e-beirais.md`.

**Receita C - castelo e românico** [NÃO TESTADO, só [INT] das notas]
- Muralha: `stone_bricks` com `mossy_stone_bricks` e `cracked_stone_bricks` pontuais; espessura 2-3 blocos; ameia alternando bloco e vazio (ou `cobblestone_wall`).
- Seteira: `iron_bars` em fenda 1x2 [TESTADO X02: "funciona muito bem"].
- Torre redonda: só lê como círculo a partir de diâmetro ~15; abaixo disso assuma octógono ou quadrada de cantos chanfrados [TESTADO X03].
- Janela românica: arco pleno exige vão >= 5 [TESTADO X02: 3 de largura lê como trapézio].
- Matacães: escada invertida + alçapão sob o parapeito [NÃO TESTADO].

**Receita D - fantasia** [NÃO TESTADO]: telhado 2:1 ou 3:1 em cores saturadas (`purple_concrete`, `dark_oak_stairs` etc.), beiral extra de 1-2 blocos, torre torta deslocando 1 bloco a cada 4-6 camadas mantendo contato, no máximo 3 materiais + 1 de destaque.

## Combina com
- `gotico.md`, `../estruturas/castelos-e-fortalezas.md`, `../estruturas/casas-e-edificios-residenciais.md`
- `../fundamentos/profundidade-contraste-transicoes.md`, `../materiais/paletas-e-combinacoes.md`, `../materiais/envelhecimento-e-deterioracao.md`
- `../tecnicas/cantos-e-vigas.md`, `../tecnicas/telhados-e-beirais.md`, `../tecnicas/portas-e-entradas.md`, `../tecnicas/praca-e-espaco-publico.md`

## Erros comuns
- Fachada enxaimel só "caixa com moldura": sem avanço do andar nem diagonais (1 plano) [INT, medido em X02].
- Viga horizontal no canto expondo os anéis, sem tronco vertical [TESTADO-AULA02].
- Telhado sem beiral, ou só o anel de escadas (céu visível por dentro).
- Castelo todo cinza liso, torre fina sem ameia; torre "redonda" de diâmetro 6-8 que lê como quadrado arredondado.
- Fantasia = "medieval colorido" ou torre torta sem estrutura aparente [INT].

## Limitações e dúvidas
- Diagonais reais e madeira entalhada: impossíveis; aproximar.
- Não testado: matacães, ameias, torre torta, qualquer cor (o render do projeto não mostra cor final).
- Nada foi testado andando no jogo.
- Fantasia: nenhuma fonte aberta trata de telhados exagerados ou torres tortas como escolha deliberada [NV].
- Rodada 1 listou Minas Tirith como inspirada em Mont-Saint-Michel etc.: só busca, baixa confiança; não usar como regra.

## Fontes e evidências
- Wikipédia EN, abertas via resumo: Timber framing, Romanesque architecture, Castle, Abbey (terciárias, trechos parciais).
- bookreporter.com entrevista com Alan Lee (aberta via resumo, rodada 2); swissinfo.ch sobre John Howe (aberta via resumo, rodada 2); theonering.net e repositório da Univ. do Porto: só busca.
- Experimentos `../experimentos/X01-telhados/RESULTADO.md`, `X02-fachadas-e-janelas/RESULTADO.md`, `X03-curvas-e-diagonais/RESULTADO.md`; Vila Pedra-Musgo (`../aulas/aula-02/`).
