# Postes de luz (modelo do dono)

**Evidência** (blocos lidos no mundo; o dono refinou o meu primeiro modelo):

| Camada (do chão) | Bloco |
|---|---|
| 0 | `stone_brick_wall` (base) |
| 1, 2 | `spruce_fence` ×2 (haste) |
| 3 (topo) | `spruce_slab` (parte de baixo): capa do poste |
| 3, ao lado | `spruce_stairs` como braço, `weirdo_direction` = para fora (a ponta alta sai do poste) |
| 2, sob o braço | `lantern` pendurada |
| 2, lado oposto | `spruce_slab` com `vertical_half=top`: contrapeso |

- **Por que funciona (interpretação, confiança média)**: braço curto com ponta elevada dá silhueta de "gancho"; laje de capa e contrapeso quebram a linha reta.
- **Regras de colocação (minhas, de erros E-12/E-14/E-16)**: base no terreno, nunca sobre outro objeto; fora de ruas e anéis de passagem (o braço pode ficar sobre a rua, aéreo); mínimo 4 blocos entre postes.
- **Código**: `poste_h()` em `aulas/aula-02/codigo/vila.py`.
