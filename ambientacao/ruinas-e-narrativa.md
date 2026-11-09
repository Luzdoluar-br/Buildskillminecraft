# Ruínas, deterioração com causa e narrativa ambiental

> Status: rascunho validado por métrica e render (X04), sem teste no jogo | Confiança: média (mecanismos de falha: média-alta; receitas de inundação e reocupação: baixa) | Última revisão: 2026-11-09

## Resumo
- Ruína convincente = uma CAUSA escolhida, uma ORDEM de falha física, dano em GRADIENTE, entulho embaixo do que falta e vegetação onde há água.
- Dano aleatório deixou 106 blocos flutuantes e nenhuma história; causa + gradiente + remoção de flutuantes deixou 0-3 [TESTADO X04].
- A história se resume a 1 frase, 3-5 evidências coerentes e 1 ponto focal (Carson, Level Design Book).

## Conceito
**Princípio.** Alvenaria sem manutenção falha por mecanismos de água, gelo, raízes e perda de apoio; o olho lê a causa pelo padrão do dano. A ordem abaixo vem do PDF irlandês *Ruins: Conservation and Repair of Masonry Ruins* (Dept. Env., 2010) [DOC, aberta: só a seção 3 foi lida; o PDF inteiro não]:

| # | Mecanismo documentado | Efeito visível |
|---|---|---|
| 1 | Perda do telhado: alvenaria exposta absorve água | paredes manchadas, juntas lavadas |
| 2 | Topos de muro quebrados retêm chuva que desce pelo núcleo | topo irregular, reboco e rejunte soltos |
| 3 | Gelo-degelo (parede saturada + geada): erode argamassa, solta lascas (arenito, calcário, tijolo, terracota vulneráveis) | faces lascadas em placas |
| 4 | Raízes e hera abrem juntas; folhagem aumenta o efeito do vento; raízes no núcleo abaulam a face | vegetação nas juntas e topos |
| 5 | Perda de uma face expõe e derruba o núcleo (pedra miúda + argamassa) | buracos que atravessam a parede |
| 6 | Arcos perdem argamassa, achatam, perdem aduelas; janelas estreitas em série falham em cadeia | arcos com 1-2 peças faltando |
| 7 | Empenas altas e chaminés expostas balançam e caem com vento; colapso parcial pode ser súbito | empenas em dentes |
| 8 | Fundação enfraquecida causa grandes colapsos, muitas vezes atribuídos a "tempestade" | colapso de trechos inteiros |

A ordem numérica 1→8 foi organizada pela pesquisa a partir do texto (parafraseada), não é uma tabela do PDF.
Corrosão de armadura em concreto [DOC, icorr.org, aberta]: película alcalina (pH ~12,5) protege o aço; carbonatação (pH < 9) ou cloretos a quebram; a ferrugem ocupa mais volume e fissura o concreto. Lascamento (spalling) não aparece na página lida: extensão por inferência.
Incêndio [DOC parcial, PDF Ecclesiastical, aberto]: pisos e telhados de madeira queimam, paredes de tijolo/pedra resistem melhor, aço enverga. "Chaminés sobrevivem" e "parede sem piso/telhado cai ao vento" vêm só de busca [NV].

## Características / regras
**Causa -> sequência de alterações** (tradução Minecraft [INT], salvo onde marcado):

| Causa | Sequência | No código (`ruina.py`) |
|---|---|---|
| Abandono (tempo e água) | telhado/madeira alta -> portas e vidraças -> pisos -> topos e cantos de pedra -> vegetação | `abandono()` [TESTADO X04] |
| Impacto (explosão, guerra) | origem -> raio -> gradiente -> chamuscado -> entulho | `impacto()` [TESTADO X04] |
| Incêndio | toda a madeira some; pedra fica; fuligem acima das aberturas; chaminé em pé | `incendio()` [TESTADO X04] |
| Inundação [INT, sem código] | linha d'água constante nas paredes; entulho submerso; musgo na linha; mobília empilhada no piso alto | manual |
| Reocupação em décadas [INT, sem código] | fase 1 núcleo (paleta A) -> fase 2 anexo/andar extra (paleta B) e vãos tapados -> fase 3 remendos e estruturas leves sobre topos | manual |

Inspiração da reocupação: Kowloon [DOC, Wikipedia/Far Out/Metropolis, abertas]: origem em forte, crescimento sem plano, 2-3 para 6-7 andares nos anos 1960, até 13-14 andares (limite do aeroporto Kai Tak), becos de 1-2 m, construções sobre as antigas; 2,6 ha; ~33.000 hab. (1987). Alturas em metros: não informadas. Guia de registro da Historic England sobre fases: 403, [NV].

**Vegetação por sucessão e umidade.** [DOC, só busca: Historic England *Plants on Walls* 403, Suffolk WT]: algas e líquens, musgos, ervas e samambaias nas juntas, por fim lenhosas (hera, arbustos, árvores), as mais danosas. [INT] Estágios: jovem = musgo pontual e grama nas juntas; médio = vinhas, arbustos no entulho; velho = árvore dentro do recinto sem telhado. Densidade cai com a distância da água/solo e com a altura; máxima em arestas quebradas, topos e base úmida.

## Como construir no Bedrock
**Algoritmos de `ferramentas/construcao/ruina.py`** [TESTADO X04, só render + métrica]. Ordem de chamada de `abandono`: remove madeira e vidro, erode pedra, `limitar_balancos_de_madeira`, `remover_flutuantes`, `vegetar`.
1. Abandono, pedra: p(remover) = 0,55 x intensidade x alt^1,4 x (0,6 + 0,8 x exposição). alt = altura relativa; base quase intacta, topo em dentes.
2. Abandono, madeira alta/escadas/lajes: p = min(0,97; 0,45 + 0,6 x intensidade x (0,5 + 0,5 x exposição)); portas e alçapões 80%; madeira baixa 0,55 x intensidade. Vidro/vidraça: removido todo.
3. Pedra restante: `stone_bricks` vira `mossy_stone_bricks` (~musgo) ou `cracked_stone_bricks`; `cobblestone` vira `mossy_cobblestone`; mais musgo na base.
4. `remover_flutuantes`: agrupa blocos por vizinhança de face; o que não toca o chão sai; 35% vira entulho que cai até o primeiro apoio (nunca de madeira).
5. `limitar_balancos_de_madeira`: madeira a mais de 3 células de qualquer apoio de pedra é removida (evita cumeeira no ar).
6. `vegetar`: 25% x densidade dos topos recebem `short_grass`/`fern`/`moss_carpet` (30% desses com `moss_block` embaixo); no chão, 35% x densidade.
7. `impacto`: p(remover) = 1 - 0,8 x (d/raio)^1,6 dentro do raio; chamuscado (`blackstone`, `cracked_stone_bricks`, `polished_blackstone_bricks`) até 1,7 x raio; entulho em ~raio^2 x 1,2 pontos, gaussiano, até 3 blocos de altura.
8. `incendio`: remove madeira e vidraças; acima de cada vidraça removida, fuligem (`blackstone`, `polished_blackstone_bricks`) com p = 0,8 - 0,2 x dy, dy = 1..3; 12% da pedra vira rachada.
Receita manual de inundação [NÃO TESTADO]: (a) escolha a cota da água; (b) em TODAS as paredes, troque 1 faixa à cota por `mossy_stone_bricks`; (c) abaixo, entulho e `mud`; (d) no andar de cima, móveis empilhados; (e) mesmo nível em cômodos conectados. Ver E-06 em [terreno-biomas-agua.md](terreno-biomas-agua.md).
**Narrativa de Carson** [DOC, Game Developer, aberta]: 1 frase de história; 3-5 evidências (porta arrombada, marca de explosão, nível d'água marcado); 1 ponto focal com mais detalhe e luz; trilha de pistas até ele; menos detalhe no resto. Level Design Book [DOC, aberto]: sugerir evento passado em escala de cômodo, não eventos presentes.

## Combina com
[../materiais/envelhecimento-e-deterioracao.md](../materiais/envelhecimento-e-deterioracao.md) · [../estilos/pos-apocaliptico-subterraneo-liminal.md](../estilos/pos-apocaliptico-subterraneo-liminal.md) · [../fundamentos/composicao-hierarquia-silhueta.md](../fundamentos/composicao-hierarquia-silhueta.md) · [../experimentos/X04-ruinas-com-causa/RESULTADO.md](../experimentos/X04-ruinas-com-causa/RESULTADO.md) · [iluminacao-e-atmosfera.md](iluminacao-e-atmosfera.md) · [../tecnicas/vegetacao-e-ambientacao.md](../tecnicas/vegetacao-e-ambientacao.md)

## Erros comuns
- Remover blocos sem causa nem entulho (queijo suíço) [TESTADO X04].
- Telhado intacto com paredes destruídas, ou empena/chaminé alta intacta sobre parede arrasada (na documentação, empenas e chaminés caem primeiro).
- Madeira sobrevivendo à pedra; vegetação uniforme; árvore grande em ruína recém-abandonada.
- Pistas contraditórias; história sem ponto focal; reocupação com mistura de materiais sem lógica temporal [INT].

## Limitações e dúvidas
- Impacto não derruba o telhado quando só um trecho de parede cai: falta regra de "telhado sem apoio de um lado desmorona" [TESTADO X04, falha registrada].
- Resíduo de madeira alta na empena persiste; vegetação esparsa e não calibrada; sem comparação com fotos de ruínas reais.
- Inclinação de parede não existe em blocos: simular por degraus de queda [INT].
- Armadura exposta: bloco "ferrugem" não definido [NV]; candidatos como `weathered_copper`/`oxidized_copper` são ideia sem teste.
- Nada foi testado andando no jogo. Ruin porn/pátina (fotógrafos), estratigrafia e Historic England: [NV].

## Fontes e evidências
- Ruins: Conservation and Repair of Masonry Ruins (Irlanda, 2010): aberta, seção 3 via pdftotext.
- icorr.org (corrosão): aberta. Ecclesiastical (fogo): aberta. preventionweb: 403.
- Kowloon: Wikipedia, Far Out, Metropolis: abertas. Historic England (HEAG099, soft capping, plants on walls): 403/só busca.
- Don Carson (Game Developer): aberta. Level Design Book: aberta.
- Experimento X04 e `ruina.py`: lidos integralmente.
