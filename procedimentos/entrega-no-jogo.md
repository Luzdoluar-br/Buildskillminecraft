# Entrega no jogo: gerar, empacotar, instalar, colocar

> Status: TESTADO-AULA02 (a Vila Pedra-Musgo foi entregue assim e carregou no jogo do dono) | Última revisão: 2026-11-09

## Resumo
`Cena` → `.mcstructure` → **behavior pack** com funções `preparar`, `limpar`, `colocar`, `salvar` → instalado dentro do mundo → comandos no jogo. Código de referência: `../aulas/aula-02/codigo/`; formato do arquivo: `../referencia/mcstructure-formato.md`; limites e comandos: `../referencia/bedrock-comandos-e-limites.md`.

## Passo a passo
1. **Gerar** a estrutura com `construcao.exportar.gravar(cena, "x.mcstructure")` (tamanho máx. 64×384×64 por estrutura; se maior, dividir em módulos).
2. **Auditar** (`checklist-de-validacao.md`). Só continuar com TOTAL 0.
3. **Pack**: pasta com
   - `manifest.json` (format_version 2; `header.uuid` e `modules[0].uuid` **diferentes e novos**; `modules[0].type = "data"`; `min_engine_version`);
   - `structures/<ns>/<nome>.mcstructure`;
   - `functions/<ns>/preparar.mcfunction` → `tickingarea add x1 y z1 x2 y z2 <nome>` cobrindo a área;
   - `functions/<ns>/limpar.mcfunction` → `fill … air` em fatias de ≤ 8 camadas (≈ 30 mil blocos) + `kill @e[type=item,…]` (**apaga tudo na área, inclusive edições do dono**);
   - `functions/<ns>/colocar.mcfunction` → `structure load <ns>:<nome> x y z` (o canto mínimo da estrutura vai para x y z; o solo do projeto fica no y escolhido);
   - `functions/<ns>/salvar.mcfunction` → `structure save <nome> x1 y1 z1 x2 y2 z2 disk`.
4. **Instalar no mundo**: copiar a pasta para `<mundo>/behavior_packs/<nome>` e acrescentar `{pack_id, version}` em `world_behavior_packs.json` (e a entrada em `world_behavior_pack_history.json`). **Fazer backup dos `.json` antes.** Funções novas exigem reiniciar o jogo.
5. **No jogo** (cheats ativados): `/function <ns>/preparar` → esperar → (`/function <ns>/limpar`) → `/function <ns>/colocar`.
6. **Avisar o dono**: `limpar` e `colocar` sobrescrevem edições dele; sugerir `salvar` antes se ele quiser guardar o que fez (ele já preferiu passar prints em vez de usar `salvar`).

## Coordenadas da Vila (exemplo)
Canto mínimo em (−130, 96, −10); solo da vila em y = 100 (mesmo nível das estruturas da Aula 01, que ficam em x 0–650, z 0–350).

## Armadilhas já vividas
- Chunks não gerados: `structure load` falha; use `preparar` e espere. [TESTADO]
- O jogo **só grava o mundo no disco ao salvar/sair**: para ler as edições do dono, ele precisa sair do mundo antes. (E-32)
- Nomes de bloco inexistentes e estados antigos passam sem aviso: auditoria antes de empacotar. (E-01, E-31)
- Beds sem `block_entity_data` desaparecem. (E-04; teste com entidade ainda pendente no jogo)
