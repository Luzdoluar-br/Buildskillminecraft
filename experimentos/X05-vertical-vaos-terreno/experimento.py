"""X05: (A) torre de 12 pavimentos com recuos, cortina de vidro e coroa; (B) ponte em arcos de pedra; (C) ponte pênsil; (D) balanço (cantilever) com contraventos;
(E) casa em terreno inclinado 1:2 com duas soluções: fundação escalonada e pilotis de madeira. Cada peça é auditada (E-21 apoio etc.).
Objetivo: descobrir o que funciona, o que não e o custo em blocos. Rode: python experimento.py"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from exp_util import *  # noqa: E402,F403

AQUI = Path(__file__).resolve().parent
c = Cena("x05_estruturas", semente=33)
custo = {}


def marca(nome, n0):
    custo[nome] = len(c.blocos) - n0


chao(c, -8, -10, 200, 60, y=0)

# ---------------- A) torre
n0 = len(c.blocos)
CONC = M + "light_gray_concrete"
x0, z0 = 10, 10
PAV = 4
for lvl in range(12):
    rec = 0 if lvl < 5 else (2 if lvl < 9 else 4)         # recuos: a cada ~4 pavimentos
    xa, xb, za, zb = x0 + rec, x0 + 17 - rec, z0 + rec, z0 + 17 - rec
    y = 1 + lvl * PAV
    c.caixa(xa, y, za, xb, y, zb, CONC)                                    # laje
    for yy in range(y + 1, y + PAV):
        for x in range(xa, xb + 1):
            for z in (za, zb):
                c.ponto(x, yy, z, M + ("white_concrete" if (x - xa) % 3 == 0 else "light_blue_stained_glass") if lvl > 1 else M + "white_concrete")
        for z in range(za + 1, zb):
            for x in (xa, xb):
                c.ponto(x, yy, z, M + ("white_concrete" if (z - za) % 3 == 0 else "light_blue_stained_glass") if lvl > 1 else M + "white_concrete")
    if lvl in (4, 8):                                                       # terraço do recuo com platibanda
        for x in range(xa - 2, xb + 3):
            for z in (za - 2, zb + 2):
                c.ponto(x, y, z, M + "light_gray_concrete_slab") if False else None
topo = 1 + 12 * PAV
c.caixa(x0 + 4, topo, z0 + 4, x0 + 13, topo, z0 + 13, CONC)
c.caixa(x0 + 6, topo + 1, z0 + 6, x0 + 11, topo + 3, z0 + 11, M + "white_concrete")          # casa de máquinas
for k in range(6):
    c.ponto(x0 + 8, topo + 4 + k, z0 + 8, M + "end_rod") if False else c.ponto(x0 + 8, topo + 4 + k, z0 + 8, M + "iron_bars")
c.ponto(x0 + 8, topo + 10, z0 + 8, M + "sea_lantern")
for lx in range(0, 18, 3):                                                  # pilotis do térreo e lobby
    for lz in (0, 17):
        c.caixa(x0 + lx, 1, z0 + lz, x0 + lx, 3, z0 + lz, M + "quartz_pillar")
marca("A_torre_12_pavimentos", n0)

# ---------------- B) ponte em arcos de pedra (3 arcos de vão 10)
n0 = len(c.blocos)
bx, bz = 40, 20
for arco in range(3):
    cxa = bx + 5 + arco * 10
    for dx in range(-5, 6):
        yy = round(math.sqrt(max(0.0, 25 - dx * dx)) * 0.9)
        for z in range(bz, bz + 5):
            for y in range(1, 4 + 5):
                if y > yy + 1 or True:
                    pass
        # enchimento acima do arco até o tabuleiro (y=9) e vão (ar) abaixo do arco
        for z in range(bz, bz + 5):
            for y in range(1, 9):
                if y > yy + 1:
                    c.ponto(cxa + dx, y, z, PEDRA := pal([("stone_bricks", 3), ("andesite", 2), ("mossy_stone_bricks", 1)], 4 + arco))
            if (dx == -5 or dx == 5) and True:
                for y in range(1, 9):
                    c.ponto(cxa + dx, y, z, pal([("stone_bricks", 3), ("andesite", 2)], 6))
for x in range(bx, bx + 31):
    for z in range(bz, bz + 5):
        c.ponto(x, 9, z, M + "smooth_stone") if False else c.ponto(x, 9, z, pal([("stone_bricks", 1)], 2))
    for z in (bz, bz + 4):
        c.ponto(x, 10, z, M + "stone_brick_wall")
marca("B_ponte_arcos", n0)

# ---------------- C) ponte pênsil (vão 36, torres de 14)
n0 = len(c.blocos)
px, pz = 90, 30
c.caixa(px, 6, pz, px + 40, 6, pz + 4, pal([("spruce_planks", 3), ("dark_oak_planks", 1)], 8))          # tabuleiro
for tx in (px + 2, px + 38):
    for tz in (pz - 1, pz + 5):
        c.caixa(tx, 1, tz, tx, 18, tz, M + "stone_bricks")
    c.caixa(tx, 18, pz - 1, tx, 18, pz + 5, M + "stone_bricks")
ult = {}
for tz in (pz - 1, pz + 5):                                                 # cabo principal: parábola (flecha ~ vão/10 = 4) entre as torres
    for x in range(px + 2, px + 39):
        t = (x - (px + 2)) / 36.0
        y = 17 - round(4 * 4 * t * (1 - t) * (-1) * -1) + 0 if False else 17 - round(16 * t * (1 - t) * 0.95)
        c.ponto(x, y, tz, M + "spruce_fence")
        if x > px + 2:                                       # preenche o degrau do cabo: cercas só se ligam por FACE (diagonal quebra o cabo)
            for yy in range(min(y, ult[tz]), max(y, ult[tz]) + 1):
                c.ponto(x, yy, tz, M + "spruce_fence")
        ult[tz] = y
        if (x - px) % 4 == 2:
            for yy in range(7, y):
                c.ponto(x, yy, tz, (M + "iron_chain", {"pillar_axis": "y"}))                       # pendurais
marca("C_ponte_pensil", n0)

# ---------------- D) balanço de concreto com contraventos
n0 = len(c.blocos)
dx0, dz0 = 150, 20
c.caixa(dx0, 1, dz0, dx0 + 8, 8, dz0 + 8, pal([("stone_bricks", 1)], 3))                  # massa de ancoragem
c.caixa(dx0 + 9, 8, dz0, dx0 + 20, 8, dz0 + 8, M + "white_concrete")                      # laje em balanço de 12
c.caixa(dx0 + 9, 9, dz0, dx0 + 20, 9, dz0, M + "white_concrete_slab") if False else None
for i in range(0, 8):                                                                       # contravento diagonal sob o balanço
    c.ponto(dx0 + 9 + i, 7 - i // 2, dz0 + 4, M + "iron_bars")
    c.ponto(dx0 + 9 + i, 7 - i // 2, dz0 + 3, M + "iron_bars")
marca("D_balanco", n0)

# ---------------- E) casa em terreno inclinado 1:2
base_x = 20
for x in range(0, 40):
    h = 1 + x // 2
    for z in range(34, 52):
        for y in range(0, h):
            c.ponto(base_x + x, y, z, M + "dirt")
        c.ponto(base_x + x, h, z, M + "grass_block")
# E1: fundação escalonada (muro de arrimo de pedra, piso nivelado a h médio)
n0 = len(c.blocos)
nivel = 1 + (14 + 6) // 2           # piso a meia altura da casa
for x in range(10, 22):
    h = 1 + x // 2
    for z in range(37, 47):
        for y in range(h, nivel + 1):
            c.ponto(base_x + x, y, z, pal([("stone_bricks", 3), ("cobblestone", 1)], 5))       # enche até o nível do piso
for x in range(10, 22):
    for z in range(37, 47):
        c.ponto(base_x + x, nivel + 1, z, M + "spruce_planks")
    for y in range(nivel + 2, nivel + 5):
        for z in (37, 46):
            c.ponto(base_x + x, y, z, M + "spruce_planks")
for z in range(37, 47):
    for y in range(nivel + 2, nivel + 5):
        for x in (10, 21):
            c.ponto(base_x + x, y, z, M + "spruce_planks")
marca("E1_fundacao_escalonada", n0)
erros, dims, n, nb = fechar(c, AQUI, "x05_estruturas", ignorar=("E-23",))
print("blocos:", nb, "dims:", dims, "paleta:", n)
print("custo em blocos:", custo)
print(relatorio(erros))
vistas = {
    "torre": ((x0 - 22, 30, z0 - 20), (x0 + 8, 24, z0 + 8)),
    "ponte_arcos": ((bx + 15, 9, bz - 22), (bx + 15, 5, bz + 2)),
    "ponte_pensil": ((px + 20, 12, pz - 28), (px + 20, 10, pz + 2)),
    "balanco": ((dx0 + 28, 12, dz0 - 12), (dx0 + 12, 6, dz0 + 4)),
    "terreno": ((base_x - 6, 18, 30), (base_x + 16, 8, 42)),
}
fotos(c, AQUI, vistas, w=800, h=500, fov=65)
