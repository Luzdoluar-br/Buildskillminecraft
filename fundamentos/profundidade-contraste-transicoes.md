# Profundidade, contraste e transições

> Status: rascunho de biblioteca | Confiança: média-alta para profundidade (X02); média para o resto ([INT]) | Última revisão: 2026-11-09

## Resumo
- Fachada de 1 plano parece papelão; 3 a 4 planos leem como arquitetura (X02). O recurso mais barato é mover uma faixa 1 bloco para frente ou para dentro.
- Contraste (material, cor, textura, escala) separa estrutura de preenchimento; a quantidade de materiais principais deve ser pequena.
- Transições entre materiais seguem função (Sullivan), sem razão numérica; cantos e juntas são onde o desenho mais denuncia pressa.

## Conceito
Profundidade = camadas de planos que criam sombra e escala. Espaço negativo = vazio ou parede calma que dá descanso às zonas ricas (conceito de "ma" japonês, Wikipedia Negative space) [DOC]. Contraste = diferença perceptível entre elementos adjacentes. Transição = ponto onde muda material ou volume.

## Características / regras

### Profundidade (X02, TESTADO)
| Fachada | Planos | O que cria profundidade |
|---|---|---|
| Controle liso | 1 | nada: "papelão" |
| Moderna | 3 | pilotis, lajes salientes, montantes a cada 3 |
| Medieval, brutalista, gótica | 4 | avanço de andar, recessos de 3 de profundidade, contrafortes |
| Japonesa | 7 (conta 2 níveis de beiral) | plataforma, engawa, shoji recuado, beiral largo |
Teste [INT, A1_r2]: em corte/planta contar >= 3 planos (parede, +1 pilar, -1 janela) e beiral/sacada >= 1; no pôr do sol deve haver sombra visível.

### Espaço negativo [INT sobre DOC]
Reservar áreas calmas contíguas de ~3x3 blocos ao lado das zonas ricas; se todo bloco 3x3 tem >= 2 tipos de bloco/prop, há ruído (limiar [INT]). Parede lisa ao lado de uma entrada rica valoriza a entrada.

### Contraste [INT; teste de A1_r2]
- Material: tronco descascado (estrutura) contra tábua/concreto (preenchimento) [TESTADO-AULA02, ver materiais-e-paletas.md T2].
- Cor/valor: moldura x parede devem diferir em escala de cinza; no máximo ~4 materiais principais (heurística de guias de Minecraft, só busca).
- Textura: padrão forte (tijolo, tronco) só onde se quer atenção; na massa principal use pedras neutras próximas.
- Escala: elemento que foge ao módulo vira ênfase (Ching: tamanho excepcional) [DOC].

### Transições base/corpo/coroa [DOC + INT]
- Sullivan: divisão por função, sem proporção (1:3:1 refutado). Base mais aberta e generosa, corpo repetido, coroa com peso.
- Teste [INT]: no render de elevação, as mudanças de material caem em linhas horizontais claras (base, cornija); nenhuma em diagonal ou no meio de parede sem linha; base visualmente mais pesada/escura que o topo.
- Troque de material ou de plano em linha reta, na altura de uma laje, cornija ou soleira.

### Cantos e juntas
- Canto de madeira: tronco vertical contínuo (C-1); canto do dono com tronco + escada + lanterna pendurada + ponta de viga é padrão confirmado (C-2) [TESTADO-AULA02].
- Porta: batentes no material da parede, abertura exata de 2 + verga em escada invertida, entrada livre (P-1 a P-4).
- Pilar/quina distinto da parede torna o canto legível [INT].

## Como construir no Bedrock
1. Da fachada lisa, mova uma faixa 1 bloco: avanço do andar superior, recesso das janelas, laje saliente por piso. [TESTADO X02]
2. Janela com moldura: soleira em laje, verga em escada invertida, ombreiras em pedra polida. [TESTADO X02]
3. Recesso profundo (3) em concreto: lê como brutalista com baixo custo. [TESTADO X02]
4. Contrafortes salientes com capa em escada a cada travée para ritmo e sombra (gótico). [TESTADO X02]
5. Cornija: 1 fileira de escadas/lajes invertidas projetando 1 bloco no topo; base: 1-2 fiadas de pedra mais escura. [INT, NÃO TESTADO como receita]
6. Luz baixa (pôr do sol) para conferir sombras; o render noturno ajuda a ver a profundidade. [INT]
7. Persianas (alçapões abertos) funcionam, mas a direção do alçapão aberto precisa conferir no jogo. [X02 NÃO VALIDADO no jogo]

## Combina com
- [escala-e-proporcao.md](escala-e-proporcao.md)
- [composicao-hierarquia-silhueta.md](composicao-hierarquia-silhueta.md)
- [../tecnicas/cantos-e-vigas.md](../tecnicas/cantos-e-vigas.md)
- [../tecnicas/portas-e-entradas.md](../tecnicas/portas-e-entradas.md)
- [../materiais/paletas-e-combinacoes.md](../materiais/paletas-e-combinacoes.md)

## Erros comuns
- Janelas rente à parede e telhado sem beiral.
- Recuos de meio bloco que somem sem sombra forte [INT, A1_fundamentos].
- Mudança de material em diagonal ou sem linha de apoio.
- Detalhar com blocos diferentes em vez de mover planos (X02: o plano é mais barato).
- Ponta de tronco exposta sem lanterna/escada no canto (erro C-1).
- Ruído: padrões fortes em toda parte, sem parede calma.

## Limitações e dúvidas
- Limiares (3x3, 4 materiais, 3 planos) são [INT]; só "3 a 4 planos" tem base experimental, e é render, não jogo.
- Contagem japonesa de 7 planos inclui os dois níveis de beiral (artefato da métrica).
- Percepção de sombra no jogo (AO, luz) não foi testada.

## Fontes e evidências
- X02 (render + métrica); aula 02 via `tecnicas/cantos-e-vigas.md` e `portas-e-entradas.md`.
- A1_r2: Sullivan (LI), Ching (LI), testes 8-11 (limiares [INT]); Wikipedia Negative space (A1_fundamentos, aberta).
- "Máximo ~4 materiais": só busca.
