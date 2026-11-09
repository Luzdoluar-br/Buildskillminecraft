# Checklist de validação (antes de entregar qualquer construção)

> Status: consolidado dos erros E-01…E-36 de `../erros-e-licoes.md` (TESTADO-AULA02) | Última revisão: 2026-11-09

## Resumo
Quatro camadas, nesta ordem: (1) **auditoria automática** = TOTAL 0; (2) **render** de várias vistas; (3) **leitura dos dados** (não só da imagem); (4) **teste no jogo** do que só o jogo prova. Imagem bonita não prova que a construção está correta (E-07).

## 1. Auditoria automática
```python
import sys; sys.path.insert(0, "ferramentas")                  # antes de qualquer outro pacote chamado `construcao`
from construcao.auditoria_geral import auditar, relatorio, Contexto
print(relatorio(auditar(cena, contexto=ctx)))                   # ctx opcional (terreno, rede de caminhos, objetos)
```
| Regra | Pega | Origem |
|---|---|---|
| E-01 | ID que não existe no Bedrock (lista oficial de 1.466) | E-01, E-20, E-33, E-34 |
| E-31 | estado/valor inexistente para o bloco | E-32 |
| E-21 | mobília, planta, cerca, lanterna flutuando (grupos de cerca ligados à estrutura passam: cabos) | E-21, E-36 |
| E-02/E-03/E-10/E-11 | porta barrada, sem metade de cima, sem verga, com vidro/vazio no batente | E-02, E-10, E-11 |
| E-05 | lanterna pendurada sem bloco acima | E-05 |
| E-06 | água com ar ao lado (vaza) | E-06 |
| E-23 | ponta de tronco exposta no canto (aceita se houver lanterna pendurada embaixo) | E-23, C-2 |
| E-24/E-25 | máquina virada para parede; para-raios fora de `facing_direction=1`; cama sem entidade | E-24, E-25, E-04 |
| E-29 | escadas internas: degraus, cabeça livre, piso à frente do último | E-29 |
| E-12/E-14/E-15/E-16/E-19 (com `Contexto`) | obstáculo em via, objeto de chão fora do terreno, falta de anel livre, colisão de objetos, degrau alto em caminho | E-12…E-19 |

Regra de processo: **ao achar um erro novo, ampliar a auditoria** e testá-la com um caso negativo (um erro de propósito deve ser reprovado) — como foi feito com E-29 (escada falsa de 5 degraus) e com os estados.

## 2. Render (ferramentas/construcao/camera.py)
- Pelo menos: vista aérea geral, 2 vistas de cada construção principal (frente e oblíqua), **interior** das que têm interior, entradas e escadas.
- O render **não mostra** cor final de folhas, cobre, lã, nem prova que dá para andar. Usar para forma, silhueta, profundidade (≥ 3 planos), proporção.
- Posicionar a câmera fora de paredes (uma foto "dentro de um bloco" é cinza uniforme).

## 3. Ler os dados
- Releia o `.mcstructure` gravado (`construcao.exportar.ler`) e confira tamanho, paleta e entidades.
- Se o dono editou o mundo: copie o `db` **com o jogo fechado** (o jogo só grava ao sair) e compare com o gerado (`ferramentas/world.py`, `cmp.py`).

## 4. Testes que só o jogo prova (pedir ao dono; registrar em `../limitacoes-e-duvidas.md`)
Portas e escadas andáveis; cama com entidade de bloco; limite de `/fill`; direção de alçapões abertos; nascimento de monstros; cor real de folhas/cobre; carregamento da estrutura em chunk não gerado.

## 5. Antes de dizer "pronto"
- [ ] Auditoria TOTAL 0 (e o que foi isentado está justificado).
- [ ] Imagens de todas as construções principais, de fora e de dentro.
- [ ] Portas com 2 de altura + verga; nada barrando a frente; escadas com nº de degraus = altura entre pisos.
- [ ] Nada nasce sobre outro objeto; anel livre ao redor de fonte/poço/barraca.
- [ ] Todos os IDs e estados conferidos na lista oficial.
- [ ] Pack reinstalado e **aviso** ao dono: `colocar`/`limpar` apagam edições feitas por ele.
- [ ] Aprendizados registrados e **publicados no git** (`registrar-aprendizados.md`).
- [ ] O relatório diz o que foi testado e o que NÃO foi.
