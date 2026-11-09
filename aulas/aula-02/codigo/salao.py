"""Construção principal: o Salão da Vila, com nave de duas águas, torre-relógio central e escadaria."""
from casas2 import *  # noqa: F401,F403


def salao(c, x, z, y, flip=False):
    m = Molde(c, x, z, 21, 18, y, flip)
    fundacao(c, m)
    m.box(0, 0, 0, 20, 0, 12, PEDRA)
    m.box(1, 0, 1, 19, 0, 11, pal([("stone_bricks", 3), ("polished_andesite", 2), ("andesite", 1.5), ("tuff_bricks", 1)], 71))
    # ------------------------------------------------------------ nave: soco de pedra alto (4) + andar de reboco/madeira (2)
    m.oca(0, 1, 0, 20, 4, 12, PEDRA)
    for lx in range(21):
        for lz in (0, 12):
            m.p(lx, 4, lz, M + "polished_andesite")                      # friso (stringcourse)
    for lz in range(1, 12):
        for lx in (0, 20):
            m.p(lx, 4, lz, M + "polished_andesite")
    m.oca(0, 5, 0, 20, 6, 12, REBOCO)
    anel(m, 0, 0, 20, 12, 5, "stripped_dark_oak_log")
    anel(m, 0, 0, 20, 12, 7, "stripped_dark_oak_log")
    for lx in (0, 4, 8, 12, 16, 20):                                     # ritmo de pilares (P1)
        m.box(lx, 5, 12, lx, 7, 12, M + "stripped_dark_oak_log")
        m.box(lx, 5, 0, lx, 7, 0, M + "stripped_dark_oak_log")
    for lz in (0, 6, 12):
        for lx in (0, 20):
            m.box(lx, 5, lz, lx, 7, lz, M + "stripped_dark_oak_log")
    for (lx, lz) in ((0, 0), (20, 0), (0, 12), (20, 12)):
        m.box(lx, 1, lz, lx, 4, lz, PEDRA_ESCURA)                         # cantos
    # contrafortes na frente e no fundo entre as janelas (profundidade; 3 camadas na parede)
    for lx in (2, 6, 14, 18):
        for lz in (13,):
            m.box(lx, 1, lz, lx, 3, lz, PEDRA_ESCURA)
            m.st(lx, 4, lz, "stone_brick_stairs", SUL)
        m.box(lx, 1, -1, lx, 3, -1, PEDRA_ESCURA)
        m.st(lx, 4, -1, "stone_brick_stairs", NORTE)
    for lz in (3, 9):
        for lx in (-1, 21):
            m.box(lx, 1, lz, lx, 3, lz, PEDRA_ESCURA)
            m.st(lx, 4, lz, "stone_brick_stairs", OESTE if lx == -1 else LESTE)
    # janelas altas do soco (3 de altura, 1 de largura) com luz atrás
    for lx in (4, 12 - 6, 16):
        pass
    for lx in (4, 16, 10 - 4, 14):
        m.box(lx, 2, 12, lx, 4, 12, M + "glass_pane")
        m.box(lx, 2, 0, lx, 4, 0, M + "glass_pane")
    for lz in (3, 6, 9):
        for lx in (0, 20):
            m.box(lx, 2, lz, lx, 3, lz, M + "glass_pane")
    # janelas do andar de reboco
    for lx in (2, 6, 14, 18):
        m.p(lx, 6, 12, M + "white_stained_glass_pane")
        m.p(lx, 6, 0, M + "white_stained_glass_pane")
    # teto fechado e telhado de ardósia com cumeeira de cobre (accent 10%)
    m.box(0, 8, 0, 20, 8, 12, TABUA_ESCURA)
    alto = m.telhado_x(0, 20, 0, 12, 9, TELHA_ARDOSIA, REBOCO, beiral=1, beiral_x=1, cumeeira=M + "waxed_weathered_cut_copper_slab")
    for lx in (0, 20):
        for lz in (6,):
            m.box(lx, 9, lz, lx, alto - 1, lz, M + "stripped_dark_oak_log")
        m.p(lx, 10, 4, M + "white_stained_glass_pane")
        m.p(lx, 10, 8, M + "white_stained_glass_pane")
        m.p(lx, 11, 6, M + "white_stained_glass_pane") if False else None
    for lx in range(-1, 22):
        m.sl(lx, 8, 13, "dark_oak", True)                                 # forro do beiral (R3)
        m.sl(lx, 8, -1, "dark_oak", True)
    # chaminés duplas
    for lx in (3, 17):
        m.box(lx, 12, 2, lx, alto + 2, 3, PEDRA)
        m.box(lx, alto + 3, 2, lx, alto + 3, 3, M + "stone_brick_slab")
    # ------------------------------------------------------------ torre-relógio frontal (5x5, z 13..17)
    m.box(8, 0, 13, 12, 0, 17, PEDRA)
    m.oca(8, 1, 13, 12, 16, 17, PEDRA)
    for ly in (4, 9, 14):
        for lx in range(8, 13):
            for lz in (13, 17):
                m.p(lx, ly, lz, M + "polished_andesite")
        for lz in range(14, 17):
            for lx in (8, 12):
                m.p(lx, ly, lz, M + "polished_andesite")
    for (lx, lz) in ((8, 13), (12, 13), (8, 17), (12, 17)):
        m.box(lx, 1, lz, lx, 16, lz, PEDRA_ESCURA)
    # contrafortes inclinados na base da torre (taludes em escada)
    for lx in (8, 12):
        m.st(lx, 5, 18, "stone_brick_stairs", SUL)
        m.box(lx, 1, 18, lx, 4, 18, PEDRA_ESCURA)
    # entrada em arco, porta e janelas laterais
    m.limpar(9, 1, 17, 11, 3, 17)
    m.porta(10, 1, 17, "dark_oak")
    for lx in (9, 11):
        m.p(lx, 1, 17, M + "white_stained_glass_pane")
        m.p(lx, 2, 17, M + "white_stained_glass_pane")
    m.st(9, 3, 17, "stone_brick_stairs", LESTE, True)
    m.st(11, 3, 17, "stone_brick_stairs", OESTE, True)
    m.p(10, 3, 17, M + "dark_oak_slab") if False else None
    m.p(10, 3, 17, laje(M + "stone_brick_slab", True))
    m.limpar(10, 1, 13, 10, 2, 13)                                         # passagem tower -> nave
    m.limpar(10, 1, 12, 10, 2, 12)
    for lx in (8, 12):
        m.p(lx, 6, 15, M + "glass_pane")
    for lz in (14, 16):
        m.p(8, 6, lz, M + "glass_pane")
        m.p(12, 6, lz, M + "glass_pane")
    # relógio: face de concreto claro com ponteiros escuros na frente (z=18), 3x3
    for lx in (9, 10, 11):
        for ly in (10, 11, 12):
            m.p(lx, ly, 17, M + "white_concrete") if (lx, ly) != (10, 11) else m.p(lx, ly, 17, M + "black_concrete")
    m.p(10, 12, 17, M + "black_concrete")
    m.p(11, 11, 17, M + "black_concrete")
    # campanário (y 15..17): aberturas em arco nos quatro lados com lanterna
    for lx in (9, 11):
        m.limpar(lx, 15, 17, lx, 16, 17)
    for lx in (9, 11):
        m.limpar(lx, 15, 13, lx, 16, 13)
    for lz in (14, 16):
        m.limpar(8, 15, lz, 8, 16, lz)
        m.limpar(12, 15, lz, 12, 16, lz)
    m.box(9, 14, 14, 11, 14, 16, TABUA_ESCURA)
    m.p(10, 15, 15, (M + "lantern", {"hanging": False}))
    m.p(10, 14, 15, M + "polished_andesite") if False else None
    # telhado da torre: quatro águas de cobre, íngreme, com espigão
    m.box(8, 17, 13, 12, 17, 17, TABUA_ESCURA)
    topo = m.tenda(8, 12, 13, 17, 18, TELHA_COBRE, beiral=1)
    m.box(10, topo + 1, 15, 10, topo + 3, 15, M + "waxed_copper_block") if False else None
    for k in range(1, 4):
        m.p(10, topo + k, 15, M + "waxed_weathered_copper")
    m.p(10, topo + 4, 15, M + "lightning_rod")
    # ------------------------------------------------------------ interior do salão: mesas longas, bancos e candelabros
    m.box(2, 1, 2, 18, 1, 10, M + "light_gray_carpet") if False else None
    for lz in (3, 9):
        for lx in range(3, 18):
            m.p(lx, 1, lz, M + "spruce_fence") if lx % 4 == 0 else None
            m.sl(lx, 2, lz, "spruce", False) if lx % 4 != 0 else m.sl(lx, 2, lz, "spruce", False)
    for lz in (2, 4, 8, 10):
        for lx in range(4, 17, 2):
            m.st(lx, 1, lz, "spruce_stairs", SUL if lz in (2, 8) else NORTE)
    for lx in range(2, 19):
        m.p(lx, 1, 6, M + "light_gray_carpet")
    for lx in (5, 10, 15):
        m.p(lx, 7, 6, (M + "iron_chain", {"pillar_axis": "y"}))
        m.p(lx, 6, 6, (M + "iron_chain", {"pillar_axis": "y"}))
        m.p(lx, 5, 6, (M + "lantern", {"hanging": True}))
    m.box(1, 1, 5, 1, 3, 7, M + "bookshelf")
    m.p(19, 1, 3, (M + "barrel", {"facing_direction": 1, "open_bit": False}))
    m.p(19, 1, 4, (M + "barrel", {"facing_direction": 1, "open_bit": False}))
    m.p(19, 1, 9, M + "crafting_table")
    m.p(19, 1, 10, (M + "blast_furnace", {"facing_direction": 2}))
    m.p(10, 5, 11, (M + "lantern", {"hanging": True}))
    return m
