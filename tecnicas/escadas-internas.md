# Escadas internas

Origem: prints do dono na Vila (Aula 02) e erro E-29. **Evidência** = visto/medido; *interpretação* marcada.

- **S-1 Contagem**: número de degraus = diferença de altura entre os pisos. Piso de cima 4 acima do de baixo → 4 degraus; o **último degrau fica no nível do piso de cima** (substitui um bloco do piso). 3 degraus deixam um pulo de 1 bloco (erro E-29).
- **S-2 Direção**: `weirdo_direction` = direção em que a escada **sobe**, igual em todos os degraus do lance; cada degrau sobe 1 e avança 1.
- **S-3 Abertura**: tirar o piso de cima sobre os degraus (3 blocos de comprimento num lance de 4) para a cabeça passar; 2 blocos de altura livres sobre cada degrau.
- **S-4 Trajetória livre**: nenhum móvel (estante, barril, bancada) nas células do lance nem na frente do primeiro degrau. Estantes e bancadas ficam em outra parede.
- **S-5 Acesso**: todo andar/torre/loft precisa de acesso (escada) ou ser declarado decorativo fechado (ver E-31).
- **S-6 Parede de apoio**: lance encostado em uma parede (lado do lance sem blocos soltos), como o dono refez na tela 19 (*interpretação a confirmar com o dono ao ler o mundo salvo*).

Checagem: regra E-29 em `aulas/aula-02/codigo/auditoria.py` (lances registrados em `ESCADAS`).

## Variantes (decididas com o dono: escada interna para tudo)
- **Lance reto** (`lance()`): para andares largos, junto a uma parede; abre o piso/forro só sobre os degraus.
- **Caracol 3x3** (`espiral()`): para torres/torretas; 8 células de anel, 1 bloco de altura por célula; direção do degrau = rumo à próxima célula do anel. Começar o anel de modo que as células de porta/passagem só tenham degrau em y>=4.
- **Terraço sobre beiral**: quando o andar de cima é um mirante em cima do telhado, o lance sai no terraço e a porta do mirante abre para ele, com guarda-corpo no poço.
- Sempre registrar o lance em `ESCADAS` para a auditoria E-29.
