# Portas e entradas

Origem: correções do dono na Vila (Aula 02), lidas no mundo. **Evidência** salvo quando marcado como interpretação.

- **P-1 Porta embutida em parede maciça (evidência)**: nada de vidro ou vazio nos batentes; usar o mesmo material da parede, em toda a altura da abertura.
- **P-2 Altura exata (evidência)**: abertura = 2 de altura (a porta) + verga; sobrar 1 bloco vazio acima da folha é erro.
- **P-3 Verga em escada invertida (evidência)**: `upside_down_bit=1`, subindo em direção ao interior (`weirdo_direction` = direção de dentro), no material da parede.
- **P-4 Entrada livre (evidência)**: nenhum bloco sólido nos 2 blocos à frente e atrás da porta, em `y` e `y+1`; sem degrau na frente quando o piso está rente ao chão.
- **P-5 Degraus que levam a uma plataforma sobem em direção à porta (evidência de erro meu)**: `weirdo_direction` = direção em que a escada sobe.
- **P-6 Luz ao lado da entrada (interpretação, confiança média)**: postes com lanterna dos dois lados marcam o acesso.
- **P-7 Bancos e mobiliário urbano fora do eixo de porta e de rua (evidência)**.

Checagem automática: `aulas/aula-02/codigo/auditoria.py`.
