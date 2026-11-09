# Escala e proporção

> Status: rascunho de biblioteca | Confiança: média (números humanos confirmados; traduções para blocos são [INT]) | Última revisão: 2026-11-09

## Resumo
- Convenção da biblioteca: 1 bloco = 1 m; jogador = 2 blocos de altura; porta mínima 1x2.
- Medidas humanas só valem quando confirmadas (ADA, Blondel, Modulor); o resto é [INT] rotulado.
- Casas de Minecraft parecem "baixas" porque o degrau e o andar são quantizados em 1 bloco; a solução é pé-direito maior, meio bloco (laje/escada) e módulo claro.

## Conceito
Proporção = relação entre partes e o todo; escala = tamanho percebido frente ao corpo. Um edifício pode ser proporcional e estar fora de escala (A1_fundamentos, W4, só busca/Wikipedia). Em Minecraft o corpo de referência é o jogador (2 blocos de altura, convenção do projeto), não o humano de 1,75 m.

## Características / regras

### Medidas humanas confirmadas (A1_r2)
| Item | Valor | Status |
|---|---|---|
| Vão livre de porta (ADA 404.2.3) | >= 32 pol = 815 mm | [DOC] access-board.gov, resumo aberto |
| Rota acessível (ADA 403.5.1) | >= 36 pol = 915 mm | [DOC] access-board.gov |
| Degrau (ADA cap. 5) | espelho 4-7 pol (100-180 mm); piso >= 11 pol (280 mm) | [DOC] espelho do texto ADA (corada.com) |
| Balcão de atendimento (ADA cap. 9) | <= 36 pol = 915 mm | [DOC] espelho do texto ADA |
| Blondel | 2 espelhos + 1 piso = 63-65 cm | [DOC] ArchDaily (cita Neufert); a data de 1675 é [NV] |
| Modulor (Le Corbusier) | homem 1,83 m; braço erguido 2,26 m | [DOC] Wikipedia; é escolha declarada do autor, não lei |

NÃO usar como fato: pé-direito residencial 2,4-2,7 m, porta de 2,0 m, largura de corredor de código (IBC/IRC): só busca, fontes divergem [NV].

### Conversão 1 bloco = 1 m e suas distorções [INT]
- Degrau real ~0,18 m; em Minecraft 1 m (ou 0,5 m com escada/laje). Só o meio bloco aproxima a escala real.
- Porta de 1 bloco de largura (1 m) já excede o mínimo ADA de 0,815 m; porta dupla = 2 m.
- Jogador de 2 blocos de altura numa porta de 2 de altura "roça" a cabeça: sensação de baixo. Por isso casas parecem baixas e achatadas.
- Largura de passagem: 1 bloco é estreito, 2 é confortável, 3 é largo (A1_r2 sec. 3, [INT]).

### Razões [DOC/NV]
- 1,618: usada explicitamente por Le Corbusier (Modulor); no Partenon/Pirâmide as alegações históricas são "largamente desacreditadas" (Wikipedia, Golden ratio). Não tratar como regra histórica. Numa grade de blocos o efeito é imperceptível [INT].
- 3:4:5 como razão arquitetônica histórica: [NV] (só existe como triângulo retângulo de locação, também [NV] aqui).
- Razões simples (1:1, 2:3, 3:2, 1:2) bastam [INT]. Janelas altas e estreitas (2:1 ou 3:1) são típicas de lancetas [DOC, W4], aplicação [INT].

### Dimensões em blocos recomendadas
| Elemento | Recomendação | Rótulo |
|---|---|---|
| Porta | 1 de largura x 2 de altura (verga acima) | [DOC] ADA mín. + [TESTADO-AULA02] portas.md P-2 |
| Porta dupla/portão | 2 x 2 a 2 x 3 | [INT] |
| Passagem principal interna | >= 2 de largura | [INT] |
| Pé-direito interno livre | >= 3 (casa); 4-5 (sala nobre) | [INT] |
| Edifício monumental | pé-direito 5-8 | [INT] (A1_fundamentos) |
| Degrau | 1 bloco; use escada/laje p/ meio bloco; patamar a cada ~4-6 subidas | [INT]; Neufert: lance máx. 15 degraus [DOC via ArchDaily] |
| Balcão/bancada | 1 bloco, ou laje inferior (0,5 m) | [DOC] ADA 36 pol + [INT] |
| Travée (módulo de fachada) | 3 a 5 blocos (vão + pilar) | [INT] |
| Janela | 1x2 lê como furo; com moldura lê melhor | [TESTADO X02] |
| Janela ogival | >= 3 de largura e >= 6 de altura | [TESTADO X02] |
| Arco pleno | >= 5 de largura | [TESTADO X02] |
| Círculo/torre redonda | diâmetro >= ~15; abaixo disso assuma octógono | [TESTADO X03] |

### Janela x parede
Não há razão numérica documentada. Resultado de X02: janela com moldura (soleira em laje, verga em escada invertida, ombreiras em pedra polida) é a melhor relação custo/efeito; janela simples rente à parede lê como "furo". Fita com montantes lê como moderno; seteira com `iron_bars` lê como fortificação. Proporção parede/vão por estilo: [INT], decidir pela travée.

### Escalas de monumentalidade [INT]
1. Íntima (pé-direito 3, portas 1x2). 2. Cívica (4-5, portas 2x3). 3. Monumental (6-8+, degraus de acesso, portal desproporcional). Ching: tamanho excepcional é um dos meios de ênfase [DOC]; ver `composicao-hierarquia-silhueta.md`.

## Como construir no Bedrock
1. Fixe o módulo antes de modelar: travée de 3 ou 5 blocos. Fachada de 15 = 3 travées de 5 ou 5 de 3. [INT]
2. Casa comum: pé-direito interno 3, porta 1x2 mais verga, janela 1x2 com moldura. [NÃO TESTADO como conjunto; moldura: TESTADO X02]
3. Para parecer menos "baixa": suba o pé-direito 1 bloco, aumente beiral, use laje/escada no meio bloco (soleira, degrau). [INT]
4. Teste de boneco: ao lado de cada abertura desenhe 2 blocos de altura; porta >= 2, passagem principal >= 2. [INT, A1_r2]
5. Torre redonda pequena: faça octógono ou quadrada com cantos chanfrados. [TESTADO X03]

## Combina com
- [composicao-hierarquia-silhueta.md](composicao-hierarquia-silhueta.md)
- [profundidade-contraste-transicoes.md](profundidade-contraste-transicoes.md)
- [../tecnicas/portas-e-entradas.md](../tecnicas/portas-e-entradas.md)
- [../tecnicas/escadas-internas.md](../tecnicas/escadas-internas.md)
- [../experimentos/X02-fachadas-e-janelas/RESULTADO.md](../experimentos/X02-fachadas-e-janelas/RESULTADO.md)

## Erros comuns
- Pé-direito de 2 blocos (parece porão) [INT].
- Perseguir 1,618 ou 3:4:5 como "regra histórica".
- Portas e janelas de 1 bloco soltas, sem travée.
- Arco ogival de 1 bloco de largura (X02: não lê) e círculo de diâmetro < 15 (X03).
- Escada com espelho de 1 m sem patamar em prédio "realista".

## Limitações e dúvidas
- Neufert (livro) e IBC/IRC não verificados; só via ArchDaily/busca.
- Tabela de dimensões em blocos é majoritariamente [INT]; nada foi testado andando no jogo.
- Hitbox/altura exata do jogador no Bedrock não está nas notas (2 blocos é a convenção do projeto).

## Fontes e evidências
- A1_r2: ADA (access-board.gov resumo aberto; corada.com espelho, resumo), ArchDaily Blondel/Neufert (resumo aberto), Ching cap. 7 (lido por trechos).
- A1_fundamentos: Wikipedia Golden ratio, Modulor, Vitruvian Man (abertas); ArchDaily/Britannica 403.
- Experimentos X02 e X03 (render + métrica, sem teste no jogo).
