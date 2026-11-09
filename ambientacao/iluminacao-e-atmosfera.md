# Iluminação e atmosfera

> Status: rascunho; níveis de luz e spawn vêm da wiki da comunidade e NÃO foram testados no jogo | Confiança: média (níveis de luz, IDs); baixa (espaçamento, alternativas de atmosfera) | Última revisão: 2026-11-09

## Resumo
- Luz é hierarquia e narrativa: poucos focos quentes, luz geral fraca, escuridão = abandono; cada luz precisa de fonte lógica.
- Em estrutura Bedrock cabem blocos de luz (`light_block_0..15`, lanternas, etc.); névoa, partículas e iluminação volumétrica NÃO cabem num `.mcstructure`.
- Hostis precisam de luz de bloco 0 segundo a wiki [DOC comunidade, não testado]: luz mínima em toda superfície válida de spawn.

## Conceito
**Level Design Book** [DOC, oficial, aberto]: iluminação em 4 categorias: global, wayfinding (orientação/caminho crítico), gameplay, detalhe/humor; estratégias espaciais: ponto focal, moldura focal, caminho/limite (faces 4-6 do D6 não detalhadas no texto obtido). Uma luminária visível pode motivar várias luzes; resolver a passagem de luz cedo.
**Carson** [DOC, aberto]: iluminação seletiva, penumbra, luz destacando o objeto importante; contraste claro/escuro.
**Temperatura de cor** [DOC secundário, PDF de Cambridge MA, aberto, citando Wikipedia]: 2700-3000 K = quente; acima de 5000 K = fria. Recomendações IES/CIE e níveis de iluminância: [NV] (não encontradas abertas).
Uso em Minecraft [INT]: quente (lanterna, fogo, janela acesa) em abrigos e ruas principais; fria (luz da lua, `soul_lantern`) em ruínas e cavernas; uma cor dominante e uma de contraste.

## Características / regras
**Hierarquia de luz** [INT, baseada nas 4 categorias]:
| Nível | Função | Exemplo em blocos |
|---|---|---|
| Global | visibilidade mínima, humor | `light_block_N` baixo oculto; luar |
| Wayfinding | guia até o destino | postes ao longo da rua principal, janela acesa na entrada |
| Foco | marca o ponto focal | `lantern` + `campfire` na praça; lareira (`lit_furnace`) na sala |
| Detalhe | humor | `candle`, `soul_torch`, `crying_obsidian` |
**Luz como narrativa** [INT]: janelas acesas = habitada; escuridão e uma única luz fria = abandono; luz quente isolada numa ruína = alguém esteve aqui (evidência para [ruinas-e-narrativa.md](ruinas-e-narrativa.md)).
**Níveis de luz de bloco no Bedrock** [DOC comunidade: minecraft.wiki Light, só busca; NÃO testado]:
| Nível | Fontes |
|---|---|
| 15 | farol, `glowstone`, `sea_lantern`, `lantern`, abóbora esculpida acesa (`lit_pumpkin`), lava, fogo |
| 14 | `torch`, `end_rod` |
| 13 | fornalha/defumador/alto-forno acesos |
| 12 | 4 velas acesas (e vault ativo) |
| 10 | `soul_torch`, `soul_lantern`, `crying_obsidian` |
| 9 | 3 velas acesas |
| 7 | mesa de encantamento, tocha de redstone acesa |
| 3 | 1 vela acesa, `magma` |
Campfire comum e 2 velas: não listados nas notas [NV]. `shroomlight` e `froglight`: níveis não verificados.
**Spawn** [DOC comunidade, minecraft.wiki Mob_spawning, só busca; NÃO testado]: hostis precisam de luz de bloco 0 (muitos) e luz do céu interna <= 7; superfície de spawn precisa de topo sólido cheio (tapete, laje inferior, cerca e escada não servem; escada invertida também não, em Bedrock); passivos exigem luz >= 7. Ou seja: luz >= 1 em todo bloco de piso, ou piso não sólido.
**Espaçamento** [INT, nada aqui vem de fonte]: em rua principal, pontos de luz a cada 7-10 blocos; em vielas, mais espaçados e mais baixos; na Vila adotou-se mínimo de 4 blocos entre postes [TESTADO-AULA02, regra própria] e poste fora de ruas e anéis de passagem ([../tecnicas/postes-de-luz.md](../tecnicas/postes-de-luz.md)). Como a luz cai com a distância (conhecimento geral do jogo, fora das notas [NV]), valide em jogo.

## Como construir no Bedrock
**O que cabe em `.mcstructure`**: blocos emissivos e `light_block_0`..`light_block_15` (IDs separados, sem estados; `minecraft:light_block` sozinho NÃO existe na lista 1.26.60.5) [DOC oficial, Mojang/bedrock-samples, aberto]. Na estrutura: `name: minecraft:light_block_N`, `states: {}`. O bloco só é visível com o item de luz na mão (wiki, Light_Block) [DOC comunidade].
**Receita anti-spawn** [NÃO TESTADO]: (1) liste pisos sólidos ao ar livre e em interiores escuros; (2) sob cada 2-3 blocos de piso, ou num bloco de ar acima, coloque `light_block_1` (oculto); (3) em cavernas/porões use luzes de nível >= 1 em lanterna ou `torch`; (4) alternativa: piso de laje superior ou bloco não sólido.
**O que NÃO é possível dentro de `.mcstructure`** [DOC oficial, Microsoft Learn, aberto]:
- Névoa (fog): é JSON em resource pack (`fogs/`), ligada a bioma via `biomes_client.json` ou ao jogador via `/fog push|pop|remove`; não é bloco nem entidade.
- Partículas: JSON em `particles/` do resource pack; disparadas por `/particle`, animação de entidade ou animation controller. Uma partícula não é parte de uma estrutura (só uma entidade custom carregada junto, ou função com `/particle` repetido).
- Iluminação volumétrica: só com Ray Tracing / Vibrant Visuals e `volumetric` no fog.
**Alternativas em blocos** [NÃO TESTADO]: `web` (teia) e vidros tingidos para turbidez; `campfire` para fumaça (efeito do jogo, não testado em estrutura); `soul_torch`/`soul_lantern` para luz fria; `snow`/`powder_snow` para brancura. Névoa visual por blocos é só aproximação.

## Combina com
[../materiais/vidro-luz-e-metal.md](../materiais/vidro-luz-e-metal.md) · [../fundamentos/profundidade-contraste-transicoes.md](../fundamentos/profundidade-contraste-transicoes.md) · [../fundamentos/composicao-hierarquia-silhueta.md](../fundamentos/composicao-hierarquia-silhueta.md) · [../estilos/futurista-cyberpunk-solarpunk.md](../estilos/futurista-cyberpunk-solarpunk.md) · [ruinas-e-narrativa.md](ruinas-e-narrativa.md) · [../tecnicas/postes-de-luz.md](../tecnicas/postes-de-luz.md) · [../referencia/blocos-bedrock.md](../referencia/blocos-bedrock.md)

## Erros comuns
- Luz uniforme em tudo; tochas em fileira regular numa ruína; luz sem fonte lógica [INT, A5].
- Usar `light_block` sem número ou com estado `block_light_level` (não existe nessa versão).
- Prometer névoa, fumaça ou partículas "na estrutura" [REFUTADO por design nas notas A6].
- Confiar na luz da lista acima sem testar: níveis vêm de wiki, não de teste.
- Esperar spawn em piso de tapete, laje inferior ou escada: segundo a wiki essas superfícies não servem; só topo sólido cheio permite spawn.

## Limitações e dúvidas
- Níveis de luz, regra do spawn e visibilidade do `light_block`: wiki, não testados; versões mudaram os IDs de `light_block` (antes `light_block` + dado).
- Propagação da luz e espaçamento ideal: não nas notas; [INT].
- Faixas de iluminância (IES/CIE): [NV]. Dark Sky/3000 K só por blog de vendedor: não usar.
- Nada testado: torre à noite, interior e vidro foram citados como não testados no X05.

## Fontes e evidências
- Level Design Book (oficial): aberto. Carson (Game Developer): aberto. Cambridge MA (temperatura de cor): aberto; Grand Rapids: 403.
- Microsoft Learn (fogs, particles): abertas. Mojang/bedrock-samples `mojang-blocks.json` (light_block): aberto.
- minecraft.wiki Light, Light_Block, Mob_spawning: citadas na rodada 1 de A6 (grau de leitura não detalhado nas notas; tratar como wiki, não testada).
- Nenhum experimento deste repositório testou luz ou spawn.
