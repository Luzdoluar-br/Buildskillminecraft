# X05 — Estrutura vertical, vãos, balanço e terreno inclinado

**Script**: `experimento.py`. **Imagens**: `imagens/montagem.png` (torre, ponte em arcos, ponte pênsil, balanço, casa em encosta).

| Peça | Blocos | Resultado |
|---|---|---|
| A. torre 18×18, 12 pavimentos de 4, 2 recuos, cortina de vidro com montantes a cada 3, pilotis no térreo, casa de máquinas e antena | 4.887 | **Funciona**: lê como arranha-céu (base → corpo → coroa; recuos dão silhueta). Pavimento de 4 (1 laje + 3 livres) foi o módulo usado |
| B. ponte em 3 arcos de vão 10 | 812 | **FALHOU**: o resultado parece um muro de pedra sobre pilares com vãos retangulares, não arcos. Arco de vão 10 com flecha ≤ 5 não lê; precisaria de vão e flecha maiores e de escadas no intradorso (NÃO TESTADO) |
| C. ponte pênsil, vão 36, torres de 14, cabo parabólico, pendurais de corrente | 483 | **Funciona** e é barata; descoberta: **cabo diagonal feito de cerca não se liga** (cercas só conectam por face): é preciso preencher o degrau vertical de cada passo |
| D. balanço de concreto de 12 sobre massa de ancoragem, com contravento diagonal de grades de ferro | 772 | Lê bem; o contravento "justifica" o balanço visualmente (interpretação), não calculado |
| E. casa em encosta 1:2 com fundação escalonada de pedra | 540 | Funciona como "casa encaixada na encosta" (patamar nivelado + muro de arrimo); pilotis de madeira NÃO foi testado (código removido para não afirmar o que não fiz) |

## Achados técnicos (viraram regras da ferramenta)
- A auditoria E-21 (apoio) acusou os cabos da ponte pênsil como "flutuando". Não era erro de construção: era elemento suspenso intencional. A regra foi **refinada**: cerca no ar só é aceita se o grupo de cercas toca em algo sólido (cabo preso à torre passa; cerca solta não). Esse refinamento expôs o cabo diagonal quebrado (acima).
- Custo em blocos escala com a **casca**, não com o volume: a torre de 60 de altura custou ~4,9 mil blocos (só fachada + lajes).

## Falhas / limites
- Arco de ponte: falha registrada, nenhuma técnica validada.
- Torre: não testei iluminação noturna nem interior; vidro azul aparece aproximado.
- Balanço: não há cálculo estrutural; a aceitação visual vem do contravento (INTERPRETAÇÃO PRÓPRIA).
