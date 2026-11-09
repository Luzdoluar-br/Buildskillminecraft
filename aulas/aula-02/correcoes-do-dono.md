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
