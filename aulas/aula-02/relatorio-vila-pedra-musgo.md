# Aula 02 — Teste prático: Vila Pedra-Musgo

> Seção separada dos registros da Aula 01 (que não foram alterados). Escrita **depois** de concluir a avaliação.

## Projeto
- **Conceito**: aldeia medieval/fantástica numa clareira, rua principal leste-oeste que atravessa uma praça central; Salão com torre-relógio ao norte, em terraço (nível 3), alcançado por escadaria.
- **Tamanho**: estrutura única 64 × 33 × 59 blocos (≈ 60 × 56 de vila), 31.662 blocos, 176 tipos de bloco/estados.
- **Paleta (60-30-10)**: 60% pedra mista cinza (stone_bricks, andesite, tuff_bricks, polished_andesite, cobble, mossy); 30% madeira escura em troncos descascados + reboco claro (calcite/diorite/concreto cinza); 10% acentos: cobre oxidado (telhado do hortelão, torre do Salão), lã laranja/azul das barracas, lanternas.
- **Construções**: Salão (principal) + 4 casas distintas + praça (fonte, poço, 4 barracas) + lagoa com píer + horta + 13 postes + 24 árvores.

| # | Construção | Silhueta / diferencial |
|---|---|---|
| Principal | Salão da Vila | nave longa de ardósia com cumeeira de cobre, torre-relógio central de 5×5, escadaria |
| 1 | Chalé enxaimel | 2 andares com avanço sobre pórtico, varanda, telhado de madeira |
| 2 | Casa de pedra com torreta | corpo de duas águas + torreta alta de quatro águas, contrafortes |
| 3 | Casa do hortelão | empena virada para a frente, telhado de cobre oxidado, alpendre, horta cercada |
| 4 | Casa de chá | plataforma, dois beirais largos de quatro águas, mirante, cantos levantados |

## Aplicação da Aula 01
| Técnica (código) | Onde foi aplicada | Adaptação |
|---|---|---|
| T1 paleta mista | todas as paredes de pedra (`PEDRA`, `PEDRA_ESCURA`, `PRACA`) | 6 materiais por peso aleatório, nenhum > ~30% |
| T2 tronco = esqueleto | vigas e cantos em `stripped_*_log` em chalé, hortelão, chá, Salão | cada casa com uma madeira diferente (spruce, dark_oak) |
| T5 vidraça | todas as janelas em `*_glass_pane` (nunca bloco de vidro) | 1 de largura × 2–3 de altura |
| P1 ritmo de pilares | fachada superior do chalé e do Salão | intervalo de 6 (chalé) e 4 (Salão), ajustado ao vão |
| R1 teto fechado | todos os telhados têm plano de forro por baixo | corrigido o beiral flutuante da casa de chá |
| R2 beiral largo | casa de chá (2 blocos), Salão, chalé | 2 níveis de beiral na casa de chá |
| R3 lajes invertidas como forro | sob beirais de chalé, Salão, chá, casa de pedra | `vertical_half=top` |
| I1 interior com blocos de função | todas as casas e o Salão | cama, barril, defumador, estante, carpete, lanternas |
| V1/V2 cobertura de solo e musgo | ~40% grama baixa, 10% alta, samambaia, 8% flores, musgo ao pé das árvores | proporção medida no código |
| V3 galhos na copa | 24 árvores com troncos internos | 3 galhos por árvore |
| C1 caminho irregular | rua e ligações a portas | 6 materiais, largura variável |
| C2 poço com solo desgastado | poço SW da praça | `grass_path`/`coarse_dirt` em volta |
| C3 fonte escalonada | fonte central | bacia de pedra, anel de lajes, pilar com copa d'água |

**Combinações**: T1+T2+P1 na fachada do Salão; R1+R2+R3 no telhado da casa de chá; V1+V2+V3 em cada árvore.

## Verificação feita
- `Cena.validar()` sem avisos (nenhuma peça solta).
- Fotos por câmera de raycast: vistas aéreas (S, O, NE), fachadas de chalé, casa de pedra, hortelão, chá, Salão, rua e praça.
- Arquivo `.mcstructure` escrito pelo próprio exportador e **relido** (tamanho, paleta e índices conferidos).

## Autoavaliação
- **Melhores**: Salão com torre (silhueta e hierarquia), casa de chá (silhueta), praça.
- **A melhorar**: chalé (telhado simples, sem empena cruzada); interiores básicos; textura de parede ainda pouco variada em escala; poucas janelas com moldura.
- **Mais difícil**: telhados (empena cruzada falhou e foi removida), balanço da sacada da casa de pedra, orientação de blocos (portas, camas, alçapões).
- **Ainda preciso aprender**: telhados complexos, iluminação em escala, integração do terreno com o mundo real.

## Limitações (honestas)
- O render usado **não tinge folhas e não reproduz cobre/ardósia/lã colorida** (aparecem cinza); as cores finais só se confirmam no jogo.
- **Não testado no Minecraft**: portas, camas, alçapões, estados de escada, fluxo de água e carregamento da estrutura. Precisa de print do jogo.
- Nada foi colocado no mundo "Aula"; foi gerado um add-on novo (`VULPUS_Vila_BP.mcpack`).

## Novos aprendizados (somente desta aula)
1. Telhados com material misto (ex.: 85% dark_oak + 15% spruce) reduzem a massa chapada; mais de 2 materiais vira ruído.
2. Pilares a cada 4 deixam pouco reboco em painéis de 3; subir para 6 em fachadas de ~13 blocos.
3. Hanging lantern precisa de bloco acima; validar sempre.
4. Estruturas > ~77 estados exigem exportador próprio (o da biblioteca limita símbolos).

## Como colocar e salvar no jogo
1. Importar `VULPUS_Vila_BP.mcpack` e ativar o add-on no mundo.
2. `/function vila/preparar` (cria a área de carregamento), esperar alguns segundos, depois `/function vila/colocar`.
3. Local: canto mínimo em (-130, 96, -10); o solo da vila fica em y=100.
4. Depois de editar: `/function vila/salvar` grava a área (x -130..-67, y 96..128, z -10..48) como `vila_modificada` no mundo, igual ao `salvar` da Aula 01.

## Correção pós-teste (2026-11-09)
Ao entrar no jogo, o dono encontrou blocos estranhos, portas bloqueadas e portas sem a metade de cima. A afirmação acima de "validação sem avisos" **não pegou** IDs de bloco inválidos (≈202 lajes com nome sem `_slab`). Detalhes, causas e correções em `erros-e-licoes.md` (E-01 a E-09). A versão corrigida foi regerada e reinstalada no mundo.
