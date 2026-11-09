# Combinar estilos e especialidades

> Status: matriz de decisão [INT] baseada nas pesquisas e na Vila; nenhuma combinação inédita foi construída ainda | Confiança: média-baixa | Última revisão: 2026-11-09

## Resumo
Um pedido real mistura campos (urbanismo + estilo + estrutura + ambientação). Em vez de consultar um documento por vez, use a **matriz** abaixo para saber quais documentos ler juntos e qual é a regra de convivência entre estilos. Sem regra, a mistura vira colagem.

## Regra de convivência entre estilos [INT]
1. **Um dominante** define volumes, telhados e paleta de ~70% da cena.
2. **Um secundário** entra por *detalhe, material ou ocupação do espaço*, nunca pelos volumes principais (ex.: casa japonesa em montanha = estilo japonês domina; implantação e materiais seguem o terreno).
3. **Ponte entre estilos**: um material ou uma cor presente nos dois (ex.: madeira escura com concreto cinza) faz a transição.
4. **Camadas no tempo** (construções modificadas por décadas): cada fase tem paleta e alinhamento próprios; ver `../ambientacao/ruinas-e-narrativa.md`.
5. Misturas que pedem protótipo antes: telhados curvos sobre estrutura industrial, neon sobre pedra medieval, vegetação sobre arquitetura de vidro.

## Matriz: pedido → documentos a ler
| Tipo de pedido | Estilo(s) | Estrutura(s) | Ambientação / material | Fundamentos críticos |
|---|---|---|---|---|
| Vila medieval em montanha nevada | `medieval-europeu-e-fantasia` | `vilas-e-cidades`, `casas-e-edificios-residenciais`, `castelos-e-fortalezas` | `terreno-biomas-agua` (encosta, neve [NV]), `paletas-e-combinacoes` | hierarquia, implantação no terreno |
| Vila japonesa em montanha | `japones-tradicional` | `vilas-e-cidades`, `templos-e-monumentos` | `terreno-biomas-agua` | escala (ken ≈ 2 blocos), profundidade (beiral) |
| Cidade futurista em pântano | `futurista-cyberpunk-solarpunk`, `modernista-e-contemporaneo` | `vilas-e-cidades` (camadas), `arranha-ceus`, `pontes-e-viadutos`, `subterraneas-e-suspensas` | `terreno-biomas-agua` (palafitas, água), `iluminacao-e-atmosfera`, `vidro-luz-e-metal` | silhueta, ritmo, equilíbrio |
| Cidade cyberpunk vertical | `futurista-cyberpunk-solarpunk`, `industrial-e-brutalista` | `arranha-ceus`, `pontes-e-viadutos`, `vilas-e-cidades` | `iluminacao-e-atmosfera`, `vidro-luz-e-metal` | densidade, contraste, camadas |
| Estação ferroviária subterrânea industrial | `industrial-e-brutalista`, `pos-apocaliptico-subterraneo-liminal` | `estacoes-e-ferrovias`, `subterraneas-e-suspensas` | `iluminacao-e-atmosfera` | escala, fluxo |
| Templo esquecido em floresta gigante | `chines-tradicional` ou `japones-tradicional` ou `gotico` + ruína | `templos-e-monumentos` | `ruinas-e-narrativa`, `terreno-biomas-agua`, `envelhecimento-e-deterioracao` | hierarquia, narrativa |
| Instalação científica abandonada no fundo do oceano | `modernista-e-contemporaneo`, `futurista-cyberpunk-solarpunk` + ruína | `instalacoes-industriais-e-laboratorios` ([NV] submarino), `subterraneas-e-suspensas` | `ruinas-e-narrativa`, `iluminacao-e-atmosfera` | luz como narrativa |
| Casa antiga abandonada no topo de prédio destruído (Backrooms Vermelhas) | `vitoriano` ou `medieval…` sobre `pos-apocaliptico-subterraneo-liminal` | `casas-e-edificios-residenciais`, `arranha-ceus` (em ruína) | `ruinas-e-narrativa`, `iluminacao-e-atmosfera` | contraste de escala e de época, estrutura sobre estrutura |
| Cidade sobre ruínas de civilização antiga | `templos-e-monumentos` (ruína) + estilo atual | `vilas-e-cidades` | `ruinas-e-narrativa` (palimpsesto) | camadas no tempo |

(Os nomes referem-se a arquivos de `../estilos/`, `../estruturas/`, `../materiais/`, `../ambientacao/`, `../fundamentos/`.)

## Como combinar (algoritmo curto)
1. Escreva a história em 1 frase e extraia **substantivo (o que é)**, **adjetivo (estado/estilo)**, **lugar**.
2. Substantivo → tipo de estrutura (`../estruturas/`). Adjetivo → estilo e deterioração (`../estilos/`, `../ambientacao/ruinas-e-narrativa.md`). Lugar → terreno e bioma (`../ambientacao/terreno-biomas-agua.md`).
3. Liste conflitos (ex.: vidro e madeira x pântano úmido) e resolva com a regra de convivência.
4. Escolha a paleta pela *emoção* (frio/quente, limpo/sujo) e confirme IDs em `../referencia/blocos-bedrock.md`.
5. Verifique a viabilidade técnica no Bedrock (`../referencia/bedrock-comandos-e-limites.md`): tamanho, entidades de bloco, luz.

## Erros comuns
- Concatenar estilos com todos os elementos de cada um (colagem).
- Esquecer que o lugar (pântano, neve, oceano) muda **fundação, materiais e escala de detalhe** (`../ambientacao/terreno-biomas-agua.md`).
- Aplicar uma paleta "de gênero" sem checar contraste (neon exige superfícies escuras e sujas para brilhar).

## Limitações e dúvidas
- Biomas (neve, mangue, deserto, submarino) e vários estilos têm pouca fonte confirmada; as linhas dessa matriz que dependem deles são [INT]/[NV].
- Nenhuma dessas combinações foi construída: **plano, não resultado**.
