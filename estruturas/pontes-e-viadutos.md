# Pontes e viadutos

> Status: rascunho consolidado | Confiança: média para lógica por tipo; as faixas de vão por tipo da 1ª rodada estão REFUTADAS/não verificadas | Última revisão: 2026-11-09

## Resumo
Cada tipo (viga, arco, treliça, pênsil, estaiada, cantilever) tem uma lógica de força que o olho precisa ver. No X05 a ponte pênsil funcionou e a de arcos de vão 10 FALHOU (leu como muro com pilares). Há hipóteses para consertar o arco, todas não testadas.

## Conceito
- [DOC, aberta secundária] Viga trabalha à flexão e raramente passa de ~80 m (simples). Treliça Pratt prática até ~76 m; Hart Bridge 332 m. Arco = compressão com empuxo nos encontros.
- [DOC] Arco histórico: vão/flecha 5,2-6,4 (Limyra 5,3; Zhaozhou 5,2; Fleischbrücke 6,4); alvenaria máx. Danhe 146 m; maior arco Tian'e Longtan 600 m.
- [DOC] Cantilever: balanço equilibrado por braços de ancoragem; Quebec 549 m, Forth 521 m x2.
- [DOC] Pênsil: Çanakkale 2.023 m; Akashi 1.991 m (1.995 m é erro). Razão flecha/vão 1:8-1:12: NÃO verificada em fonte aberta.
- [DOC] Estaiada: vão intermediário entre cantilever e pênsil; razão altura do mastro/vão: [NV].
- REFUTADO/NÃO VERIFICADO: a tabela AASHTO da R1 (ex.: "viga 30-300 m", "treliça 90-550 m"): não usar como regra.

## Características / regras
| Tipo | Leitura em blocos | Rótulo |
|---|---|---|
| Viga/viaduto: pilares + tabuleiro grosso; vão 8-16 (viaduto repetitivo 10-12) | | [INT] |
| Arco: flecha ~1/5 do vão (vão/flecha 5,2-6,4 histórico) | | [DOC] + [INT] |
| Pênsil: cabo parabólico, pendurais; torres 25-40 acima do tabuleiro; flecha ~1/10 do vão | flecha 1/10: [NV]; o teste X05 funcionou com vão 36 e torres de 14 | [TESTADO X05] (parâmetros); [INT] (1/10) |
| Treliça: pórtico 4-6 de altura, diagonais a 45° a cada 4-6 | | [INT] |
| Tabuleiro 5-9 de largura, espessura 1-2 mais guarda-corpo 1 | | [INT] |
| Cabo diagonal de `oak_fence`/cerca não se liga: preencher o degrau vertical em cada passo | | [TESTADO X05] |
| Ponte em arcos de vão 10, flecha <= 5: NÃO lê como arco | | [TESTADO X05] fracasso |

## Como construir no Bedrock
**Receita A: ponte pênsil (vão 36, torres 14)** [TESTADO X05: 483 blocos; funciona e é barata]
1. Duas torres de pedra (`stone_bricks`) com 14 de altura acima do tabuleiro, em fundação visível; em cada lado, massa de ancoragem.
2. Tabuleiro de `spruce_planks`/`spruce_slab` 3-5 de largura entre as torres, guarda-corpo de `spruce_fence`.
3. Cabo parabólico do topo da torre até o centro, cerca ou `iron_chain` (ID real: `iron_chain`, não "chain"). Em cada passo, preencher o degrau vertical senão o cabo quebra [TESTADO X05; E-36 em `../erros-e-licoes.md`].
4. Pendurais verticais (corrente ou barra) a cada 4-6 blocos ligando cabo e tabuleiro.
5. Auditar: cabo preso à torre passa na regra de apoio; cerca solta, não.

**Receita B: ponte em arcos** (o fracasso e o que testar)
- FRACASSO [TESTADO X05]: 3 arcos de vão 10 (812 blocos) -> "muro de pedra sobre pilares com vãos retangulares". Arco de vão 10 com flecha <= 5 não lê.
- Por que (hipótese [INT], coerente com X03 e X01e): com 10 blocos de vão não há resolução para curvar; e a razão histórica (vão/flecha ~5,2-6,4) daria flecha de só 1,6-1,9 para vão 10, plana demais para blocos; arco de berço de raio 4 também falhou (X01e).
- Hipóteses NÃO TESTADAS para consertar (testar uma por vez, com render):
  1. Vão >= 24-30 e flecha ~vão/5 (5-6): mais pixels para a curva (X03: círculo só lê a partir de diâmetro ~15).
  2. Intradorso com `stone_brick_stairs` invertidas e `stone_brick_slab`, para suavizar os degraus (lajes funcionaram na cúpula de raio >= 8 em X03).
  3. Anel do arco com espessura 2 e tímpano (parede acima do arco) em material diferente.
  4. Pilares mais estreitos que o vão e com talha-mar (formato de cunha no lado da água).
  5. Menos blocos de "muro": abrir o tímpano com arcos menores (arco aliviado) ou usar apenas 1 arco grande com flecha forte.
  6. Variar o ritmo: arco central maior que os laterais.
- Receita provisória [NÃO TESTADA]: 3 arcos de vão 24, flecha 5, pilares 4x4 afunilados, tabuleiro 7, guarda-corpo 1.

**Receita C: viaduto de viga** [NÃO TESTADO]: pilares 2x2 a 3x3 afunilados a cada 10-12, viga de `smooth_stone`/`white_concrete` 2 de espessura, juntas visíveis a cada 20; rampas de acesso (`stone_brick_stairs`) nas cabeceiras.

**Receita D: balanço (cantilever) e estaiada**: balanço em [subterraneas-e-suspensas.md](subterraneas-e-suspensas.md); estaiada: mastro e cabos em leque (`iron_bars`); altura do mastro 1/3-1/4 do vão [INT, NV].

## Combina com
[subterraneas-e-suspensas.md](subterraneas-e-suspensas.md) · [estacoes-e-ferrovias.md](estacoes-e-ferrovias.md) · [castelos-e-fortalezas.md](castelos-e-fortalezas.md) · [vilas-e-cidades.md](vilas-e-cidades.md) · [../ambientacao/terreno-biomas-agua.md](../ambientacao/terreno-biomas-agua.md) · [../estilos/industrial-e-brutalista.md](../estilos/industrial-e-brutalista.md) · [../fundamentos/escala-e-proporcao.md](../fundamentos/escala-e-proporcao.md)

## Erros comuns
- Arco de vão pequeno que vira muro furado; arco com anel de 1 (sem espessura).
- Pilares finos 1x1 muito espaçados; cabo sem torre; cabo diagonal de cerca com buraco.
- Tabuleiro grosso e plano; sem acesso ou fundação.
- Misturar tipos sem lógica.

## Limitações e dúvidas
- Nenhuma faixa de vão por tipo está verificada; use só os números documentados acima.
- Razões do pênsil (1:8-1:12), estaiada (mastro/vão) e viga (vão/altura 10-35): [NV].
- Espaçamento de pilares de viadutos: [NV].
- Nada testado andando no jogo.

## Fontes e evidências
- Wikipedia "Beam bridge", "Truss bridge", "Arch bridge", "Suspension bridge", "Cable-stayed bridge", "Cantilever bridge" (abertas, secundárias).
- Tabela AASHTO (material de aula, só busca): REFUTADA/não verificada.
- X05-B e X05-C (`../experimentos/X05-vertical-vaos-terreno/RESULTADO.md`); X03; X01; E-36.
- Notas: A4_r2.md.
