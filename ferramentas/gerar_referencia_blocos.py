"""Gera referencia/blocos-bedrock.md/.csv e ferramentas/construcao/blocos_validos.txt a partir da lista OFICIAL de blocos da Mojang.

Fonte primária: https://raw.githubusercontent.com/Mojang/bedrock-samples/main/metadata/vanilladata_modules/mojang-blocks.json
(guardada em referencia/fonte/mojang-blocks.json; versão baixada: bedrock-samples v1.26.60.5). Nomes em inglês vêm, quando existem, de
recipe-item-catalog.json do @minecraft/creator-tools (opcional).

Uso: python gerar_referencia_blocos.py <mojang-blocks.json> <pasta_saida_referencia> <caminho_blocos_validos.txt> [recipe-item-catalog.json]
"""
import csv
import json
import os
import sys

fonte, saida, validos = sys.argv[1:4]
catalogo = sys.argv[4] if len(sys.argv) > 4 else None
d = json.load(open(fonte, encoding="utf-8"))
props = {p["name"]: (p["type"], [v["value"] for v in p["values"]]) for p in d["block_properties"]}
nomes = {}
if catalogo and os.path.exists(catalogo):
    nomes = {i["id"].replace("minecraft:", ""): i["n"] for i in json.load(open(catalogo, encoding="utf-8"))["items"]}


def fmt(v):
    if v and all(isinstance(x, int) and not isinstance(x, bool) for x in v) and v == list(range(v[0], v[0] + len(v))):
        return "%d..%d" % (v[0], v[-1])
    return ", ".join(str(int(x)) if isinstance(x, bool) else str(x) for x in v)


linhas = []
for b in sorted(d["data_items"], key=lambda b: b["name"]):
    bid = b["name"].replace("minecraft:", "")
    est = "; ".join("%s = %s" % (p["name"], fmt(props[p["name"]][1])) for p in b.get("properties", []) if p["name"] in props)
    linhas.append((bid, nomes.get(bid, ""), est))

os.makedirs(saida, exist_ok=True)
with open(os.path.join(saida, "blocos-bedrock.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["id", "nome_en", "estados_oficiais"])
    w.writerows(linhas)
with open(os.path.join(saida, "blocos-bedrock.md"), "w", encoding="utf-8") as f:
    f.write("# Blocos do Minecraft Bedrock: IDs e estados OFICIAIS\n\n")
    f.write("**%d blocos.** Fonte primária: `mojang-blocks.json` do repositório oficial Mojang/bedrock-samples (versão 1.26.60.5, cópia em `fonte/mojang-blocks.json`). " % len(linhas))
    f.write("Use SEMPRE `minecraft:<id>` exatamente como está. **Se o ID não está aqui, ele não existe** (nem nomes do Java Edition ou de memória).\n\n")
    f.write("- Coluna *estados*: propriedades oficiais do bloco e valores possíveis (`0..3` = inteiros de 0 a 3; booleanos aparecem como `0, 1`). Vazio = bloco sem estados.\n")
    f.write("- Significado/rotação dos estados e armadilhas: `estados-e-rotacao.md`. Formato do arquivo de estrutura: `mcstructure-formato.md`.\n")
    f.write("- Gerado por `ferramentas/gerar_referencia_blocos.py`. Regenerar quando sair uma versão nova do bedrock-samples.\n\n")
    f.write("| ID | Nome (EN) | Estados oficiais |\n|---|---|---|\n")
    for bid, n, est in linhas:
        f.write("| `%s` | %s | %s |\n" % (bid, n, est.replace("|", "/")))
open(validos, "w", encoding="utf-8").write("\n".join(sorted({l[0] for l in linhas})) + "\n")
print("blocos:", len(linhas), "| com estados:", sum(1 for l in linhas if l[2]), "| propriedades distintas:", len(props))
tabela = {b["name"].replace("minecraft:", ""): {p["name"]: [(int(x) if isinstance(x, bool) else x) for x in props[p["name"]][1]] for p in b.get("properties", []) if p["name"] in props} for b in d["data_items"]}
json.dump(tabela, open(os.path.join(os.path.dirname(validos), "estados_validos.json"), "w", encoding="utf-8"), separators=(",", ":"))
print("estados_validos.json:", len(tabela), "blocos")
