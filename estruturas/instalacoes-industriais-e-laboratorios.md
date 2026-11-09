# Instalações industriais e laboratórios

> Status: rascunho consolidado | Confiança: média (torres de resfriamento), baixa (refinaria, submarino) | Última revisão: 2026-11-09

## Resumo
Instalação industrial = layout que segue o fluxo do processo, com tubulação ligando tudo, ferrugem e escala humana. A torre hiperboloide só lê em raio grande (X03). Instalações submarinas não têm fonte lida: tudo como [NV]/[INT].

## Conceito
- [DOC, só busca R1] Layout segue matéria-prima -> processamento -> armazenagem -> expedição; áreas de risco separadas.
- [DOC, só busca R1] Torre de resfriamento hiperboloide: ar sobe por efeito chaminé; a forma é feita de retas. Tiragem natural até ~200 m de altura e ~100 m de base; exemplo de 202 m (Kalisindh, base 142 m); primeira construída em 1917 (Heerlen); datas variam entre fontes.
- [DOC, só busca R1] Refinaria: espaçamento entre tanques >= 0,5 x diâmetro do maior (OISD 118, slide, confiança baixa).
- [DOC, só busca R1] Laboratório: módulo ~3,05 m (10 pés); duas fileiras de bancada de 2,5 pés + corredor central de 5 pés (U. Arizona); corredor mínimo de 44 pol em outra universidade.
- [NV] Submarino: Conshelf II (habitat em estrela a 33 pés, outro a 100 pés, hangar) em Wikipedia/Smithsonian, só busca; por que formas curvas resistem à pressão: fontes não explicam, só conhecimento geral.

## Características / regras
| Item | Valor | Rótulo |
|---|---|---|
| Torre de resfriamento: base 30-40 de diâmetro, altura 50-70, cintura a ~70% da altura com diâmetro ~60-65% da base | | [INT] |
| Círculo só lê a partir de diâmetro ~15; abaixo, octógono | | [TESTADO X03] |
| Cúpula: lajes suavizam o degrau a partir de raio 8 | | [TESTADO X03] |
| Galpão 20x40, pé-direito 8-10, telhado dentes de serra | | [INT] |
| Silos cilíndricos 7-9 de diâmetro, altura 25-40: diâmetro < 15 lê como quadrado arredondado | | [INT] + [TESTADO X03] |
| Chaminé 40-60 com anéis; pipe racks a 4-6 de altura | | [INT] |
| Laboratório: módulo 4x(8-10), corredor 3 de largura, pé-direito 4 | | [INT] |
| Cúpula submarina: raio 8-12, módulos cilíndricos 7-9, tubos 3x3 | | [NV]/[INT] |
- Paleta industrial: concreto, aço, ferro enferrujado; sinalização em faixas laranja/azul [INT]; ver [../estilos/industrial-e-brutalista.md](../estilos/industrial-e-brutalista.md).

## Como construir no Bedrock
**Receita A: torre de resfriamento** [NÃO TESTADA; baseia-se em X03]
1. Base 36 de diâmetro, altura 60. Em cada camada y, o raio r(y) varia suavemente: de 18 na base até ~11 na cintura (y ~ 42) e volta a ~13 no topo [INT].
2. Cada camada é um anel de 1-2 blocos de `light_gray_concrete`; testar o contorno por trecho reto máximo (< 1/3 do diâmetro, X03).
3. Base: abertura de entrada de ar com colunas inclinadas de `stone_brick_wall`/`iron_bars` (treliça).
4. Vapor: `campfire` com fumaça na boca ou partículas (verificar disponibilidade [NV]).
**Receita B: fábrica com fluxo** [NÃO TESTADA]
1. Desenhar o fluxo em linha: entrada de ferrovia/rua -> galpão -> silos -> expedição.
2. Galpão com telhado em dentes de serra de `stone_brick_stairs`/`iron_block` e `glass_pane` na face vertical.
3. Pipe rack a 4-6 de altura com `iron_bars`, `iron_chain` (ID real é `iron_chain`), passarelas de `iron_trapdoor`.
4. Envelhecimento: ferrugem com `oxidized_copper`/`exposed_copper`/`weathered_copper` (ID real; disponibilidade em cada versão a conferir) e manchas de água sob as juntas (`../materiais/envelhecimento-e-deterioracao.md`).
5. Escala humana: portas de serviço 3x3, escadas com guarda-corpo, passarelas.
**Receita C: laboratório** [NÃO TESTADA]
1. Módulo repetível 4x9, corredor central 3 de largura e pé-direito 4; paredes `white_concrete`/`quartz_block`, janelas internas `glass_pane`.
2. Antecâmara 3x3 com duas portas (`iron_door`).
3. Bancadas `smooth_stone_slab` com `furnace`, `blast_furnace`, `smoker`, `cauldron`, `hopper` como equipamentos; faixas de cor para sinalização.
**Receita D: base submarina [NV]**: módulos cilíndricos (diâmetro 7-9, X03 sugere octógono) ligados por tubos 3x3 de `glass`/`white_concrete`; escotilhas; `sea_lantern`; estacas/pilares até o fundo; água contida por vidro [INT]. Sem teste e sem fonte.

## Combina com
[estacoes-e-ferrovias.md](estacoes-e-ferrovias.md) · [subterraneas-e-suspensas.md](subterraneas-e-suspensas.md) · [../estilos/industrial-e-brutalista.md](../estilos/industrial-e-brutalista.md) · [../estilos/futurista-cyberpunk-solarpunk.md](../estilos/futurista-cyberpunk-solarpunk.md) · [../materiais/envelhecimento-e-deterioracao.md](../materiais/envelhecimento-e-deterioracao.md) · [../materiais/vidro-luz-e-metal.md](../materiais/vidro-luz-e-metal.md) · [../ambientacao/ruinas-e-narrativa.md](../ambientacao/ruinas-e-narrativa.md)

## Erros comuns
- Edifícios espalhados sem fluxo nem tubulação.
- Paleta limpa demais; sem ferrugem.
- Torre cilíndrica reta; círculo pequeno que lê como quadrado.
- Laboratório que parece escritório; sala sem equipamento.
- Módulo submarino sem conexão lógica, sem janela ou luz; cúpula sem estrutura aparente.

## Limitações e dúvidas
- Nenhuma página destas notas foi aberta na íntegra (só busca): números de torres, refinaria e laboratório com confiança baixa.
- Instalações submarinas: sem fonte; torna-se [NV].
- Vapor e partículas no Bedrock: [NV].

## Fontes e evidências
- designingbuildings (torres), Zenodo Kalisindh, OISD 118, U. Arizona, UVM, WBDG, Smithsonian: só busca (R1).
- X03 (círculo, cúpula); X01 (abóbada de raio 4 falhou).
- Notas: A4_tipos_de_estrutura.md; A4_r2.md não reabriu estes itens.
