# Praça e espaço público

Origem: feedback do dono na Vila (Aula 02). **Evidência** de uso real no jogo, com medidas do que foi corrigido.

- **S-1 Anel livre ao redor do que fica no meio da rua (regra do dono)**: fonte >= 3 blocos de caminho em volta; poço, barraca e demais >= 2. Nada sólido na altura do corpo (y+1, y+2) nem água nesse anel.
- **S-2 Escala da fonte**: raio total ~4 (bacia r=2,9 + borda) num espaço de ~29 x 16; fonte de raio 5+ em praça de 13 de profundidade fecha a passagem.
- **S-3 Equipamentos nos cantos, não no eixo**: barracas, poço e bancos longe do eixo das ruas e de portas; a rua reta dentro da praça.
- **S-4 Faixa de pedra diferente delimita o anel** (interpretação, confiança média).
- **S-5 Postes de luz**: base no terreno, fora de ruas e anéis; o braço pode pender sobre a rua.
- **S-6 Bancos**: voltados para o ponto de interesse; as costas ficam no lado oposto (a escada sobe em direção às costas).
- **S-7 Árvores**: copa não invade construções; sem tronco em rua, anel ou píer.

Checagem automática: `aulas/aula-02/codigo/auditoria.py` (regras E-12, E-14, E-15, E-16, E-19).
