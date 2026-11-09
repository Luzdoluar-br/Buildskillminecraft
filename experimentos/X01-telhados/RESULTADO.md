# X01 — Telhados

**Pergunta**: como se comportam sete telhados sobre a mesma caixa de pedra 9×7 (paredes de 4)? **Script**: `experimento.py`. **Imagens**: `imagens/montagem.png`, `suave.png`, `par1.png`, `laterais.png`.

| Telhado | Blocos do telhado | Resultado (render) |
|---|---|---|
| a. duas águas 1:1 (`telhado_x`) | 131 | Silhueta clássica, forte; ângulo de 45° |
| b. duas águas 1:2 (`telhado_suave_x`) | 155 | Inclinação baixa e longa, aspecto de casa rural/escandinava; **funciona** depois de fechar as empenas |
| c. quatro águas (`tenda`) | 99 | Silhueta compacta, estável |
| d. mansarda (3 fileiras íngremes + tampa plana) | 99 | Lê como "chapéu" de telhado francês; tampa plana ainda aparece como retângulo |
| e1. abóbada de berço, só blocos, raio 4 | 216 | **Falhou**: parece uma caixa com cantos chanfrados, não uma curva |
| e2. mesma, com escadas de suavização | 234 | Idem: a escada não salva um raio tão pequeno |
| f. pagode, 2 beirais + cantos levantados | 275 | Silhueta mais rica e reconhecível; custa 2,1× o 4 águas |
| g. plano com platibanda e friso | 113 | Estilo moderno/industrial lê bem; precisa de platibanda para não parecer "tampa" |

## Método novo validado
`Molde.telhado_suave_x(x1,x2,z1,z2,y,escada,empena,beiral,beiral_x)` (em `ferramentas/construcao/moldes.py`): da borda para dentro alterna **escada (nível k)** e **laje inferior (nível k+1)** com um bloco de enchimento sob a laje; empenas fechadas por coluna. Inclinação ≈ 1 bloco de subida a cada 2 colunas.

## Conclusões (TESTADO por render)
1. 1:1 e 1:2 são duas "linguagens": 1:1 = casa europeia íngreme/chalé; 1:2 = casa baixa, galpão, rural.
2. Curva só lê com raio grande (ver X03). Em prédios pequenos, prefira telhado inclinado a abóbada.
3. Beiral largo + forro de laje invertida + canto levantado (f) é a maneira mais barata de ganhar identidade asiática.

## Falhas / limites
- O fechamento da empena do 1:2 só ficou correto depois de calcular o enchimento por coluna (primeira tentativa deixou buracos).
- Telhado de madeira renderiza só em cor de textura; o render não mostra telha de cobre/ardósia real.
- Não testado andando: sótão, goteira, acesso à chaminé.
