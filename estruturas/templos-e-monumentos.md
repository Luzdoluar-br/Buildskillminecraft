# Templos e monumentos

> Status: rascunho consolidado | Confiança: média (números de Karnak e Partenon em Wikipedia, secundária; alturas de coluna de Partenon não obtidas) | Última revisão: 2026-11-09

## Resumo
Templo = eixo, sequência de espaços decrescentes e ponto focal sagrado. Karnak e Partenon têm números documentados (secundária). Colunas de 3 blocos de diâmetro e hipostila com nave central mais alta é a tradução mais forte; é [INT] não testada.

## Conceito
- [DOC, R1 só busca] Templo egípcio: avenida de esfinges, pilono, pátio, sala hipostila, santuário; o piso sobe e o teto desce rumo ao santuário (UCSC; Britannica não aberta).
- [DOC secundária, aberta] Karnak: Grande Sala Hipostila 5.000 m², 134 colunas em 16 fileiras; 122 colunas de 10 m e 12 de 21 m; diâmetro > 3 m. Recinto de Amun ~25 ha; pilono 113 m de largura e 15 m de espessura. Atenção: a altura "43 m" do pilono não tem referência: não usar.
- [DOC secundária, aberta] Partenon: 69,5 x 30,9 m; cella 29,8 x 19,2 m; altura 13,72 m; 8 colunas nas frentes e 17 nas laterais. Diâmetro/altura da coluna: não obtidos.
- [DOC secundária] Obelisco de Hatshepsut ~30 m.
- Razão áurea como regra da Antiguidade: mito, não usar.

## Características / regras
| Item | Valor | Rótulo |
|---|---|---|
| Hipostila: nave central com colunas 20-21 de altura, laterais 10; diâmetro 3; espaçamento ~1,5 diâmetro | traduzido de 21 m/10 m | [INT] |
| Partenon em 1:1: base 70x31, 8x17 colunas, altura total ~14; colunas de ~10 | altura de coluna estimada, não da fonte | [INT] |
| Eixo marcado por piso de material diferente | | [INT] |
| Cada espaço sucessivo menor e mais escuro | A4 R1 sugere 15-20% menor | [INT] |
| Base elevada 3-6 blocos com escadaria larga | | [INT] |
| Pilono: dois blocos trapezoidais com portal central | altura 20-30 [INT, a fonte de 43 m é duvidosa] | [INT] |
- Coluna de diâmetro 3: círculo 3x3 sem cantos ou "plus"; só a partir de diâmetro ~15 um círculo lê como curva [TESTADO X03], então colunas pequenas leem como quadrados: compensar com capitel e base.
- Monumento isolado: base larga, fuste, topo contrastante [INT].

## Como construir no Bedrock
**Receita: sala hipostila (modelo Karnak, 25x20)** [NÃO TESTADO]
1. Piso e plataforma elevada 1-3 acima do terreno; eixo em `smooth_sandstone` ou `cut_sandstone` com contraste.
2. Grade de colunas 3x3 a ~4-5 de passo, 4 filas x 5 colunas; nave central de 2 fileiras com 12-18 de altura e naves laterais de 7-10 [INT].
3. Fuste em `sandstone`/`cut_sandstone`, base e capitel em `chiseled_sandstone`; segmentos visíveis por faixas.
4. Clerestório: laje de cobertura da nave central acima da lateral, com janela estreita (`sandstone_wall` ou vazios) entre os dois níveis para luz alta.
5. Teto: lajes `cut_sandstone_slab`/blocos; interior mais escuro que o pátio, pouca luz (`soul_lantern` ou `lantern` isolada).
6. Santuário 7x7 com teto 5-6 no fim do eixo, lintel e altar `chiseled_stone_bricks`.
7. Pilono na frente: dois blocos de 8-10 de largura, portal 3x5 como referência de escala humana [INT].
8. Pátio 25x25 antes do pilono; escadaria larga.

**Receita: templo grego (modelo Partenon, 1:1 reduzido)** [NÃO TESTADO]
1. Estilóbato 70x31 em 3 degraus (`quartz_block`/`smooth_stone`); 8 colunas nas frentes e 17 nas laterais com espaçamento ~4 (17 colunas em 70 m: ~4,1 m de passo).
2. Colunas 3x3 (ou 3x3 com cantos vazados) de ~10 de altura, canelura por alternância `quartz_pillar` e `smooth_quartz`.
3. Entablamento 2 blocos e frontão triangular 1:2 (X01).
4. Cella interna 30x19 recuada dentro do peristilo.

## Combina com
[castelos-e-fortalezas.md](castelos-e-fortalezas.md) · [../estilos/gotico.md](../estilos/gotico.md) · [../estilos/chines-tradicional.md](../estilos/chines-tradicional.md) · [../estilos/japones-tradicional.md](../estilos/japones-tradicional.md) · [../fundamentos/escala-e-proporcao.md](../fundamentos/escala-e-proporcao.md) · [../ambientacao/iluminacao-e-atmosfera.md](../ambientacao/iluminacao-e-atmosfera.md) · [../ambientacao/ruinas-e-narrativa.md](../ambientacao/ruinas-e-narrativa.md) · [vilas-e-cidades.md](vilas-e-cidades.md)

## Erros comuns
- Sem eixo ou sequência; escada escondida; interior tão iluminado quanto o exterior.
- Colunas finas de 1 bloco sem base/capitel; colunas "circulares" de diâmetro pequeno tratadas como curva.
- Escala monumental sem referência humana (porta 3x5, pessoas, braseiros).
- Quartzo muito branco sem pátina; ver [../materiais/envelhecimento-e-deterioracao.md](../materiais/envelhecimento-e-deterioracao.md).

## Limitações e dúvidas
- Altura e diâmetro das colunas do Partenon não foram obtidos.
- A altura do pilono de Karnak (43 m) é duvidosa; a espessura 15 m é a que ficou.
- Templos maia, asiáticos e góticos: sem medidas lidas; ver estilos específicos.
- As receitas são traduções [INT] sem teste de render.

## Fontes e evidências
- Wikipedia "Karnak", "Precinct of Amun-Re", "Parthenon" (abertas, secundárias).
- UCSC digitalkarnak, Britannica, memphis.edu: só busca (R1).
- X03 (círculo), X01 (inclinação 1:2).
- Notas: A4_r2.md (tabela e traduções), A4_tipos_de_estrutura.md.
