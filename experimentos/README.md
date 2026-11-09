# Experimentos

Protótipos pequenos e isolados (não tocam nas construções das aulas) para transformar técnica "de livro" em técnica **testada**. Cada pasta tem `experimento.py` (reproduzível), `imagens/` e um `RESULTADO.md` com números, conclusões e **falhas**.

Como rodar qualquer um: `python experimentos/XNN-nome/experimento.py` (precisa de `numpy`, `pillow` e internet na 1ª execução para baixar texturas; ver `ferramentas/README.md`).

| ID | Pergunta | Resultado em uma linha | Status |
|---|---|---|---|
| X01 telhados | Como ficam 7 tipos de telhado na mesma caixa? | Telhado 1:2 (escada+laje) funciona e virou método `Molde.telhado_suave_x`; abóbada de raio ≤ 4 NÃO lê como curva | TESTADO (render) |
| X02 fachadas e janelas | Quanta profundidade cada estilo de fachada precisa e que janelas funcionam? | Fachada de 1 plano parece papelão; 3+ planos leem como arquitetura; janelas pequenas não leem como arco/círculo | TESTADO (render) |
| X03 curvas e diagonais | A partir de que tamanho um círculo/cúpula "lê"? | Círculo lê a partir de diâmetro ~15; cúpula com lajes tem degraus mais finos por +9–24% de blocos | TESTADO (render + métrica) |
| X04 ruínas com causa | Dano com causa lê melhor que dano aleatório? | Sim: aleatório deixa 106 blocos flutuantes, causas físicas 0–3; módulo `ruina.py` | TESTADO (métrica + render) |
| X05 vertical, vãos, terreno | Torre com recuos, pontes, balanço, casa em encosta | Torre e ponte pênsil funcionam; ponte em arcos de vão 10 FALHOU (viu-se muro com pilares); cabo diagonal de cerca não se liga | TESTADO (render + auditoria) |

## Regras comuns
- Todo experimento é auditado por `ferramentas/construcao/auditoria_geral.py` (IDs e estados oficiais, apoio, etc.). Falsos positivos revelados pelos experimentos viraram refinamentos da regra (ver `erros-e-licoes.md`).
- O render por raycast **não mostra cor final** de folhas, cobre, lã etc. (aparecem cinza): ele valida **forma e silhueta**, não paleta.
- **Nada aqui foi testado andando no jogo**, só renderizado e auditado. Itens que exigem o jogo estão em `limitacoes-e-duvidas.md`.
