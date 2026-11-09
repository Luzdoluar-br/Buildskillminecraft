# Composição, hierarquia e silhueta

> Status: rascunho de biblioteca | Confiança: média (conceitos de Ching confirmados; limiares numéricos são [INT]) | Última revisão: 2026-11-09

## Resumo
- Um edifício legível tem UM ponto de ênfase, 3-5 volumes com um dominante e uma silhueta reconhecível em preto sobre branco.
- Ching: algo é hierárquico quando é "unicamente visível" por tamanho excepcional, forma única ou localização estratégica.
- Os testes abaixo são observáveis no render; limiares numéricos são heurísticas próprias, não normas.

## Conceito
Composição = organização de volumes, vãos e materiais para guiar o olhar. Hierarquia = diferença deliberada de importância. Massing = arranjo dos volumes. Silhueta = contorno do conjunto contra o céu. Ritmo = recorrência padronizada. Simetria/assimetria = equilíbrio por espelho ou por compensação de massas (A1_fundamentos, W8, Wikipedia).

## Características / regras

### Hierarquia (Ching, cap. 7, LI por trechos) [DOC]
- Meios de ênfase: (1) tamanho excepcional, (2) forma única, (3) localização estratégica (fim de eixo, centro de organização simétrica, deslocado em primeiro plano).
- "Quando tudo é enfatizado, nada é enfatizado"; acentos secundários são permitidos.
- Pode ser hierarquia por ser MENOR em cenário bem definido.
- Simetria pode ser local/parcial para responder ao sítio.

### Sullivan e coroamento [DOC]
Base, corpo e coroa por função, sem razão numérica (1:3:1 é refutado). Corpo = pavimentos idênticos; base mais generosa com a entrada marcada; coroa com massa fechada. Tradução [INT]: corpo com >= 3 repetições exatas.

### Testes observáveis (A1_r2 sec. 5; limiares = [INT])
| Tema | Teste | Passa se |
|---|---|---|
| Hierarquia | Render de longe; apontar "o edifício principal" em 1 s | Não há hesitação entre dois |
| Hierarquia | Contar elementos > 1,5x a altura média | 1 landmark ok; 3+ competem |
| Massing | Render em cor lisa por volume | 3-5 volumes, 1 dominante (>= 40% da planta ou altura); 1 caixa ou > 6 parecidos = falha |
| Silhueta | Preto sobre branco, 40-60 blocos, sem textura | Ainda lê como casa/castelo/igreja; >= 3 níveis de altura |
| Ritmo | Contar travées | >= 3 iguais com erro 0 e 1 quebra deliberada (porta/balcão) |
| Simetria | Espelhar a imagem | Formal: coincide 100% (1 bloco de diferença = erro) |
| Assimetria | Somar massa dos dois lados | Dentro de ~60/40 (limiar [INT]) |
| Equilíbrio | Render cinza e desfocado, peso escuro E x D | Não passa de ~65/35 sem compensação [INT] |

### Resultados dos experimentos [TESTADO]
- X01 (telhados): o telhado define a silhueta. 1:1 lê como casa europeia íngreme; 1:2 como casa baixa/galpão/rural; quatro águas é compacto e estável; pagode (275 blocos, 2,1x o 4 águas) tem a silhueta mais rica; plano exige platibanda para não parecer "tampa".
- X02 (fachadas): ritmo e ênfase vêm de contrafortes (gótica), lajes salientes e montantes a cada 3 (moderna), recessos fundos (brutalista).
- X03 (curvas): torre menor que diâmetro ~15 não vira círculo na silhueta; use octógono. Cúpula com lajes suaviza o contorno a partir de raio 8 (+24% de blocos).

## Como construir no Bedrock
1. Escolha o dominante primeiro: o volume mais alto ou mais largo, 40% ou mais. Os outros subordinados. [INT]
2. Dê ao dominante UM meio de ênfase de Ching (altura, forma de telhado distinta ou posição de fim de eixo). [INT sobre DOC]
3. Ritmo: travée de 3-5 blocos, 3+ repetições, entrada como quebra no eixo. [INT]
4. Silhueta: varie 3+ alturas de cumeeira/platibanda; evite topo reto de 1 linha. Teste preto sobre branco. [INT; teste NÃO TESTADO como procedimento]
5. Simétrico: confira espelhando coordenadas; assimétrico: compense massa com altura ou com volume do outro lado. [INT]
6. Torre: base com entrada marcada + N pavimentos idênticos + coroa fechada com beiral/cornija. [INT sobre DOC Sullivan]

## Combina com
- [escala-e-proporcao.md](escala-e-proporcao.md)
- [profundidade-contraste-transicoes.md](profundidade-contraste-transicoes.md)
- [../tecnicas/telhados-e-beirais.md](../tecnicas/telhados-e-beirais.md)
- [../tecnicas/paredes-estrutura-e-ritmo.md](../tecnicas/paredes-estrutura-e-ritmo.md)
- [../experimentos/X01-telhados/RESULTADO.md](../experimentos/X01-telhados/RESULTADO.md)
- [../experimentos/X03-curvas-e-diagonais/RESULTADO.md](../experimentos/X03-curvas-e-diagonais/RESULTADO.md)

## Erros comuns
- Dois marcos do mesmo tamanho disputando a atenção.
- Caixa única sem volumes (massing falho).
- Espaçamento irregular casual; repetição sem nenhuma quebra.
- Simetria "quase": 1 bloco de erro parece engano.
- Telhado plano sem platibanda (X01).
- Usar razão 1:3:1 ou razão áurea como regra.

## Limitações e dúvidas
- Todos os limiares (1,5x, 40%, 60/40, 65/35) são [INT] sem fonte.
- Os testes de silhueta e de espelho não foram aplicados em construção real da biblioteca.
- Ching lido só no cap. 7 (cópia no archive.org); notas de curso etown/CUNY não abriram.
- Nada foi visto no jogo; render por raycast valida forma, não cor.

## Fontes e evidências
- A1_r2: Ching, Architecture: Form, Space & Order, cap. 7 (LI, trechos, archive.org); Sullivan, Lippincott's 1896 (LI, archive.org).
- A1_fundamentos: Wikipedia (simetria, ritmo/baias, hierarquia, landmark); só busca em parte.
- Experimentos X01, X02, X03 (render + métrica).
