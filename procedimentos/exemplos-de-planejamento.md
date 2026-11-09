# Exemplos de planejamento (PLANOS, não construções)

> Status: **planos NÃO executados**. Servem para treinar o uso do método (`metodo-de-projeto.md`) e da matriz (`combinar-estilos-e-especialidades.md`). Tudo que é decisão de design é [INT]; IDs de bloco foram conferidos em `../referencia/blocos-bedrock.md`; técnicas ainda sem teste estão marcadas [NÃO TESTADO] | Última revisão: 2026-11-09

Formato de cada plano: interpretação → estilo → paleta → escala → planta → hierarquia → técnicas-chave → riscos → como validar.

## 1. Cidade futurista construída sobre um pântano
- **Interpretação**: cidade (médio/grande) elevada acima da água; história: "cidade que sobe para fugir da inundação, ligada por passarelas". Premissas: sem terreno firme; bioma = pântano.
- **Estilo**: dominante futurista/contemporâneo; secundário solarpunk (vegetação sobre estruturas); engenharia de palafitas/pilotis. Ver `../estilos/futurista-cyberpunk-solarpunk.md`, `../estruturas/vilas-e-cidades.md`, `../ambientacao/terreno-biomas-agua.md`.
- **Paleta** [INT]: dominante `white_concrete`/`light_gray_concrete` + vidro `tinted_glass`; apoio `waxed_copper`/`waxed_weathered_copper`; acento `sea_lantern`; água/vegetação: `mud`, `mangrove_log`, `mangrove_roots`, `muddy_mangrove_roots`, `moss_block`, `waterlily`, `vine`.
- **Escala**: 150×150 de planta; torres de 30–60; módulos ≤ 64×384×64 [NÃO TESTADO como cidade; torre de 60 foi X05-A, 4.887 blocos].
- **Planta**: marco central (torre alta), anel de passarelas, "bairros" em plataformas ligadas por pontes pênseis (X05-C funciona; cabo diagonal de cerca exige preencher o degrau).
- **Hierarquia**: 1 torre-marco; plataformas secundárias baixas; vegetação como moldura.
- **Técnicas**: pilotis fundos até o leito (ver X05-E: fundação/estaca), torre com recuos e cortina de vidro (X05-A), registro de ocupação.
- **Riscos**: água com vazamento (E-06), pilotis flutuando (E-21), muitas luzes sem lógica.
- **Validação**: auditoria com `Contexto`; renders aéreos e de nível de rua; checar acesso entre plataformas.

## 2. Casa antiga abandonada no topo de um prédio destruído (Backrooms Vermelhas)
- **Interpretação**: estrutura sobre estrutura + liminal + ruína. Premissa: "Backrooms Vermelhas" = estética liminal com dominância vermelha [INT; a origem da estética está em `../estilos/pos-apocaliptico-subterraneo-liminal.md`].
- **Estilo**: casa vitoriana/enxaimel em ruína sobre prédio brutalista ou moderno em colapso; liminal na parte interna do prédio (corredores repetidos).
- **Paleta** [INT]: prédio: `gray_concrete`, `light_gray_concrete`, `red_concrete`, `red_terracotta`; casa: `spruce_planks`, `cracked_stone_bricks`, `mossy_stone_bricks`; luz: `redstone_lamp`/`shroomlight` baixos.
- **Escala**: prédio 24×24×40 colapsado de um lado; casa 12×9 no topo.
- **Hierarquia**: contraste de escala e de época: a casa pequena e "intacta" contra o prédio quebrado.
- **Técnicas**: `ferramentas/construcao/ruina.py` (impacto no lado do colapso, abandono na casa) + remoção de flutuantes (X04); a casa precisa de apoio plausível (pilar/viga visível).
- **Riscos**: casa flutuando sobre vazio (E-21); dano aleatório (X04: 106 flutuantes).
- **Validação**: métrica de blocos flutuantes ≈ 0; render de baixo para ver o apoio.

## 3. Estação ferroviária subterrânea em cidade industrial
- **Interpretação**: caixa subterrânea + abóbada + tecido industrial acima. Ver `../estruturas/estacoes-e-ferrovias.md`, `../estruturas/subterraneas-e-suspensas.md`.
- **Paleta** [INT]: `deepslate_bricks`, `cobbled_deepslate`, `polished_blackstone_bricks`, ferro `iron_bars`, trilhos `rail`/`golden_rail`; luz indireta `sea_lantern` escondida.
- **Escala**: plataformas de 5–8 de largura, 30–40 de comprimento, abóbada de 9–11 de vão (dados de A4 são [INT]).
- **Planta**: saguão → escadas → plataforma → trilhos; passagem inferior.
- **Técnicas**: abóbada com escadas [NÃO TESTADO; arco pequeno falhou no X05-B: usar vão ≥ 14]; luz no pé da abóbada; fluxo de pessoas legível.
- **Riscos**: luz = nascimento de monstros (sem teste no jogo), arco que lê como retângulo.

## 4. Vila medieval em montanha nevada
- **Interpretação**: vila (médio) em encosta com neve. Ver `../estilos/medieval-europeu-e-fantasia.md`, `../estruturas/vilas-e-cidades.md`.
- **Paleta** [INT]: `stone_bricks`, `spruce_planks`, `dark_oak_planks`, telhados `spruce_stairs`; neve `snow`, `powder_snow` (cuidado: é um bloco de armadilha), `packed_ice` para riachos congelados.
- **Escala/planta**: patamares com muros de arrimo (X05-E funciona), rua principal serpenteando, praça com anel livre (TESTADO-AULA02), 1 construção principal (salão ou igreja) no ponto mais alto.
- **Técnicas**: telhados 1:1 íngremes para neve (X01-a), acúmulo de neve nas águas protegidas [INT/NV], enxaimel com avanço (X02-F1).
- **Riscos**: biomas de neve sem fonte confirmada ([NV]); `snow` precisa de apoio sólido.

## 5. Cidade cyberpunk vertical
- **Interpretação**: densidade + camadas + letreiros. Ver `../estilos/futurista-cyberpunk-solarpunk.md`, `../estruturas/arranha-ceus.md`, `../estruturas/pontes-e-viadutos.md`.
- **Paleta** [INT]: base suja `gray_concrete`, `black_concrete`, `blackstone`; neon `cyan_concrete`, `magenta_concrete`, `sea_lantern`, `glowstone`; vidro `tinted_glass`; metais `iron_bars`, `iron_chain`.
- **Escala/planta**: quarteirões estreitos (ruas de 5–9 entre fachadas de 20–60, enclosure forte [INT]), torres com recuos, pontes pênseis entre torres (X05-C), passarelas em balanço (X05-D).
- **Técnicas**: letreiros como painéis de concreto colorido com recesso (X02-F2), luz focal quente/fria, camadas sobrepostas.
- **Riscos**: excesso de neon sem hierarquia; luz uniforme.

## 6. Templo esquecido dentro de uma floresta gigantesca
- **Interpretação**: templo (eixo + procissão) + ruína + vegetação gigante. Ver `../estruturas/templos-e-monumentos.md`, `../ambientacao/ruinas-e-narrativa.md`.
- **Estilo**: tradição a escolher (chinês, japonês, gótico ou outra); ruína por abandono (água/tempo).
- **Paleta** [INT]: `mossy_stone_bricks`, `cracked_stone_bricks`, `stone_bricks`, `moss_block`, `vine`, `hanging_roots`, `azalea_leaves`, `flowering_azalea`.
- **Técnicas**: `ruina.abandono` (topos de muro em dentes, musgo, vegetação nos topos, X04), árvores gigantes com raízes (TESTADO-AULA02 para árvores comuns; gigantes [NÃO TESTADO]), luz filtrada.
- **Riscos**: árvore gigante invadindo a estrutura: usar o registro de ocupação para decidir onde a árvore "venceu" a pedra.

## 7. Instalação científica abandonada no fundo do oceano
- **Interpretação**: laboratório pressurizado + ruína + oceano. Ver `../estruturas/instalacoes-industriais-e-laboratorios.md` ([NV] submarino).
- **Paleta** [INT]: `prismarine`, `dark_prismarine`, `prismarine_bricks`, `waxed_oxidized_copper`/`oxidized_copper`, `iron_bars`, vidro `tinted_glass`; vida `kelp`, `seagrass`, `sea_pickle`, `tube_coral_block`.
- **Técnicas**: cúpulas (raio ≥ 8 para ler como curva, X03), tubos de ligação, luz como narrativa (poucas luzes ainda acesas), entulho e vegetação marinha.
- **Riscos**: água com vazamento entre ambientes secos e alagados (E-06); estruturas dentro d'água exigem planejamento de bolsas de ar [NÃO TESTADO].

## 8. Cidade construída sobre ruínas de uma civilização antiga
- **Interpretação**: palimpsesto: fundações antigas visíveis sob construções novas.
- **Técnicas**: camadas no tempo (fase 1 ruína com paleta A, fase 2 construção com paleta B e alinhamento diferente), "estrutura sobre estrutura": manter arcos e fundações antigas à vista (ver `../ambientacao/ruinas-e-narrativa.md`), usar `ruina.abandono` na camada antiga e construção limpa na nova.
- **Riscos**: mistura aleatória de materiais (erro comum); acessos que ignoram a camada antiga.

## Como usar estes planos
Eles são **hipóteses**. Ao executar um deles: rodar o método, abrir um experimento isolado para a parte mais arriscada, registrar o resultado (inclusive falhas) em `../experimentos/` e atualizar este documento marcando o que passou a ser TESTADO.
