# Estruturas subterrâneas e suspensas

> Status: rascunho consolidado | Confiança: baixa-média (abóbadas qualitativas documentadas; dimensões de galerias e aceitação visual são [INT]/[NV]) | Última revisão: 2026-11-09

## Resumo
Abóbada leva carga por compressão e empurra para os lados; balanço precisa de ancoragem/contrapeso. No X05 o balanço de 12 com contravento e a casa em encosta funcionaram. Abóbadas de raio pequeno não leem como curva (X01, X03). Como o olho aceita balanços é interpretação própria.

## Conceito
- [DOC, aberta secundária] Abóbada de berço empurra lateralmente; ogival gera menos empuxo; nervurada leva a carga pelas nervuras; Ctesifonte ~25 m de vão com coroa ~1,5 m (Wikipedia "Vault (architecture)").
- [DOC] Cantilever: balanço equilibrado por braços de ancoragem/contrapeso (Wikipedia "Cantilever bridge").
- [DOC] Fallingwater: terraços em balanço a partir da chaminé; flechas de ~180 mm (quase 2 graus) por falta de contra-flecha e armadura; pós-tensão concluída em 2001-03 (Wikipedia, citando Silman, Toker, Hoffmann). Não há comprimento de balanço nem ancoragem na rocha na fonte.
- [DOC, só busca R1] Poços de ventilação de Varsóvia resistem por espessura; luz indireta em abóbadas de metrô.
- [NV] Dimensões de galerias subterrâneas; razão balanço/vão.

## Características / regras
| Item | Valor | Rótulo |
|---|---|---|
| Abóbada de berço 7-11 de largura; altura 0,6-0,7 da largura; colunas a cada 4-6 | | [INT] |
| Abóbada/cobertura curva de raio <= 4 não lê: parece caixa chanfrada | | [TESTADO X01] |
| Curva lê a partir de diâmetro ~15; cúpula com lajes melhor a partir de raio 8 | | [TESTADO X03] |
| Galeria de mina 3x3 a 5x5 com escoras a cada 4; poços 2x2 a 4x4 | | [INT] |
| Balanço de concreto de 12 sobre massa de ancoragem com contravento diagonal de `iron_bars` | lê bem | [TESTADO X05] |
| Balanço natural até 1/3 do trecho ancorado; acima, tirantes ou apoio escondido | | [INT] sem fonte |
| Balanço 4-8 em casa moderna; 10-15 com tirantes inclinados | | [INT] |
| Casa em encosta 1:2 com fundação escalonada de pedra e patamar nivelado | | [TESTADO X05] |

**Como o olho aceita um balanço** [INT, sem fonte aberta]: (1) massa contrapesada visível no lado oposto; (2) laje mais fina na ponta; (3) linhas horizontais fortes; (4) tirantes/contraventos que apontam para a ancoragem; (5) sombra sob o balanço. X05 só confirma que o contravento "justifica" visualmente: é interpretação, sem cálculo estrutural.

## Como construir no Bedrock
**Receita A: balanço com contravento** [TESTADO X05, 772 blocos]
1. Massa de ancoragem: bloco de concreto/pedra 8x8x10 ligado ao terreno ou ao edifício.
2. Laje em balanço de 12 de comprimento, 1-2 de espessura, em `white_concrete`/`smooth_stone`, saindo da massa.
3. Contravento diagonal de `iron_bars` (ou escoras) da ponta da laje à base da massa; se for cerca/barra em diagonal, preencher o degrau vertical senão não se liga (E-36).
4. Guarda-corpo de `iron_bars` ou vidro; sombra visível sob a laje.
5. Auditoria: elementos suspensos precisam tocar em sólido (regra refinada em X05).
**Receita B: casa em encosta** [TESTADO X05, 540 blocos]
1. Terreno 1:2; cortar um patamar nivelado.
2. Fundação escalonada em `cobblestone`/`stone_bricks` acompanhando a inclinação (muro de arrimo) até o patamar.
3. Casa sobre o patamar; pilotis de madeira: NÃO testado.
**Receita C: galeria abobadada** [NÃO TESTADO]
1. Largura 9-11, altura 6-7; berço em `stone_brick_stairs`/`stone_brick_slab` com sapata de 1 de pedra maciça.
2. Costelas a cada 4-6 (nervuras de `stone_bricks` salientes 1 bloco) para quebrar o berço liso.
3. Luz indireta em nichos nos pés da abóbada (`lantern` oculta a cada 6-8).
4. Piso com drenagem visível e saídas/poços a cada ~30 [INT]; saída pela superfície disfarçada por pequeno edifício.
**Receita D: caverna/mina** [NÃO TESTADO]: túnel 3x3 a 5x5 com escoras `spruce_log`/`spruce_planks` a cada 4; evitar reta uniforme: variar altura e largura; `pointed_dripstone`, `dripstone_block`, `moss_block`.
**Receita E: passarela suspensa** [NÃO TESTADO]: tabuleiro 3 de largura, cabos a cada 4-6, torres de apoio; princípio da ponte pênsil de [pontes-e-viadutos.md](pontes-e-viadutos.md).

## Combina com
[pontes-e-viadutos.md](pontes-e-viadutos.md) · [estacoes-e-ferrovias.md](estacoes-e-ferrovias.md) · [instalacoes-industriais-e-laboratorios.md](instalacoes-industriais-e-laboratorios.md) · [../estilos/pos-apocaliptico-subterraneo-liminal.md](../estilos/pos-apocaliptico-subterraneo-liminal.md) · [../estilos/modernista-e-contemporaneo.md](../estilos/modernista-e-contemporaneo.md) · [../ambientacao/terreno-biomas-agua.md](../ambientacao/terreno-biomas-agua.md) · [../ambientacao/iluminacao-e-atmosfera.md](../ambientacao/iluminacao-e-atmosfera.md) · [casas-e-edificios-residenciais.md](casas-e-edificios-residenciais.md)

## Erros comuns
- Balanço sem massa de compensação; laje grossa e curta flutuando.
- Cabos que não levam a lugar nenhum; cabo diagonal de cerca com buracos.
- Abóbada de raio pequeno tentando parecer curva.
- Túnel reto uniforme 3x3 com luz uniforme, sem suporte aparente nem saída.
- Casa em terreno aplainado em caixa, sem muro de arrimo.
- Blocos com gravidade (`gravel`, `sand`) sem apoio.

## Limitações e dúvidas
- Dimensões reais de galerias e abóbadas subterrâneas: [NV].
- Aceitação visual do balanço: nenhuma fonte; X05 é render, não jogo.
- Casa na árvore e rocha escavada: tema não pesquisado aqui; limite de blocos com gravidade no Bedrock: não verificado.

## Fontes e evidências
- Wikipedia "Vault (architecture)", "Cantilever bridge", "Fallingwater" (abertas, secundárias).
- tclf, NEH, designingbuildings, czasopisma.pan.pl: só busca (R1).
- X01-e, X03, X05-D/E; E-36.
- Notas: A4_tipos_de_estrutura.md, A4_r2.md.
