# Correções feitas pelo dono na Vila (aprendizado da Aula 02)

Método (igual à Aula 01): comparar o mundo salvo com a estrutura que eu gerei. Cada correção abaixo foi **lida no mundo**, não presumida. Entradas novas no fim.

## 2026-11-09 · Entrada da torre do Salão (centro: x -98, y 104, z 12)
Lido no LevelDB do mundo "Aula" (diferenças na caixa da entrada):

| O que eu fiz | O que o dono fez | Princípio |
|---|---|---|
| Vidraças (`white_stained_glass_pane`) ao lado da porta, 2 de altura | `stone_bricks` maciço | porta dentro de parede contínua, sem vidro nos batentes |
| Escadas invertidas laterais acima dos vidros | `stone_bricks` | verga só no centro; laterais maciças |
| Laje superior (`stone_brick_slab` top) acima da porta | `stone_brick_stairs` invertida, `weirdo_direction=3` | verga em escada, no material da parede |
| Degraus `stone_brick_stairs` em frente (eram os bancos da praça) | removidos (ar) | entrada rente ao chão, sem degrau barrando |
| (já existiam) postes com lanterna ao lado | mantidos | luz ao lado da entrada |

Regras extraídas: ver `tecnicas/portas-e-entradas.md` e erros E-10, E-11, E-12 em `erros-e-licoes.md`.

## Como pedir novas correções
O dono não usa mais `/function vila/salvar`: ele passa prints e descrições; eu leio o mundo, registro aqui, generalizo para todas as estruturas (E-13) e rodo `auditoria.py`.

## 2026-11-09 · Praça e objetos soltos (feedback por texto e prints, não lido no mundo)
| Observação do dono | Princípio |
|---|---|
| "Esse meio está muito apertado; ninguém passa de um lado para o outro. Abra espaço para um caminho POR VOLTA da fonte. Vale para todo tipo de construção no meio da rua." | anel de passagem livre ao redor de tudo que fica no meio (fonte ≥3 blocos, poço/barraca ≥2) |
| "Por que tem poste de luz em cima das barracas?" / "poste em cima de poste" | objetos de chão nascem no terreno, nunca no topo de outra construção |
| "Estruturas se fundindo (barraca com poço) + árvore cortada pela metade, flutuante" | nenhum objeto pode ocupar espaço de outro; registro de ocupação |
| "Arrume bugs em geral, não só as estruturas que estou apontando" | cada relato é uma classe de erro; varrer tudo |
| "Adicione um function que limpa o local totalmente" | `functions/vila/limpar.mcfunction` (apaga a área e itens; rodar antes do `colocar`) |

## Funções do add-on (vila/)
`preparar` (ticking area) → `limpar` (opcional, APAGA TUDO na área) → `colocar`. `salvar` continua disponível.

## 2026-11-09 · Blocos flutuantes, erros de textura e poste novo (prints + leitura do mundo)
| Observação do dono | O que achei | Registro |
|---|---|---|
| "Há muitos blocos flutuantes" (print: barril e cerca no ar na casa de chá) | mobília 1 bloco acima do piso; copa da fonte e píer sem apoio | E-21 |
| "Blocos com erros de texturas" (print: cubos manchados no chão) | `rooted_dirt` e `lily_pad` não existem no Bedrock | E-20 |
| "Melhoria para esse estilo de poste" (print) | lido no mundo: laje de topo, braço em escada, lanterna embaixo, contrapeso | E-22, `tecnicas/postes-de-luz.md` |
| "Não se esqueça de anotar tudo no git" | tudo registrado e publicado | este arquivo |

## 2026-11-09 · Cantos, rotação e referência de blocos (prints + leitura do mundo)
| Observação do dono | O que fiz / aprendi | Registro |
|---|---|---|
| Prints "ERRADO ---> / CERTO ---> " nos cantos de madeira (ponta de tronco exposta vs pilar contínuo); ele corrigiu à mão | cantos viram tronco vertical em todas as casas | E-23, `tecnicas/cantos-e-vigas.md` C-1 |
| "Algumas estruturas com os troncos todos na mesma direção; trabalhe a rotação dos blocos" | revisão de `pillar_axis`, máquinas com `cardinal_direction`, para-raios, abóboras, giro (flip) | E-24, E-25, `referencia/estados-e-rotacao.md` |
| "Quero um arquivo com todos os blocos do Minecraft e seus IDs" | `referencia/blocos-bedrock.md` (1187 IDs) | E-26 |
| Melhoria dos cantos (prints + blocos no mundo: viga projetada, lanterna, escada) | lido 1 canto; padrão descrito em C-2 (a confirmar) | `tecnicas/cantos-e-vigas.md` C-2 |
| "Não esqueça de anotar seus aprendizados no git, é muito importante; o foco é te ensinar e registrar" | checklist de fim de rodada | E-27 |

## 2026-11-09 · Canto do dono confirmado para todos os cantos
| Observação do dono | O que fiz |
|---|---|
| "Só coloquei 1 canto como exemplo, é para usar nos cantos em geral. E como assim mísula?" | explicado o termo (degrau de escada sob a viga); `canto_lampada()` aplicada em chalé, hortelão e casa de chá; padrão C-2 marcado como confirmado; E-28 |
