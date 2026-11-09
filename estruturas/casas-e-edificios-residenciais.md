# Casas e edifícios residenciais

> Status: rascunho consolidado | Confiança: média (números documentados em fonte secundária; dimensões em blocos são sobretudo [INT]) | Última revisão: 2026-11-09

## Resumo
Casa legível = programa (social/serviço/íntimo) + circulação curta + escada com espaço + telhado com beiral. Números de norma são fonte secundária e não valem como regra universal; as medidas em blocos são calibradas pela Vila Pedra-Musgo e por X01/X05. Escada e porta têm regras testadas na Vila.

## Conceito
- [INT] Planta organizada em zonas: social (sala), serviço (cozinha, banheiro), íntima (quartos), ligadas por circulação curta. Fonte de 1ª rodada (só busca) descreve o mesmo programa; nenhum texto de norma foi aberto para isso.
- [INT] Estrutura em paredes portantes ou pórtico; o telhado define a silhueta (ver `../tecnicas/telhados-e-beirais.md`).
- Escala: 1 bloco = 1 m; o jogador ocupa 2 blocos de altura (convenção do projeto).

## Características / regras
| Item | Valor | Rótulo |
|---|---|---|
| Escada residencial (IRC 2024): espelho máx. 8,25 pol, piso mín. 9 pol, passagem 6 pés 8 pol, largura 36 pol | fonte secundária aberta (jaspector.com); edições anteriores 7¾/10 pol (não aberta); texto oficial ICC deu 403 | [DOC] só secundária |
| Pé-direito mínimo 7 pés (2.134 mm) no IRC; 2,4 m na Austrália | só resumo de busca da rodada 1, não reaberto | [NV] |
| Piso a piso em torres: residencial 3,1 m, escritório 3,9 m | Wikipedia "Storey" citando Saroglou et al. 2017 (aberta, secundária) | [DOC] |
| Pavimento residencial em blocos: 4 (1 laje + 3 livres); 3 é apertado | tradução de 3,1 m | [INT] |
| Casa pequena: planta 9x7 a 11x9; casa grande 15-25 de frente com volumes escalonados | calibrada na Vila (chalé, casa de pedra) | [INT] |
| Quarto/banheiro mínimo 3x3 internos; sala ~5x4 | sem fonte | [INT] |
| Telhado 1:1 = casa íngreme/chalé; 1:2 = casa baixa/rural | X01 | [TESTADO X01] |
| Mais de 3 materiais na fachada tende a poluir | heurística | [INT] |
- Prédio residencial: núcleo de escada central, varandas em balanço de 1-2 blocos, módulo de janela repetido a cada 3-4 blocos [INT]; ver [arranha-ceus.md](arranha-ceus.md) para torres.

## Como construir no Bedrock
**Receita: casa pequena de pedra e madeira (10x8, 2 pavimentos)** [TESTADO-AULA02 nos elementos; a casa completa como receita é NÃO TESTADA]
1. Implantação: nivelar um patamar 12x10 (margem de 1 para beiral). Registrar a pegada antes de construir (registro de ocupação, ver [vilas-e-cidades.md](vilas-e-cidades.md)).
2. Soco: 1 bloco de `cobblestone` ou `stone_bricks` em todo o perímetro.
3. Paredes: 4 de altura por pavimento; canto = coluna vertical contínua (`spruce_log` com `pillar_axis=y`), nunca viga horizontal no canto (E-23 em `../erros-e-licoes.md`).
4. Ritmo: pilar de `stripped_spruce_log` + painel de `spruce_planks` a cada 2 blocos (P-1 de `../tecnicas/paredes-estrutura-e-ritmo.md`).
5. Janelas: `glass_pane` 1x2 com alçapão aberto como veneziana; nunca bloco de vidro cheio nas casas da Vila.
6. Porta: batentes do mesmo material da parede, 2 de folha + escada invertida de verga; nada sólido a 2 blocos à frente/atrás (`../tecnicas/portas-e-entradas.md`).
7. Piso do 2º pavimento: laje `spruce_planks` 1 bloco; deixar abertura só sobre a escada.
8. Escada interna: lance reto de 4 degraus de `spruce_stairs`, `weirdo_direction` igual em todos, o 4º degrau no nível do piso, 2 blocos livres de cabeça, nada nas células do lance (`../tecnicas/escadas-internas.md`) [TESTADO-AULA02].
9. Telhado: 1:1 com `spruce_stairs` + beiral de 1 (X01a) ou 1:2 com escada+laje (X01b); fechar as empenas por coluna.
10. Mobiliário: medir o nível do piso (plataforma + carpete) antes; item sobre laje exige laje `top` ou bloco inteiro (E-21, E-30).
11. Auditoria: rodar a auditoria geral (IDs, estados, apoio, porta livre, escadas).

**Receita: caracol 3x3 em torreta** (8 células do anel, direção de cada degrau aponta para a próxima célula; primeiro degrau fora das células de porta) [TESTADO-AULA02, não andado no jogo].

## Combina com
[telhados](../tecnicas/telhados-e-beirais.md) · [escadas](../tecnicas/escadas-internas.md) · [interiores](../tecnicas/interiores-e-mobiliario.md) · [vilas-e-cidades.md](vilas-e-cidades.md) · [arranha-ceus.md](arranha-ceus.md) · [../fundamentos/escala-e-proporcao.md](../fundamentos/escala-e-proporcao.md) · [../estilos/medieval-europeu-e-fantasia.md](../estilos/medieval-europeu-e-fantasia.md) · [../estilos/vitoriano.md](../estilos/vitoriano.md) · [../ambientacao/terreno-biomas-agua.md](../ambientacao/terreno-biomas-agua.md)

## Erros comuns
- Caixa sem soco nem beiral; fachada de 1 plano parece papelão (X02: 3+ planos leem como arquitetura).
- Andar sem escada (E-31); escada com degrau a menos (E-29); móvel no lance.
- Cômodo 6x6 vazio; pé-direito 2.
- Janelas de tamanhos aleatórios; porta com vidro nas laterais ou vazio acima da folha (E-10, E-11).
- Casa em terreno inclinado: ver encosta em [subterraneas-e-suspensas.md](subterraneas-e-suspensas.md) e X05-E.

## Limitações e dúvidas
- Nenhuma dimensão de código de obras é regra universal; pé-direito é [NV].
- Nada foi testado andando no jogo; escadas da Vila aguardam confirmação do dono.
- Proporção janela/parede: amostra insuficiente (`../limitacoes-e-duvidas.md`).
- Casa em pilotis de madeira em encosta: não testada (código removido no X05).

## Fontes e evidências
- IRC 2024 escada: jaspector.com (aberta, secundária); ICC (403); IRC 7 pés e NCC 2,4 m: só busca, rodada 1.
- Wikipedia "Storey" / Saroglou 2017: aberta, secundária.
- Experimentos X01, X02, X05; erros E-10, E-11, E-21, E-23, E-29, E-30, E-31 de `../erros-e-licoes.md`; técnicas da Vila.
- Notas: A4_tipos_de_estrutura.md, A4_r2.md.
