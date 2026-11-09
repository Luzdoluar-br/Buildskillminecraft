# X02 — Fachadas com profundidade e janelas

**Pergunta**: quantos planos de profundidade cada estilo de fachada usa e quais janelas "leem" em Minecraft? **Script**: `experimento.py`. **Imagens**: `imagens/montagem_fachadas.png`, `montagem_janelas.png`.

## Fachadas (17 de largura × 12 de altura)
Métrica: nº de planos distintos (valores de z ocupados) numa coluna típica da fachada.

| Fachada | Planos | O que cria a profundidade | Leitura visual |
|---|---|---|---|
| F0 controle liso | **1** | nada (janelas rente à parede) | Parece "papelão": sem sombra, sem escala |
| F1 medieval enxaimel | 4 | soco recuado, andar que avança 1 bloco, pilares de tronco, mãos-francesas | Forte; o avanço do andar de cima é o que mais ajuda |
| F2 brutalista | 4 | janelas em recesso de 3 de profundidade, brises/lajes salientes por piso, cornija pesada | Muito forte para o custo: massa + vazio profundo + repetição |
| F3 modernista | 3 | pilotis (térreo livre), lajes salientes, cortina de vidro com montantes a cada 3 | Lê como moderno; os montantes e as lajes são o que evita "caixa de vidro" |
| F4 gótica | 4 | contrafortes salientes com capa em escada, janelas fundas, cornija | Boa verticalidade; contrafortes dão ritmo |
| F5 japonesa | 7* | plataforma, engawa, pilares, shoji recuado, beiral largo em 2 níveis | Mais camadas e silhueta marcante (*a contagem inclui os dois níveis de beiral) |

**Conclusão (TESTADO por render + métrica)**: fachada com 1 plano é a pior; 3 a 4 planos já leem como arquitetura. O recurso mais barato por camada de profundidade é **mover uma faixa 1 bloco para frente ou para dentro** (avanço, recesso, laje saliente), não detalhar com blocos diferentes.

## Janelas (painéis de 8×9 em parede de pedra)
| Janela | Resultado |
|---|---|
| simples 1×2 | Lê como janela, mas "furo na parede" |
| com moldura (soleira em laje, verga em escada invertida, ombreiras em pedra polida) | **Melhor relação custo/efeito** |
| com persianas (alçapões abertos) | Funciona; a direção do alçapão aberto precisa ser conferida no jogo |
| ogival 1 de largura | **Não lê**: parece entalhe; arco ogival pede ≥ 3 de largura e ≥ 6 de altura |
| arco pleno 3 de largura | Lê como trapézio; arco pleno exige ≥ 5 de largura |
| seteira com `iron_bars` | Funciona muito bem para fortificações |
| em fita com montantes | Lê como moderno/industrial |
| "redonda" 3×3 | Não lê como círculo (ver X03: círculo só lê a partir de ~diâmetro 15) |

## Falhas e limites
- A primeira versão do script usou `stone_slab`, que **não existe** no Bedrock (o ID é `normal_stone_slab`): a auditoria nova acusou na hora (ver `erros-e-licoes.md`).
- Vidros e cores aparecem aproximados no render; não confirma transparência real no jogo.
- Direção dos alçapões abertos (persiana): não validada no jogo.
