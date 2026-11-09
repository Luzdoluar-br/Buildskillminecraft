"""Casa do hortelão, casa de chá, horta."""
from casas import *  # noqa: F401,F403


# =====================================================================================================================
# 3. CASA DO HORTELÃO (empena virada para a frente, telhado de cobre oxidado, alpendre, horta cercada ao lado)
# =====================================================================================================================
def casa_hortelao(c, x, z, y, flip=False):
    m = Molde(c, x, z, 9, 14, y, flip)       # 9 em x, 14 em z (casa 9 x 10 mais alpendre)
    fundacao(c, m)
    m.box(0, 0, 0, 8, 0, 13, PEDRA)
    m.box(1, 0, 1, 7, 0, 9, TABUA_ESCURA)
    m.oca(0, 1, 0, 8, 1, 9, PEDRA)                       # soco de pedra
    m.oca(0, 2, 0, 8, 5, 9, REBOCO)                      # reboco claro
    anel(m, 0, 0, 8, 9, 2, "stripped_dark_oak_log")      # vigas: tronco escuro = esqueleto (T2)
    anel(m, 0, 0, 8, 9, 5, "stripped_dark_oak_log")
    for (lx, lz) in ((0, 0), (8, 0), (0, 9), (8, 9), (4, 0), (4, 9), (0, 5), (8, 5)):
        m.box(lx, 2, lz, lx, 5, lz, M + "stripped_dark_oak_log")
    for lz in (2, 7):
        for lx in (0, 8):
            m.p(lx, 3, lz, M + "white_stained_glass_pane")
            m.p(lx, 4, lz, M + "white_stained_glass_pane")
    for lx in (2, 6):
        m.p(lx, 3, 9, M + "white_stained_glass_pane")
        m.p(lx, 4, 9, M + "white_stained_glass_pane")
        m.sl(lx, 2, 10, "dark_oak", False)               # peitoril projetado
    m.limpar(4, 1, 9, 4, 3, 9)
    m.p(4, 4, 9, M + "stripped_dark_oak_log")
    m.porta(4, 1, 9, "dark_oak")
    # forro + telhado de cobre (cumeeira ao longo de z)
    m.box(0, 6, 0, 8, 6, 9, TABUA_ESCURA)
    alto = m.telhado_z(0, 8, 0, 9, 6, TELHA_COBRE, REBOCO, beiral=1, beiral_z=1, cumeeira=M + "waxed_weathered_cut_copper_slab")
    for ly in range(6, alto):
        m.p(4, ly, 9, M + "stripped_dark_oak_log")
    for k in range(1, 4):
        m.p(4 - k, 6 + k - 1, 9, M + "stripped_dark_oak_log")
        m.p(4 + k, 6 + k - 1, 9, M + "stripped_dark_oak_log")
    m.p(4, 7, 9, M + "white_stained_glass_pane")
    m.p(4, 8, 9, M + "white_stained_glass_pane")
    # alpendre: piso de pedra, 2 postes, telhado de uma água
    m.box(0, 0, 10, 8, 0, 13, PEDRA)
    for lx in (1, 7):
        m.box(lx, 1, 13, lx, 3, 13, M + "stripped_dark_oak_log")
    for lx in range(0, 9):
        m.st(lx, 4, 12, "dark_oak_stairs", NORTE)
        m.sl(lx, 4, 13, "dark_oak", False)
    m.box(0, 4, 10, 8, 4, 11, TABUA_ESCURA)
    m.p(2, 3, 13, (M + "lantern", {"hanging": True}))
    m.p(6, 3, 13, (M + "lantern", {"hanging": True}))
    m.st(3, 1, 12, "dark_oak_stairs", SUL)
    m.st(5, 1, 12, "dark_oak_stairs", SUL)
    m.p(1, 1, 11, (M + "barrel", {"facing_direction": 1, "open_bit": False}))
    m.p(7, 1, 11, (M + "barrel", {"facing_direction": 1, "open_bit": False}))
    m.box(6, 7, 3, 6, alto + 2, 3, PEDRA)                 # chaminé
    m.p(6, alto + 3, 3, M + "stone_brick_slab")
    # interior: cozinha
    m.p(1, 1, 1, M + "crafting_table")
    m.p(2, 1, 1, (M + "smoker", {"facing_direction": 3}))
    m.p(3, 1, 1, (M + "barrel", {"facing_direction": 1, "open_bit": False}))
    m.p(7, 1, 1, (M + "barrel", {"facing_direction": 1, "open_bit": False}))
    m.cama(6, 1, 6, 0)
    m.box(2, 1, 3, 5, 1, 7, M + "light_gray_carpet")
    m.box(1, 1, 8, 1, 2, 8, M + "bookshelf")
    m.p(4, 5, 5, (M + "lantern", {"hanging": True}))
    return m


def horta(c, x1, z1, x2, z2, y):
    """Horta cercada com canteiros de cenoura/batata/trigo alternando com água (y = nível do solo)."""
    r = random.Random(x1 * 31 + z1)
    for x in range(x1, x2 + 1):
        for z in range(z1, z2 + 1):
            if x in (x1, x2) or z in (z1, z2):
                c.ponto(x, y + 1, z, M + "spruce_fence")
            elif (x - x1) % 2 == 1:
                c.ponto(x, y, z, (M + "farmland", {"moisturized_amount": 7}))
                c.ponto(x, y + 1, z, (M + r.choice(["carrots", "potatoes", "wheat"]), {"growth": 7}))
            else:
                c.ponto(x, y, z, M + "water")
    c.ponto((x1 + x2) // 2, y + 1, z2, M + "air")


# =====================================================================================================================
# 4. CASA DE CHÁ (um andar + mirante, dois níveis de beiral largo, lanternas, cantos levantados)
# =====================================================================================================================
def casa_cha(c, x, z, y, flip=False):
    m = Molde(c, x, z, 13, 13, y, flip)
    fundacao(c, m)
    m.box(0, 0, 0, 12, 0, 12, PEDRA)                      # plataforma que ultrapassa as paredes (profundidade)
    m.box(1, 1, 1, 11, 1, 11, pal([("stone_bricks", 3), ("polished_andesite", 2), ("andesite", 1)], 61))
    m.oca(2, 2, 2, 10, 5, 10, REBOCO_CINZA)
    for lx in (2, 6, 10):
        for lz in (2, 6, 10):
            m.box(lx, 2, lz, lx, 5, lz, M + "stripped_dark_oak_log")
    anel(m, 2, 2, 10, 10, 2, "stripped_dark_oak_log")
    anel(m, 2, 2, 10, 10, 5, "stripped_dark_oak_log")
    for lx in (4, 8):
        for lz in (2, 10):
            m.p(lx, 3, lz, M + "white_stained_glass_pane")
            m.p(lx, 4, lz, M + "white_stained_glass_pane")
    for lz in (4, 8):
        for lx in (2, 10):
            m.p(lx, 3, lz, M + "white_stained_glass_pane")
            m.p(lx, 4, lz, M + "white_stained_glass_pane")
    m.limpar(6, 2, 10, 6, 4, 10)
    m.porta(6, 2, 10, "pale_oak")
    for lx in (5, 6, 7):
        m.st(lx, 1, 11, "stone_brick_stairs", SUL)
    # primeiro beiral: 2 linhas largas, forro de lajes invertidas sob a borda (R2/R3)
    m.box(1, 6, 1, 11, 6, 11, pal([("pale_oak_planks", 3), ("spruce_planks", 1)], 62))
    m.tenda(2, 10, 2, 10, 7, TELHA_CHA, beiral=2, linhas=2)
    for lx in range(0, 13):
        for lz in (0, 12):
            m.sl(lx, 6, lz, "pale_oak", True)
    for lz in range(1, 12):
        for lx in (0, 12):
            m.sl(lx, 6, lz, "pale_oak", True)
    m.box(1, 8, 1, 11, 8, 11, pal([("spruce_planks", 3), ("dark_oak_planks", 1)], 63))
    # mirante 5x5
    m.oca(4, 9, 4, 8, 11, 8, REBOCO_CINZA)
    for (lx, lz) in ((4, 4), (8, 4), (4, 8), (8, 8), (6, 4), (6, 8), (4, 6), (8, 6)):
        m.box(lx, 9, lz, lx, 11, lz, M + "stripped_dark_oak_log")
    for lz in (4, 8):
        for lx in (5, 7):
            m.p(lx, 10, lz, M + "white_stained_glass_pane")
    for lx in (4, 8):
        for lz in (5, 7):
            m.p(lx, 10, lz, M + "white_stained_glass_pane")
    m.box(4, 12, 4, 8, 12, 8, pal([("pale_oak_planks", 3), ("spruce_planks", 1)], 64))
    topo = m.tenda(4, 8, 4, 8, 13, TELHA_CHA, beiral=2)
    m.box(6, topo + 1, 6, 6, topo + 2, 6, M + "spruce_fence")
    m.p(6, topo + 3, 6, (M + "lantern", {"hanging": False}))
    for (lx, lz) in ((0, 0), (12, 0), (0, 12), (12, 12)):
        m.sl(lx, 7, lz, "spruce", False)                  # cantos levantados
    for (lx, lz) in ((1, 1), (11, 1), (1, 11), (11, 11)):
        m.p(lx, 5, lz, (M + "lantern", {"hanging": True}))
    # interior: salão de chá com mesa baixa
    m.box(3, 2, 3, 9, 2, 9, M + "light_gray_carpet")
    m.p(3, 3, 3, (M + "barrel", {"facing_direction": 1, "open_bit": False}))
    m.p(4, 3, 3, (M + "smoker", {"facing_direction": 3}))
    m.p(9, 3, 3, M + "crafting_table")
    m.p(3, 3, 9, M + "bookshelf")
    m.p(6, 3, 6, M + "spruce_fence")
    m.p(6, 5, 6, (M + "lantern", {"hanging": True}))
    for (lx, lz) in ((5, 5), (7, 5), (5, 7), (7, 7)):
        m.sl(lx, 3, lz, "spruce", False)
    m.cama(6, 9, 6, 3)
    return m
