# Modernista e contemporâneo

> Status: rascunho; modernista com teste X02/X05, contemporâneo sem teste próprio | Confiança: média-alta nos conceitos, média nas medidas | Última revisão: 2026-11-09

## Resumo
Modernista/Estilo Internacional: volume leve, planos finos, pilotis, janela em fita, cortina de vidro, sem ornamento. Receita TESTADA (X02 F3: 3 planos; X05-A: torre de 12 pavimentos). Contemporâneo: assimetria, balanços, vidro e materiais mistos; receita é adaptação [NÃO TESTADA].

## Conceito
- [DOC] Estilo Internacional (Hitchcock e Johnson): arquitetura como volume (planos finos, não massa), regularidade em vez de simetria, sem ornamento aplicado; vidro, aço e concreto (Wikipedia, resumo).
- [DOC] Cinco pontos de Le Corbusier: pilotis; teto-jardim; planta livre; janelas em fita; fachada livre. Fonte única: Wikipedia (Villa Savoye/International Style), resumo; [NV] fora disso.
- [DOC] Mies: "less is more"; Farnsworth House (1946-51), Seagram Building (1958, fachada-cortina de bronze com montantes em H). Wikipedia.
- [DOC] Contemporâneo (séc. XXI): fachadas assimétricas e balanços (Denver Art Museum), materiais mistos, sustentabilidade (Wikipedia). "Contemporâneo" é um rótulo amplo, não um estilo fechado [INT].
- Parametricismo: termo de Patrik Schumacher (2008), variação gradual em vez de repetição serial [DOC, Wikipedia].

## Características / regras
| Item | Dado | Status |
|---|---|---|
| Malha Chicago Federal Center | 8,5 m (28 ft) | [DOC] CONFIRMADA (ArchDaily e Wikipedia, abertas) |
| Módulo 1,4 m (6 por baia) | aritmética confere (28 ft / 6 = 1,42 m) | [NV] só busca, não em página aberta |
| Malha Villa Savoye | 5 m reduzida para 4,75 m por custo | [NV] fonte única (Wikipedia) |
| Malha em blocos | 5 blocos como aproximação | [INT] |
| Pavimento | 4 blocos = 1 laje + 3 livres | [TESTADO X05-A] |
| Montantes | a cada 3 blocos | [TESTADO X02 F3 e X05-A] (escolha do teste; a medida de Mies não foi usada) |
| Paleta | branco, preto, vidro claro/cinza; sem cor saturada em todos os planos | [INT] |
- Flynn e o modernismo: ver [futurista-cyberpunk-solarpunk.md](futurista-cyberpunk-solarpunk.md) (crítica solarpunk ao "liso, limpo e branco").

## Como construir no Bedrock
**Receita M1 — fachada modernista 17 x 13 [TESTADO X02 F3, 3 planos]**
1. Pilotis: colunas 1x1 de `white_concrete` em x = 0, 4, 8, 12, 16, y = 1 a 3, no mesmo plano z do vidro. Térreo livre.
2. Lajes: faixas de `white_concrete` com 3 de profundidade e 17 de largura em y = 4, 8, 12 (1 bloco à frente e 1 atrás do plano do vidro).
3. Cortina: nos pisos y = 5-7 e 9-11, uma linha de 17 blocos por 3 de altura; montante `white_concrete` quando x mod 3 = 0, senão `light_blue_stained_glass`.
4. Planos: laje, vidro/montante, pilotis. Os montantes e as lajes é que evitam "caixa de vidro".
5. Janela em fita: a mesma faixa de vidro com montantes lê como moderno/industrial [TESTADO X02].

**Receita M2 — torre de 12 pavimentos [TESTADO X05-A: "funciona", 4.887 blocos]**
- Planta 18 x 18, 12 pavimentos de 4 blocos, 2 recuos, cortina com montantes a cada 3, pilotis no térreo, casa de máquinas e antena no topo. Lê como base → corpo → coroa. Iluminação noturna e interior NÃO testados.
- Custo escala com a casca, não com o volume [TESTADO X05].

**Receita M3 — volume suspenso [NÃO TESTADO como casa]**
- Caixa horizontal (ex.: 17 x 9 x 8) sobre pilotis, laje de cobertura fina; teto-jardim com `moss_block`/`azalea` e guarda-corpo `iron_bars` [INT]. Telhado plano precisa de platibanda/friso para não parecer "tampa" [TESTADO X01-g].

**Receita C1 — contemporâneo [NÃO TESTADO]**
1. Volumes retangulares empilhados e deslocados; balanços de 3-6 blocos com pilar recuado [INT]. Balanço de 12 sobre ancoragem com contravento diagonal de `iron_bars` leu bem [TESTADO X05-D, 772 blocos, sem cálculo estrutural].
2. Regra dos materiais [INT]: 1 dominante (`white_concrete`), 1 quente (`stripped_birch_log` ou `birch_planks`), 1 vidro, 1 acento (`cut_copper`). Heurística de decoração sem fonte.
3. Vidro piso-teto com moldura mínima (`black_concrete` ou `iron_bars`); beiral fino de laje.
4. Assimetria: não repetir a mesma fachada em duas faces; deslocar pelo menos um volume 2-3 blocos.
5. Paramétrico [INT]: variar o espaçamento de brises em gradiente (ex.: 1, 2, 3 blocos), nunca aleatório.

## Combina com
- [Industrial e brutalista](industrial-e-brutalista.md) (módulo e concreto), [Futurista](futurista-cyberpunk-solarpunk.md) (Streamline é modernismo curvo).
- [Arranha-céus](../estruturas/arranha-ceus.md), [Casas e residenciais](../estruturas/casas-e-edificios-residenciais.md), [Vidro, luz e metal](../materiais/vidro-luz-e-metal.md), [Escala e proporção](../fundamentos/escala-e-proporcao.md), [Paletas](../materiais/paletas-e-combinacoes.md).

## Erros comuns
- Simetria rígida, ornamento (frisos, molduras) ou vidro com muitas divisões [INT].
- Vidro liso sem lajes salientes nem montantes: parece "caixa de vidro" [TESTADO X02].
- Esquecer pilotis e a leveza do volume; cor saturada em todos os planos [INT].
- Contemporâneo sem assimetria; materiais demais; paramétrico aleatório [INT].
- Janela rente à parede: 1 plano [TESTADO X02].

## Limitações e dúvidas
- Medidas reais (8,5 m, 4,75 m) são de edifícios específicos, não regras do estilo. Villa Savoye 4,75 m: fonte única.
- Pilotis de Villa Savoye "parcialmente simbólicos" e infiltrações [DOC Wikipedia]: não afetam a receita.
- Não há teste do contemporâneo (assimetria + materiais mistos) em render.
- Fonte para "contemporâneo" não usa o termo "paramétrico" (confiança baixa-média).

## Fontes e evidências
- Wikipedia: International Style, Villa Savoye, Mies van der Rohe, Contemporary architecture, Parametricism (resumos, rodada 1).
- ArchDaily "AD Classics: Chicago Federal Center" e Wikipedia Chicago Federal Center (abertas, resumo): malha de 8,5 m. Módulo de 1,4 m: só busca. architecture.org (aberta) não traz o módulo.
- Britannica: 403; MoMA/Tate: não consultados.
- `../experimentos/X02-fachadas-e-janelas/RESULTADO.md`, `../experimentos/X05-vertical-vaos-terreno/RESULTADO.md`, `../experimentos/X01-telhados/RESULTADO.md`.
