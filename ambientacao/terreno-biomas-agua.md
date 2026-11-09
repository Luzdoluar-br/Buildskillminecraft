# Implantação no terreno, biomas e água

> Status: rascunho; só encosta (X05-E) e água da Vila (aula-02) foram construídas | Confiança: baixa-média (biomas sem fonte lida; palafitas e Shibam só em fonte enciclopédica) | Última revisão: 2026-11-09

## Resumo
- Construção se encaixa no terreno: patamar nivelado + muro de arrimo + escada; nunca bloco flutuante nem terreno aplainado sem fundação.
- Material local por bioma é regra de coerência [INT]; a documentação lida cobre só palafitas e Shibam; neve, mangue, floresta e submarino são [NV].
- Água precisa de borda sólida e nível constante: sem isso escorre (E-06 da Vila).

## Conceito
**Princípio -> manifestação real.**
- Palafitas alpinas [DOC, Wikipedia *Prehistoric pile dwellings around the Alps*, aberta; UNESCO whc 403]: casas sobre estacas em margens de lagos, rios e áreas alagadiças, para evitar cheias ocasionais; não necessariamente sobre a água.
- Áreas alagadas [DOC, designingbuildings.co.uk, aberta, divulgação]: palafitas de madeira ou pedra (Ko Panyi, Ganvie, Tonle Sap), casas flutuantes (Uros, com totora), acesso por barco e pontes.
- Deserto [DOC, Wikipedia *Shibam*, aberta]: torres de tijolo de barro de 5-11 andares, ~500 torres, muralha, manutenção constante com nova camada de lama.
- Terraços de encosta (Ifugao, Honghe Hani): PDF UNESCO ilegível, só busca [NV].
- Neve (telhado inclinado, beiral, base de pedra), mangue (palafita 1-2 m acima da maré, madeira e zinco), floresta densa, submarino: [NV] (só busca fraca ou não pesquisado). O que segue para eles é [INT].

## Características / regras
| Situação | Regra de implantação [INT] | Material local [INT] |
|---|---|---|
| Encosta | patamar nivelado a meia altura do desnível; muro de arrimo escalonado a cada bloco de subida; escada na linha de maior declive | pedra (`stone_bricks`, `cobblestone`) na fundação, madeira acima |
| Pântano/mangue [NV] | piso 1-2 blocos acima da cota máxima da água; estacas até o fundo; ponte/escada e barco | madeira (`mangrove_log`, `mangrove_planks`), `mud_bricks`, `packed_mud` |
| Neve [NV] | base de pedra; telhado inclinado com beiral fundo; neve acumulada nas águas protegidas | `spruce_log`, `spruce_planks`, `snow_layer`, `snow` |
| Deserto [DOC parcial] | massa de barro espessa, poucas aberturas, pátio, muralha | `sandstone`, `cut_sandstone`, `smooth_sandstone`, `mud_bricks` |
| Floresta [NV] | clareira pequena, copas sobre a construção, material de madeira | `spruce_log`/`oak_log`, `moss_block`, `vine` |
| Submarino [NV] | estrutura fechada com luz (ver [iluminacao-e-atmosfera.md](iluminacao-e-atmosfera.md)) | `prismarine`, `dark_prismarine`, `sea_lantern`; sem teste de vidro e água |

Regras gerais [INT]: fundação variável em altura para acomodar o declive; chão natural escalonado com no máximo 1 de diferença entre vizinhos (regra de `terreno.py`); mesma paleta de pedra nos muros de arrimo e na base da casa.

## Como construir no Bedrock
**Casa em encosta 1:2** [TESTADO X05-E, render + auditoria, 540 blocos]: terreno sobe 1 bloco a cada 2 em x. Piso nivelado a `nivel = 1 + (14 + 6)//2` (meia altura da casa). Para cada coluna x, encher de `h = 1 + x//2` até `nivel` com `stone_bricks` e `cobblestone` (3:1) = muro de arrimo escalonado. Piso `spruce_planks` em `nivel + 1`, paredes de 3 de altura. Resultado: "casa encaixada na encosta".
**Terreno por mapa de alturas** [`ferramentas/construcao/terreno.py`, usado na Vila]: pads planos com margem, interpolação da margem, relaxamento 40 passes até inclinação <= 1 entre vizinhos, preenchimento. Ver [../tecnicas/terreno-caminhos-e-pracas.md](../tecnicas/terreno-caminhos-e-pracas.md) (caminho de `grass_path`/`coarse_dirt` em volta de pontos de uso) [TESTADO-AULA02].
**Pilotis** [NÃO TESTADO; o código foi removido do X05 para não afirmar o que não foi feito]: estacas de tronco a cada 3-4 blocos, do fundo ao piso; contraventos de cerca opcionais; escada ou ponte até a terra.
**Píer e lagoa da Vila** [TESTADO-AULA02]: tábuas e postes sobre a água exigem estacas até o fundo (E-21); a auditoria não aceita água como apoio.
**Água e áreas alagadas** [INT]:
1. Defina UMA cota de superfície e use-a em todos os corpos de água ligados (canal, cômodo alagado).
2. Contenha com borda sólida: muro de pedra, cais ou margem mais alta que a água em todo o perímetro.
3. Marca de enchente em parede = mesma altura em todas as paredes; musgo na linha d'água.
4. Pontes, passarelas e degraus que mergulham na água; entulho submerso.
**E-06 da Vila** [TESTADO-AULA02, ver [../erros-e-licoes.md](../erros-e-licoes.md)]: o anel de margem da lagoa (H=0) sobrepôs a borda da horta (H=1); a água da horta, ao nível do chão, escorreu para o terreno mais baixo. Correção: lagoa deslocada e horta reduzida. Regra: nunca deixar água ao nível do solo encostada em terreno mais baixo.
Blocos: `water` e `flowing_water` têm `liquid_depth = 0..15`; confira em [../referencia/blocos-bedrock.md](../referencia/blocos-bedrock.md). Lírio: `waterlily`, não `lily_pad`.

## Combina com
[../estruturas/vilas-e-cidades.md](../estruturas/vilas-e-cidades.md) · [../estruturas/casas-e-edificios-residenciais.md](../estruturas/casas-e-edificios-residenciais.md) · [../materiais/paletas-e-combinacoes.md](../materiais/paletas-e-combinacoes.md) · [../fundamentos/profundidade-contraste-transicoes.md](../fundamentos/profundidade-contraste-transicoes.md) · [ruinas-e-narrativa.md](ruinas-e-narrativa.md) · [../tecnicas/vegetacao-e-ambientacao.md](../tecnicas/vegetacao-e-ambientacao.md)

## Erros comuns
- Terreno aplainado sem fundação; casa sobre bloco único flutuando; mesmo material em todos os biomas [INT].
- Palafita sem acesso (escada, ponte, barco) [INT, e documentado pelo uso de barcos e pontes nas fontes].
- Água sem muro de contenção ou com níveis diferentes em cômodos conectados [TESTADO-AULA02 para a contenção].
- Objetos de chão posicionados pelo bloco mais alto da coluna: nascem em cima de telhados e toldos (E-14).
- Pier/estaca flutuando sobre a água (E-21).

## Limitações e dúvidas
- Fluxo de água ao carregar a estrutura no jogo: não testado (relatório da Vila).
- Pilotis, pântano, neve, floresta e submarino: nenhum construído; materiais listados são sugestão [INT]/[NV].
- Disponibilidade dos blocos na versão em uso: todos os IDs acima foram conferidos na lista oficial; `chain` não existe (o ID é `iron_chain`).
- Terraços agrícolas, mangue e neve sem fonte lida; a rodada 3 de pesquisa deve abrir fontes para eles.
- Altura em metros do "pé-direito" ou enclosure em vilas: ver doc de vilas; não repetido aqui.

## Fontes e evidências
- Wikipedia (palafitas alpinas, Shibam): abertas. UNESCO whc: 403. designingbuildings.co.uk: aberta.
- Terraços UNESCO: PDF ilegível/só busca. Neve, mangue: só busca. Floresta, submarino: não pesquisados.
- X05 `RESULTADO.md` e `experimento.py` (E1): lidos. `terreno.py`: lido. `erros-e-licoes.md` (E-06, E-14, E-21), relatório da Vila: lidos.
- IDs: `referencia/blocos-bedrock.md`.
