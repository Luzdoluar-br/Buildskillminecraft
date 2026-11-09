# Vilas e cidades

> Status: rascunho consolidado | Confiança: média para Lynch e hierarquia de ruas (enciclopédia), média para enclosure 1:1, baixa para 1:2 e 1:3; lições da Vila são evidência real | Última revisão: 2026-11-09

## Resumo
Cidade legível = eixo principal, limite, 2-3 distritos, 1-2 nós (praça), 1-2 marcos. Praça precisa de anel livre; ocupação precisa de registro; camadas ajudam na cidade vertical. A Vila Pedra-Musgo mostrou os erros reais.

## Conceito
- [DOC, aberta secundária] Kevin Lynch: cinco elementos da imagem da cidade: vias, limites, distritos, nós, marcos (Wikipedia "The Image of the City"; livro não lido; Taylor & Francis só busca).
- [DOC, aberta secundária] Hierarquia de ruas: arterial > coletora > local > cul-de-sac; objetivo reduzir tráfego de passagem; há críticas (Wikipedia "Street hierarchy").
- [DOC, aberta] Enclosure: Essex Design Guide confirma largura <= altura (1:1 ou mais fechada) para espaços de pedestres; árvores e fachadas contínuas compensam larguras maiores; empenas e chaminés aumentam a altura aparente. A faixa 1:1-1:3 e os rótulos "forte/moderada": só busca, NÃO verificados (1:2 e 1:3 não lidos).
- [DOC] Kowloon Walled City: 2,6 ha, ~33.000 habitantes (1987), 300-350 edifícios, altura máx. 13-14 andares (limite Kai Tak), 2-3 para 6-7 andares nos anos 1960, becos de 1-2 m, demolição 1993-94; altura em metros não informada.
- [DOC] Shibam: torres de tijolo de barro de 5-11 andares, ~500 torres, muralha (Wikipedia).

## Características / regras
| Regra | Valor | Rótulo |
|---|---|---|
| Rua principal da porta à praça; ruas locais; vielas | | [INT] (a partir de hierarquia [DOC]) |
| Checagem Lynch: 1 eixo, 1 limite (muralha/rio), 2-3 distritos distintos, 1-2 nós, 1-2 marcos | | [INT] |
| Rua principal 5-9 entre fachadas com prédios 5-9 de altura (1:1); vielas 2-4 | sem fonte; 1:1 é o que o Essex confirma | [INT] |
| Praça: construção no meio exige anel livre ao redor (fonte >= 3 de caminho, poço/barraca >= 2) | | [TESTADO-AULA02] |
| Equipamentos nos cantos, não no eixo das ruas ou portas | | [TESTADO-AULA02] |
| Nada sólido em y+1/y+2 no anel; nada na frente das portas | | [TESTADO-AULA02] |
| Desnível entre células vizinhas do caminho <= 1 bloco na rede de caminhos | | [TESTADO-AULA02] |
| Registro de ocupação: todo objeto reserva sua pegada, colisão é recusada | | [TESTADO-AULA02] |
| Cidade vertical em camadas (ver abaixo) | | [INT] |

## Como construir no Bedrock
**Receita A: vila medieval pequena** [TESTADO-AULA02 nos blocos; a receita genérica é adaptação]
1. Escolher o eixo (rua principal) e o marco (salão com torre-relógio, no nível elevado).
2. Reservar com registro de ocupação (`reservar()` / `livre()` na Vila) todas as pegadas: casas com varanda e margem, barracas com toldo, poço, fonte, píer, postes, árvores.
3. Praça no cruzamento ou diante do prédio principal: fonte pequena (bacia r~3,9, total ~4) com anel livre de 3,1 de largura, faixa de `polished_andesite` ou `smooth_stone` marcando o anel; praça ~35x16 (x 13..47, z 25..40 na Vila).
4. Barracas, poço e bancos nos cantos; bancos com as costas para o lado oposto ao foco (E-17).
5. Casas de tipos distintos (chalé, casa de pedra, hortelão, casa de chá) para variedade de distrito; porta com batentes maciços (`../tecnicas/portas-e-entradas.md`).
6. Caminhos com 6 materiais e largura variável (`../tecnicas/terreno-caminhos-e-pracas.md`); postes com lanterna fora da trilha (`../tecnicas/postes-de-luz.md`).
7. Árvores sem copa invadindo casas; só nascem onde há espaço livre.
8. Auditoria: conflitos de pegada = 0, anel livre, portas livres, escadas com cabeça livre.
**Receita B: planejamento em camadas para cidade vertical** [INT; Shibam e Kowloon são só inspiração]
1. Camada 0 (solo): rua, praça, entradas e comércio; mantém a regra do anel e a hierarquia de ruas.
2. Camada 1 (base e plataforma): garagens/fundações e passarelas a 4-8 acima, com escadas visíveis.
3. Camada 2 (corpo): habitação em módulos de pavimento 3-4 (casa e arranha-céu), densidade crescente; recuos para luz.
4. Camada 3 (coroa): marcos altos (1-2) e terraços técnicos.
5. Camada de acréscimos (estilo Kowloon): fases 2-3 em paleta distinta, anexos, balanços (ver [subterraneas-e-suspensas.md](subterraneas-e-suspensas.md)).
6. Registrar cada camada com reserva de pegada antes de construir.
**Receita C: muralha com portas** [INT]: portas onde as estradas principais chegam (ver [castelos-e-fortalezas.md](castelos-e-fortalezas.md)).

## Combina com
[casas-e-edificios-residenciais.md](casas-e-edificios-residenciais.md) · [arranha-ceus.md](arranha-ceus.md) · [pontes-e-viadutos.md](pontes-e-viadutos.md) · [estacoes-e-ferrovias.md](estacoes-e-ferrovias.md) · [templos-e-monumentos.md](templos-e-monumentos.md) · [../tecnicas/praca-e-espaco-publico.md](../tecnicas/praca-e-espaco-publico.md) · [../estilos/medieval-europeu-e-fantasia.md](../estilos/medieval-europeu-e-fantasia.md) · [../fundamentos/composicao-hierarquia-silhueta.md](../fundamentos/composicao-hierarquia-silhueta.md) · [../ambientacao/ruinas-e-narrativa.md](../ambientacao/ruinas-e-narrativa.md) · [../ambientacao/terreno-biomas-agua.md](../ambientacao/terreno-biomas-agua.md)

## Erros comuns
- Fonte ou barraca ocupando a praça sem anel (E-15); equipamento no eixo da porta ou da rua (E-12).
- Objetos sobrepostos (barraca + poço, E-16); poste/árvore sobre outro objeto (E-14).
- Ruas largas demais com casas baixas; todas as casas com mesma altura e alinhamento.
- Sem praça, marco ou portão na muralha.
- Degraus de 2-3 blocos na rede de caminhos (E-19).

## Limitações e dúvidas
- Enclosure 1:2 e 1:3 não verificados; os valores em blocos de rua são [INT].
- Altura em metros de Kowloon: não informada (3 m por andar é estimativa).
- Quarteirões, tamanho de lote e terraços (Ifugao, Honghe): sem fonte lida.
- A Vila não foi testada andando: confirmação do dono pendente em escadas.

## Fontes e evidências
- Wikipedia "The Image of the City", "Street hierarchy", "Kowloon Walled City", "Shibam" (abertas); Far Out e Metropolis (abertas); Essex Design Guide (aberta).
- NSW (403), Urban Road Design Manual: só busca.
- Vila Pedra-Musgo: `../erros-e-licoes.md` (E-12, E-14, E-15, E-16, E-17, E-19), `../tecnicas/*.md`.
- Notas: A5_r2.md (tabela), A5_ruinas_ambientacao_urbanismo.md.
