# Industrial e brutalista

> Status: rascunho validado parcialmente (brutalista com teste X02; industrial sem teste) | Confiança: média (brutalista), baixa-média (industrial) | Última revisão: 2026-11-09

## Resumo
Dois estilos de "função e material à vista". Brutalista: massa de concreto, módulo repetido, janela funda; tem receita TESTADA (X02 F2, 4 planos). Industrial: tijolo, aço, telhado dente-de-serra, chaminé; só o conceito tem fonte, a receita em blocos é [NÃO TESTADO].

## Conceito
- [DOC] Brutalismo: "new brutalism" usado por Alison e Peter Smithson em 1953; Reyner Banham o popularizou em 1955 e o ligou ao *béton brut* de Le Corbusier. Mais ética que estética: honestidade, funcionalidade, respeito aos materiais; legibilidade da planta e estrutura exposta (Wikipedia, resumo). Críticas: frio, autoritário; concreto mancha e cria musgo em clima úmido.
- [DOC] Industrial: materiais duráveis (concreto, tijolo, metal, vidro), estrutura de ferro/aço, pé-direito alto, janelas grandes, plantas abertas (Wikipedia, Industrial architecture).
- Em comum [INT]: a forma vem da repetição de um módulo e da estrutura visível, não de ornamento.

## Características / regras
| Item | Brutalista | Industrial |
|---|---|---|
| Material | concreto aparente com marca de fôrma; tijolo, aço, madeira [DOC] | tijolo, aço, vidro, concreto [DOC] |
| Módulo | baia repetida em grade [DOC: "módulos repetidos"]; medidas [NV] | baias de pilastra a pilastra [INT]; medidas [NV] |
| Abertura | janela profunda: [INT] comum, não confirmada na fonte lida | grandes panos, grade de painéis pequenos [INT] |
| Telhado | plano, cornija pesada [INT] | dente-de-serra: faces inclinadas envidraçadas, de costas para o equador, luz difusa [DOC, glossário + Wikipedia] |
| Verticais | pilares grossos, balanços [INT] | chaminé: India Mill, Darwen, 91 m, 1867 [DOC só Wikipedia]; silos e pontes rolantes [NV] |
| Paleta | cinzas claros a escuros, manchas de umidade [INT] | tijolo-vermelho, cinza-aço, fuligem, ferrugem [INT] |

## Como construir no Bedrock
**Receita B1 — fachada brutalista 17 x 12 [TESTADO X02 F2: 4 planos, "muito forte para o custo"]**
1. Parede: 17 de largura, 12 de altura, 3 de espessura, mistura aleatória `light_gray_concrete` (5) : `stone` (1) : `andesite` (1) para imitar fôrma/manchas.
2. Recessos: em cada um dos 3 pisos de janela (y = 2, 5, 8) abrir 4 vãos de 3 de largura x 2 de altura, em x = 1, 5, 9, 13, com profundidade 3 (`air`). No fundo do recesso, 1 camada de `glass_pane`.
3. Brises/lajes salientes: uma linha contínua de `normal_stone_slab` 1 bloco à frente da parede em y = 4, 7, 10 (cada piso).
4. Cornija pesada: no topo (y = 12), faixa de concreto de 2 de profundidade avançando 1 bloco.
5. Planos obtidos: fundo do recesso, parede, brise, cornija. Regra: criar profundidade movendo uma faixa 1 bloco, não trocando blocos.
6. Envelhecimento [NÃO TESTADO nesta receita]: salpicos de `moss_block`, `mossy_stone_bricks`, `cracked_stone_bricks`, `tuff` sob os recessos e brises (onde a água escorre).

**Receita B2 — massa e balanço [NÃO TESTADO como estilo; balanço de 12 com contravento TESTADO X05-D]**
- Pilares de 2x2 em `light_gray_concrete`; balanços de 2-4 blocos sobre eles; rasgos verticais e caixas salientes para quebrar a monotonia [INT].

**Receita I1 — galpão industrial [NÃO TESTADO]**
1. Parede de `brick_block` (o ID é `brick_block`, não `bricks`) com pilastras de `stone_bricks` ou `deepslate_bricks` a cada 5 blocos [INT] (ritmo de baia).
2. Janelas altas em grade de `glass_pane` entre pilastras; soleira em `stone_brick_slab`.
3. Telhado: X01 mostra que plano com platibanda e friso lê bem como moderno/industrial [TESTADO X01-g, 113 blocos no teste]. Dente-de-serra: repetir perfil escada + vidro a cada 5-6 blocos [INT, NÃO TESTADO]; só o conceito é [DOC].
4. Chaminé: fuste quadrado 3x3 ou octogonal; círculo só lê com diâmetro ~15 (X03), então não force círculo [TESTADO X03]. Topo em `blackstone`.
5. Dutos e vigas: `iron_bars`, `iron_chain`, `polished_deepslate`, `stone_brick_wall` [INT].
6. Silo: cilindro de `light_gray_concrete`; mesma restrição de círculo (X03). Silos e pontes rolantes: [NV].

## Combina com
- [Modernista e contemporâneo](modernista-e-contemporaneo.md) (mesma lógica de módulo), [Pós-apocalíptico](pos-apocaliptico-subterraneo-liminal.md) (brutalista + moss + corrosão).
- [Instalações industriais](../estruturas/instalacoes-industriais-e-laboratorios.md), [Envelhecimento](../materiais/envelhecimento-e-deterioracao.md), [Paredes e ritmo](../tecnicas/paredes-estrutura-e-ritmo.md), [Profundidade](../fundamentos/profundidade-contraste-transicoes.md).

## Erros comuns
- Janela rente à parede: fachada de 1 plano parece "papelão" [TESTADO X02-F0].
- Concreto de um tom só, sem pilastras ou recessos [INT].
- Pé-direito baixo e sem vegetação/rastro de uso [INT].
- Telhado industrial reto sem luz zenital; esquecer chaminé/dutos [INT].
- Usar `stone_slab` (não existe): usar `normal_stone_slab` [TESTADO-AULA02/X02, E-34].

## Limitações e dúvidas
- Nenhuma medida de módulo brutalista ou industrial foi documentada [NV]; 3 de profundidade e 5 de baia são escolhas do teste e minhas.
- Silos, pontes rolantes: sem fonte aberta. Dente-de-serra: só definição, sem medidas de inclinação.
- Render X02 não prova a transparência real do vidro no jogo.

## Fontes e evidências
- Wikipedia, Brutalist architecture (resumo, rodada 1); Wikipedia, Industrial architecture e Sawtooth roof (rodada 1); glossário de patrimônio inglês por busca (dente-de-serra, parcial); Wikipedia, British industrial architecture (aberta, resumo; India Mill 91 m).
- Historic England: 403. Silos/pontes rolantes: sem fonte.
- Experimentos: `../experimentos/X02-fachadas-e-janelas/RESULTADO.md`, `../experimentos/X01-telhados/RESULTADO.md`, `../experimentos/X03-curvas-e-diagonais/RESULTADO.md`, `../experimentos/X05-vertical-vaos-terreno/RESULTADO.md`.
