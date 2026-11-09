"""Auditoria automática da vila: roda TODAS as regras aprendidas (erros-e-licoes.md) em todas as estruturas.
Uso: python auditoria.py   (ideal: TOTAL 0). Cada regra tem o código do erro (E-xx) do registro."""
import math

import vila

c, H, CAM, PRACA, W, D = vila.c, vila.H, vila.CAM, vila.PRACA_CEL, vila.W, vila.D
BRUTAS = {"spruce", "dark_oak", "pale_oak", "oak", "birch", "cherry", "stone_brick", "bed"}
import pathlib
VALIDOS = set(pathlib.Path(__file__).with_name("blocos_validos.txt").read_text().split()) | {"air"}      # 1187 IDs oficiais do Bedrock (atlas do Creator Tools)
PRECISA_APOIO = ("barrel", "smoker", "furnace", "crafting_table", "bookshelf", "lectern", "anvil", "hay_block", "melon_block", "pumpkin", "carpet",
                 "_door", "fence", "lantern", "carrots", "potatoes", "wheat", "short_grass", "tall_grass", "fern", "tulip", "poppy", "cornflower",
                 "bluet", "daisy", "valley", "dandelion", "berry", "azalea", "waterlily", "farmland", "stone_brick_wall")
TERRENO = ("grass", "dirt", "moss", "podzol", "path", "gravel", "cobble", "andesite", "stone", "tuff", "polished")


def nome(b):
    return "air" if b is None else (b if isinstance(b, str) else b[0]).replace("minecraft:", "")


def estado(b):
    return {} if b is None or isinstance(b, str) else b[1]


def passavel(n):
    return n == "air" or any(k in n for k in ("grass", "fern", "tulip", "poppy", "cornflower", "bluet", "daisy", "valley", "dandelion", "berry",
                                              "azalea", "carpet", "lily_pad", "farmland", "stairs", "slab", "lantern", "rose"))


def solido(n):
    return not passavel(n) and not any(k in n for k in ("pane", "door", "water"))


def auditar():
    erros = []
    # E-01 IDs inválidos
    for p, b in c.blocos.items():
        if nome(b) in BRUTAS or nome(b) not in VALIDOS:
            erros.append(("E-01 ID inexistente no Bedrock", p, nome(b)))
    # E-21 bloco que precisa de apoio embaixo (mobília, plantas, cercas, lanternas no chão) flutuando
    for (x, y, z), b in c.blocos.items():
        n = nome(b)
        if not any(k in n for k in PRECISA_APOIO) or (n == "lantern" and estado(b).get("hanging")):
            continue
        if "fence" in n and any(nome(c.pegar(x + dx, y, z + dz)) != "air" and "fence" not in nome(c.pegar(x + dx, y, z + dz)) and "plank" in nome(c.pegar(x + dx, y, z + dz)) for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1))) and nome(c.pegar(x, y - 1, z)) == "air":
            erros.append(("E-21 cerca sem apoio embaixo (so presa ao lado)", (x, y, z), n))
            continue
        abaixo = nome(c.pegar(x, y - 1, z))
        if abaixo == "air" or (abaixo == "water" and "waterlily" not in n):
            erros.append(("E-21 bloco sem apoio (flutuando): %s sobre %s" % (n, abaixo), (x, y, z), n))
    # portas: E-03 metade de cima, E-10 verga, E-11 batentes, E-02/E-12 passagem
    for (x, y, z), b in c.blocos.items():
        if not (isinstance(b, tuple) and nome(b).endswith("_door") and not b[1].get("upper_block_bit")):
            continue
        if nome(c.pegar(x, y + 1, z)) != nome(b):
            erros.append(("E-03 porta sem metade de cima", (x, y, z), nome(b)))
        if c.pegar(x, y + 2, z) is None:
            erros.append(("E-10 vao acima da porta (falta verga)", (x, y, z), nome(b)))
        dz = 1 if b[1].get("minecraft:cardinal_direction") == "south" else -1
        for lado, d in (("fora", dz), ("dentro", -dz)):
            for dy in (0, 1):
                n = nome(c.pegar(x, y + dy, z + d))
                if solido(n):
                    erros.append(("E-02/E-12 porta barrada (%s)" % lado, (x, y + dy, z + d), n))
        for ax in (-1, 1):
            for dy in (0, 1, 2):
                n = nome(c.pegar(x + ax, y + dy, z))
                if n == "air" or "pane" in n or "glass" in n:
                    erros.append(("E-11 porta desconexa da parede (batente %s)" % ("vidro" if n != "air" else "vazio"), (x + ax, y + dy, z), n))
    # E-23 tronco horizontal com a PONTA (anéis) exposta ao ar: canto/encontro errado; troncos de árvore (sem 'stripped') são galhos e podem
    for (x, y, z), b in c.blocos.items():
        n = nome(b)
        eixo = estado(b).get("pillar_axis")
        if n.startswith("stripped_") and n.endswith("_log") and eixo in ("x", "z"):
            d = (1, 0) if eixo == "x" else (0, 1)
            for s in (1, -1):
                viz = nome(c.pegar(x + d[0] * s, y, z + d[1] * s))
                if viz == "air":
                    erros.append(("E-23 ponta de tronco exposta (canto/encontro errado)", (x, y, z), "%s axis=%s" % (n, eixo)))
                    break
    # E-24 máquinas orientadas: a FRENTE (cardinal_direction) tem de dar para um espaço livre, não para parede
    ve = {"north": (0, -1), "south": (0, 1), "east": (1, 0), "west": (-1, 0)}
    for (x, y, z), b in c.blocos.items():
        n = nome(b)
        card = estado(b).get("minecraft:cardinal_direction")
        if n in ("smoker", "blast_furnace", "furnace", "lectern", "anvil") and card:
            dx, dz = ve[card]
            if solido(nome(c.pegar(x + dx, y, z + dz))):
                erros.append(("E-24 maquina virada para a parede", (x, y, z), "%s frente=%s" % (n, card)))
        if n in ("smoker", "blast_furnace", "furnace", "lectern", "anvil", "pumpkin") and not card:
            erros.append(("E-24 maquina sem orientacao (cardinal_direction)", (x, y, z), n))
        if n == "lightning_rod" and estado(b).get("facing_direction") != 1:
            erros.append(("E-25 para-raios nao aponta para cima (facing_direction=1)", (x, y, z), n))
    # E-05 lanternas penduradas sem suporte
    for (x, y, z), b in c.blocos.items():
        if nome(b) == "lantern" and estado(b).get("hanging") and c.pegar(x, y + 1, z) is None:
            erros.append(("E-05 lanterna pendurada sem suporte", (x, y, z), "lantern"))
    # E-06 água com ar ao lado (vazamento)
    for (x, y, z), b in c.blocos.items():
        if nome(b) == "water" and any(c.pegar(x + dx, y, z + dz) is None for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            erros.append(("E-06 agua com ar ao lado (pode vazar)", (x, y, z), "water"))
    # E-14 postes e árvores devem nascer no TERRENO (nunca sobre toldo, telhado ou outro poste)
    for (x, y, z), b in c.blocos.items():
        if nome(b) == "stone_brick_wall" and nome(c.pegar(x, y + 1, z)) == "spruce_fence":
            abaixo = nome(c.pegar(x, y - 1, z))
            if abaixo == "air" or not any(k in abaixo for k in TERRENO) or y - 1 != H[x][z]:
                erros.append(("E-14 poste fora do terreno (sobre %s)" % abaixo, (x, y, z), "poste"))
    for (x, z) in vila.ARV:
        abaixo = nome(c.pegar(x, H[x][z], z))
        if not any(k in abaixo for k in TERRENO):
            erros.append(("E-14 arvore fora do terreno (sobre %s)" % abaixo, (x, H[x][z], z), "arvore"))
    # E-16 colisões entre objetos (registro de ocupação)
    for conf in vila.CONFLITOS:
        erros.append(("E-16 objetos colidindo/posicao invalida", conf[2], "%s x %s" % (conf[0], conf[1])))
    # E-15 caminho livre ao redor de tudo que fica no meio da rua
    for (nm, tipo, geo, r_obj, anel) in vila.OBJETOS:
        if tipo == "disco":
            cels = vila.disco(geo[0], geo[1], anel, r_obj)
        else:
            x1, z1, x2, z2 = geo
            cels = [(x, z) for x in range(x1 - anel, x2 + anel + 1) for z in range(z1 - anel, z2 + anel + 1) if not (x1 <= x <= x2 and z1 <= z <= z2)]
        for (x, z) in cels:
            if not (0 <= x < W and 0 <= z < D):
                continue
            for dy in (1, 2):
                n = nome(c.pegar(x, H[x][z] + dy, z))
                if solido(n):
                    erros.append(("E-15 sem caminho livre ao redor de %s" % nm, (x, H[x][z] + dy, z), n))
            if (x, z) in vila.AGUA:
                erros.append(("E-15 agua no anel de %s" % nm, (x, z), "agua"))
    # E-12 obstáculo sólido na rede de caminhos (rua, praça)
    perto = {(x + a, z + b) for (x, z) in vila.ocupado for a in range(-1, 2) for b in range(-1, 2)}
    for (_n, tp, g, _r, _a) in vila.OBJETOS:
        if tp == "ret":
            perto |= {(x, z) for x in range(g[0] - 1, g[2] + 2) for z in range(g[1] - 1, g[3] + 2)}
    perto |= {(x, z) for x in range(23, 30) for z in range(37, 44)}   # poço (telhado 5x5)
    for (x, z) in set(CAM) | set(PRACA):
        if not (0 <= x < W and 0 <= z < D) or (x, z) in perto or (32 <= x <= 35 and 41 <= z <= 46):
            continue
        if math.hypot(x - vila.FX, z - vila.FZ) <= vila.R_BORDA:
            continue
        for dy in (1, 2):
            n = nome(c.pegar(x, H[x][z] + dy, z))
            if solido(n) and not (n == "spruce_fence" and "lantern" in nome(c.pegar(x, H[x][z] + dy + 1, z))) and not (n == "stone_brick_wall" and nome(c.pegar(x, H[x][z] + dy + 1, z)) == "spruce_fence") and not (n == "spruce_fence" and nome(c.pegar(x, H[x][z] + dy - 1, z)) == "stone_brick_wall"):
                erros.append(("E-12 obstaculo no caminho/praca", (x, H[x][z] + dy, z), n))
    # E-19 degrau alto (>1) dentro da rede de caminhos
    rede = {k for k in (set(CAM) | set(PRACA)) if 0 <= k[0] < W and 0 <= k[1] < D}
    for (x, z) in rede:
        for dx, dz in ((1, 0), (0, 1)):
            q = (x + dx, z + dz)
            if q in rede and abs(H[x][z] - H[q[0]][q[1]]) > 1:
                erros.append(("E-19 degrau alto no caminho", (x, z), "dH=%d" % abs(H[x][z] - H[q[0]][q[1]])))
    return erros


if __name__ == "__main__":
    import collections
    erros = auditar()
    print("TOTAL:", len(erros))
    for k, v in collections.Counter(e[0] for e in erros).most_common():
        print("%4d  %s" % (v, k))
        for e in [e for e in erros if e[0] == k][:6]:
            print("        ", e[1], e[2])
