# Cantos e vigas de madeira

Origem: correções do dono na Vila (Aula 02). **Evidência** = lido no mundo ou visto nos prints dele; *interpretação* marcada.

## C-1 Canto = tronco vertical contínuo (evidência: prints ERRADO / CERTO)
O canto de toda parede de madeira é um tronco `pillar_axis=y` do chão até a viga do topo. Viga horizontal no canto expõe a ponta (anéis) na lateral: errado. O dono corrigiu à mão vários cantos assim.

## C-2 Melhoria do dono: canto com ponta de viga projetada, lanterna e mísula (evidência PARCIAL: 1 canto lido no mundo + 4 prints)
- Pilar vertical contínuo (`stripped_dark_oak_log`).
- No nível do beiral, **uma viga horizontal avança 1 bloco para fora do canto** (`pillar_axis` na direção da parede); a **ponta exposta é intencional** (detalhe de enxaimel), diferente do erro C-1.
- **Lanterna pendurada** logo abaixo da ponta da viga.
- Abaixo, **mísula de escada** (`dark_oak_stairs`, `weirdo_direction` voltado para o pilar) formando degrau saliente junto ao pilar.
- *Interpretação*: a projeção cria sombra e silhueta no canto; a mísula "assenta" a viga; a luz marca o canto.
- *A confirmar*: número exato de degraus da mísula e se vale para todos os cantos ou só os de fachada. Aplicar no gerador só depois de confirmar com o dono.

## C-3 Pórtico do chalé
As extremidades da viga frontal sobem como tronco vertical (poste do canto), sem ponta exposta.

Checagem automática: regra E-23 em `aulas/aula-02/codigo/auditoria.py`.
