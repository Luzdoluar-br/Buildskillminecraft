# Registro de bugs e erros (LEIA ANTES DE CONSTRUIR)

Regra do dono do projeto: **todo bug ou erro descoberto deve ser anotado aqui**, com causa e correção, para não se repetir e para que outras IAs, sem o contexto da conversa, consigam trabalhar. Entradas novas no topo. Nunca apagar entradas antigas.

Formato: **Sintoma** → **Causa** → **Correção** → **Como evitar / checar**.

---

## 2026-11-09 — Aula 02 (Vila Pedra-Musgo)
Descobertos pelo dono ao entrar no jogo (primeiro teste real) e confirmados lendo o LevelDB do mundo.

### E-01 · Blocos "terrosos/estranhos" espalhados (≈202 blocos)
- **Sintoma**: cubos marrons manchados acima das portas, forros e soleiras; um cubo de pedra onde devia haver laje.
- **Causa**: o helper `Molde.sl(x,y,z,nome)` montava `minecraft:<nome>` sem o sufixo, e chamei com `"spruce"`, `"dark_oak"`, `"pale_oak"`, `"stone_brick"`. IDs inexistentes: o Bedrock **aceita e grava** o nome errado e mostra bloco desconhecido. Nenhum erro aparece na geração nem no render.
- **Correção**: `sl()` agora acrescenta `_slab` quando falta.
- **Como evitar**: depois de gerar, listar os nomes únicos da paleta do `.mcstructure` e conferir um a um. Nomes de madeira/pedra sem sufixo (`spruce`, `stone_brick`, `oak`) são sempre suspeitos.

### E-02 · Portas bloqueadas
- **Causa A (Salão)**: eu colocava piso interno da torre em `y=1`, na mesma altura da porta; só sobrava 1 bloco livre. O piso fica em `y=0`.
- **Causa B (chalé)**: a porta da varanda estava 1 bloco acima do piso do andar (`y=6` em vez de `5`) e havia cerca exatamente na frente dela.
- **Correção**: piso removido; porta ao nível do piso; deck da varanda rente ao piso; guarda-corpo só nas pontas.
- **Como evitar**: para cada porta, conferir que a célula na frente e atrás, em `y` e `y+1`, não é sólida (script de checagem de portas no relatório da Aula 02).

### E-03 · Porta "sem parte de cima"
- **Estado**: no arquivo e no mundo as 6 portas tinham metade de cima (`upper_block_bit=1`). **Causa não confirmada**; hipótese: a porta da varanda do chalé ficava deslocada/obstruída (E-02). Reavaliar no jogo após a correção. Se persistir, anotar aqui com coordenadas.

### E-04 · Camas sumiram
- **Causa**: o Bedrock descarta o bloco `bed` ao carregar uma estrutura que não traz a entidade de bloco (cor).
- **Correção**: cama simulada com `white_wool` (travesseiro) + `light_blue_wool`.
- **Como evitar**: blocos com entidade de bloco (cama, placa, baú, banner, vaso com planta) exigem `block_position_data`; sem isso, trocar por equivalente simples.

### E-05 · Lanternas penduradas sumiram
- **Causa**: `lantern[hanging=true]` sem bloco acima é removida pelo jogo.
- **Correção**: função `corrigir_lanternas()` apoia no chão ou remove. Validar sempre.

### E-06 · Água vazando da lagoa/horta
- **Causa**: o anel de margem da lagoa (H=0) sobrepôs a borda da horta (H=1); a água da horta, ao nível do chão, escorreu pelo terreno mais baixo.
- **Correção**: lagoa deslocada para x=34 e horta reduzida (x 15..22).
- **Como evitar**: nunca deixar água ao nível do solo encostada em terreno mais baixo; áreas de água precisam de borda sólida.

### E-07 · O render não mostra a verdade de tudo
- Folhas, cobre, ardósia e lã colorida aparecem cinza; IDs inválidos não aparecem como erro. **Imagem boa ≠ construção correta**: sempre ler o `.mcstructure` e o mundo (ver ferramentas da Aula 01).

### E-08 · Exportador da biblioteca estoura com muitos blocos
- `Cena.construir()` falha com `IndexError` acima de ~77 estados distintos. Usar `aulas/aula-02/codigo/exportar.py`.

### E-09 · Telhados: empena cruzada falhou
- A tentativa de empena cruzada no chalé gerou buracos e blocos soltos; removida. Telhados mistos (2 materiais) funcionam; mais que isso vira ruído.

---

## 2026-11-09 — Aula 01
- **Autoria**: salvar uma estrutura não significa modificá-la (a 15 estava idêntica ao original).
- **Ruído do jogo** que NÃO é edição humana: `grass_block→dirt`, estados `corner` de escadas, `update_bit`/`persistent_bit`, fluxo de água. Ver `aulas/aula-01/metodo-e-autoria.md`.
- **Chunks ausentes** no mundo (estruturas 30, 39, 40, 47–50): não avaliáveis.

---

## Ferramentas e armadilhas do ambiente (Windows)
- Mundo Bedrock local: `%APPDATA%\Minecraft Bedrock\Users\<id>\games\com.mojang\minecraftWorlds\<pasta>`; add-on embutido vai em `<mundo>\behavior_packs\<nome>` + `world_behavior_packs.json` (**fazer backup antes**).
- `Expand-Archive` não aceita `.mcpack`; copiar da pasta-fonte ou renomear para `.zip`.
- O LevelDB do Bedrock usa compressão zlib raw: bibliotecas comuns (plyvel) não leem; usar `ferramentas/ldb.py`.
- `amulet-core` não compila no ambiente; o leitor próprio resolve.
- Feche o Minecraft antes de copiar/ler o mundo (o jogo grava o `db` ao sair).
