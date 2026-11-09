"""X02: fachadas com profundidade por estilo + tipos de janela, lado a lado.
Fachadas (17 de largura x 12 de altura), cada uma com 3 camadas de profundidade (recuo, plano principal, elementos salientes):
 F0 controle liso | F1 medieval (soco, enxaimel, avanço do andar) | F2 brutalista (módulos com janelas profundas) | F3 modernista (cortina de vidro, lajes)
 F4 gótica (janelas ogivais, contrafortes) | F5 japonesa (engawa, shoji, beiral largo).
Janelas (painéis 7 x 9): simples, com moldura, com persiana, ogival, em arco pleno, fenda (seteira), fita/cortina, redonda.
A profundidade é medida: número de planos distintos (valores de z ocupados) numa coluna típica da fachada.
Rode: python experimento.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from exp_util import *  # noqa: E402,F403

AQUI = Path(__file__).resolve().parent
c = Cena("x02_fachadas", semente=9)
chao(c, -4, -8, 6 * 22 + 6, 8, y=0, bloco=M + "smooth_stone")
planos = {}


def profundidade(nome, x, y0, y1, z_lo, z_hi):
    zs = set()
    for (xx, y, z), b in c.blocos.items():
        if xx == x and y0 <= y <= y1 and z_lo <= z <= z_hi:
            zs.add(z)
    planos[nome] = len(zs)


def parede(x0, z0, w, h, bloco, prof=1):
    c.caixa(x0, 1, z0, x0 + w - 1, h, z0 + prof - 1, bloco)


# ---------------- F0 controle
x0 = 0
parede(x0, 0, 17, 12, pal([("stone_bricks", 1)]))
for ly in (3, 7):
    for lx in (3, 8, 13):
        c.caixa(x0 + lx, ly, 0, x0 + lx + 1, ly + 2, 0, M + "glass_pane")
profundidade("F0_controle", x0 + 3, 1, 12, -3, 4)

# ---------------- F1 medieval (enxaimel com avanço)
x0 = 22
PEDRA = pal([("stone_bricks", 3), ("andesite", 2), ("cobblestone", 1)], 4)
parede(x0, 1, 17, 3, PEDRA, 2)                                              # soco recuado (camada 1)
c.caixa(x0, 4, 0, x0 + 16, 4, 0, M + "stripped_spruce_log")                # viga de respaldo
c.caixa(x0, 5, -1, x0 + 16, 5, 0, M + "spruce_planks")                      # piso do andar que AVANÇA 1 (camada 3)
for ly in range(6, 10):
    c.caixa(x0, ly, -1, x0 + 16, ly, -1, pal([("calcite", 3), ("diorite", 1)], 5))
for lx in (0, 4, 8, 12, 16):
    c.caixa(x0 + lx, 6, -1, x0 + lx, 9, -1, M + "stripped_spruce_log")      # pilares
c.caixa(x0, 10, -1, x0 + 16, 10, -1, M + "stripped_spruce_log")
for lx in (2, 6, 10, 14):
    c.caixa(x0 + lx, 7, -1, x0 + lx, 8, -1, M + "glass_pane")
for lx in (2, 8, 14):
    c.caixa(x0 + lx, 2, 1, x0 + lx, 3, 1, M + "glass_pane")
for lx in range(1, 16, 2):
    c.ponto(x0 + lx, 4, -1, escada(M + "spruce_stairs", NORTE, True))        # mãos-francesas sob o avanço
profundidade("F1_medieval", x0 + 4, 1, 12, -3, 4)

# ---------------- F2 brutalista: massa de concreto, módulos repetidos, janelas fundas (recuo 2) e brises salientes
x0 = 44
CONC = pal([("light_gray_concrete", 5), ("stone", 1), ("andesite", 1)], 6)
parede(x0, 0, 17, 12, CONC, 3)
for ly in (2, 5, 8):
    for lx in (1, 5, 9, 13):
        c.caixa(x0 + lx, ly, 0, x0 + lx + 2, ly + 1, 2, M + "air")           # recesso de 3 de profundidade
        c.caixa(x0 + lx, ly, 2, x0 + lx + 2, ly + 1, 2, M + "glass_pane")      # vidro no fundo
for ly in (4, 7, 10):
    c.caixa(x0, ly, -1, x0 + 16, ly, -1, M + "smooth_stone_slab") if False else None
    for lx in range(0, 17):
        c.ponto(x0 + lx, ly, -1, laje(M + "normal_stone_slab", False))              # brise/laje saliente em cada piso
c.caixa(x0, 12, -1, x0 + 16, 12, 0, CONC)                                    # cornija pesada
profundidade("F2_brutalista", x0 + 2, 1, 12, -3, 4)

# ---------------- F3 modernista: pilotis, cortina de vidro com montantes a cada 3, faixas de laje
x0 = 66
for lx in range(0, 17, 4):
    c.caixa(x0 + lx, 1, 1, x0 + lx, 3, 1, M + "white_concrete")               # pilotis (térreo livre)
for ly in (4, 8, 12):
    c.caixa(x0, ly, 0, x0 + 16, ly, 2, M + "white_concrete")                  # lajes de piso salientes
for ly in (5, 9):
    for lx in range(0, 17):
        c.caixa(x0 + lx, ly, 1, x0 + lx, ly + 2, 1, M + ("white_concrete" if lx % 3 == 0 else "light_blue_stained_glass"))
c.caixa(x0, 13, 0, x0 + 16, 13, 2, M + "white_concrete_slab") if False else None
profundidade("F3_modernista", x0 + 3, 1, 13, -3, 4)

# ---------------- F4 gótica: contrafortes, janelas ogivais com moldura, friso
x0 = 88
GRAN = pal([("stone_bricks", 3), ("polished_andesite", 1), ("andesite", 2)], 8)
parede(x0, 1, 17, 11, GRAN, 2)
for lx in (0, 4, 8, 12, 16):                                                  # contrafortes salientes (camada 3)
    c.caixa(x0 + lx, 1, -2, x0 + lx, 9, -1, GRAN)
    c.ponto(x0 + lx, 10, -2, escada(M + "stone_brick_stairs", SUL))
    c.ponto(x0 + lx, 10, -1, M + "stone_bricks")
for lx in (2, 6, 10, 14):                                                     # janela ogival 1x5 com cantos em escada
    c.caixa(x0 + lx, 3, 1, x0 + lx, 7, 2, M + "air")
    c.caixa(x0 + lx, 3, 2, x0 + lx, 7, 2, M + "glass_pane")
    c.ponto(x0 + lx - 1, 8, 1, escada(M + "stone_brick_stairs", LESTE, True))
    c.ponto(x0 + lx + 1, 8, 1, escada(M + "stone_brick_stairs", OESTE, True))
    c.ponto(x0 + lx, 8, 1, M + "stone_bricks")
c.caixa(x0, 11, -1, x0 + 16, 11, 0, M + "polished_andesite")
profundidade("F4_gotica", x0 + 2, 1, 12, -3, 4)

# ---------------- F5 japonesa: base de pedra, engawa (varanda) com pilares, shoji recuado, beiral largo
x0 = 110
parede(x0, 2, 17, 1, M + "stone_bricks", 1) if False else None
c.caixa(x0, 1, -2, x0 + 16, 1, 3, pal([("stone_bricks", 3), ("andesite", 1)], 2))        # plataforma
c.caixa(x0, 2, -2, x0 + 16, 2, -2, M + "pale_oak_planks")                              # engawa (piso de madeira)
c.caixa(x0, 2, -1, x0 + 16, 2, 1, M + "pale_oak_planks")
for lx in range(0, 17, 4):
    c.caixa(x0 + lx, 2, -1, x0 + lx, 7, -1, M + "stripped_dark_oak_log")             # pilares da frente (camada 3)
c.caixa(x0 + 1, 3, 2, x0 + 15, 6, 2, M + "white_stained_glass_pane")                # shoji recuado (camada 1)
for lx in range(0, 17, 2):
    c.caixa(x0 + lx, 3, 2, x0 + lx, 6, 2, M + "spruce_trapdoor") if False else None
for lx in range(1, 16, 4):
    c.caixa(x0 + lx, 3, 2, x0 + lx, 6, 2, M + "stripped_dark_oak_log")
c.caixa(x0 - 1, 7, -3, x0 + 17, 7, 3, M + "dark_oak_planks")                          # viga/forro do beiral
for lx in range(-1, 18):
    c.ponto(x0 + lx, 8, -3, escada(M + "spruce_stairs", SUL))                       # beiral largo
    c.ponto(x0 + lx, 9, -2, escada(M + "spruce_stairs", SUL))
c.caixa(x0 - 1, 10, -1, x0 + 17, 10, 3, M + "spruce_planks")
profundidade("F5_japonesa", x0 + 4, 1, 12, -4, 4)

# ---------------- janelas (painéis independentes, 7 x 9, parede de pedra)
base_z = 20
chao(c, -4, 12, 6 * 22 + 6, 28, y=0, bloco=M + "smooth_stone")
tipos = ["simples", "moldura", "persiana", "ogival", "arco_pleno", "seteira", "fita", "redonda"]
for k, t in enumerate(tipos):
    x = k * 12
    c.caixa(x, 1, base_z, x + 8, 9, base_z + 1, pal([("stone_bricks", 3), ("andesite", 1)], 20 + k))
    cx = x + 4
    if t == "simples":
        c.caixa(cx, 4, base_z, cx, 5, base_z, M + "glass_pane")
    elif t == "moldura":
        c.caixa(cx - 1, 3, base_z, cx + 1, 6, base_z, M + "air")
        c.caixa(cx, 4, base_z + 1, cx, 5, base_z + 1, M + "glass_pane")
        for dx in (-1, 0, 1):
            c.ponto(cx + dx, 6, base_z, M + "stone_brick_stairs") if False else c.ponto(cx + dx, 6, base_z, escada(M + "stone_brick_stairs", SUL, True))
            c.ponto(cx + dx, 3, base_z, laje(M + "stone_brick_slab", False))
        c.ponto(cx - 1, 4, base_z, M + "polished_andesite"); c.ponto(cx - 1, 5, base_z, M + "polished_andesite")
        c.ponto(cx + 1, 4, base_z, M + "polished_andesite"); c.ponto(cx + 1, 5, base_z, M + "polished_andesite")
    elif t == "persiana":
        c.caixa(cx, 4, base_z, cx, 5, base_z, M + "glass_pane")
        for dy in (4, 5):
            c.ponto(cx - 1, dy, base_z - 1, (M + "spruce_trapdoor", {"direction": 0, "open_bit": True, "upside_down_bit": False}))
            c.ponto(cx + 1, dy, base_z - 1, (M + "spruce_trapdoor", {"direction": 1, "open_bit": True, "upside_down_bit": False}))
    elif t == "ogival":
        c.caixa(cx, 3, base_z, cx, 6, base_z, M + "glass_pane")
        c.ponto(cx - 1, 7, base_z, escada(M + "stone_brick_stairs", LESTE, True))
        c.ponto(cx + 1, 7, base_z, escada(M + "stone_brick_stairs", OESTE, True))
        c.ponto(cx, 7, base_z, M + "glass_pane")
        c.ponto(cx - 1, 6, base_z, M + "air"); c.ponto(cx + 1, 6, base_z, M + "air")
    elif t == "arco_pleno":
        c.caixa(cx - 1, 3, base_z, cx + 1, 5, base_z, M + "glass_pane")
        c.ponto(cx - 1, 6, base_z, escada(M + "stone_brick_stairs", LESTE, True)); c.ponto(cx + 1, 6, base_z, escada(M + "stone_brick_stairs", OESTE, True))
        c.ponto(cx, 6, base_z, M + "glass_pane")
    elif t == "seteira":
        c.caixa(cx, 3, base_z, cx, 6, base_z + 1, M + "air")
        c.caixa(cx, 3, base_z + 1, cx, 6, base_z + 1, M + "iron_bars")
    elif t == "fita":
        c.caixa(x + 1, 4, base_z, x + 7, 5, base_z, M + "glass_pane")
        for dx in (1, 4, 7):
            c.caixa(x + dx, 4, base_z, x + dx, 5, base_z, M + "stone_bricks")
    elif t == "redonda":
        for (dx, dy) in ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, 1), (1, 1), (-1, -1), (1, -1)):
            c.ponto(cx + dx, 5 + dy, base_z, M + "glass_pane") if False else None
        c.caixa(cx - 1, 4, base_z, cx + 1, 6, base_z, M + "glass")
        for (dx, dy) in ((-1, 4), (1, 4), (-1, 6), (1, 6)):
            c.ponto(cx + dx, dy, base_z, M + "stone_bricks")
        c.ponto(cx, 5, base_z, M + "black_stained_glass_pane") if False else None

erros, dims, n, nb = fechar(c, AQUI, "x02_fachadas", ignorar=("E-21",))
print("blocos:", nb, "dims:", dims, "paleta:", n)
print("planos de profundidade por fachada (nº de valores de z distintos numa coluna):", planos)
print(relatorio(erros))
vistas = {}
for k in range(6):
    x0 = k * 22
    vistas["fachada_%d_frente" % k] = ((x0 + 8, 6, -14), (x0 + 8, 6, 0))
    vistas["fachada_%d_obliqua" % k] = ((x0 - 8, 7, -9), (x0 + 8, 6, 0))
for k in range(8):
    x = k * 12 + 4
    vistas["janela_%d" % k] = ((x, 5, base_z - 8), (x, 5, base_z))
fotos(c, AQUI, vistas, w=640, h=420, fov=60)
