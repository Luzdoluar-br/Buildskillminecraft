# Build Skill Minecraft (VULPUS) — biblioteca de arquitetura para Minecraft Bedrock

## 1. O que é
Biblioteca de conhecimento (texto + ferramentas Python + experimentos) para **planejar, construir, validar e corrigir** qualquer estrutura em **Minecraft Bedrock Edition**, a partir de um pedido livre (ex.: "cidade futurista em um pântano"). Não é um catálogo de um estilo só.

## 2. Objetivo
Uma IA **sem contexto prévio** deve conseguir: ler este README → entender → planejar um pedido novo → executar → validar → corrigir → registrar o que aprendeu.

## 3. Leitura obrigatória antes de construir (nesta ordem)
1. `erros-e-licoes.md` — erros já cometidos (não repetir).
2. `limitacoes-e-duvidas.md` — o que NÃO está provado.
3. `procedimentos/metodo-de-projeto.md` — método em 13 passos (flexível).
4. `referencia/blocos-bedrock.md` — **consultar para QUALQUER bloco** (1466 IDs oficiais + estados).
5. `procedimentos/checklist-de-validacao.md` — antes de entregar.
6. `aulas/aula-02/correcoes-do-dono.md` — preferências do dono (valem para TODAS as estruturas).

## 4. Como planejar um pedido novo
1. Interpretar o pedido (tipo + estilo + ambiente + narrativa); declarar premissas.
2. Escolher estilo(s) em `estilos/`, tipo em `estruturas/`, ambiente em `ambientacao/`; cruzar com `procedimentos/combinar-estilos-e-especialidades.md`.
3. Fundamentos de escala/composição: `fundamentos/`. Paleta: `materiais/` + `tecnicas/materiais-e-paletas.md`.
4. Ver planos de exemplo (não executados) em `procedimentos/exemplos-de-planejamento.md`.
5. Parte arriscada → experimento isolado em `experimentos/` antes (resultados X01–X05 já existem, inclusive falhas).

## 5. Como escolher blocos e usar as ferramentas
- ID e estados: `referencia/blocos-bedrock.md` / `.csv`; rotação: `referencia/estados-e-rotacao.md`.
- Código: `ferramentas/README.md` (pacote `construcao/`: `Cena`, `Molde`, terreno, registro de ocupação, exportador `.mcstructure`, auditoria geral, ruína). Exemplo mínimo: `ferramentas/construcao/exemplos/exemplo_minimo.py`.
- Cuidado: importar o pacote `construcao` **deste repositório** antes de qualquer outro de mesmo nome.
- Formato do arquivo e limites do Bedrock: `referencia/mcstructure-formato.md`, `referencia/bedrock-comandos-e-limites.md`. Entrega no jogo: `procedimentos/entrega-no-jogo.md`.

## 6. Como validar
`procedimentos/checklist-de-validacao.md` + `ferramentas/construcao/auditoria_geral.py` (regras E-01…E-31) + render (`camera.py`). Só entregar com auditoria zerada. QA da biblioteca: `python ferramentas/verificar_biblioteca.py` (links e IDs).

## 7. Como registrar aprendizados
`procedimentos/registrar-aprendizados.md`. Resumo: erro → `erros-e-licoes.md`; correção do dono → `aulas/aula-02/correcoes-do-dono.md` + técnica em `tecnicas/`; teste → `experimentos/`; dúvida → `limitacoes-e-duvidas.md`. Commit + push e conferir com `git ls-remote origin HEAD`.

## 8. Regras de ouro (condensadas)
- Nada flutuando; apoio visível. Nada colocado sem checar ocupação. Objeto no meio de rua = anel livre para andar.
- Portas completas (2 blocos), entrada livre; escadas coerentes com a parede; cantos e troncos com eixo correto.
- Uma correção do dono vale para **todas** as estruturas. Nunca sobrescrever edição do dono sem avisar.
- Explicar jargão em palavras simples. Respostas curtas e objetivas.

## 9. Rótulos de confiança (obrigatórios)
**[DOC]** documentado por terceiros (com fonte) · **[INT]** interpretação própria · **[NV]** não verificado · **[TESTADO Xnn]** testado em experimento · **[TESTADO-AULA02]** aprendido na Vila · **[NÃO TESTADO]** tradução sem teste · **[TESTADO no jogo]** só com confirmação do dono. Evidência ≠ interpretação ≠ hipótese. Nada testado andando no jogo ainda, salvo confirmação explícita.

## 10. Índice completo
| Área | Documentos |
|---|---|
| **fundamentos/** | `escala-e-proporcao`, `composicao-hierarquia-silhueta`, `profundidade-contraste-transicoes` |
| **estilos/** | `medieval-europeu-e-fantasia`, `gotico`, `japones-tradicional`, `chines-tradicional`, `vitoriano`, `industrial-e-brutalista`, `modernista-e-contemporaneo`, `futurista-cyberpunk-solarpunk`, `pos-apocaliptico-subterraneo-liminal` |
| **estruturas/** | `casas-e-edificios-residenciais`, `arranha-ceus`, `castelos-e-fortalezas`, `templos-e-monumentos`, `pontes-e-viadutos`, `estacoes-e-ferrovias`, `instalacoes-industriais-e-laboratorios`, `subterraneas-e-suspensas`, `vilas-e-cidades` |
| **materiais/** | `paletas-e-combinacoes`, `envelhecimento-e-deterioracao`, `vidro-luz-e-metal` |
| **ambientacao/** | `terreno-biomas-agua`, `iluminacao-e-atmosfera`, `ruinas-e-narrativa` |
| **tecnicas/** (do dono, Aulas 01/02) | `cantos-e-vigas`, `escadas-internas`, `interiores-e-mobiliario`, `materiais-e-paletas`, `paredes-estrutura-e-ritmo`, `portas-e-entradas`, `postes-de-luz`, `praca-e-espaco-publico`, `telhados-e-beirais`, `terreno-caminhos-e-pracas`, `vegetacao-e-ambientacao` |
| **procedimentos/** | `metodo-de-projeto`, `combinar-estilos-e-especialidades`, `checklist-de-validacao`, `registrar-aprendizados`, `entrega-no-jogo`, `exemplos-de-planejamento` |
| **experimentos/** | `README` (tabela), X01 telhados, X02 fachadas/janelas, X03 curvas/diagonais, X04 ruínas com causa, X05 vertical/vãos/terreno |
| **referencia/** | `blocos-bedrock` (.md/.csv), `estados-e-rotacao`, `mcstructure-formato`, `bedrock-comandos-e-limites`, `fonte/mojang-blocks.json` |
| **ferramentas/** | `README`, pacote `construcao/`, `gerar_referencia_blocos.py`, `verificar_biblioteca.py`, leitores de mundo (`ldb.py`, `world.py`, …) |
| **aulas/** | `aula-01/` (50 estruturas analisadas, método), `aula-02/` (Vila Pedra-Musgo: relatório, código, imagens, correções do dono) |
| **raiz** | `erros-e-licoes.md`, `limitacoes-e-duvidas.md` |

Registros antigos nunca são apagados; correções entram como nova seção datada.
