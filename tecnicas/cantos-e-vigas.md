# Cantos e vigas de madeira

Origem: correções do dono na Vila (Aula 02). **Evidência** = lido no mundo ou visto nos prints dele; *interpretação* marcada.

## C-1 Canto = tronco vertical contínuo (evidência: prints ERRADO / CERTO)
O canto de toda parede de madeira é um tronco `pillar_axis=y` do chão até a viga do topo. Viga horizontal no canto expõe a ponta (anéis) na lateral: errado. O dono corrigiu à mão vários cantos assim.

## C-2 Canto do dono: coluna de canto com degrau de escada, lanterna e ponta de viga (CONFIRMADO pelo dono: vale para TODOS os cantos)
Evidência: 1 canto construído pelo dono (lido no mundo) + prints; o dono confirmou que é o padrão para os cantos em geral.

Em cada canto, **fora da parede e alinhada com a parede lateral**, sobe uma coluna (de baixo para cima):
1. **Troncos verticais** (`stripped_*_log`, `pillar_axis=y`) do chão até logo abaixo da escada;
2. **1 escada** (`*_stairs`) que **sobe em direção à casa** (o degrau fica para fora);
3. **Lanterna pendurada** (`lantern`, `hanging=1`);
4. **Ponta da viga lateral** (`stripped_*_log`, `pillar_axis` na direção da parede lateral) que avança 1 bloco além da fachada. **A ponta exposta aqui é intencional** (diferente do erro C-1).

No canto da casa de chá o dono usou exatamente: 1 tronco + 1 escada + lanterna + ponta de viga (alturas relativas -1, 0, +1, +2).
Termos: o que chamei de "mísula" é só o degrau de escada embaixo da viga (suporte em degrau).

*Interpretação (confiança média)*: a projeção cria sombra e silhueta no canto, a escada assenta a viga e a lanterna marca o canto à noite.

**Implementação**: `canto_lampada()` em `aulas/aula-02/codigo/casas.py`, aplicada em chalé (cantos de trás; os da frente ficam livres para o pórtico), casa do hortelão (cantos de trás; os da frente são ocupados pelo alpendre) e casa de chá (4 cantos). Só entra onde o espaço está livre. Casas de pedra (casa com torreta, base do Salão) não usam: o canto delas é de pedra.
**Auditoria**: E-23 aceita ponta de viga exposta quando há lanterna pendurada logo abaixo.

## C-3 Pórtico do chalé
As extremidades da viga frontal sobem como tronco vertical (poste do canto), sem ponta exposta.

Checagem automática: regra E-23 em `aulas/aula-02/codigo/auditoria.py`.
