"""Auditoria automática da vila: roda TODAS as regras aprendidas (erros-e-licoes.md) em todas as estruturas.
Uso: python auditoria.py   (sai com lista de problemas; ideal = vazio)."""
import vila
from base import M

c, H, CAM, PRACA = vila.c, vila.H, vila.CAM, vila.PRACA_CEL
BRUTAS = {"spruce", "dark_oak", "pale_oak", "oak", "birch", "cherry", "stone_brick", "bed"}


def nome(b):
    if b is None:
        return "air"
    return (b if isinstance(b, str) else b[0]).replace("minecraft:", "")


def estado(b):
    return {} if b is None or isinstance(b, str) else b[1]


def passavel(n):
    """Blocos em que o jogador passa sem barrar (plantas, tapete, ar, lanterna no chão não conta como passagem livre mas não bloqueia)."""
    return n == "air" or any(k in n for k in ("grass", "fern", "tulip", "poppy", "cornflower", "bluet", "daisy", "valley", "dandelion", "berry", "azalea", "carpet", "lily_pad", "water", "farmland"))


def solido(n):
    return not passavel(n) and not any(k in n for k in ("lantern", "pane", "door"))


def auditar():
    erros = []
    # 1) IDs inválidos (E-01)
    for p, b in c.blocos.items():
        if nome(b) in BRUTAS:
            erros.append(("E-01 ID invalido", p, nome(b)))
    # 2) portas (E-02, E-03, E-10, E-11, E-12)
    for (x, y, z), b in c.blocos.items():
        if not (isinstance(b, tuple) and nome(b).endswith("_door") and not b[1].get("upper_block_bit")):
            continue
        if nome(c.pegar(x, y + 1, z)) != nome(b):
            erros.append(("E-03 porta sem metade de cima", (x, y, z), nome(b)))
        if c.pegar(x, y + 2, z) is None:
            erros.append(("E-10 vao acima da porta (falta verga)", (x, y, z), nome(b)))
        card = b[1].get("minecraft:cardinal_direction")
        dz = 1 if card == "south" else -1                      # lado de fora
        for lado, d in (("fora", dz), ("dentro", -dz)):
            for k in (1,):
                for dy in (0, 1):
                    n = nome(c.pegar(x, y + dy, z + d * k))
                    if solido(n):
                        erros.append(("E-02/E-12 porta barrada (%s, %d bloco(s))" % (lado, k), (x, y + dy, z + d * k), n))
        # E-11: batentes sólidos dos dois lados (nada de vidro/ar ao lado da porta)
        for ax in (-1, 1):
            for dy in (0, 1, 2):
                n = nome(c.pegar(x + ax, y + dy, z))
                if n == "air" or "pane" in n or "glass" in n:
                    erros.append(("E-11 porta desconexa da parede (batente %s)" % ("vidro" if n != "air" else "vazio"), (x + ax, y + dy, z), n))
    # 3) lanternas penduradas sem suporte (E-05)
    for (x, y, z), b in c.blocos.items():
        if nome(b) == "lantern" and estado(b).get("hanging") and c.pegar(x, y + 1, z) is None:
            erros.append(("E-05 lanterna pendurada sem suporte", (x, y, z), "lantern"))
    # 4) obstáculos em caminhos/praça (E-12): bloco sólido na altura do corpo
    isento = lambda x, z: (((x - vila.FX) ** 2 + (z - vila.FZ) ** 2) ** 0.5 <= 6.2
                           or any(bx <= x < bx + 5 and bz <= z < bz + 3 for bx, bz in ((21, 26), (35, 26), (21, 33), (35, 33)))
                           or (22 <= x <= 26 and 34 <= z <= 38) or (vila.ESC_X.start <= x < vila.ESC_X.stop and z in (23, 24)))
    perto = {(x + a, z + b) for (x, z) in vila.ocupado for a in range(-1, 2) for b in range(-1, 2)}
    for (x, z) in set(CAM) | set(PRACA):
        if not (0 <= x < vila.W and 0 <= z < vila.D) or isento(x, z) or (x, z) in perto or (32 <= x <= 35 and 41 <= z <= 46):
            continue
        for dy in (1, 2):
            n = nome(c.pegar(x, H[x][z] + dy, z))
            if solido(n) and "stairs" not in n and "slab" not in n and not (n == "spruce_fence" and "lantern" in nome(c.pegar(x, H[x][z] + dy + 1, z))):
                erros.append(("E-12 obstaculo no caminho/praca", (x, H[x][z] + dy, z), n))
            elif "stairs" in n and dy == 1:
                erros.append(("E-12 degrau/banco sobre caminho (confira)", (x, H[x][z] + dy, z), n))
    # 5) vazamento de água (E-06): água com ar ao lado no mesmo nível
    for (x, y, z), b in c.blocos.items():
        if nome(b) == "water":
            for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                if c.pegar(x + dx, y, z + dz) is None:
                    erros.append(("E-06 agua com ar ao lado (pode vazar)", (x, y, z), "water"))
                    break
    return erros


if __name__ == "__main__":
    import collections
    erros = auditar()
    resumo = collections.Counter(e[0] for e in erros)
    print("TOTAL:", len(erros))
    for k, v in resumo.most_common():
        print("%4d  %s" % (v, k))
        for e in [e for e in erros if e[0] == k][:6]:
            print("        ", e[1], e[2])
