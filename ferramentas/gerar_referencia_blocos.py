"""Gera referencia/blocos-bedrock.md e .csv: TODOS os IDs de bloco do Minecraft Bedrock + nome + estados observados no jogo.
Fontes: (1) block-atlas.json do @minecraft/creator-tools (lista oficial de IDs); (2) recipe-item-catalog.json (nomes em inglês);
(3) paletas de subchunks de um mundo real salvo pelo jogo (estados e valores que o PRÓPRIO jogo gravou).
Uso: python gerar_referencia_blocos.py <pasta_data_do_creator_tools> <pasta_db_do_mundo> <pasta_saida>"""
import collections
import csv
import json
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(__file__))
import ldb  # noqa: E402

data, db, saida = sys.argv[1:4]
atlas = sorted(json.load(open(os.path.join(data, "block-atlas.json"), encoding="utf-8"))["blocks"])
itens = {i["id"].replace("minecraft:", ""): i for i in json.load(open(os.path.join(data, "recipe-item-catalog.json"), encoding="utf-8"))["items"]}
valores = collections.defaultdict(lambda: collections.defaultdict(set))
vistos = collections.Counter()
for k, v in ldb.load(db).items():
    if len(k) in (9, 10, 13, 14) and k[8:9] == b"\x2f" or (len(k) == 10 and k[8] == 0x2f):
        try:
            ver, ns = v[0], v[1]
            i = 3 if ver == 9 else 2
            for _ in range(ns):
                bits = v[i] >> 1
                i += 1
                bpw = 32 // bits
                i += 4 * (-(-4096 // bpw))
                n = struct.unpack("<i", v[i:i + 4])[0]
                i += 4
                for _ in range(n):
                    c, i = ldb.nbt_root(v, i)
                    nome = c["name"].replace("minecraft:", "")
                    vistos[nome] += 1
                    for sk, sv in c.get("states", {}).items():
                        valores[nome][sk].add(str(sv))
        except Exception:
            continue
linhas = []
for bid in atlas:
    est = "; ".join("%s = %s" % (sk, ", ".join(sorted(vs, key=lambda s: (len(s), s))[:8])) for sk, vs in sorted(valores.get(bid, {}).items()))
    it = itens.get(bid, {})
    linhas.append((bid, it.get("n", ""), it.get("c", ""), est))
os.makedirs(saida, exist_ok=True)
with open(os.path.join(saida, "blocos-bedrock.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["id", "nome_en", "categoria", "estados_observados"])
    w.writerows(linhas)
with open(os.path.join(saida, "blocos-bedrock.md"), "w", encoding="utf-8") as f:
    f.write("# Blocos do Minecraft Bedrock: IDs de referência\n\n")
    f.write("**%d blocos.** Use SEMPRE `minecraft:<id>` exatamente como está na coluna ID. Se um bloco não está nesta tabela, **ele não existe** (ou foi renomeado): nunca usar nomes de memória ou do Java Edition.\n\n" % len(linhas))
    f.write("- Estados mostrados = os que o jogo realmente gravou num mundo real (campo vazio = nenhum observado, não quer dizer que não existam). Rotação e convenções: ver `estados-e-rotacao.md`.\n")
    f.write("- Gerado por `ferramentas/gerar_referencia_blocos.py` (fonte: lista oficial de IDs do Minecraft Creator Tools).\n\n")
    f.write("| ID | Nome (EN) | Categoria | Estados observados |\n|---|---|---|---|\n")
    for bid, n, cat, est in linhas:
        f.write("| `%s` | %s | %s | %s |\n" % (bid, n, cat, est.replace("|", "/")))
print("blocos:", len(linhas), "com estados observados:", sum(1 for l in linhas if l[3]))
