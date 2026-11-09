# Limitações e dúvidas (aula 01)

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
