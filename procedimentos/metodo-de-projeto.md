# Método de projeto (de um pedido livre a uma construção executável)

> Status: método PROPOSTO a partir da Vila (TESTADO-AULA02) e dos experimentos X01–X05; as fases de pesquisa de estilo ainda NÃO foram usadas em um projeto inédito completo | Confiança: média | Última revisão: 2026-11-09

## Resumo
Treze etapas, mas **não são obrigatórias em bloco**: o porte do pedido decide quais rodar e com que profundidade (tabela abaixo). Cada etapa produz um artefato escrito (ficha do projeto) para que outra sessão, sem contexto, possa continuar. Regra de ouro: **nada é entregue sem passar pela auditoria** (`ferramentas/construcao/auditoria_geral.py`) e sem registrar o que se aprendeu.

## Quanto planejamento cada pedido exige
| Porte | Exemplos | Etapas | Orçamento típico |
|---|---|---|---|
| Pequeno | casa, poste, ponte curta | 1, 3, 4, 5, 8, 9, 11, 13 (conceito em 2 linhas) | < 3 mil blocos |
| Médio | vila, templo, castelo, estação | todas, com 6 e 7 detalhadas | 20–60 mil blocos (a Vila Pedra-Musgo: 31 mil) |
| Grande | cidade, megaestrutura, cidade vertical | todas; 6 em camadas (ver `../estruturas/vilas-e-cidades.md`); dividir em módulos ≤ 64×384×64 | > 100 mil; construir por módulos e conferir cada um |
| Experimental / incomum | edifício "que desafia a gravidade", mistura de estilos, ruína narrativa | 1–2 longas; 8 com protótipo isolado (ver `../experimentos/`) antes do projeto | variável |

## As etapas
| # | Etapa | Pergunta-guia | Saída escrita | Onde consultar |
|---|---|---|---|---|
| 1 | Interpretar o pedido | Quem/onde/quando/estado (nova, velha, abandonada)? Escala? Função no jogo? | **premissas** assumidas (se faltar dado, assumir e registrar; perguntar só o que muda tudo) | `combinar-estilos-e-especialidades.md` |
| 2 | Conceito e identidade visual | Qual é a história em 1 frase? Quais 3 palavras definem o visual? | frase + 3 palavras + 3 referências | `../ambientacao/ruinas-e-narrativa.md` |
| 3 | Estilo | Qual linguagem domina e quais elementos de outra entram? | estilo dominante + até 2 secundários + regra de convivência | `../estilos/` |
| 4 | Paleta | 3 grupos (dominante, apoio, acento) e quais blocos exatos? | lista de IDs **conferidos** em `../referencia/blocos-bedrock.md` | `../materiais/paletas-e-combinacoes.md` |
| 5 | Escala e dimensões | Quantos blocos de frente/altura? Quantas estruturas? Dividir em módulos? | tabela de dimensões e orçamento de blocos | `../fundamentos/escala-e-proporcao.md`, `../referencia/bedrock-comandos-e-limites.md` |
| 6 | Distribuição espacial | Onde ficam vias, nós, marcos, zonas, terreno? Onde NÃO pode haver objeto? | planta em texto + **registro de ocupação** (`construcao/registro.py`) | `../estruturas/vilas-e-cidades.md`, `../ambientacao/terreno-biomas-agua.md` |
| 7 | Principal e secundárias | Qual é a UMA ênfase? O resto apoia | hierarquia | `../fundamentos/composicao-hierarquia-silhueta.md` |
| 8 | Volumes e silhuetas | A silhueta em preto e branco lê? Há 3+ planos de profundidade? | croqui de massas; protótipo se for incomum | `../fundamentos/profundidade-contraste-transicoes.md`, `../experimentos/` |
| 9 | Construir | Em que ordem? | scripts por módulo | seção "Ordem de construção" abaixo |
| 10 | Detalhes e ambientação | Luz, vegetação, narrativa, deterioração com causa | lista de detalhes por zona | `../ambientacao/`, `../materiais/` |
| 11 | Verificar | Auditoria 0? Render de várias vistas? Portas/escadas andáveis? | relatório da auditoria + imagens | `checklist-de-validacao.md` |
| 12 | Corrigir | É um erro isolado ou uma **classe** de erro? | correção em TODAS as ocorrências + nova regra na auditoria | `../erros-e-licoes.md` |
| 13 | Registrar | O que aprendi que outra sessão precisa saber? | `erros-e-licoes.md`, técnica/experimento, commit e push | `registrar-aprendizados.md` |

## Ordem de construção (aprendida na Vila)
1. Terreno (mapa de alturas, pads planos, inclinação ≤ 1 entre vizinhos).
2. Vias e rede de circulação (marcar células; nada sólido nelas).
3. Construções principais e secundárias **reservando o espaço** (porches e margens incluídos).
4. Objetos centrais (praça, fonte, poço) **com anel de passagem livre** (fonte ≥ 3, demais ≥ 2 blocos).
5. Postes e árvores **só em célula livre e com base no terreno** (nunca no "bloco mais alto").
6. Cobertura de solo, cursos d'água, pedras.
7. Pós-correções automáticas (lanternas sem suporte, vergas das portas).
8. Auditoria → render → exportar → instalar.

## Ficha do projeto (copiar para o início de cada trabalho)
```
PEDIDO: <texto literal>
PREMISSAS: <o que foi assumido>
HISTÓRIA (1 frase): ...        PALAVRAS-CHAVE VISUAIS: a, b, c
ESTILO: dominante=...  secundário=...  regra de convivência=...
PALETA: dominante=[ids]  apoio=[ids]  acento=[ids]
ESCALA/DIMENSÕES: ...   ORÇAMENTO: ~N blocos   MÓDULOS: ...
PLANTA: eixos/vias/marcos/zonas (texto ou ASCII)
HIERARQUIA: principal=...  secundárias=...
RISCOS TÉCNICOS: (estados, entidades de bloco, limites de comando, chunks)
VALIDAÇÃO: auditoria TOTAL=_  vistas=_  testes no jogo pendentes=_
APRENDIZADOS A REGISTRAR: ...
```

## Erros comuns do método
- Começar a colocar blocos antes de decidir hierarquia e paleta (resultado: várias construções "iguais com fachada trocada").
- Tratar o render como prova de cor ou de que dá para andar (o render mostra forma; o jogo mostra o resto).
- Corrigir só o item apontado: o dono já pediu várias vezes que cada correção seja generalizada (ver `../erros-e-licoes.md` E-13).
- Estilo misturado sem regra: escolher dominante e deixar o secundário aparecer só em detalhes, materiais ou implantação (ver `combinar-estilos-e-especialidades.md`).

## Limitações
- Método ainda NÃO validado em um pedido inédito de ponta a ponta (a Vila foi construída antes de existirem estas etapas; foram depois reconstruídas a partir dela). Os planos em `exemplos-de-planejamento.md` são **planos não executados**.
