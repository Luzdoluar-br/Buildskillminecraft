# Registro de bugs e erros (LEIA ANTES DE CONSTRUIR)

Regra do dono do projeto: **todo bug ou erro descoberto deve ser anotado aqui**, com causa e correção, para não se repetir e para que outras IAs, sem o contexto da conversa, consigam trabalhar. Entradas novas no topo. Nunca apagar entradas antigas.

Formato: **Sintoma** → **Causa** → **Correção** → **Como evitar / checar**.

---

## 2026-11-09 — Missão de estudo autônomo (biblioteca geral)

### E-38 · Fatos refutados na pesquisa quase viraram texto
- Chartres 38 m, Beauvais 1248, Akashi 1995, razão 1:3:1, "vitral" no manifesto solarpunk, `waxed_copper_block` vinham das pesquisas. Auditoria por grep nos documentos: só aparecem como "refutado". **Evitar**: lista de refutados em `limitacoes-e-duvidas.md` seção D.

### E-37 · IDs "de memória" errados ao redigir documentos
- Redatores escreveram `bricks`, `chain`, `jack_o_lantern`, `stained_glass_pane` (genérico), `oak_fence_gate`, `waxed_copper_block`, `stone_slab`: nenhum existe. Corretos: `brick_block`, `iron_chain`, `lit_pumpkin`, `<cor>_stained_glass_pane`, `fence_gate`, `waxed_copper`, `normal_stone_slab`. **Evitar**: conferir em `referencia/blocos-bedrock.md`; rodar `ferramentas/verificar_biblioteca.py`.

### E-36 · Cabo diagonal de cerca não se liga (X05)
- Cercas conectam só por **face**; um cabo que muda de altura com células em diagonal fica quebrado. **Correção**: preencher o degrau vertical em cada passo. Registrado em `experimentos/X05-vertical-vaos-terreno/RESULTADO.md`.

### E-35 · Métrica ruim não vira conclusão; bugs nos próprios experimentos (X03, X04)
- "Erro de circularidade" do X03 era ≤ 0,5 por construção e não discriminava: trocada por **maior trecho reto**. No X04 o "chão" estava em y=0 e a casa começava em y=1 (tudo "flutuava"), e as paredes tinham 7 de altura com telhado em y=9 (1 bloco de vão). A **métrica de flutuantes** revelou o segundo bug. **Regra**: validar a métrica com um controle (casa intacta deve dar ≈ 0) antes de comparar variantes.

### E-34 · ID de memória errado: `stone_slab` não existe (X02)
- A auditoria nova (E-01) acusou na hora. O ID correto é `normal_stone_slab` (e `normal_stone_stairs`). **Regra**: nunca digitar ID de memória; procurar em `referencia/blocos-bedrock.md` (`grep`).

### E-33 · Lista de IDs "oficial" estava desatualizada (atlas do Creator Tools)
- O atlas usado antes tinha 1.187 IDs; a lista oficial da Mojang (`bedrock-samples` v1.26.60.5) tem **1.466**, incluindo `black_concrete_stairs` que o dono já usava: o validador antigo daria falso erro. **Correção**: fonte única = `referencia/fonte/mojang-blocks.json`; `blocos_validos.txt` e `estados_validos.json` são gerados dela (`ferramentas/gerar_referencia_blocos.py`). **Fonte primária > cópia derivada.**

### E-32 · Estados inválidos passam sem aviso (E-31 da auditoria)
- Estados que não existem para um bloco (ex.: `facing_direction` em defumador, `wood_type` em cerca) o jogo ignora ou converte sem avisar. A auditoria agora valida **cada estado e valor** contra `estados_validos.json` (oficial). Rodada contra a vila inteira: 0 estados inválidos (confirmação independente).

## 2026-11-09 — Aula 02 (Vila Pedra-Musgo)
Descobertos pelo dono ao entrar no jogo (primeiro teste real) e confirmados lendo o LevelDB do mundo.

### E-32 · O mundo salvo só mostra as edições do dono depois que o JOGO grava
- Ao ler o LevelDB, as correções recentes dele (ex.: a escada refeita da tela 19) **não apareciam**: o jogo só grava no disco ao salvar/sair do mundo. Só 4 alterações antigas estavam no arquivo.
- **Como fazer**: pedir ao dono para **sair do mundo (ou fechar o jogo)** antes de eu copiar o `db`; sem isso, aprender pelos prints e perguntar o que for ambíguo.

### E-31 · Ambientes inacessíveis (andares e torres sem escada) — DECIDIDO pelo dono: (a) escada interna
- Eram inacessíveis: mirante da casa de chá, andar de cima da torreta e campanário da torre-relógio do Salão. **O dono escolheu escada interna** para todos.
- **Implementação** (`aulas/aula-02/codigo/casas.py`: `lance()` e `espiral()`):
  - **Casa de chá**: lance reto de 7 degraus junto à parede leste, de `(9,2,9)` até `(9,8,3)`, que sai no terraço sobre o beiral (o forro e o piso do terraço são abertos sobre os degraus); guarda-corpo de cerca do lado de fora do poço; **porta do mirante** na parede norte (`porta_dir`, frente para o terraço), sem janela colada à porta.
  - **Torre-relógio do Salão**: caracol de 14 degraus no poço 3x3 até o piso do campanário (y=14).
  - **Torreta da casa de pedra**: arco de passagem entre o corpo e a torreta (2 de altura + verga de escada invertida dos dois lados) e caracol de 10 degraus até o sótão (y=10).
- **Lições de projeto**:
  1. Caracol 3x3 = anel de 8 células; cada célula recebe um degrau a cada 8 de altura; **a direção de cada degrau aponta para a próxima célula do anel**.
  2. O primeiro degrau não pode ficar nas células da porta/passagem: escolher o início do anel para que essas células só recebam degrau acima de y=3.
  3. Para chegar a um andar, abrir o piso/forro **só onde há degraus** (2 blocos de cabeça); o último degrau fica no nível do piso e à sua frente tem de haver piso sólido.
  4. Plano de forro/telhado atravessado por escada: limpar as células de cabeça, nunca o plano inteiro.
- **Auditoria**: E-29 agora confere 5 lances (chalé, casa de pedra, chá, torre, torreta): 36 degraus, cabeça livre e piso à frente do último. **Não testado andando no jogo**: pedir ao dono para confirmar se dá para subir.

### E-30 · Produtos "flutuando" meio bloco acima do balcão das barracas (print do dono)
- **Causa**: balcão em laje inferior (`bottom`) em `y=1`; os produtos (feno, abóbora, melancia) em `y=2` ficam meio bloco acima da laje = vão.
- **Correção aplicada**: balcão em bloco inteiro (`spruce_planks`) nas 4 barracas.
- **Regra**: item sobre laje precisa estar em laje `top` ou sobre bloco inteiro; senão sobra meia altura de vão. Vale para qualquer mobília sobre laje.

### E-29 · Escada interna curta e estantes sobre a escada (casa de pedra) — prints do dono (tela 17: "blocos sem sentido"; telas 18/19: "escadas incoerentes")
- **Sintoma**: degraus de pedra soltos junto ao teto, estantes misturadas com os degraus; a escada não chegava ao andar.
- **Causa**: o andar de cima fica 4 blocos acima do térreo, mas montei só **3 degraus**; o 4º degrau (no nível do piso) faltava, então sobrava um pulo de 1 bloco. Além disso as estantes ocupavam as mesmas células da escada.
- **Regra de escada interna**: nº de degraus = altura entre pisos (piso de cima a 4 → 4 degraus; o último fica NO nível do piso); abertura no piso sobre os degraus (3 blocos); 2 blocos livres de altura; nada na trajetória (móveis, estantes); degraus sempre na mesma direção, sem blocos soltos nos lados. Ver `tecnicas/escadas-internas.md`.
- **Correção aplicada**: casa de pedra com 4 degraus (o 4º em `(12,4,5)` no nível do piso), estantes movidas para x 10..11, tapete fora da escada.
- **Auditoria**: E-29 confere, para cada lance registrado em `ESCADAS` (`base.py`), degraus na direção certa, 2 blocos de cabeça livre e piso à frente do último degrau. Testado: um lance falso de 5 degraus é reprovado (a regra pega o erro antigo).

### E-28 · Termo técnico sem explicar ("mísula") e padrão do canto
- O dono perguntou o que era "mísula": **explicar em palavras simples** (suporte em degrau embaixo da viga). Evitar jargão com o dono.
- Ele também esclareceu que o canto mostrado como exemplo vale para TODOS os cantos: quando ele mostrar 1 exemplo, **o padrão é para tudo**; perguntar só o que for realmente ambíguo e depois aplicar em todas as construções (C-2).
- Cuidado de implementação: a coluna de canto só deve ser colocada **depois** de varandas/alpendres/forros (ou checar se o espaço está livre), senão eles sobrescrevem a lanterna e deixam uma ponta de viga solta (acontecido no alpendre do hortelão).

### E-27 · PROCESSO: registrar aprendizados no git NA HORA (cobrança repetida do dono)
- O foco do trabalho é **ensinar a IA e registrar**: tudo o que o dono corrige, mostra em print ou pede vira registro no git no mesmo turno (erro, causa, correção, técnica). Não deixar acumular.
- Checklist ao fim de cada rodada: `erros-e-licoes.md` + `aulas/aula-02/correcoes-do-dono.md` + `tecnicas/` + código + `git push` + confirmar com `git ls-remote`.

### E-26 · PROCESSO: consultar `referencia/` antes de usar qualquer bloco (pedido do dono)
- O dono pediu um arquivo com **todos os blocos e IDs** para evitar IDs inventados (E-01, E-20). Criado: `referencia/blocos-bedrock.md` (+ `.csv`), 1187 IDs com nome em inglês e os estados que o jogo gravou; `referencia/estados-e-rotacao.md` (rotação e equivalências Java→Bedrock). Gerador: `ferramentas/gerar_referencia_blocos.py`.
- **Regra**: bloco que não está na tabela não existe. Estado de rotação: ver `estados-e-rotacao.md`.

### E-25 · Para-raios apontando para baixo
- `lightning_rod` sem estado vira `facing_direction=0` (para baixo). **Correção**: `facing_direction=1`. Auditoria E-25.

### E-24 · Máquinas e blocos orientados com estado errado ou virados para a parede
- **Causa**: usei `facing_direction` em forno/defumador/alto-forno (o jogo converte para `minecraft:cardinal_direction`) e a mesma direção em casas viradas ao contrário (flip); o alto-forno do Salão olhava para o norte.
- **Correção**: `Molde.maq()` usa `minecraft:cardinal_direction` e gira com a casa; frente sempre para o interior. Abóboras das barracas viradas para o cliente.
- **Auditoria**: E-24 (frente não pode dar em parede; máquina sem orientação).

### E-23 · "Cantos errados": ponta de tronco (anéis) exposta no canto (feedback do dono, prints ERRADO/CERTO)
- **Sintoma**: no canto das paredes aparecia um bloco liso/escuro com a ponta do tronco virada para o lado; o dono corrigiu à mão (canto vertical contínuo).
- **Causa**: a viga horizontal (`pillar_axis=x/z`) cobria também a célula do canto; na lateral perpendicular aparece a ponta. O mesmo no pórtico do chalé.
- **Correção**: `anel()` coloca **troncos verticais (`y`) nos 4 cantos**; extremidades da viga do pórtico viram verticais. Auditoria E-23: tronco *stripped* horizontal com a ponta no ar = erro.
- **Regra**: canto de parede = tronco vertical contínuo; vigas encostam nele. Ponta de viga exposta só como detalhe intencional (ver `tecnicas/cantos-e-vigas.md`).

### E-22 · Poste de luz: modelo melhorado pelo dono (aprendizado, lido no mundo)
- **Evidência** (blocos lidos no mundo, coluna do poste em x -73, z 24): `stone_brick_wall` (base) → 2 × `spruce_fence` → `spruce_slab` (laje de topo, parte de baixo) ; braço = **1 `spruce_stairs`** (`weirdo_direction` = direção para fora, a ponta alta fica longe do poste) no nível da laje; **lanterna pendurada** logo abaixo da escada; **`spruce_slab` invertida (`vertical_half=top`)** do lado oposto ao braço, na altura da última cerca (contrapeso).
- **Antes (meu)**: base de parede + cerca + 2 tábuas de braço. **Depois**: braço curto em escada com gancho elevado, laje de capa e contrapeso (mais silhueta).
- **Implementação**: `poste_h()` em `vila.py`. Detalhes em `tecnicas/postes-de-luz.md`.

### E-21 · Blocos flutuantes (feedback do dono, com prints)
- **Sintoma**: barril/cerca flutuando no meio do salão da casa de chá; peças da fonte e do píer sem apoio.
- **Causas**: (a) mobília da casa de chá colocada em `y=3` quando o piso (carpete) está em `y=2`: tudo 1 bloco acima; (b) copa da fonte (paredes) sem apoio, só encostada no lado; (c) tábuas e postes do píer sobre a água sem estacas.
- **Correção**: mobília em `y=2`; mísulas (escadas invertidas) sob a copa da fonte; estacas até o fundo da lagoa e postes começando dentro da água.
- **Como evitar**: regra E-21 em `auditoria.py`: mobília, plantas, cercas, lanternas no chão, portas, carpetes e culturas exigem bloco sólido embaixo (água não vale). **Interior: sempre medir o nível do piso (plataforma + carpete) antes de colocar móveis.**

### E-20 · "Erros de textura": ID de bloco que NÃO existe (feedback do dono)
- **Sintoma**: cubos marrons manchados no chão (textura de erro).
- **Causa**: `rooted_dirt` não existe no Bedrock (o ID é `dirt_with_roots`); `lily_pad` também não está na lista atual (`waterlily`). O jogo grava o nome errado e mostra bloco de erro, sem aviso.
- **Correção**: nomes trocados. **A checagem E-01 agora valida TODOS os nomes contra a lista oficial de 1187 IDs do Bedrock** (`aulas/aula-02/codigo/blocos_validos.txt`, extraída do atlas do Minecraft Creator Tools), em vez de uma lista curta de suspeitos.
- **Como evitar**: nunca inventar/lembrar ID de memória; qualquer bloco novo precisa estar em `blocos_validos.txt`. Cuidado com nomes Java (ex.: `rooted_dirt`, `lily_pad`, `grass_path` vs `dirt_path`) — conferir sempre na lista.

### E-19 · Degrau alto (>1 bloco) na rede de caminhos
- **Causa**: ondulação aleatória da rua + colinas de borda criavam desníveis de 2-3 blocos em cima do caminho.
- **Correção**: pontas da rua retas; auditoria checa |dH| <= 1 entre células vizinhas de caminho/praça.

### E-18 · Telhado/beiral "solto" na casa de chá (validação de peças soltas)
- **Causa**: anéis de escadas do beiral não encostavam no plano de forro (só tocavam na diagonal). **Correção**: planos de forro cobrem toda a área do beiral (0..12 e 2..10). **Dica**: o aviso `PECA SOLTA` da `Cena.validar()` nunca é ignorável.

### E-17 · Bancos virados ao contrário
- `weirdo_direction` da escada = direção em que ela SOBE (as costas ficam desse lado). Banco voltado para a fonte tem as costas para o lado oposto à fonte. Eu tinha invertido.

### E-16 · Estruturas fundidas (barraca + poço) e árvore cortada ao meio, flutuando (feedback do dono)
- **Sintoma**: barraca e poço se sobrepunham; árvore com a copa cortada e meio solta.
- **Causa**: cada objeto era colocado sem checar se o espaço já estava ocupado; objetos posteriores sobrescreviam blocos de anteriores.
- **Correção**: **registro de ocupação** em `vila.py` (`RES`, `reservar()`, `livre()`): todo objeto reserva sua pegada (casas com varanda e margem, barracas com o toldo, poço, fonte, píer, poste, árvore); se colidir, a posição é recusada (`CONFLITOS`) e a auditoria reprova.
- **Como evitar**: nunca colocar nada sem `livre()`/`reservar()`. Árvores só nascem onde a copa não invade casas.

### E-15 · Praça apertada: sem caminho AO REDOR da fonte (feedback do dono)
- **Sintoma**: a fonte (raio ~5) ocupava quase toda a praça e as barracas encostavam nela; ninguém passava de um lado para o outro.
- **Regra do dono**: **toda construção no meio da rua precisa de caminho ao redor** (fonte, poço, barraca, etc.).
- **Correção**: fonte menor (bacia r=3,9) + anel pavimentado livre de 3,1 blocos de largura (até r=7,0) marcado por faixa de pedra polida; praça ampliada (x 13..47, z 25..40); barracas nos cantos (anel de 2 blocos); poço e banco fora do anel; rua reta dentro da praça.
- **Como evitar**: `OBJETOS` em `vila.py` + regra E-15 em `auditoria.py` (nada sólido nos anéis).

### E-14 · Poste de luz em cima de barraca e poste em cima de poste (feedback do dono)
- **Causa**: `Cena.poste()`/`Cena.arvore()` da biblioteca usam `chao()` = **bloco mais alto da coluna**; se havia toldo, telhado ou outro poste, o objeto nascia em cima.
- **Correção**: `poste_h()` e `arvore_h()` usam a altura do TERRENO (`H`) e só constroem em célula livre; o braço do poste pode pender sobre a rua (aéreo), nunca sobre objetos.
- **Como evitar**: nunca usar `chao()` para objetos de chão. A auditoria reprova poste/árvore cuja base não é terreno.

### E-13 · PROCESSO: cada correção do dono vira regra para TODAS as estruturas
- **Regra do dono**: quando ele corrige algo em uma estrutura, eu devo procurar o mesmo erro (e erros parecidos) nas outras, sem esperar que ele corrija uma por uma, e registrar aqui tudo o que ele pedir.
- **Como fazer**: (1) ler no mundo o que ele mudou (comparar o LevelDB com o gerado, ferramentas da Aula 01); (2) registrar a correção em `aulas/aula-02/correcoes-do-dono.md`; (3) transformar em checagem em `aulas/aula-02/codigo/auditoria.py`; (4) rodar a auditoria em todas as estruturas e corrigir; (5) só então exportar. Meta da auditoria: 0 problemas.
- **Corolário (pedido do dono)**: quando ele aponta um bug em UMA estrutura, tratar como CLASSE de erro: procurar e corrigir em TODAS e também outros bugs gerais, sem esperar ser apontado. Ao corrigir, ampliar a auditoria.
- **Cuidado**: o dono edita o mundo à mão. `/function vila/colocar` **sobrescreve** as edições dele; nunca pedir para rodar sem avisar.

### E-12 · Itens bloqueando entradas e caminhos (feedback do dono)
- **Sintoma**: degraus "barrando" a porta do Salão; o dono removeu.
- **Causa**: os bancos da praça (`FX±8, FZ±8`) caíam no eixo da porta do Salão e **em cima da rua** (leste/oeste) e da trilha da lagoa. Além disso, degraus de entrada de chalé e casa de pedra ficavam na frente da porta, e os degraus da casa de chá subiam de costas para a porta.
- **Correção**: bancos reposicionados fora de rua/eixos; degraus removidos onde a entrada é rente ao chão; degraus da casa de chá viram `NORTE` (sobem em direção à porta); postes de rua saem da trilha.
- **Como evitar**: `auditoria.py` checa 1 bloco livre na frente e atrás de cada porta (em `y` e `y+1`) e obstáculos sólidos em ruas/praça.

### E-11 · Porta "desconexa da parede" (feedback do dono)
- **Sintoma**: a porta da torre do Salão tinha vidros nas laterais (sidelights) e escadas invertidas dos lados; parecia colada na parede.
- **Causa**: eu desenhei "entrada em arco" com vidro e escadas laterais, o que quebra a continuidade da pedra.
- **Correção (padrão do dono, lido no mundo)**: batentes em `stone_bricks` maciço nos dois lados, 3 blocos de altura; só 1 escada invertida (`stone_brick_stairs`, `upside_down_bit=1`, `weirdo_direction=3`) acima da porta como verga; nenhum degrau na frente. Detalhes em `aulas/aula-02/correcoes-do-dono.md`.
- **Como evitar**: a auditoria reprova vidro ou vazio ao lado da porta (batente).

### E-10 · Vão vazio acima da folha da porta (feedback do dono, 2ª rodada)
- **Sintoma**: em algumas portas (hortelão, casa de chá, varanda do chalé) sobrava um buraco de 1 bloco acima da porta; o dono pediu uma escada no material da parede.
- **Causa**: abri a parede com 3 de altura (`limpar(..., y..y+2)`) mas a porta só tem 2; o terceiro bloco ficou vazio (ou só com vidraça).
- **Correção**: função `vergas_das_portas()` em `vila.py`: para toda porta com `y+2` vazio, coloca escada invertida (`upside_down_bit=1`) no material da parede vizinha (mapeamento material -> escada). Na varanda do chalé a vidraça virou `spruce_stairs` invertida.
- **Como evitar**: abertura de porta = exatamente 2 de altura + verga (escada invertida/laje/tronco) no `y+2`. Checar `y+2` de toda porta no script de portas.
- **Limite**: o raycaster de teste não desenha portas, então isso só foi conferido pelos dados do `.mcstructure`, não por imagem.

### E-01 · Blocos "terrosos/estranhos" espalhados (≈202 blocos)
- **Sintoma**: cubos marrons manchados acima das portas, forros e soleiras; um cubo de pedra onde devia haver laje.
- **Causa**: o helper `Molde.sl(x,y,z,nome)` montava `minecraft:<nome>` sem o sufixo, e chamei com `"spruce"`, `"dark_oak"`, `"pale_oak"`, `"stone_brick"`. IDs inexistentes: o Bedrock **aceita e grava** o nome errado e mostra bloco desconhecido. Nenhum erro aparece na geração nem no render.
- **Correção**: `sl()` agora acrescenta `_slab` quando falta.
- **Como evitar**: depois de gerar, listar os nomes únicos da paleta do `.mcstructure` e conferir um a um. Nomes de madeira/pedra sem sufixo (`spruce`, `stone_brick`, `oak`) são sempre suspeitos.

### E-02 · Portas bloqueadas
- **Causa A (Salão)**: eu colocava piso interno da torre em `y=1`, na mesma altura da porta; só sobrava 1 bloco livre. O piso fica em `y=0`.
- **Causa B (chalé)**: a porta da varanda estava 1 bloco acima do piso do andar (`y=6` em vez de `5`) e havia cerca exatamente na frente dela.
- **Correção**: piso removido; porta ao nível do piso; deck da varanda rente ao piso; guarda-corpo só nas pontas.
- **Como evitar**: para cada porta, conferir que a célula na frente e atrás, em `y` e `y+1`, não é sólida (script de checagem de portas no relatório da Aula 02).

### E-03 · Porta "sem parte de cima"
- **Estado**: no arquivo e no mundo as 6 portas tinham metade de cima (`upper_block_bit=1`). **Causa não confirmada**; hipótese: a porta da varanda do chalé ficava deslocada/obstruída (E-02). Reavaliar no jogo após a correção. Se persistir, anotar aqui com coordenadas.

### E-04 · Camas sumiram
- **Causa**: o Bedrock descarta o bloco `bed` ao carregar uma estrutura que não traz a entidade de bloco (cor).
- **Correção**: cama simulada com `white_wool` (travesseiro) + `light_blue_wool`.
- **Como evitar**: blocos com entidade de bloco (cama, placa, baú, banner, vaso com planta) exigem `block_position_data`; sem isso, trocar por equivalente simples.

### E-05 · Lanternas penduradas sumiram
- **Causa**: `lantern[hanging=true]` sem bloco acima é removida pelo jogo.
- **Correção**: função `corrigir_lanternas()` apoia no chão ou remove. Validar sempre.

### E-06 · Água vazando da lagoa/horta
- **Causa**: o anel de margem da lagoa (H=0) sobrepôs a borda da horta (H=1); a água da horta, ao nível do chão, escorreu pelo terreno mais baixo.
- **Correção**: lagoa deslocada para x=34 e horta reduzida (x 15..22).
- **Como evitar**: nunca deixar água ao nível do solo encostada em terreno mais baixo; áreas de água precisam de borda sólida.

### E-07 · O render não mostra a verdade de tudo
- Folhas, cobre, ardósia e lã colorida aparecem cinza; IDs inválidos não aparecem como erro. **Imagem boa ≠ construção correta**: sempre ler o `.mcstructure` e o mundo (ver ferramentas da Aula 01).

### E-08 · Exportador da biblioteca estoura com muitos blocos
- `Cena.construir()` falha com `IndexError` acima de ~77 estados distintos. Usar `aulas/aula-02/codigo/exportar.py`.

### E-09 · Telhados: empena cruzada falhou
- A tentativa de empena cruzada no chalé gerou buracos e blocos soltos; removida. Telhados mistos (2 materiais) funcionam; mais que isso vira ruído.

---

## 2026-11-09 — Aula 01
- **Autoria**: salvar uma estrutura não significa modificá-la (a 15 estava idêntica ao original).
- **Ruído do jogo** que NÃO é edição humana: `grass_block→dirt`, estados `corner` de escadas, `update_bit`/`persistent_bit`, fluxo de água. Ver `aulas/aula-01/metodo-e-autoria.md`.
- **Chunks ausentes** no mundo (estruturas 30, 39, 40, 47–50): não avaliáveis.

---

## Ferramentas e armadilhas do ambiente (Windows)
- Mundo Bedrock local: `%APPDATA%\Minecraft Bedrock\Users\<id>\games\com.mojang\minecraftWorlds\<pasta>`; add-on embutido vai em `<mundo>\behavior_packs\<nome>` + `world_behavior_packs.json` (**fazer backup antes**).
- `Expand-Archive` não aceita `.mcpack`; copiar da pasta-fonte ou renomear para `.zip`.
- O LevelDB do Bedrock usa compressão zlib raw: bibliotecas comuns (plyvel) não leem; usar `ferramentas/ldb.py`.
- `amulet-core` não compila no ambiente; o leitor próprio resolve.
- Feche o Minecraft antes de copiar/ler o mundo (o jogo grava o `db` ao sair).

---

## 2026-11-11 — Armaduras, vitrines e Hunter (servidor VULPUS)
- **Armor stand tem a família `mob`** no jogo. Todo filtro "apaga bicho" (lobby, Arcade) apagava as vitrines do spawn. Sempre excluir `minecraft:armor_stand` de filtros por família (medido no servidor local: `hasTypeFamily("mob") == true`).
- **Armor stand NÃO expõe `minecraft:equippable` ao script** (medido): `getComponent` devolve `undefined` para qualquer peça. Vestir só por `replaceitem entity @s slot.armor.<head|chest|legs|feet> 0 <item> 1` rodado como o próprio boneco; checar com `testfor @e[type=armor_stand,hasitem={item=...,location=slot.armor.head}]`.
- **Armadura "pisca" (z-fighting)**: duas faces que olham para o mesmo lado a menos de ~0,07 uma da outra e se sobrepondo brigam. Vale entre ossos e peças DIFERENTES (braço x tronco, calça x bota), entre cubos GIRADOS e contra a camada extra da skin do jogador (jaqueta/mangas/calças/chapéu, 0,25 maior que o corpo). Conferir sempre em 3D com caixas orientadas; amostrar a face perde faixas finas, então caixas de mesma orientação se conferem por intervalos exatos.
- **Moldura nativa + pele**: a pele no mesmo plano do fundo da moldura do jogo briga com ele; afastar 0,12 px.
- **Dimensão customizada nova** (`registerCustomDimension` no `startup`) funciona no BDS 1.26 e permite construir por script (Pincel) sem erro de bloco; validar blocos/estados com `@minecraft/vanilla-data` antes (ids de 1.26: `iron_chain`, `light_block_<n>`; `minecraft:chain` não existe).
- **O servidor só tem 64 blocos de simulação** (`tick-distance 4`): arena grande precisa de ticking area por comando (`tickingarea add`), senão o monstro longe de jogadores não anda.
- **Item de poder de minigame**: não usar `ender_eye` (é arremessado e consumido); bússola e pena não têm ação de uso.

## 2026-11-11 — Hunter, lobby (Pavilhão da Floresta Silenciosa)
### E-39 · Cabines e portal construídos de costas (frente e fundo trocados)
- **Erro**: as cabines do lobby ficaram com a parede de vitral voltada para o centro (a entrada) e a parte aberta virada para a parede; o portal de saída também saiu virado. Eu só olhei renders de fora e li a planta, nunca vi a cena do ponto de entrada.
- **Como evitar**: depois de construir, renderizar/fotografar **do ponto onde o jogador chega** (`camera.olhos`) e testar por código que o caminho do jogador até cada ponto de interação está livre (teste automático por cabine). Definir o parâmetro de orientação de forma que o nome diga o que é ("lado do fundo", não "lado").
### E-40 · Cerca baixa deixa o jogador em meio bloco e quebra a mecânica
- **Erro**: guarda-corpo de cerca em volta do pad deixava jogadores pararem em cima/no canto, fora da área de detecção; o minigame não começava e ninguém entendia por quê.
- **Correção (do dono)**: slab sobre a cerca. **Regra**: em volta de pontos de interação do jogo, nunca deixar superfícies de meio bloco ou de 1,5 bloco onde se possa ficar em pé; testar caminhando de verdade.
### E-41 · Lobby montado de novo apagaria a edição do dono
- **Risco**: o sistema reconstrói o lobby pela estrutura. O dono já tinha ajustado o lobby no jogo. **Regra**: depois que o dono edita uma construção, o mundo é a fonte da verdade; só recolocar a estrutura com aviso explícito (e a versão do lobby no código sobe só quando o dono pedir).

### E-42 · Ignorei o aviso de "peça solta": galhos de árvore ligados só pela quina viraram "tronco voando"
- **Erro**: o export do lobby do Hunter avisou "PEÇA SOLTA: dark_oak_log" (galhos da árvore central) e eu entreguei assim. Os galhos subiam em diagonal e só se tocavam pela quina; no jogo parecem flutuar. O bulbo de luz e a corrente também pendiam no ar, longe do galho. A skill já dizia que peça solta é erro.
- **Correção**: caminho em Manhattan (anda em x, depois em z, depois sobe), sempre face com face; o bulbo pende do FIM do galho por corrente contínua. Teste automático: `validar()` sem nenhum aviso de peça solta (`tests/test_addon_hunter.py`). Para o mundo já editado: comando idempotente que só acrescenta os blocos que faltam.
### E-43 · `oca()` deixou a parede da frente do corredor fechando a passagem
- **Erro**: o corredor de entrada era uma caixa oca; ao limpar o interior esqueci a face da frente (z0 - 2), que ficou como parede entre o arco e o véu de volta. O jogador via só uma parede de pedra. Eu só tinha olhado renders de fora.
- **Correção**: limpar o interior incluindo as faces de contato com a abertura; teste que caminha o eixo da porta (do véu ao salão) e exige ar na altura da pessoa. Regra: **todo caminho de entrada/saída precisa de um teste de passagem**, não só de olhar.

### E-44 · Render controller com `uv_anim` desloca a textura de TUDO que ele desenha (bandeira da VULPUS)
- **Quase-erro (pego antes de subir)**: ao pôr a franja do pano dentro do osso do pano (desenhado pelo controller Kitsune, que troca de quadro com `uv_anim` offset 1/4), a franja teria piscado/sumido: o deslocamento de UV vale para todas as faces de todos os ossos do controller, e a região da franja só existia uma vez na textura.
- **Regra**: tudo que um controller com `uv_anim` desenha precisa ter as N cópias (uma por quadro) na textura, na mesma coluna. Peças sem quadros vão para um osso próprio, desenhado por outro controller (sem `uv_anim`), mesmo sendo filho do osso animado (herda a rotação, não o controller).
- **Material emissivo [NV]**: `entity_emissive_alpha` lê o alpha como brilho (quanto menor, mais brilha; 0 = recorte); `entity_emissive` não recorta. Usei alpha 140 para brilho parcial (acima do corte de 50%) e 24 para brilho cheio na orbe. Conferir no jogo à noite e anotar aqui o resultado.

### E-45 · Botão que "não faz nada" no Discord: rótulo de campo do modal com mais de 45 caracteres (Kiza, "Abrir corte")
- **Sintoma**: o botão Abrir corte dos painéis da equipe não respondia. Os testes passavam, porque ninguém instanciava o modal com a API real.
- **Causa**: `TextInput(label="Infração: xray, dupe, cheat, conduta, abuso, outra")` tinha 50 caracteres. O Discord limita o rótulo a 45 e recusa o modal inteiro (erro 50035), então o clique falha em silêncio para o usuário.
- **Regra**: rótulo de TextInput até 45 caracteres e placeholder até 100. A lista de opções vai no `placeholder`, não no rótulo.
- **Prevenção**: teste que percorre todos os `TextInput(...)` dos cogs (AST) e confere os limites; assim um modal novo não repete o erro.
