# Aula 01 — Método e regra de autoria

## Fontes
- **Original**: add-on `VULPUS_Aula_BP.mcpack` (50 `.mcstructure`, carregadas por `functions/aula/colocar.mcfunction` em grade de 70 blocos, y=100).
- **Modificado**: mundo "Aula" (Bedrock). Duas fontes: (a) blocos reais nos chunks, comparados na posição de colocação; (b) 5 estruturas salvas pelo dono (`modificada_04, 13, 14, 15, 24`).
- Trabalhou-se sempre em **cópia**; add-on e mundo originais não foram alterados.

## Método
1. Ler o LevelDB do mundo com leitor próprio (`ferramentas/ldb.py`, `world.py`).
2. Para cada estrutura N, origem = (70·col, 100, 70·linha). Comparar bloco a bloco com o `.mcstructure` original.
3. **Normalizar** estados irrelevantes antes de comparar.
4. Filtrar ruído natural; o resto é "alteração substantiva".

## Ruído descartado (NÃO é autoria do dono)
- `grass_block → dirt` (aparece até em estruturas sem nenhuma edição, ex.: 05, 42).
- Estados derivados: `corner` de escadas, `connection_*` de cercas/vidraças/muros, `update_bit`/`persistent_bit`, `pillar_axis=y`, `liquid_depth`, `hanging`.
- Fluxo de água.
- `folhas → ar`: ambíguo (decaimento vs poda). Tratado como **inconclusivo**.

## Critérios de classificação
- **Modificada**: ≥ ~100 alterações substantivas coerentes (materiais novos, estrutura nova).
- **Modificada (evidência limitada)**: 20–60 alterações coerentes.
- **Inconclusiva**: 1–16 alterações isoladas.
- **Original**: 0 alterações substantivas.
- **Não avaliável**: chunks inexistentes no mundo (estrutura nunca foi carregada ali).

## Limite da prova
A comparação prova **que** um bloco mudou, não **quem** o mudou. Atribuo ao dono porque o original é o add-on gerado por mim e o mundo só difere dele onde há edição humana ou efeitos naturais já filtrados. A estrutura 15 foi salva como "modificada" mas é **idêntica** ao original: salvar não significa modificar.
