# Envelhecimento e deterioração de materiais

> Status: rascunho de biblioteca | Confiança: média-alta para IDs (oficiais) e para o módulo `ruina.py`; média para a ordem de falha | Última revisão: 2026-11-09

## Resumo
- O Minecraft já traz cadeias prontas de desgaste: pedra (rachada/musgo), cobre (4 estágios + cera), mais vegetação e musgo para o resto.
- Desgaste só convence com causa e gradiente (X04): topos e cantos expostos envelhecem mais que a base; pedra sobrevive à madeira.
- Metal ferroso não oxida no jogo: o ferro envelhece por substituição (escurecer, rachar, correntes), não por ID.

## Conceito
Envelhecer = substituir blocos por variantes desgastadas segundo uma causa (tempo, água, fogo, impacto). Princípio documentado: sem telhado a água entra, topos de parede irregulares retêm chuva, geada e raízes abrem juntas, e arcos/empenas altas caem primeiro (A5_r2, Ruins: Conservation and Repair of Masonry Ruins, PDF aberto, seção 3) [DOC]. A ordem de falha usada no código (cobertura, topos de muro, madeiramento, esquadrias, cantos/empenas) é [INT] apoiada nesse guia.

## Características / regras

### Cadeias com IDs oficiais (conferidos em `../referencia/blocos-bedrock.md`)
| Material | Cadeia de desgaste |
|---|---|
| Tijolo de pedra | `stone_bricks` -> `cracked_stone_bricks` / `mossy_stone_bricks` |
| Pedra bruta | `cobblestone` -> `mossy_cobblestone` (existem escadas/laje/muro mossy) |
| Deepslate | `deepslate_bricks` -> `cracked_deepslate_bricks`; `deepslate_tiles` -> `cracked_deepslate_tiles` |
| Tijolo infernal | `nether_brick` -> `cracked_nether_bricks`; também `red_nether_brick` |
| Chamuscado | `blackstone`, `polished_blackstone_bricks`, `cracked_polished_blackstone_bricks` |
| Cobre | `copper_block` -> `exposed_copper` -> `weathered_copper` -> `oxidized_copper` |
| Cobre encerado (cera) | `waxed_copper`, `waxed_exposed_copper`, `waxed_weathered_copper`, `waxed_oxidized_copper` |
| Cobre cortado | `cut_copper`, `exposed_cut_copper`, `weathered_cut_copper`, `oxidized_cut_copper` (+ `*_cut_copper_stairs`, `*_cut_copper_slab`) |
| Outras peças de cobre | `copper_lantern`, `copper_chain`, `copper_bulb`, `copper_grate`, `copper_door`, `lightning_rod` têm variantes exposed/weathered/oxidized/waxed |
| Madeira | sem estado de envelhecimento; use `moss_block`, `moss_carpet`, `vine`, remoção de peças |
| Ferro | sem oxidação no jogo; ver abaixo |
Nome oficial CONFIRMADO (A6_r2 #29): o encerado base é `waxed_copper`, NÃO `waxed_copper_block` (a wiki da rodada 1 estava errada).

### Ferro e metal [INT, NÃO TESTADO]
Não há ferrugem no ID de `iron_block`, `iron_bars`, `iron_chain`. Para "ferro velho": misturar `iron_bars` com remoção de segmentos, trocar por `blackstone`/`cracked_*` em volta, e usar cobre oxidado como "metal que envelhece" quando o visual pedir verdete.

### Progressão por idade [INT]
| Idade | Aplicar |
|---|---|
| Novo | pedra lisa, cobre `copper_block` |
| Usado | ~10% rachado/musgo na pedra; cobre `exposed_copper` |
| Velho | 25% musgo, 15-20% rachado, topos de parede com dentes; `weathered_copper` |
| Ruína | cobertura perdida, madeira removida, vegetação nos topos, `oxidized_copper` |
Valores em % vêm do código `ruina.py` (musgo 0,3 e rachado 0,15 a 0,2 por padrão no abandono), parâmetros de projeto [INT].

### Módulo `ferramentas/construcao/ruina.py` (lido) [TESTADO X04]
- `abandono`: madeira alta some primeiro, pedra erode por altura/exposição, `_envelhece` troca `stone_bricks` por mossy/cracked e `cobblestone` por mossy, depois `vegetar`.
- `impacto`: gradiente de dano a partir de um centro; chamusca com `blackstone`, `cracked_stone_bricks`, `polished_blackstone_bricks`; entulho no chão.
- `incendio`: remove madeira, fuligem acima das aberturas, chaminé em pé.
- `remover_flutuantes` e `limitar_balancos_de_madeira`: física mínima.
Resultado X04: aleatório deixou 106 blocos flutuantes; causas físicas, 0-3.

## Como construir no Bedrock
1. Escolha a causa antes de tocar nos blocos (abandono, impacto, incêndio). [TESTADO X04]
2. Chame `abandono(c, caixa, y_base, ...)` ou `impacto`/`incendio`; depois `remover_flutuantes`. [TESTADO X04]
3. Cobre: faça gradiente por exposição (topo/beiral mais oxidado, abrigado menos); use cera (`waxed_*`) para travar o estágio. [DOC ID; uso INT]
4. Madeira em ruína: remova em vez de "envelhecer"; adicione `moss_carpet`/`vine`/`moss_block` nas faces úmidas. [INT, parte em X04]
5. Verifique flutuantes e auditoria (`ferramentas/construcao/auditoria_geral.py`). [TESTADO X04]
6. Narrativa: um evento por construção; ver `../ambientacao/ruinas-e-narrativa.md`.

## Combina com
- [../ambientacao/ruinas-e-narrativa.md](../ambientacao/ruinas-e-narrativa.md)
- [paletas-e-combinacoes.md](paletas-e-combinacoes.md)
- [vidro-luz-e-metal.md](vidro-luz-e-metal.md)
- [../experimentos/X04-ruinas-com-causa/RESULTADO.md](../experimentos/X04-ruinas-com-causa/RESULTADO.md)
- [../estilos/pos-apocaliptico-subterraneo-liminal.md](../estilos/pos-apocaliptico-subterraneo-liminal.md)
- [../tecnicas/vegetacao-e-ambientacao.md](../tecnicas/vegetacao-e-ambientacao.md)

## Erros comuns
- `waxed_copper_block` (não existe), `stone_slab` (é `normal_stone_slab`).
- Dano aleatório uniforme: "queijo suíço" (X04).
- Telhado intacto após impacto na parede (limite conhecido de X04).
- Musgo uniforme em toda a parede, sem relação com umidade.
- Cobre oxidado em edifício novo sem justificar.
- Madeira "rachada": não existe; remova ou queime.

## Limitações e dúvidas
- Impacto não derruba o telhado quando só um trecho cai; falta regra de colapso por perda de apoio (X04).
- Vegetação esparsa e não calibrada; comparação com ruínas reais por foto não feita.
- Colapso de ruína sobre madeira e "chaminés sobrevivem" vêm só de busca [NV] (A5_r2 #13).
- Cor final de cobre e musgo não aparece no render; conferir no jogo.

## Fontes e evidências
- A5_r2: guia irlandês de ruínas (PDF aberto, seção 3), icorr.org (aberto), Ecclesiastical (PDF aberto, parcial); Historic England 403.
- A6_r2 #29 (IDs de cobre, bedrock-samples v1.26.60.5, aberto).
- `ferramentas/construcao/ruina.py` e `../experimentos/X04-ruinas-com-causa/RESULTADO.md` (render + métrica).
