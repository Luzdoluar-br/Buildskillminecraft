"""Vila Pedra-Musgo: montagem completa (terreno, casas, praça, caminhos, paisagismo)."""
import math
import random
import sys
from pathlib import Path

from base import *  # noqa: F401,F403
import salao as S

W, D = 60, 56
rnd = random.Random(2026)
c = Cena("vila_pedra_musgo", semente=17)

# ============================================================================================================ terreno
PONTE = (34, 47)          # centro da lagoa
LAGOA_A, LAGOA_B = 7.5, 5.0
pads = [
    (18, 2, 42, 22, 3, 3),      # terraço do Salão (nível 3)
    (19, 25, 41, 37, 1, 2),     # praça
    (0, 29, 18, 32, 1, 2), (42, 29, 59, 32, 1, 2),    # rua principal
    (2, 15, 18, 26, 1, 2),      # chalé
    (44, 15, 59, 26, 1, 2),     # casa de pedra
    (3, 35, 24, 50, 1, 2),      # casa do hortelão e horta
    (43, 37, 57, 51, 1, 2),     # casa de chá
]
fixas = {}
for x in range(W):
    for z in range(D):
        d = math.hypot((x - PONTE[0]) / LAGOA_A, (z - PONTE[1]) / LAGOA_B)
        if d <= 1.0:
            fixas[(x, z)] = -1
        elif d <= 1.38:
            fixas[(x, z)] = 0
H, FIXO = gerar_terreno(c, W, D, pads, 1.0, semente=5, fixas=fixas)
# moldura de colinas nas bordas (a vila fica numa clareira)
for x in range(W):
    for z in range(D):
        if not FIXO[x][z]:
            borda = min(x, W - 1 - x, z, D - 1 - z)
            if borda < 5:
                H[x][z] = min(H[x][z] + (5 - borda) // 2 + (1 if borda < 2 else 0), 4)
for _ in range(30):  # re-suaviza (inclinação <= 1 entre vizinhos)
    for x in range(W):
        for z in range(D):
            if FIXO[x][z]:
                continue
            viz = [H[a][b] for a, b in ((x + 1, z), (x - 1, z), (x, z + 1), (x, z - 1)) if 0 <= a < W and 0 <= b < D]
            lo, hi = max(viz) - 1, min(viz) + 1
            if lo <= hi:
                H[x][z] = min(max(H[x][z], lo), hi)
AGUA = {(x, z) for (x, z), n in fixas.items() if n == -1}

# escadaria do Salão: 2 degraus (z=24 -> y=2 ; z=23 -> y=3), 5 de largura
ESC_X = range(28, 33)
H_ESC = {24: 1, 23: 2}
for z, h in H_ESC.items():
    for x in ESC_X:
        H[x][z] = h

preencher_terreno(c, H, W, D)


def topo(x, z):
    return H[x][z]


# ============================================================================================================ caminhos
CAM = set()


def trilha(pts, larg=2, vai=0.6):
    for (a, b) in zip(pts, pts[1:]):
        (x1, z1), (x2, z2) = a, b
        n = max(abs(x2 - x1), abs(z2 - z1), 1)
        for i in range(n + 1):
            x = round(x1 + (x2 - x1) * i / n)
            z = round(z1 + (z2 - z1) * i / n)
            for dx in range(-(larg // 2), larg - larg // 2 + (1 if rnd.random() < vai else 0)):
                for dz in range(-(larg // 2), larg - larg // 2 + (1 if rnd.random() < vai else 0)):
                    xx, zz = x + dx, z + dz
                    if 0 <= xx < W and 0 <= zz < D and (xx, zz) not in AGUA:
                        CAM.add((xx, zz))


# rua principal (curva suave), ligações às portas, praça, lagoa
trilha([(0, 31), (10, 30), (19, 31), (30, 30), (41, 31), (50, 30), (59, 31)], 3, 0.35)
trilha([(9, 26), (9, 30)], 2)                 # chalé
trilha([(54, 26), (54, 30)], 2)               # casa de pedra
trilha([(8, 35), (8, 31)], 2)                 # hortelão
trilha([(50, 36), (50, 31)], 2)               # casa de chá
trilha([(32, 38), (34, 41)], 3, 0.5)          # praça -> lagoa
trilha([(30, 25), (30, 22)], 5, 0.0)          # praça -> escadaria

# ============================================================================================================ praça
PRACA_CEL = set()
for x in range(20, 41):
    for z in range(26, 37):
        # contorno irregular: cantos chanfrados
        if (x in (20, 40) or z in (26, 36)) and rnd.random() < 0.55:
            continue
        PRACA_CEL.add((x, z))

for (x, z) in CAM:
    if 0 <= x < W and 0 <= z < D:
        c.ponto(x, H[x][z], z, CAMINHO)
for (x, z) in PRACA_CEL:
    c.ponto(x, H[x][z], z, PRACA)
for x in ESC_X:
    for z in (23, 24):
        y = H[x][z]
        c.ponto(x, y, z, PEDRA)
        c.ponto(x, y + 1, z, escada(M + "stone_brick_stairs", NORTE))
for z in (23, 24):                      # muretas laterais da escadaria
    for x in (27, 33):
        y = H[x][z]
        c.ponto(x, y + 1, z, M + "stone_brick_wall") if False else None

# fonte (C3): bacia em degraus, pilar central, copa com água
FX, FZ = 30, 30
for x in range(FX - 6, FX + 7):
    for z in range(FZ - 6, FZ + 7):
        d = math.hypot(x - FX, z - FZ)
        y = H[x][z]
        if d <= 5.4:
            c.ponto(x, y, z, PRACA if d > 4.6 else PEDRA)
        if 4.0 < d <= 5.0:
            c.ponto(x, y + 1, z, PEDRA)
            c.ponto(x, y + 2, z, laje(M + "stone_brick_slab", False)) if 4.5 < d else c.ponto(x, y + 2, z, M + "stone_brick_wall") if False else None
        elif d <= 4.0:
            c.ponto(x, y, z, M + "stone_bricks")
            c.ponto(x, y + 1, z, (M + "water", {"liquid_depth": 0}))
y0 = H[FX][FZ]
for k in range(1, 4):
    c.ponto(FX, y0 + k, FZ, M + "stone_bricks")
c.ponto(FX, y0 + 4, FZ, PEDRA)
for (dx, dz) in ((1, 0), (-1, 0), (0, 1), (0, -1)):
    c.ponto(FX + dx, y0 + 4, FZ + dz, escada(M + "stone_brick_stairs", {(1, 0): OESTE, (-1, 0): LESTE, (0, 1): NORTE, (0, -1): SUL}[(dx, dz)], True)) if False else c.ponto(FX + dx, y0 + 4, FZ + dz, M + "stone_brick_wall")
c.ponto(FX, y0 + 5, FZ, (M + "water", {"liquid_depth": 0}))
for (dx, dz) in ((1, 0), (-1, 0), (0, 1), (0, -1)):
    c.ponto(FX + dx, y0 + 5, FZ + dz, M + "stone_brick_wall")
for k in range(1, 3):
    c.ponto(FX, y0 + 5 + k, FZ, (M + "iron_chain", {"pillar_axis": "y"}))
c.ponto(FX, y0 + 7, FZ, (M + "lantern", {"hanging": True}))
# espelho d'água extra no pilar: cascata de lajes e musgo
for (dx, dz) in ((2, 2), (-2, 2), (2, -2), (-2, -2)):
    c.ponto(FX + dx, y0 + 2, FZ + dz, M + "moss_carpet") if False else None

# bancos de pedra voltados para a fonte: FORA da rua (z 29..32), do eixo da escadaria do Salão e da trilha da lagoa (E-12)
for (bx, bz, d) in ((26, 36, NORTE), (34, 36, NORTE)):
    for k in (-1, 0, 1):
        xx, zz = bx + k, bz
        if 0 <= xx < W and 0 <= zz < D and (xx, zz) not in CAM:
            c.ponto(xx, H[xx][zz] + 1, zz, escada(M + "stone_brick_stairs", d))
    for k in (-2, 2):
        xx, zz = bx + k, bz
        if 0 <= xx < W and 0 <= zz < D and (xx, zz) not in CAM:
            c.ponto(xx, H[xx][zz] + 1, zz, M + "spruce_fence")
            c.ponto(xx, H[xx][zz] + 2, zz, (M + "lantern", {"hanging": False}))


# ============================================================================================================ poço (C2)
def poco(px, pz):
    y = H[px][pz]
    for dx in range(-1, 2):
        for dz in range(-1, 2):
            c.ponto(px + dx, y, pz + dz, PEDRA)
            if (dx, dz) != (0, 0):
                c.ponto(px + dx, y + 1, pz + dz, PEDRA)
                c.ponto(px + dx, y + 2, pz + dz, laje(M + "stone_brick_slab", False)) if False else None
    c.ponto(px, y, pz, M + "stone_bricks")
    c.ponto(px, y + 1, pz, (M + "water", {"liquid_depth": 0}))
    for (dx, dz) in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        for k in (2, 3):
            c.ponto(px + dx, y + k, pz + dz, M + "spruce_fence")
    for xx in range(px - 2, px + 3):
        for zz in range(pz - 2, pz + 3):
            if (xx, zz) not in {(px + a, pz + b) for a in range(-1, 2) for b in range(-1, 2)}:
                pass
    # telhado de escada (quatro águas) sobre os quatro postes
    m = Molde(c, px - 1, pz - 1, 3, 3, y, False)
    m.tenda(0, 2, 0, 2, 4, [("spruce_stairs", 5), ("dark_oak_stairs", 1.5)], beiral=1)
    m.p(1, 1, 1, (M + "air"))
    c.ponto(px, y + 4, pz, (M + "iron_chain", {"pillar_axis": "y"})) if False else None
    # entorno desgastado (grass_path, coarse_dirt) e baldes
    for xx in range(px - 3, px + 4):
        for zz in range(pz - 3, pz + 4):
            if 0 <= xx < W and 0 <= zz < D and (xx, zz) not in PRACA_CEL and abs(xx - px) + abs(zz - pz) < 5 and rnd.random() < 0.5:
                if "grass" in str(c.pegar(xx, H[xx][zz], zz)) or "moss" in str(c.pegar(xx, H[xx][zz], zz)):
                    c.ponto(xx, H[xx][zz], zz, pal([("grass_path", 3), ("coarse_dirt", 2)], 80 + xx))


poco(24, 22 + 14)   # (24, 36) no canto sudoeste da praça


# ============================================================================================================ barracas de feira
def barraca(bx, bz, flip, cor, produto):
    m = Molde(c, bx, bz, 5, 3, H[bx + 2][bz + 1], flip)
    for lx in (0, 4):
        for lz in (0, 2):
            m.box(lx, 1, lz, lx, 3, lz, M + "stripped_spruce_log")
    # balcão de lajes e barris
    for lx in range(1, 4):
        m.p(lx, 1, 2, laje(M + "spruce_slab", False))
    m.p(0, 1, 1, (M + "barrel", {"facing_direction": 1, "open_bit": False}))
    m.p(4, 1, 1, M + "crafting_table")
    for lx in range(1, 4):
        m.p(lx, 2, 2, M + produto[lx % len(produto)])
    # toldo listrado em lã, com beiral para a frente
    for lx in range(-1, 6):
        for lz in range(-1, 4):
            m.p(lx, 4, lz, M + (cor if (lx + 1) % 2 == 0 else "white_wool"))
    for lx in range(-1, 6):
        m.st(lx, 4, 4, "spruce_stairs", SUL) if False else None
    m.p(2, 3, 2, (M + "lantern", {"hanging": True}))
    m.p(2, 5, 1, laje(M + "spruce_slab", False)) if False else None


barraca(21, 26, False, "orange_wool", ["pumpkin", "hay_block", "melon_block"])
barraca(35, 26, False, "light_blue_wool", ["bookshelf", "barrel", "bookshelf"])
barraca(21, 33, True, "orange_wool", ["melon_block", "hay_block", "pumpkin"])
barraca(35, 33, True, "light_blue_wool", ["barrel", "hay_block", "barrel"])

# ============================================================================================================ construções
chale = S.chale_enxaimel(c, 3, 16, 1, False)
torreta = S.casa_torreta(c, 45, 16, 1, False)
hort = S.casa_hortelao(c, 4, 36, 1, True)
S.horta(c, 15, 38, 22, 47, 1)
cha = S.casa_cha(c, 44, 38, 1, True)
salao = S.salao(c, 20, 3, 3, False)

# ============================================================================================================ lagoa, píer, juncos
for (x, z) in AGUA:
    c.ponto(x, 0, z, (M + "water", {"liquid_depth": 0}))
    if rnd.random() < 0.18:
        c.ponto(x, 1, z, M + "lily_pad")
for x in range(W):
    for z in range(D):
        if (x, z) in AGUA:
            continue
        if any((x + a, z + b) in AGUA for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))) and H[x][z] == 0 and rnd.random() < 0.5:
            c.ponto(x, 1, z, (M + "reeds", {"age": 0})) if False else c.ponto(x, 1, z, M + "tall_grass")
# píer de madeira entrando na lagoa
for z in range(41, 47):
    c.ponto(33, 1, z, M + "spruce_planks")
    c.ponto(34, 1, z, M + "spruce_planks")
for z in (42, 46):
    for x in (32, 35):
        c.ponto(x, 1, z, M + "spruce_fence")
        c.ponto(x, 2, z, M + "spruce_fence")
        c.ponto(x, 0, z, M + "spruce_fence") if False else None
    c.ponto(32, 3, z, (M + "lantern", {"hanging": False}))

# ============================================================================================================ postes de iluminação (pescoço de ganso)
for (px, pz, dr) in ((8, 28, (0, 1)), (14, 33, (0, -1)), (22, 33, (0, -1)), (38, 28, (0, 1)), (47, 33, (0, -1)), (52, 28, (0, 1)),
                     (26, 25, (0, 1)), (34, 25, (0, 1)), (58, 33, (0, -1)), (2, 28, (0, 1)),
                     (30, 38, (1, 0)), (26, 39, (1, 0)), (35, 39, (-1, 0))):
    for _passo in range(8):          # no máximo 8 tentativas: sai da trilha para a esquerda (sem laço infinito)
        if (px, pz) not in CAM and (px + 1, pz) not in CAM and (px - 1, pz) not in CAM:
            break
        px -= 1
    c.poste(px, pz, 4, dr, 2)


# ============================================================================================================ árvores com raízes, galhos e copa persistente
def folha(nome):
    return Paleta([((M + nome, {"persistent_bit": True, "update_bit": False}), 9)], 3)


def arvore(x, z, altura, tronco, folha_nome, copa=3.0, galhos=True):
    base = c.chao(x, z)
    if base is None or "water" in str(c.pegar(x, base, z)):
        return False
    if any(abs(x - a) < 3 and abs(z - b) < 3 for a, b in ARV):
        return False
    if not c.arvore(x, None, z, altura, (M + tronco, {"pillar_axis": "y"}), folha(folha_nome), copa):
        return False
    ARV.append((x, z))
    y = base + 1
    # raízes aparentes: lajes e escadas escuras em volta do tronco (visual do dono)
    for (dx, dz, d) in ((1, 0, OESTE), (-1, 0, LESTE), (0, 1, NORTE), (0, -1, SUL)):
        xx, zz = x + dx, z + dz
        if 0 <= xx < W and 0 <= zz < D and c.pegar(xx, H[xx][zz] + 1, zz) is None and rnd.random() < 0.7:
            c.ponto(xx, H[xx][zz] + 1, zz, escada(M + "dark_oak_stairs" if "dark" in tronco or "spruce" in tronco else M + "oak_stairs", d, False))
    if galhos:    # galhos de tronco dentro da copa (V3)
        for _ in range(3):
            dx, dz = rnd.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            gy = y + altura - 2 - rnd.randint(0, 1)
            c.ponto(x + dx, gy, z + dz, (M + tronco, {"pillar_axis": "x" if dx else "z"}))
            c.ponto(x + dx * 2, gy + 1, z + dz * 2, (M + tronco, {"pillar_axis": "x" if dx else "z"}))
    # musgo ao pé (V2)
    for dx in range(-3, 4):
        for dz in range(-3, 4):
            xx, zz = x + dx, z + dz
            if 0 <= xx < W and 0 <= zz < D and (xx, zz) not in CAM and (xx, zz) not in PRACA_CEL and "grass_block" in str(c.pegar(xx, H[xx][zz], zz)) and math.hypot(dx, dz) <= 2.6 and rnd.random() < 0.55:
                c.ponto(xx, H[xx][zz], zz, M + "moss_block")
    return True


ARV = []
arvores = [
    # (x, z, altura, tronco, folha, copa)
    (15, 8, 8, "birch_log", "birch_leaves", 3.0), (45, 9, 9, "birch_log", "birch_leaves", 3.2), (17, 15, 7, "birch_log", "birch_leaves", 2.8),
    (43, 15, 7, "birch_log", "birch_leaves", 2.8),
    (17, 25, 6, "cherry_log", "cherry_leaves", 3.2), (43, 25, 6, "cherry_log", "cherry_leaves", 3.2), (22, 38, 6, "cherry_log", "cherry_leaves", 3.0),
    (4, 5, 11, "spruce_log", "spruce_leaves", 3.0), (9, 3, 10, "spruce_log", "spruce_leaves", 2.8), (52, 5, 11, "spruce_log", "spruce_leaves", 3.0),
    (56, 11, 10, "spruce_log", "spruce_leaves", 2.8), (24, 1, 9, "spruce_log", "spruce_leaves", 2.6), (36, 1, 9, "spruce_log", "spruce_leaves", 2.6),
    (3, 53, 10, "spruce_log", "spruce_leaves", 2.8), (58, 53, 10, "spruce_log", "spruce_leaves", 3.0), (20, 53, 9, "spruce_log", "spruce_leaves", 2.6),
    (11, 14, 7, "oak_log", "oak_leaves", 3.2), (40, 40, 7, "oak_log", "oak_leaves", 3.2), (26, 48, 7, "oak_log", "oak_leaves", 3.0),
    (36, 53, 8, "oak_log", "oak_leaves", 3.2),
    (58, 41, 8, "dark_oak_log", "dark_oak_leaves", 3.3), (47, 53, 8, "dark_oak_log", "dark_oak_leaves", 3.3), (2, 40, 8, "dark_oak_log", "dark_oak_leaves", 3.2),
    (57, 21, 8, "dark_oak_log", "dark_oak_leaves", 3.2), (1, 22, 8, "dark_oak_log", "dark_oak_leaves", 3.2),
]
posta = 0
for (x, z, a, t, f, cp) in arvores:
    posta += int(bool(arvore(x, z, a, t, f, cp)))
print("árvores plantadas:", posta, "de", len(arvores))

# ============================================================================================================ cobertura de solo e arbustos (V1)
FLORES = ["poppy", "dandelion", "cornflower", "azure_bluet", "oxeye_daisy", "pink_tulip", "white_tulip", "orange_tulip", "lily_of_the_valley"]
ocupado = set()
for m_ in (chale, torreta, hort, cha, salao):
    for lx in range(m_.w):
        for lz in range(m_.d):
            x, _, z = m_.mundo(lx, 0, lz)
            ocupado.add((x, z))
for x in range(W):
    for z in range(D):
        if (x, z) in AGUA or (x, z) in CAM or (x, z) in PRACA_CEL or (x, z) in ocupado:
            continue
        y = H[x][z]
        top = str(c.pegar(x, y, z))
        if "grass_block" not in top and "moss_block" not in top:
            continue
        if c.pegar(x, y + 1, z) is not None:
            continue
        r = rnd.random()
        if r < 0.40:
            c.ponto(x, y + 1, z, M + "short_grass")
        elif r < 0.50:
            c.ponto(x, y + 1, z, (M + "tall_grass", {"upper_block_bit": False}))
            c.ponto(x, y + 2, z, (M + "tall_grass", {"upper_block_bit": True}))
        elif r < 0.58:
            c.ponto(x, y + 1, z, M + "fern")
        elif r < 0.66:
            c.ponto(x, y + 1, z, M + rnd.choice(FLORES))
        elif r < 0.68:
            c.ponto(x, y + 1, z, (M + "sweet_berry_bush", {"growth": 3}))
        elif r < 0.71:
            c.ponto(x, y + 1, z, M + "moss_carpet")
# canteiros junto às casas: faixas de flores e arbustos de azaleia
for m_, sx in ((chale, 0), (torreta, 0), (hort, 0), (cha, 0)):
    for lx in range(-1, m_.w + 1):
        for lz in (-1, m_.d):
            x, _, z = m_.mundo(lx, 0, lz)
            if 0 <= x < W and 0 <= z < D and (x, z) not in CAM and "grass" in str(c.pegar(x, H[x][z], z)) and c.pegar(x, H[x][z] + 1, z) in (None,) or False:
                if 0 <= x < W and 0 <= z < D and "grass" in str(c.pegar(x, H[x][z], z)) and rnd.random() < 0.55:
                    c.ponto(x, H[x][z] + 1, z, M + rnd.choice(["flowering_azalea", "azalea", "rose_bush", "pink_tulip"]) if False else M + rnd.choice(["flowering_azalea", "azalea", "pink_tulip", "poppy"]))

# pedras soltas à beira da lagoa e da rua (cobble/mossy)
for _ in range(26):
    x, z = rnd.randint(2, W - 3), rnd.randint(2, D - 3)
    if (x, z) in CAM or (x, z) in PRACA_CEL or (x, z) in ocupado or (x, z) in AGUA:
        continue
    y = H[x][z]
    if "grass" in str(c.pegar(x, y, z)) and c.pegar(x, y + 1, z) is None:
        c.ponto(x, y + 1, z, pal([("mossy_cobblestone", 3), ("cobblestone", 2), ("andesite", 1)], 90 + x))

# ============================================================================================================ saída
def vergas_das_portas():
    """Toda porta tem 2 de altura: se a abertura na parede tem 3, o bloco acima da folha vira uma escada invertida no material da parede."""
    mapa = [("dark_oak", "dark_oak_stairs"), ("pale_oak", "pale_oak_stairs"), ("spruce", "spruce_stairs"), ("oak_planks", "oak_stairs"),
            ("stone_brick", "stone_brick_stairs"), ("andesite", "stone_brick_stairs"), ("tuff", "stone_brick_stairs"), ("cobble", "stone_brick_stairs"),
            ("calcite", "stone_brick_stairs"), ("concrete", "stone_brick_stairs"), ("diorite", "stone_brick_stairs")]
    feitos = []
    for (x, y, z), b in list(c.blocos.items()):
        if not (isinstance(b, tuple) and b[0].endswith("_door") and not b[1].get("upper_block_bit")):
            continue
        if c.pegar(x, y + 2, z) is not None:
            continue
        card = b[1].get("minecraft:cardinal_direction")
        dz = 1 if card == "south" else -1
        mat = None
        for (ax, az) in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            viz = c.pegar(x + ax, y + 2, z + az)
            nome = viz if isinstance(viz, str) else (viz[0] if viz else "")
            for chave, st in mapa:
                if chave in nome and "stairs" not in nome and "slab" not in nome:
                    mat = st
                    break
            if mat:
                break
        mat = mat or "stone_brick_stairs"
        # sobe na direção de dentro da casa: a quina baixa fica para fora, como um pingadeira
        c.ponto(x, y + 2, z, escada(M + mat, NORTE if dz == 1 else SUL, True))
        feitos.append(((x, y, z), mat))
    return feitos


def corrigir_lanternas():
    n = 0
    for (x, y, z), b in list(c.blocos.items()):
        if isinstance(b, tuple) and b[0] == M + "lantern" and b[1].get("hanging"):
            acima = c.pegar(x, y + 1, z)
            if acima is None:
                n += 1
                if c.pegar(x, y - 1, z) is not None:
                    c.ponto(x, y, z, (M + "lantern", {"hanging": False}))
                else:
                    c.ponto(x, y, z, M + "air")
    return n


corrigir_lanternas()
vergas_das_portas()

if __name__ == "__main__":
    avisos = c.validar()
    print("blocos:", len(c.blocos), "avisos:", [a for a in avisos][:8])
    (x0, y0, z0), (x1, y1, z1) = c.caixa_limite()
    print("caixa:", (x0, y0, z0), (x1, y1, z1), "dim", (x1 - x0 + 1, y1 - y0 + 1, z1 - z0 + 1))
    import exportar
    out = Path(__file__).parent / "saida"
    dims, npal = exportar.gravar(c, out / "vila_pedra_musgo.mcstructure")
    print("mcstructure gravado:", dims, "paleta:", npal)
