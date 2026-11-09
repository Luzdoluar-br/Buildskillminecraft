# Arranha-céus

> Status: rascunho consolidado | Confiança: média (lógica estrutural documentada em secundária; proporções [INT]; torre testada em render, não no jogo) | Última revisão: 2026-11-09

## Resumo
Torre = núcleo + fachada ritmada + recuos + coroa. Piso a piso de 4 blocos funcionou em X05 (torre 18x18, 12 pavimentos, 4.887 blocos). Base/corpo/coroa é leitura por função, não razão numérica.

## Conceito
- [DOC] Núcleo de concreto dá resistência lateral; outrigger + belt truss ligam núcleo ao tubo; tubo emoldurado (Khan, 1963). Wikipedia "Skyscraper" (aberta, secundária); CTBUH não aberto.
- [DOC] Os recuos do Empire State vieram do zoneamento (mesma fonte). A lei de 1916 de Nova York e o Equitable Building (1915): só busca, rodada 1.
- [DOC] Sullivan propõe base/corpo/coroa por FUNÇÃO (lobby/comércio, andares repetidos, topo). Não existe razão numérica documentada: não usar 1:3:1.
- Fachada cortina: pele leve e não portante [DOC secundária].

## Características / regras
| Item | Valor | Rótulo |
|---|---|---|
| Piso a piso escritório 3,9 m; residencial 3,1 m | Storey/Saroglou 2017 (aberta, secundária) | [DOC] |
| Torres de Hong Kong ~4,0 m (3,73-4,20) | FIG PDF não abriu | [NV] |
| Núcleo = 20-25% da planta | blog não aberto | [NV] |
| Pavimento em blocos: 4 (1 laje + 3 livres) | tradução de 3,9 m | [INT], usado em [TESTADO X05] |
| Planta 18x18, recuos em 2 etapas, vidro com montante a cada 3, pilotis no térreo, casa de máquinas e antena | resultado: lê como arranha-céu | [TESTADO X05] |
| Pilastra a cada 3-4 blocos | calibrada no X05 (3) | [TESTADO X05] para 3; 4 [INT] |
| Altura máxima do mundo e limites de estrutura (.mcstructure) | não conferidos nesta rodada; ver `../referencia/mcstructure-formato.md` | [NV] |
- Custo escala com a casca, não com o volume: ~4,9 mil blocos para ~60 de altura [TESTADO X05].
- Base alta com lobby marcado, corpo repetitivo e coroa distinta: mínimo para silhueta [INT].

## Como construir no Bedrock
**Receita: torre de 12 pavimentos** [TESTADO X05, render + auditoria; não testado andando, nem iluminação noturna]
1. Planta 18x18 com núcleo central (escada/elevador) 6x6 a 8x8 [INT para o núcleo].
2. Térreo em pilotis [TESTADO X05]; espaçamento das colunas (ex.: a cada 3) e pé-direito do lobby maior (5-6) são [INT].
3. Cada pavimento: laje de 1 + 3 livres. Laje em `smooth_stone`/`white_concrete`; faixa de laje visível em cada pavimento.
4. Fachada: montante vertical (`light_gray_concrete` ou `quartz_pillar`) a cada 3 blocos; entre eles vidro (`light_blue_stained_glass` ou `gray_stained_glass`; `glass_pane` onde precisar de profundidade). O render não dá a cor final do vidro (X05).
5. Recuos: 2 recuos ao longo da altura [TESTADO X05]; tamanho (2 blocos por lado) e pavimento de cada recuo: [INT] (o resultado do X05 não registra esses valores).
6. Coroa: casa de máquinas menor que o último pavimento + antena de `lightning_rod`/`iron_bars`/`end_rod` (conferidos na lista).
7. Variar a profundidade da fachada em 1 bloco (montantes salientes) para sombra, como em X02.
8. Interior (não testado): núcleo oco com escada (`../tecnicas/escadas-internas.md`), cada andar com abertura sobre degraus.
9. Iluminação: `sea_lantern`/`glowstone` atrás do vidro em alguns pavimentos, não em todos [NÃO TESTADO].

**Torre muito alta** (>100 de altura): dividir em segmentos para o `.mcstructure` e empilhar na colagem [INT; limites exatos NV].

## Combina com
[vilas-e-cidades.md](vilas-e-cidades.md) (cidade vertical) · [estacoes-e-ferrovias.md](estacoes-e-ferrovias.md) · [../estilos/modernista-e-contemporaneo.md](../estilos/modernista-e-contemporaneo.md) · [../estilos/futurista-cyberpunk-solarpunk.md](../estilos/futurista-cyberpunk-solarpunk.md) · [../fundamentos/composicao-hierarquia-silhueta.md](../fundamentos/composicao-hierarquia-silhueta.md) · [../materiais/vidro-luz-e-metal.md](../materiais/vidro-luz-e-metal.md) · [casas-e-edificios-residenciais.md](casas-e-edificios-residenciais.md)

## Erros comuns
- Caixa lisa sem ritmo; pavimento de 2-3 blocos; sem lobby/base; topo cortado reto.
- Vidro uniforme sem montante; nada atrás do vidro (planejar lajes e luz interior).
- Torre esbelta sem recuo/contraforte [INT, percepção].
- Cilindro com diâmetro menor que ~15: lê como quadrado arredondado; use octógono (X03).

## Limitações e dúvidas
- Proporção base:corpo:coroa não tem fonte; a leitura por função é o que se sustenta.
- Altura máxima construível e limite do `.mcstructure`: não verificados nesta rodada.
- Interior, iluminação noturna e vidro de cor real: não testados.

## Fontes e evidências
- Wikipedia "Skyscraper" (aberta); Wikipedia "Storey" (aberta); FIG PDF (falhou); CTBUH (redirect); blog archgyan (não aberto).
- Experimento X05-A (`../experimentos/X05-vertical-vaos-terreno/RESULTADO.md`), X03-A (círculo).
- Notas: A4_r2.md (tabela e correções).
