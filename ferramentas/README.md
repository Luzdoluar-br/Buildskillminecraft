# Ferramentas

Tudo aqui é Python 3.12. Dependências: `numpy`, `pillow` (render por raycast). Opcional: Node + `@minecraft/creator-tools` (render com texturas reais e `.mcstructure` via CLI `mct`; instalar com `npm install @minecraft/creator-tools` numa pasta e apontar `MCT_DIR`).

## 1. `construcao/` — construir, exportar, validar, renderizar
| Arquivo | Função |
|---|---|
| `cena.py` | Biblioteca de construção (vendorizada do BotVulpus): `Cena`, `Paleta`, `escada()`, `laje()`, `caixa/oca/cilindro/esfera/cupula/arco_redondo/telhado_duas_aguas/ilha_flutuante/arvore/poste`, `validar()` (peças soltas) |
| `moldes.py` | `Molde`: coordenadas locais da construção com giro de 180° (`flip`), `st/sl/log/porta/porta_dir/maq/cama`, telhados (`telhado_x/z`, `tenda`), registro `ESCADAS`; `pal()` para paletas |
| `terreno.py` | Mapa de alturas com pads planos, relaxamento (inclinação ≤ 1) e preenchimento |
| `registro.py` | `Ocupacao`: reserva de espaço (nada nasce sobre outro objeto) e anéis de passagem |
| `exportar.py` | Escreve/lê `.mcstructure` (NBT little-endian) **com entidades de bloco** (`block_position_data`) |
| `auditoria_geral.py` | Regras E-01…E-31 do registro de erros: IDs e estados contra a lista oficial, apoio, portas, escadas, troncos, máquinas, água, e (com contexto) terreno/ocupação |
| `camera.py`, `previa_voxel.py` | Render por raycast com texturas vanilla (baixadas na 1ª execução para `.cache_blocos/`, precisa de internet). Folhas, cobre, lã colorida etc. aparecem cinza: **o render não prova a cor final** |
| `blocos_validos.txt`, `estados_validos.json` | IDs e estados OFICIAIS (gerados de `referencia/fonte/mojang-blocks.json`) |
| `exemplos/exemplo_minimo.py` | Casa mínima: constrói, exporta com entidade de bloco, relê e audita |

### Fluxo padrão
```python
import sys; sys.path.insert(0, "ferramentas")          # antes de qualquer outro pacote chamado `construcao`
from construcao.cena import Cena, escada, laje, LESTE, OESTE, SUL, NORTE
from construcao.moldes import Molde, pal, ESCADAS, M
from construcao.exportar import gravar, ler, Byte
from construcao.auditoria_geral import auditar, relatorio
c = Cena("minha_obra")
...                                   # construir (ver tecnicas/ e procedimentos/)
print(relatorio(auditar(c)))          # meta: TOTAL 0 antes de entregar
gravar(c, "saida/minha_obra.mcstructure")
```
Atenção: o projeto BotVulpus (se existir na máquina) tem um pacote também chamado `construcao`; importe o deste repositório primeiro.

## 2. Ler e comparar mundos Bedrock (LevelDB)
`ldb.py` (leitor puro Python de LevelDB com compressão zlib raw do Bedrock + NBT little-endian), `world.py` (blocos de chunks), `cmp.py`, `scan.py`, `deep.py`, `lay.py`, `filt.py`: comparam o mundo salvo com a estrutura gerada para ver o que o dono mudou (Aula 01 e 02). **Feche o jogo antes de copiar o `db`** (o jogo só grava ao sair). Detalhes em `aulas/aula-01/metodo-e-autoria.md`.

## 3. Referência de blocos
`gerar_referencia_blocos.py` regenera `referencia/blocos-bedrock.md/.csv`, `construcao/blocos_validos.txt` e `construcao/estados_validos.json` a partir de `referencia/fonte/mojang-blocks.json` (oficial Mojang/bedrock-samples).
