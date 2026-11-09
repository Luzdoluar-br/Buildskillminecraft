"""Construções da Vila Pedra-Musgo. Cada função recebe o canto mínimo (x, z) da pegada, o y do piso e se a fachada olha para o norte (flip)."""
from base import *  # noqa: F401,F403

TELHA_MADEIRA = [("dark_oak_stairs", 7), ("spruce_stairs", 1.0)]
TELHA_ARDOSIA = [("deepslate_tile_stairs", 6), ("cobbled_deepslate_stairs", 2.5), ("stone_brick_stairs", 0.5)]
TELHA_COBRE = [("waxed_oxidized_cut_copper_stairs", 5), ("waxed_weathered_cut_copper_stairs", 3), ("waxed_cut_copper_stairs", 0.3)]
TELHA_CHA = [("spruce_stairs", 5), ("dark_oak_stairs", 1.5)]
TABUA_ESCURA = pal([("dark_oak_planks", 5), ("spruce_planks", 1.5)], 31)
TABUA_CLARA = pal([("spruce_planks", 4), ("oak_planks", 2), ("dark_oak_planks", 1)], 32)


def fundacao(c, m):
    """Enche de pedra do fundo do terreno até o piso, para a casa nunca ficar no ar em terreno irregular."""
    for lx in range(m.w):
        for lz in range(m.d):
            x, y, z = m.mundo(lx, 0, lz)
            for yy in range(y - 4, y):
                if c.pegar(x, yy, z) is None or True:
                    c.ponto(x, yy, z, PEDRA_ESCURA)


def anel(m, x1, z1, x2, z2, y, b, eixo=True):
    """Moldura horizontal (viga) em tronco: lados maiores em x e menores em z."""
    for lx in range(x1, x2 + 1):
        m.log(lx, y, z1, b, "x")
        m.log(lx, y, z2, b, "x")
    for lz in range(z1 + 1, z2):
        m.log(x1, y, lz, b, "z")
        m.log(x2, y, lz, b, "z")


def janela(m, x, y, z, h=2, vidro="white_stained_glass_pane", persiana=None):
    for k in range(h):
        m.p(x, y + k, z, M + vidro)


def luz_interna(m, x, y, z):
    m.p(x, y, z, (M + "lantern", {"hanging": True}))


# =====================================================================================================================
# 1. CHALÉ DE ENXAIMEL  (andar de cima avança sobre pórtico; telhado de duas águas com empena cruzada na frente)
# =====================================================================================================================
def chale_enxaimel(c, x, z, y, flip=False):
    m = Molde(c, x, z, 13, 9, y, flip)
    fundacao(c, m)
    m.box(0, 0, 0, 12, 0, 8, PEDRA)
    m.box(1, 0, 1, 11, 0, 6, TABUA_CLARA)
    # térreo: base de pedra misturada, cantos em tronco, viga de respaldo
    m.oca(0, 1, 0, 12, 2, 7, PEDRA)
    anel(m, 0, 0, 12, 7, 3, "stripped_spruce_log")
    for (lx, lz) in ((0, 0), (12, 0), (0, 7), (12, 7)):
        m.box(lx, 1, lz, lx, 2, lz, M + "stripped_spruce_log")
    for lx in (2, 3, 9, 10):
        m.p(lx, 2, 7, M + "white_stained_glass_pane")
        m.sl(lx, 1, 8, "stone_brick", False)        # soleira projetada
    for lx in (1, 11):
        m.p(lx, 2, 0, M + "white_stained_glass_pane")
    m.limpar(6, 1, 7, 6, 2, 7)
    m.porta(6, 1, 7, "spruce")
    m.st(6, 1, 8, "stone_brick_stairs", SUL)       # degrau
    # pórtico sob o avanço do andar de cima: postes + viga + mãos-francesas (profundidade e elementos projetados)
    for lx in (0, 4, 8, 12):
        m.box(lx, 1, 8, lx, 2, 8, M + "stripped_spruce_log")
    for lx in range(13):
        m.log(lx, 3, 8, "stripped_spruce_log", "x")
    for lx in (1, 3, 5, 7, 9, 11):
        m.st(lx, 2, 8, "spruce_stairs", NORTE, True)
    # piso de cima
    m.box(0, 4, 0, 12, 4, 8, TABUA_CLARA)
    m.limpar(11, 4, 1, 11, 4, 3)
    for lz in range(1, 5):
        m.st(11, lz, lz, "spruce_stairs", SUL)
    # andar de cima: 4 camadas, reboco com ritmo de pilares a cada 4 (P1); viga baixa e viga alta em tronco
    m.oca(0, 5, 0, 12, 8, 8, REBOCO)
    anel(m, 0, 0, 12, 8, 5, "stripped_spruce_log")
    anel(m, 0, 0, 12, 8, 8, "stripped_spruce_log")
    for lx in (0, 6, 12):
        m.box(lx, 5, 0, lx, 8, 0, M + "stripped_spruce_log")
        m.box(lx, 5, 8, lx, 8, 8, M + "stripped_spruce_log")
    for lz in (0, 4, 8):
        for lx in (0, 12):
            m.box(lx, 5, lz, lx, 8, lz, M + "stripped_spruce_log")
    # janelas do andar de cima: uma por painel, 1 de largura x 2 de altura (sobra reboco dos dois lados)
    for lx in (3, 9):
        m.p(lx, 6, 8, M + "white_stained_glass_pane")
        m.p(lx, 7, 8, M + "white_stained_glass_pane")
    m.limpar(6, 6, 8, 6, 7, 8)
    m.porta(6, 6, 8, "spruce")                    # porta da varanda
    m.p(6, 5, 8, M + "stripped_spruce_log")
    for lx in (0, 12):
        m.p(lx, 6, 2, M + "white_stained_glass_pane")
        m.p(lx, 7, 2, M + "white_stained_glass_pane")
        m.p(lx, 6, 6, M + "white_stained_glass_pane")
        m.p(lx, 7, 6, M + "white_stained_glass_pane")
    # varanda com guarda-corpo (balcão em balanço sobre a entrada)
    for lx in range(4, 9):
        m.box(lx, 5, 9, lx, 5, 9, M + "spruce_planks")
    for lx in (4, 8):
        m.box(lx, 6, 9, lx, 6, 9, M + "spruce_fence")
    for lx in (5, 6, 7):
        m.p(lx, 6, 9, M + "spruce_fence")
    m.p(4, 6, 10, M + "air")
    # forro de lajes sob o beiral frontal (R3)
    for lx in range(-1, 14):
        m.sl(lx, 8, 9, "spruce", True)
    # telhado principal (mistura de madeira) + empena cruzada frontal
    m.telhado_x(0, 12, 0, 8, 9, TELHA_MADEIRA, REBOCO, beiral=1, beiral_x=1)
    # janelinha na empena (luz no sótão) e viga de cumeeira aparente
    for lz in (4,):
        for lx in (0, 12):
            m.p(lx, 10, lz, M + "white_stained_glass_pane")
            m.p(lx, 9, lz, M + "stripped_spruce_log")
            m.p(lx, 11, lz, M + "stripped_spruce_log")
    # chaminé de pedra
    m.box(10, 9, 1, 10, 14, 2, PEDRA)
    m.box(9, 15, 1, 11, 15, 3, M + "air")
    m.p(10, 15, 1, M + "stone_brick_slab")
    m.p(10, 15, 2, M + "stone_brick_slab")
    # interior
    m.p(1, 1, 1, M + "crafting_table")
    m.p(2, 1, 1, (M + "smoker", {"facing_direction": 3}))
    m.p(3, 1, 1, (M + "barrel", {"facing_direction": 1, "open_bit": False}))
    m.p(4, 1, 1, (M + "barrel", {"facing_direction": 1, "open_bit": False}))
    m.box(1, 1, 5, 3, 2, 5, M + "bookshelf")
    m.box(4, 1, 3, 8, 1, 5, M + "light_gray_carpet")
    m.p(10, 1, 6, M + "lectern")
    luz_interna(m, 6, 3, 4)
    m.cama(2, 5, 6, 3)
    m.box(4, 5, 4, 8, 5, 6, M + "light_gray_carpet")
    m.p(10, 5, 6, (M + "barrel", {"facing_direction": 1, "open_bit": False}))
    m.p(10, 6, 6, (M + "lantern", {"hanging": False}))
    # jardineiras com flores nas janelas
    for lx in (2, 3, 9, 10):
        m.p(lx, 3, 9, M + "air")
        m.p(lx, 2, 8, pal([("poppy", 2), ("cornflower", 2), ("azure_bluet", 1)], 40 + lx))
    return m


# =====================================================================================================================
# 2. CASA DE PEDRA COM TORRETA (telhado de ardósia, corpo de duas águas + torreta de quatro águas, contrafortes)
# =====================================================================================================================
def casa_torreta(c, x, z, y, flip=False):
    m = Molde(c, x, z, 14, 9, y, flip)
    fundacao(c, m)
    m.box(0, 0, 0, 13, 0, 8, PEDRA)
    m.box(1, 0, 1, 12, 0, 7, pal([("stone_bricks", 3), ("polished_andesite", 2), ("andesite", 2)], 21))
    # corpo: x 5..13 (9 x 7 = z 0..6 -> 7 de profundidade). torreta: x 0..4, z 0..8 (5 x 5 com base maior)
    # --- corpo principal
    m.oca(5, 1, 1, 13, 6, 7, PEDRA)
    for ly in (3, 6):
        for lx in range(5, 14):
            for lz in (1, 7):
                m.p(lx, ly, lz, M + "polished_andesite")
        for lz in range(2, 7):
            for lx in (5, 13):
                m.p(lx, ly, lz, M + "polished_andesite")
    for (lx, lz) in ((5, 1), (13, 1), (5, 7), (13, 7)):
        m.box(lx, 1, lz, lx, 6, lz, PEDRA_ESCURA)       # cantos de pedra escura (quoins)
    m.box(13, 0, 0, 13, 0, 0, PEDRA)
    # contrafortes na lateral direita e frente (profundidade)
    for lz in (2, 5):
        m.box(14, 1, lz, 14, 3, lz, PEDRA_ESCURA)
        m.st(14, 4, lz, "stone_brick_stairs", LESTE)
    for lx in (7, 10):
        m.box(lx, 1, 8, lx, 3, 8, PEDRA_ESCURA)
        m.st(lx, 4, 8, "stone_brick_stairs", SUL)
    # janelas estreitas
    for lx in (7, 11):
        m.p(lx, 2, 7, M + "glass_pane")
        m.p(lx, 4, 7, M + "glass_pane")
        m.p(lx, 5, 7, M + "glass_pane")
        m.st(lx, 6, 7, "stone_brick_stairs", SUL, True) if False else None
    for lz in (3, 5):
        m.p(13, 2, lz, M + "glass_pane")
        m.p(13, 4, lz, M + "glass_pane")
    # porta no corpo principal, com alpendre de duas águas pequeno
    m.limpar(9, 1, 7, 9, 2, 7)
    m.porta(9, 1, 7, "dark_oak")
    m.st(8, 1, 8, "stone_brick_stairs", SUL)
    m.st(9, 1, 8, "stone_brick_stairs", SUL)
    m.st(10, 1, 8, "stone_brick_stairs", SUL)
    for lx in (8, 10):
        m.box(lx, 2, 9, lx, 3, 9, M + "spruce_fence")
        m.p(lx, 1, 9, M + "stone_brick_wall")
    for lx in range(7, 12):
        m.p(lx, 4, 9, M + "dark_oak_slab")
    for lx in range(7, 12):
        m.p(lx, 4, 8, M + "dark_oak_planks")
    m.p(9, 3, 9, (M + "lantern", {"hanging": True}))
    # piso do andar de cima do corpo e beiral largo com forro de lajes (R2, R3)
    m.box(5, 4, 1, 13, 4, 7, TABUA_ESCURA)
    m.limpar(12, 4, 2, 12, 4, 4)
    for k in range(1, 4):
        m.st(12, k, 1 + k, "stone_brick_stairs", SUL)
    for lx in range(4, 15):
        for lz in (0, 8):
            m.sl(lx, 7, lz, "stone_brick", True)
    m.box(5, 7, 1, 13, 7, 7, TABUA_ESCURA)
    # telhado de ardósia de duas águas (cumeeira ao longo de x)
    alto = m.telhado_x(5, 13, 1, 7, 8, TELHA_ARDOSIA, PEDRA, beiral=1, beiral_x=1, cumeeira=M + "deepslate_tile_slab")
    # chaminé
    m.box(12, 8, 3, 12, alto + 3, 3, PEDRA)
    m.p(12, alto + 4, 3, M + "stone_brick_slab")
    # --- torreta (x 0..4, z 2..6) mais alta, com base alargada
    m.oca(0, 1, 2, 4, 9, 6, PEDRA)
    m.oca(0, 1, 2, 4, 1, 6, PEDRA_ESCURA)
    for lx in (-1, 5):
        pass
    for ly in (4, 8):
        for lx in range(0, 5):
            for lz in (2, 6):
                m.p(lx, ly, lz, M + "polished_andesite")
        for lz in range(3, 6):
            for lx in (0, 4):
                m.p(lx, ly, lz, M + "polished_andesite")
    for (lx, lz) in ((0, 2), (4, 2), (0, 6), (4, 6)):
        m.box(lx, 1, lz, lx, 9, lz, PEDRA_ESCURA)
    for ly in (3, 7):
        m.p(2, ly, 6, M + "glass_pane")
        m.p(2, ly + 1, 6, M + "glass_pane")
        m.p(0, ly, 4, M + "glass_pane")
        m.p(0, ly + 1, 4, M + "glass_pane")
    m.p(2, 1, 6, M + "air")
    m.limpar(2, 1, 6, 2, 2, 6)
    m.box(1, 9, 2, 3, 9, 6, M + "air") if False else None
    # parapeito com merlões (escada-laje) no topo da torreta, depois telhado de quatro águas íngreme
    for lx in range(-1, 6):
        for lz in (1, 7):
            m.sl(lx, 10, lz, "stone_brick", True)
    for lz in range(2, 7):
        for lx in (-1, 5):
            m.sl(lx, 10, lz, "stone_brick", True)
    m.box(0, 10, 2, 4, 10, 6, TABUA_ESCURA)
    topo = m.tenda(0, 4, 2, 6, 11, TELHA_ARDOSIA, beiral=1)
    m.box(2, topo + 1, 4, 2, topo + 2, 4, M + "lightning_rod") if False else None
    m.box(2, topo + 1, 4, 2, topo + 2, 4, M + "stone_brick_wall")
    m.p(2, topo + 3, 4, M + "lightning_rod")
    # porta da torreta no fundo da frente: escada de caracol simples interna
    for k in range(1, 4):
        m.st(1, k, 2 + k, "stone_brick_stairs", SUL) if False else None
    m.box(1, 1, 3, 3, 1, 5, M + "light_gray_carpet")
    m.p(1, 2, 3, M + "crafting_table") if False else None
    m.cama(3, 5, 5, 0) if False else None
    # interior do corpo
    m.p(6, 1, 2, M + "crafting_table")
    m.p(7, 1, 2, (M + "blast_furnace", {"facing_direction": 3}))
    m.p(8, 1, 2, M + "anvil")
    m.box(10, 1, 2, 12, 3, 2, M + "bookshelf")
    m.box(9, 1, 3, 12, 1, 5, M + "light_gray_carpet")
    m.cama(6, 5, 6, 1)
    m.box(8, 5, 3, 11, 5, 5, M + "light_gray_carpet")
    luz_interna(m, 8, 3, 4)
    luz_interna(m, 9, 6, 4)
    m.p(2, 2, 4, (M + "lantern", {"hanging": False}))
    return m
