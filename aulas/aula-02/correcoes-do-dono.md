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
