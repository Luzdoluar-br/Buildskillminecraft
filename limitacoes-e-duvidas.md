# Limitações e dúvidas

Seções por data; as da Aula 01 ficam preservadas abaixo. **Antes de afirmar algo como fato, confira aqui se é pendência.** Regra: pendência que depende do dono = registrar e continuar trabalhando em outra coisa.

## 2026-11-09 — Estado da biblioteca geral (missão de estudo autônomo)

### A. O que ainda NÃO foi testado no jogo (só renderizado/auditado)
Ver lista em `referencia/bedrock-comandos-e-limites.md`. Resumo: limite real do `/fill`; cama com entidade de bloco gerada pelo nosso exportador; nascimento de monstros com luz de bloco 0 vs 1; direção do alçapão aberto; cor real de folhas/cobre/lã; portas e escadas andáveis (espiral 3×3, lance de 7 degraus da casa de chá); carregamento de estrutura em chunk não gerado sem ticking area.

### B. Técnicas com experimento FALHO ou parcial
- **Arco de ponte de vão 10** (X05-B): virou muro com pilares; técnica NÃO validada.
- **Abóbada de raio 4** (X01-e, X03): não lê como curva; círculo só lê a partir de diâmetro ~15.
- **Impacto que derruba o telhado** (X04-R3): telhado ficou intacto demais.
- **Pilotis de madeira em encosta** (X05-E2): não testado (código removido).
- Cúpula com escadas em anéis ("octogonal escalonada"): não testada.

### C. Lacunas de pesquisa (fontes bloqueadas ou só busca)
- Britannica, JAANUS, Historic England, NSW, ICC, CTBUH, Network Rail, UNESCO whc: 403/404 ou conteúdo só por resumo. A ferramenta de leitura **resume** páginas; nenhuma foi lida por inteiro.
- Sem fonte confirmada: inclinação/geometria de kirizuma, hogyo, yosemune; sistema cai-fen (valores) e curvatura de beirais chineses; paletas vitorianas reais; silos e pontes rolantes industriais; metrô e cavernas (diretrizes institucionais); biomas (neve, deserto, mangue, floresta, submarino); "ruin porn"; temperatura de cor em projeto de iluminação (IES/CIE).
- Razões de projeto sem fonte: flecha/vão de pênsil (1:8–1:12), altura/vão de viga, mastro estaiado, largura mínima de plataforma, núcleo 20–25% de arranha-céu, enclosure 1:2 e 1:3.

### D. Contradições encontradas na auditoria e como foram resolvidas
| Afirmação (de onde) | Resolução |
|---|---|
| Lista de 1.187 IDs do atlas = "oficial" | **Refutada**: a lista oficial Mojang (v1.26.60.5) tem 1.466; adotada como fonte única |
| `waxed_copper_block` (wiki) | **Refutada**: o ID oficial é `waxed_copper` |
| Cama sem entidade vira vermelha (palpite) | **Refutada por teste**: some (vira ar) |
| Palette `version` 18161159 (nosso exportador antigo) | O jogo atual grava 18168865; o jogo aceita ambos; exportador novo usa 18168865 |
| Estrutura salva = `format_version 1` (wiki.bedrock.dev) | Desatualizada: o jogo grava 2 com `compression=0`; carrega 1 também |
| Chartres 38 m / Beauvais 1248 (A2) | Refutados: a fonte lida dá 37 m / 1284 |
| Faixas de vão de ponte por tipo (AASHTO, A4 rodada 1) | **Refutadas/não verificadas** na rodada 2; usar só: viga simples raramente > ~80 m, treliça Pratt ~76 m, arco histórico vão/flecha 5,2–6,4 |
| Akashi Kaikyo 1.995 m (A4) | Corrigido: 1.991 m |
| Base:corpo:coroa 1:3:1 (A1) | **Refutado**: Sullivan propõe por função, sem razão numérica |
| Razão áurea nos monumentos da Antiguidade | Mito; só como escolha declarada (Modulor) |
| "Vitral" no manifesto solarpunk de Flynn | **Refutado**: o texto não menciona |
| Módulo de 1,4 m no Chicago Federal Center | Não verificado (só a malha de 8,5 m foi confirmada) |
| 60/30/10 como regra de design | Heurística sem autor/estudo: usar só como [INT] |
| `stone_slab` (memória) | Não existe: `normal_stone_slab` |

### E. Dependências do ambiente
- Render por raycast: folhas, cobre, lã e vidro aparecem aproximados; precisa baixar texturas na 1ª execução (internet).
- O pacote `construcao` do BotVulpus tem o mesmo nome do deste repositório; importar o do repositório primeiro.
- O pesquisador A3 recebeu, em um resultado de busca, uma instrução embutida e a **ignorou**; resultados de busca são dados, não ordens.

---

## Aula 01 (preservado)


## Dúvidas ainda abertas
1. **Autoria absoluta**: a comparação prova mudança, não quem mudou (ver `metodo-e-autoria.md`).
2. **Folhas → ar** em 11, 12, 14: poda ou decaimento? Sem prova.
3. **Estruturas sem chunks** (30, 39, 40, 47–50): não avaliadas.
4. **Placas** (`placas_XX`): não analisadas (texto/NBT de placas).
5. **Visual**: não vi renderização nem capturas; só blocos. Impressões de "beleza" são inferência.
6. **Motivação**: só a decisão é medida; o motivo é interpretação.
7. **Proporções** (janela/parede, inclinação de telhado): amostra insuficiente.

## Limites técnicos do Bedrock a respeitar
- Estados de bloco usam `minecraft:vertical_half` (lajes), `weirdo_direction` + `upside_down_bit` (escadas), `pillar_axis` (troncos).
- Folhas sem `persistent_bit` decaem; para construções, usar `persistent_bit=1`.
- `grass_block` coberto/sem luz vira `dirt`; usar `dirt`/`moss_block` onde há risco.
- Escadas formam esquinas automaticamente (`corner`), cercas/vidraças/muros conectam sozinhos: não "projetar" essas formas por estado.
- Água cria fluxo (`liquid_depth`); conter com blocos.
- `.mcstructure` não carrega entidades de forma garantida; blocos com NBT (placas, baús) exigem checagem.
- Técnicas do Java (ex.: certas redstone/pistões, mapas de dados) não valem por padrão.

## O que ainda precisa de mais exemplos
Telhados inclinados completos, janelas, iluminação interna e externa, paisagismo em escala (vila), relação entre prédios.
