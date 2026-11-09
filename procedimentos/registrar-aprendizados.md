# Como registrar aprendizados (e por que isso é o foco do projeto)

> Status: regra do dono, repetida várias vezes ("o foco é te ensinar e registrar") | Última revisão: 2026-11-09

## Resumo
Registrar **na hora**, no mesmo turno em que se aprende, e publicar (`git push`). Uma IA sem contexto só conhece o que está neste repositório. Conhecimento não registrado é conhecimento perdido.

## O que vai onde
| O que aprendi | Onde registrar |
|---|---|
| Um erro (meu ou do ambiente) | `../erros-e-licoes.md`: **E-nn · título** com *sintoma → causa → correção → como evitar*; novas entradas no topo da seção da data; nunca apagar entradas antigas |
| Uma correção ou preferência do dono | `../aulas/aula-02/correcoes-do-dono.md` (tabela: observação → o que fiz) + a técnica generalizada em `../tecnicas/` |
| Uma técnica de construção | `../tecnicas/<assunto>.md` (ou, se for universal, `../fundamentos/`, `../estilos/`, `../estruturas/`, `../materiais/`, `../ambientacao/`) |
| Um teste/protótipo | `../experimentos/XNN-nome/` com `experimento.py`, `imagens/`, `RESULTADO.md` (inclua as **falhas**) |
| Um fato técnico do Bedrock | `../referencia/` (com fonte e grau: OFICIAL / WIKI / TESTADO / NV) |
| Algo que não sei ou que depende do dono | `../limitacoes-e-duvidas.md` (pendência) e siga trabalhando |
| Uma regra nova de validação | `ferramentas/construcao/auditoria_geral.py` + caso negativo de teste + linha no `checklist-de-validacao.md` |

## Rótulos de confiança (usar em todo documento)
**[DOC]** documentado por terceiros (dizer a fonte e se a página foi aberta ou só vista em busca) · **[INT]** interpretação própria · **[NV]** não verificado · **[TESTADO Xnn]** testado em experimento · **[TESTADO-AULA02]** aprendido construindo/corrigindo a Vila · **[NÃO TESTADO]** tradução para Minecraft sem teste · **[TESTADO no jogo]** só quando o dono confirmou no jogo.
Nunca registrar suposição como fato. Quando uma fonte refutar algo registrado, **corrija e anote a correção** (não apague o histórico).

## Checklist ao fim de cada rodada
1. Escrevi/atualizei: erro, técnica, experimento, referência.
2. Atualizei o índice (`../README.md`) se criei arquivo novo.
3. Conferi duplicação: se a informação já existe, linkar em vez de copiar.
4. `git add -A && git commit && git push` e conferi com `git ls-remote origin HEAD` (se o push não for confirmado, **não declarar publicado**).
5. Se o dono editou algo: li o mundo, registrei o que aprendi e **generalizei** para todas as construções (E-13).

## Como evitar problemas de shell ao registrar
- Heredocs com aspas e `'''` dentro de comandos Bash falharam (E-27 lembra); prefira **escrever o arquivo com a ferramenta de escrita** e executar um script curto.
- No Windows, o `Expand-Archive` não aceita `.mcpack`; copie da pasta de origem.
