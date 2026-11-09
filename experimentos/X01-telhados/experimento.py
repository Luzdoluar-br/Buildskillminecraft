"""X01: sete tipos de telhado sobre a mesma caixa de pedra (9 x 7, 4 de altura), para comparar silhueta, custo em blocos e problemas.
Telhados: (a) duas águas 1:1, (b) duas águas 1:2 (escada+laje alternadas), (c) quatro águas, (d) mansarda (íngreme embaixo, suave em cima),
(e) abóbada de berço (curva) com e sem escadas de suavização, (f) pagode de dois beirais com cantos levantados, (g) plano com platibanda.
Rode: python experimento.py   (gera imagens/, saida/ e imprime o resumo)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from exp_util import *  # noqa: E402,F403

AQUI = Path(__file__).resolve().parent
c = Cena("x01_telhados", semente=5)
chao(c, -4, -6, 8 * 14 + 6, 16)
PEDRA = pal([("stone_bricks", 3), ("andesite", 2), ("tuff_bricks", 1.5)], 7)
ESC = "dark_oak_stairs"
LAJE = "dark_oak_slab"
contagem = {}


def caixa(i):
    m = Molde(c, i * 14, 0, 9, 7, 1)
    m.box(0, 0, 0, 8, 0, 6, PEDRA)
    m.oca(0, 1, 0, 8, 4, 6, PEDRA)
    m.limpar(4, 1, 6, 4, 2, 6)
    m.porta(4, 1, 6, "dark_oak")
    for lx in (2, 6):
        m.p(lx, 2, 6, M + "glass_pane")
    return m


def conta(nome, antes):
    contagem[nome] = len(c.blocos) - antes


# (a) duas águas 1:1 (o telhado do projeto das aulas)
m = caixa(0); n0 = len(c.blocos)
m.telhado_x(0, 8, 0, 6, 5, ESC, PEDRA, beiral=1, beiral_x=1, cumeeira=M + LAJE)
conta("a_duas_aguas_1_1", n0)

# (b) duas águas 1:2: método Molde.telhado_suave_x (escada nível k + laje nível k+1, enchimento sob a laje, empenas fechadas)
m = caixa(1); n0 = len(c.blocos)
m.telhado_suave_x(0, 8, 0, 6, 5, ESC, PEDRA, beiral=1, beiral_x=1)
conta("b_duas_aguas_1_2", n0)

# (c) quatro águas
m = caixa(2); n0 = len(c.blocos)
m.tenda(0, 8, 0, 6, 5, ESC, beiral=1)
conta("c_quatro_aguas", n0)

# (d) mansarda: 3 fileiras íngremes (1:1) e depois topo achatado em laje
m = caixa(3); n0 = len(c.blocos)
m.tenda(0, 8, 0, 6, 5, ESC, beiral=1, linhas=3)
m.box(2, 8, 2, 6, 8, 4, M + "dark_oak_planks")     # tampa plana
m.oca(1, 8, 1, 7, 8, 5, M + LAJE) if False else None
conta("d_mansarda", n0)

# (e) abóbada de berço ao longo de x. Perfil por coluna z: altura h(z) = round(sqrt(R^2 - d^2)).
R = 4.0
cx = 3.0
alturas = {z: round((R * R - (z - cx) ** 2) ** 0.5) for z in range(-1, 8) if (z - cx) ** 2 <= R * R + 0.5}
m = caixa(4); n0 = len(c.blocos)
for x in range(0, 9):
    for z, h in alturas.items():
        for y in range(5, 5 + h):
            m.p(x, y, z, M + "dark_oak_planks")                                    # (e1) só blocos, escadinha
conta("e1_abobada_blocos", n0)
m = caixa(5); n0 = len(c.blocos)
for x in range(0, 9):
    for z, h in alturas.items():
        vizinho = alturas.get(z + 1 if z < cx else z - 1, h)        # coluna mais próxima do centro
        d = SUL if z < cx else NORTE
        for y in range(5, 5 + h - 1):
            m.p(x, y, z, M + "dark_oak_planks")
        topo = 5 + h - 1
        if z != int(cx) and vizinho - h == 1:
            m.st(x, topo, z, ESC, d)           # (e2) degrau de suavização: a escada sobe em direção ao centro
        else:
            m.p(x, topo, z, M + "dark_oak_planks")
conta("e2_abobada_escadas", n0)

# (f) pagode: beiral largo de dois níveis com laje invertida por baixo e cantos levantados
m = caixa(6); n0 = len(c.blocos)
m.box(-1, 5, -1, 9, 5, 7, M + "spruce_planks")
m.tenda(0, 8, 0, 6, 6, [(ESC, 1)], beiral=2, linhas=2)
for (lx, lz) in ((-2, -2), (10, -2), (-2, 8), (10, 8)):
    m.sl(lx, 6, lz, "spruce", False)
for lx in range(-2, 11):
    for lz in (-2, 8):
        m.sl(lx, 5, lz, "spruce", True)
m.box(1, 8, 1, 7, 8, 5, M + "spruce_planks")
m.tenda(2, 6, 2, 4, 9, [(ESC, 1)], beiral=1)
conta("f_pagode", n0)

# (g) plano com platibanda e friso de laje
m = caixa(7); n0 = len(c.blocos)
m.box(0, 5, 0, 8, 5, 6, M + "smooth_stone")
for lx in range(0, 9):
    for lz in (0, 6):
        m.p(lx, 6, lz, M + "stone_brick_wall")
for lz in range(1, 6):
    for lx in (0, 8):
        m.p(lx, 6, lz, M + "stone_brick_wall")
for lx in range(-1, 10):
    for lz in (-1, 7):
        m.sl(lx, 5, lz, "stone_brick", False)
conta("g_plano_platibanda", n0)

erros, dims, npal, nb = fechar(c, AQUI, "x01_telhados", ignorar=("E-21",))
print("blocos:", nb, "dims:", dims, "paleta:", npal)
print("blocos por telhado:", contagem)
print(relatorio(erros))
vistas = {}
for i in range(8):
    x0 = i * 14 + 4
    vistas["telhado_%d" % i] = ((x0 - 9, 11, -12), (x0, 6, 3))
fotos(c, AQUI, vistas, w=700, h=450, fov=60)
