"""Vila Pedra-Musgo v2: montagem com REGISTRO DE OCUPAÇÃO (nada nasce sobre outro objeto) e anéis de passagem ao redor do que fica no meio da rua.
Regras (erros-e-licoes.md): base de objetos = terreno H (nunca 'o bloco mais alto da coluna'); caminho livre ao redor de fonte, poço e barracas."""
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
    (13, 25, 47, 40, 1, 2),     # praça ampliada (com anel de passagem ao redor da fonte)
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
for x in range(W):                         # moldura de colinas nas bordas
    for z in range(D):
        if not FIXO[x][z]:
            borda = min(x, W - 1 - x, z, D - 1 - z)
            if borda < 5:
                H[x][z] = min(H[x][z] + (5 - borda) // 2 + (1 if borda < 2 else 0), 4)
for _ in range(30):
    for x in range(W):
        for z in range(D):
            if FIXO[x][z]:
                continue
            viz = [H[a][b] for a, b in ((x + 1, z), (x - 1, z), (x, z + 1), (x, z - 1)) if 0 <= a < W and 0 <= b < D]
            lo, hi = max(viz) - 1, min(viz) + 1
            if lo <= hi:
                H[x][z] = min(max(H[x][z], lo), hi)
AGUA = {(x, z) for (x, z), n in fixas.items() if n == -1}

ESC_X = range(28, 33)                      # escadaria do Salão (2 degraus)
for z, h in {24: 1, 23: 2}.items():
    for x in ESC_X:
        H[x][z] = h
preencher_terreno(c, H, W, D)

# ============================================================================================================ registro de ocupação
RES = {}            # (x, z) -> (dono, tipo)   tipo: "solido" (ocupa espaço) ou "anel" (precisa ficar livre para andar)
CONFLITOS = []      # (dono_novo, dono_existente, celula): nunca deve haver nada aqui
OBJETOS = []        # objetos centrais que exigem caminho ao redor (auditoria E-15)
CAM = set()


def livre(cels, ignorar_cam=False):
    return all(0 <= x < W and 0 <= z < D and (x, z) not in RES and (ignorar_cam or (x, z) not in CAM) and (x, z) not in AGUA for (x, z) in cels)


def reservar(dono, cels, tipo="solido", estrito=True):
    ok = True
    for k in cels:
        if k in RES and RES[k][0] != dono:
            ok = False
            if estrito:
                CONFLITOS.append((dono, RES[k][0], k))
        else:
            RES[k] = (dono, tipo)
    return ok


def retangulo(x1, z1, x2, z2):
    return [(x, z) for x in range(x1, x2 + 1) for z in range(z1, z2 + 1)]


def disco(cx, cz, r1, r2=0.0):
    return [(x, z) for x in range(int(cx - r1) - 1, int(cx + r1) + 2) for z in range(int(cz - r1) - 1, int(cz + r1) + 2)
            if r2 < math.hypot(x - cx, z - cz) <= r1]


def pegada(m, frente=2, margem=1):
    """Células do mundo ocupadas por uma construção (inclui varanda/alpendre à frente e margem nos lados e atrás)."""
    return [(m.mundo(lx, 0, lz)[0], m.mundo(lx, 0, lz)[2]) for lx in range(-margem, m.w + margem) for lz in range(-margem, m.d + frente)]


# ============================================================================================================ caminhos
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


trilha([(0, 31), (4, 31)], 3, 0.0)
trilha([(4, 31), (10, 30), (14, 30)], 3, 0.35)           # fora da praça a rua ondula
trilha([(14, 30), (46, 30)], 3, 0.0)                     # dentro da praça a rua é reta e estreita (3): barracas não colidem
trilha([(46, 30), (50, 30), (55, 30)], 3, 0.35)
trilha([(55, 30), (59, 31)], 3, 0.0)
trilha([(9, 27), (9, 30)], 2)                 # chalé
trilha([(54, 27), (54, 30)], 2)               # casa de pedra
trilha([(8, 34), (8, 31)], 2)                 # hortelão
trilha([(50, 36), (50, 31)], 2)               # casa de chá
trilha([(32, 38), (34, 41)], 3, 0.5)          # praça -> lagoa
trilha([(30, 25), (30, 22)], 5, 0.0)          # praça -> escadaria

# ============================================================================================================ construções (primeiro: reservam seu espaço)
chale = S.chale_enxaimel(c, 3, 16, 1, False)
torreta = S.casa_torreta(c, 45, 16, 1, False)
hort = S.casa_hortelao(c, 4, 36, 1, True)
S.horta(c, 15, 38, 22, 47, 1)
cha = S.casa_cha(c, 44, 38, 1, True)
salao = S.salao(c, 20, 3, 3, False)
for nome_, m_ in (("chale", chale), ("casa_pedra", torreta), ("hortelao", hort), ("casa_cha", cha)):
    reservar(nome_, pegada(m_, frente=2 if nome_ in ("chale", "casa_pedra") else 1, margem=1))
reservar("horta", retangulo(14, 38, 23, 47))
reservar("salao", retangulo(19, 2, 41, 16) + retangulo(27, 16, 33, 22))        # nave + torre-relógio (com margem de 1)
CASAS = {(x, z) for k, (n, t) in RES.items() if t == "solido" and n in ("chale", "casa_pedra", "hortelao", "casa_cha", "salao", "horta") for (x, z) in [k]}

# ============================================================================================================ praça: pavimento, fonte e ANEL de passagem
PRACA_CEL = set()
for x in range(14, 47):
    for z in range(25, 41):
        if (x in (14, 46) or z in (25, 40)) and rnd.random() < 0.55:
            continue
        PRACA_CEL.add((x, z))
for (x, z) in CAM:
    if 0 <= x < W and 0 <= z < D and (x, z) not in CASAS:
        c.ponto(x, H[x][z], z, CAMINHO)
for (x, z) in PRACA_CEL:
    if (x, z) not in CASAS:
        c.ponto(x, H[x][z], z, PRACA)
for x in ESC_X:
    for z in (23, 24):
        y = H[x][z]
        c.ponto(x, y, z, PEDRA)
        c.ponto(x, y + 1, z, escada(M + "stone_brick_stairs", NORTE))

FX, FZ = 30, 30
R_AGUA, R_BORDA, R_ANEL = 2.9, 3.9, 7.0        # água / borda da bacia / fim do caminho livre ao redor
for x in range(FX - 9, FX + 10):
    for z in range(FZ - 9, FZ + 10):
        d = math.hypot(x - FX, z - FZ)
        y = H[x][z]
        if d <= R_AGUA:
            c.ponto(x, y, z, M + "stone_bricks")
            c.ponto(x, y + 1, z, (M + "water", {"liquid_depth": 0}))
        elif d <= R_BORDA:
            c.ponto(x, y, z, PEDRA)
            c.ponto(x, y + 1, z, PEDRA)
            c.ponto(x, y + 2, z, laje(M + "stone_brick_slab", False))
        elif d <= R_ANEL:
            c.ponto(x, y, z, PRACA)                                   # anel pavimentado, TODO livre
        elif d <= R_ANEL + 0.7:
            c.ponto(x, y, z, pal([("polished_andesite", 3), ("stone_bricks", 1)], 41))   # faixa que delimita o anel
y0 = H[FX][FZ]
for k in range(1, 4):
    c.ponto(FX, y0 + k, FZ, M + "stone_bricks")
c.ponto(FX, y0 + 4, FZ, PEDRA)
for (dx, dz) in ((1, 0), (-1, 0), (0, 1), (0, -1)):
    c.ponto(FX + dx, y0 + 3, FZ + dz, escada(M + "stone_brick_stairs", {(1, 0): OESTE, (-1, 0): LESTE, (0, 1): NORTE, (0, -1): SUL}[(dx, dz)], True))   # mísula: sustenta a copa (nada flutuando)
    c.ponto(FX + dx, y0 + 4, FZ + dz, M + "stone_brick_wall")
    c.ponto(FX + dx, y0 + 5, FZ + dz, M + "stone_brick_wall")
c.ponto(FX, y0 + 5, FZ, (M + "water", {"liquid_depth": 0}))
for k in range(1, 3):
    c.ponto(FX, y0 + 5 + k, FZ, (M + "iron_chain", {"pillar_axis": "y"}))
c.ponto(FX, y0 + 7, FZ, (M + "lantern", {"hanging": True}))
reservar("fonte", disco(FX, FZ, R_BORDA), "solido")
reservar("anel_fonte", disco(FX, FZ, R_ANEL, R_BORDA), "anel")
OBJETOS.append(("fonte", "disco", (FX, FZ), R_BORDA, R_ANEL))


# ============================================================================================================ poço
def poco(px, pz):
    y = H[px][pz]
    for dx in range(-1, 2):
        for dz in range(-1, 2):
            c.ponto(px + dx, y, pz + dz, PEDRA)
            if (dx, dz) != (0, 0):
                c.ponto(px + dx, y + 1, pz + dz, PEDRA)
    c.ponto(px, y, pz, M + "stone_bricks")
    c.ponto(px, y + 1, pz, (M + "water", {"liquid_depth": 0}))
    for (dx, dz) in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        for k in (2, 3):
            c.ponto(px + dx, y + k, pz + dz, M + "spruce_fence")
    m = Molde(c, px - 1, pz - 1, 3, 3, y, False)
    m.tenda(0, 2, 0, 2, 4, [("spruce_stairs", 5), ("dark_oak_stairs", 1.5)], beiral=1)
    for xx in range(px - 3, px + 4):                                   # entorno desgastado
        for zz in range(pz - 3, pz + 4):
            if 0 <= xx < W and 0 <= zz < D and (xx, zz) not in PRACA_CEL and abs(xx - px) + abs(zz - pz) < 5 and rnd.random() < 0.5:
                if "grass" in str(c.pegar(xx, H[xx][zz], zz)) or "moss" in str(c.pegar(xx, H[xx][zz], zz)):
                    c.ponto(xx, H[xx][zz], zz, pal([("grass_path", 3), ("coarse_dirt", 2)], 80 + xx))


# ============================================================================================================ barracas (nos cantos da praça, fora do anel da fonte)
def barraca(bx, bz, flip, cor, produto, nome):
    foot = retangulo(bx, bz, bx + 4, bz + 2)
    toldo = retangulo(bx - 1, bz - 1, bx + 5, bz + 3)
    if not livre(foot, ignorar_cam=False) or not reservar(nome, toldo):
        CONFLITOS.append((nome, "posicao_invalida", (bx, bz)))
        return False
    reservar(nome + "_anel", [(x, z) for x in range(bx - 2, bx + 7) for z in range(bz - 2, bz + 5) if not (bx <= x <= bx + 4 and bz <= z <= bz + 2)], "anel", estrito=False)
    m = Molde(c, bx, bz, 5, 3, H[bx + 2][bz + 1], flip)
    for lx in (0, 4):
        for lz in (0, 2):
            m.box(lx, 1, lz, lx, 3, lz, M + "stripped_spruce_log")
    for lx in range(1, 4):
        m.p(lx, 1, 2, M + "spruce_planks")                         # bloco inteiro: os produtos (y=2) assentam direto
    m.p(0, 1, 1, (M + "barrel", {"facing_direction": 1, "open_bit": False}))
    m.p(4, 1, 1, M + "crafting_table")
    for lx in range(1, 4):
        (m.maq(lx, 2, 2, "pumpkin", SUL) if produto[lx % len(produto)] == "pumpkin" else m.p(lx, 2, 2, M + produto[lx % len(produto)]))
    for lx in range(-1, 6):
        for lz in range(-1, 4):
            m.p(lx, 4, lz, M + (cor if (lx + 1) % 2 == 0 else "white_wool"))
    m.p(2, 3, 2, (M + "lantern", {"hanging": True}))
    OBJETOS.append((nome, "ret", (bx, bz, bx + 4, bz + 2), 2, 2))
    return True


barraca(18, 25, False, "orange_wool", ["pumpkin", "hay_block", "melon_block"], "barraca_NO")
barraca(38, 25, False, "light_blue_wool", ["bookshelf", "barrel", "bookshelf"], "barraca_NL")
barraca(18, 33, True, "orange_wool", ["melon_block", "hay_block", "pumpkin"], "barraca_SO")
barraca(38, 33, True, "light_blue_wool", ["barrel", "hay_block", "barrel"], "barraca_SL")

if reservar("poco", retangulo(24, 38, 28, 42)):         # telhado 5x5; centro (26, 40)
    poco(26, 40)
    reservar("poco_anel", [(x, z) for x in range(23, 30) for z in range(37, 44) if not (25 <= x <= 27 and 39 <= z <= 41)], "anel", estrito=False)
    OBJETOS.append(("poco", "ret", (25, 39, 27, 41), 2, 2))
else:
    CONFLITOS.append(("poco", "posicao_invalida", (26, 40)))

# banco de pedra virado para a fonte (costas para o lado oposto: a escada SOBE em direção às costas)
bx, bz = 37, 38
if livre([(bx + k, bz) for k in range(-2, 3)]) and reservar("banco", [(bx + k, bz) for k in range(-2, 3)]):
    for k in (-1, 0, 1):
        c.ponto(bx + k, H[bx + k][bz] + 1, bz, escada(M + "stone_brick_stairs", SUL))   # fonte ao norte: costas ao sul
    for k in (-2, 2):
        c.ponto(bx + k, H[bx + k][bz] + 1, bz, M + "spruce_fence")
        c.ponto(bx + k, H[bx + k][bz] + 2, bz, (M + "lantern", {"hanging": False}))

# ============================================================================================================ lagoa e píer
for (x, z) in AGUA:
    c.ponto(x, 0, z, (M + "water", {"liquid_depth": 0}))
    if rnd.random() < 0.18:
        c.ponto(x, 1, z, M + "waterlily")
PIER = retangulo(32, 41, 35, 46)
reservar("pier", PIER)
for x in range(W):
    for z in range(D):
        if (x, z) in AGUA or (x, z) in RES:
            continue
        if any((x + a, z + b) in AGUA for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))) and H[x][z] == 0 and rnd.random() < 0.5:
            c.ponto(x, 1, z, M + "tall_grass")
for z in range(41, 47):
    c.ponto(33, 1, z, M + "spruce_planks")
    c.ponto(34, 1, z, M + "spruce_planks")
for z in (43, 45):                                           # estacas do píer descem até o fundo da lagoa
    for x in (33, 34):
        c.ponto(x, 0, z, M + "spruce_fence")
for z in (42, 46):
    for x in (32, 35):
        for yy in (0, 1, 2):                                 # poste começa DENTRO da água, apoiado no fundo
            c.ponto(x, yy, z, M + "spruce_fence")
    c.ponto(32, 3, z, (M + "lantern", {"hanging": False}))


# ============================================================================================================ postes (pescoço de ganso): base no TERRENO, só em espaço livre, nunca sobre outro objeto
POSTES = []


def poste_h(px, pz, dr, altura=4, braco=1):
    """Poste no ESTILO DO DONO (lido no mundo, erros-e-licoes E-22): parede de pedra na base, 2 de cerca, laje de topo, braço em escada
    (sobe para fora) com a lanterna pendurada embaixo e laje invertida de contrapeso atrás. Base no TERRENO, só em espaço livre."""
    ascende = {(1, 0): LESTE, (-1, 0): OESTE, (0, 1): SUL, (0, -1): NORTE}[dr]
    for desloc in (0, 1, -1, 2, -2, 3, -3):
        x, z = px + desloc, pz
        frente, tras = (x + dr[0], z + dr[1]), (x - dr[0], z - dr[1])
        perto = any(abs(x - a) < 4 and abs(z - b) < 4 for a, b in POSTES)
        aereo_ok = all((0 <= a < W and 0 <= b < D) and (RES.get((a, b), (None, 'anel'))[1] == 'anel') and (a, b) not in AGUA for (a, b) in (frente, tras))
        if perto or not livre([(x, z)]) or not aereo_ok:
            continue
        y = H[x][z] + 1
        if c.pegar(x, H[x][z], z) is None or any(c.pegar(a, y + i, b) is not None for (a, b) in ((x, z), frente, tras) for i in range(0, altura)):
            continue
        c.ponto(x, y, z, M + "stone_brick_wall")
        c.ponto(x, y + 1, z, M + "spruce_fence")
        c.ponto(x, y + 2, z, M + "spruce_fence")
        c.ponto(x, y + 3, z, laje(M + "spruce_slab", False))                           # laje de topo
        c.ponto(frente[0], y + 3, frente[1], escada(M + "spruce_stairs", ascende))      # braço em escada
        c.ponto(frente[0], y + 2, frente[1], (M + "lantern", {"hanging": True}))        # lanterna embaixo do braço
        c.ponto(tras[0], y + 2, tras[1], laje(M + "spruce_slab", True))                 # contrapeso (laje invertida)
        reservar("poste", [(x, z)])
        POSTES.append((x, z))
        return True
    return False


poste_ok = [poste_h(*p) for p in (
    (26, 22, (-1, 0)), (34, 22, (1, 0)),                                   # ladeiam o topo da escadaria do Salão
    (24, 24, (1, 0)), (36, 24, (-1, 0)), (36, 36, (-1, 0)),                # cantos da praça (fora do anel)
    (6, 28, (0, 1)), (12, 28, (0, 1)), (6, 33, (0, -1)), (12, 33, (0, -1)),
    (46, 28, (0, 1)), (46, 33, (0, -1)), (57, 28, (0, 1)), (56, 33, (0, -1)),
    (30, 38, (1, 0)))]
print("postes colocados:", sum(poste_ok), "de", len(poste_ok))


# ============================================================================================================ árvores: base no terreno, copa sem invadir nada
def folha(nome):
    return Paleta([((M + nome, {"persistent_bit": True, "update_bit": False}), 9)], 3)


ARV = []


def arvore_h(x, z, altura, tronco, folha_nome, copa=3.0, galhos=True):
    base = H[x][z]
    cels_pe = [(x, z)]                       # só o tronco precisa de chão livre; as raízes só nascem onde há espaço
    if not livre(cels_pe):
        return False
    canopy = disco(x, z, copa + 0.4)
    if any(k in RES and RES[k][1] == "solido" for k in canopy) or any(k in AGUA for k in cels_pe):
        return False
    if any(abs(x - a) < 3 and abs(z - b) < 3 for a, b in ARV):
        return False
    y = base + 1
    for i in range(altura):
        c.ponto(x, y + i, z, (M + tronco, {"pillar_axis": "y"}))
    for dx in range(-int(copa) - 1, int(copa) + 2):
        for dy in range(-1, int(copa) + 1):
            for dz in range(-int(copa) - 1, int(copa) + 2):
                d = math.sqrt(dx * dx + (dy * 1.2) ** 2 + dz * dz)
                if d <= copa + rnd.random() * 0.6 and (dx or dz or dy > 0):
                    if c.pegar(x + dx, y + altura - 1 + dy, z + dz) is None:
                        c.ponto(x + dx, y + altura - 1 + dy, z + dz, folha(folha_nome))
    ARV.append((x, z))
    reservar("arvore", [(x, z)])
    for (dx, dz, d) in ((1, 0, OESTE), (-1, 0, LESTE), (0, 1, NORTE), (0, -1, SUL)):
        xx, zz = x + dx, z + dz
        if rnd.random() < 0.7 and c.pegar(xx, H[xx][zz] + 1, zz) is None:
            c.ponto(xx, H[xx][zz] + 1, zz, escada(M + ("dark_oak_stairs" if "dark" in tronco or "spruce" in tronco else "oak_stairs"), d, False))
    if galhos:
        for _ in range(3):
            dx, dz = rnd.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            gy = y + altura - 2 - rnd.randint(0, 1)
            c.ponto(x + dx, gy, z + dz, (M + tronco, {"pillar_axis": "x" if dx else "z"}))
            c.ponto(x + dx * 2, gy + 1, z + dz * 2, (M + tronco, {"pillar_axis": "x" if dx else "z"}))
    for dx in range(-3, 4):
        for dz in range(-3, 4):
            xx, zz = x + dx, z + dz
            if 0 <= xx < W and 0 <= zz < D and (xx, zz) not in CAM and (xx, zz) not in PRACA_CEL and "grass_block" in str(c.pegar(xx, H[xx][zz], zz)) and math.hypot(dx, dz) <= 2.6 and rnd.random() < 0.55:
                c.ponto(xx, H[xx][zz], zz, M + "moss_block")
    return True


def arvore_perto(x, z, *args):
    """Tenta a posição pedida e, se ocupada, procura um lugar livre por perto (raio 4)."""
    for r in range(0, 5):
        for dx in range(-r, r + 1):
            for dz in range(-r, r + 1):
                if max(abs(dx), abs(dz)) == r and 1 <= x + dx < W - 1 and 1 <= z + dz < D - 1 and arvore_h(x + dx, z + dz, *args):
                    return True
    return False


arvores = [
    (15, 8, 8, "birch_log", "birch_leaves", 3.0), (45, 9, 9, "birch_log", "birch_leaves", 3.2), (17, 14, 7, "birch_log", "birch_leaves", 2.8),
    (43, 14, 7, "birch_log", "birch_leaves", 2.8),
    (14, 42, 6, "cherry_log", "cherry_leaves", 3.0), (46, 24, 6, "cherry_log", "cherry_leaves", 3.2), (22, 29, 6, "cherry_log", "cherry_leaves", 3.0),
    (4, 5, 11, "spruce_log", "spruce_leaves", 3.0), (9, 3, 10, "spruce_log", "spruce_leaves", 2.8), (52, 5, 11, "spruce_log", "spruce_leaves", 3.0),
    (56, 11, 10, "spruce_log", "spruce_leaves", 2.8), (24, 1, 9, "spruce_log", "spruce_leaves", 2.6), (36, 1, 9, "spruce_log", "spruce_leaves", 2.6),
    (3, 53, 10, "spruce_log", "spruce_leaves", 2.8), (58, 53, 10, "spruce_log", "spruce_leaves", 3.0), (20, 53, 9, "spruce_log", "spruce_leaves", 2.6),
    (11, 13, 7, "oak_log", "oak_leaves", 3.2), (40, 44, 7, "oak_log", "oak_leaves", 3.2), (27, 49, 7, "oak_log", "oak_leaves", 3.0),
    (36, 53, 8, "oak_log", "oak_leaves", 3.2),
    (58, 41, 8, "dark_oak_log", "dark_oak_leaves", 3.3), (47, 53, 8, "dark_oak_log", "dark_oak_leaves", 3.3), (2, 42, 8, "dark_oak_log", "dark_oak_leaves", 3.2),
    (57, 21, 8, "dark_oak_log", "dark_oak_leaves", 3.2), (1, 22, 8, "dark_oak_log", "dark_oak_leaves", 3.2),
]
plantadas = sum(int(bool(arvore_perto(x, z, a, t, f, cp))) for (x, z, a, t, f, cp) in arvores)
# complementa com candidatas em espaços LIVRES (sorteio com semente fixa): borda = abetos, praça = cerejeiras, resto = mistura
rr = random.Random(77)
ESPECIES = [("birch_log", "birch_leaves", 3.0, 8), ("spruce_log", "spruce_leaves", 2.8, 10), ("oak_log", "oak_leaves", 3.2, 7), ("dark_oak_log", "dark_oak_leaves", 3.3, 8)]
extras = 0
for _ in range(1200):
    if extras >= 18:
        break
    x, z = rr.randint(2, W - 3), rr.randint(2, D - 3)
    borda = min(x, W - 1 - x, z, D - 1 - z)
    if 12 <= x <= 48 and 22 <= z <= 43:
        esp = ("cherry_log", "cherry_leaves", 3.0, 6)
    elif borda < 9:
        esp = ESPECIES[1]
    else:
        esp = rr.choice(ESPECIES)
    if arvore_h(x, z, esp[3], esp[0], esp[1], esp[2]):
        extras += 1
print("árvores plantadas:", plantadas, "de", len(arvores), "+", extras, "extras")

# ============================================================================================================ cobertura de solo (V1) e canteiros
FLORES = ["poppy", "dandelion", "cornflower", "azure_bluet", "oxeye_daisy", "pink_tulip", "white_tulip", "orange_tulip", "lily_of_the_valley"]
ocupado = set(CASAS)
for x in range(W):
    for z in range(D):
        if (x, z) in AGUA or (x, z) in CAM or (x, z) in PRACA_CEL or (x, z) in RES:
            continue
        y = H[x][z]
        top = str(c.pegar(x, y, z))
        if ("grass_block" not in top and "moss_block" not in top) or c.pegar(x, y + 1, z) is not None:
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
for m_ in (chale, torreta, hort, cha):
    for lx in range(-1, m_.w + 1):
        for lz in (-1, m_.d):
            x, _, z = m_.mundo(lx, 0, lz)
            if 0 <= x < W and 0 <= z < D and (x, z) not in CAM and (x, z) not in PRACA_CEL and "grass" in str(c.pegar(x, H[x][z], z)) \
                    and c.pegar(x, H[x][z] + 1, z) is None and rnd.random() < 0.55:
                c.ponto(x, H[x][z] + 1, z, M + rnd.choice(["flowering_azalea", "azalea", "pink_tulip", "poppy"]))
for _ in range(26):
    x, z = rnd.randint(2, W - 3), rnd.randint(2, D - 3)
    if (x, z) in CAM or (x, z) in PRACA_CEL or (x, z) in RES or (x, z) in AGUA:
        continue
    y = H[x][z]
    if "grass" in str(c.pegar(x, y, z)) and c.pegar(x, y + 1, z) is None:
        c.ponto(x, y + 1, z, pal([("mossy_cobblestone", 3), ("cobblestone", 2), ("andesite", 1)], 90 + x))


# ============================================================================================================ pós-correções
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
        dz = 1 if b[1].get("minecraft:cardinal_direction") == "south" else -1
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
        c.ponto(x, y + 2, z, escada(M + (mat or "stone_brick_stairs"), NORTE if dz == 1 else SUL, True))
        feitos.append(((x, y, z), mat))
    return feitos


def corrigir_lanternas():
    n = 0
    for (x, y, z), b in list(c.blocos.items()):
        if isinstance(b, tuple) and b[0] == M + "lantern" and b[1].get("hanging") and c.pegar(x, y + 1, z) is None:
            n += 1
            c.ponto(x, y, z, (M + "lantern", {"hanging": False}) if c.pegar(x, y - 1, z) is not None else M + "air")
    return n


corrigir_lanternas()
vergas_das_portas()
if CONFLITOS:
    print("CONFLITOS DE POSICAO:", CONFLITOS[:10])

if __name__ == "__main__":
    avisos = c.validar()
    print("blocos:", len(c.blocos), "avisos:", [a for a in avisos][:8])
    (x0, y0, z0), (x1, y1, z1) = c.caixa_limite()
    print("caixa:", (x0, y0, z0), (x1, y1, z1), "dim", (x1 - x0 + 1, y1 - y0 + 1, z1 - z0 + 1))
    import exportar
    out = Path(__file__).parent / "saida"
    dims, npal = exportar.gravar(c, out / "vila_pedra_musgo.mcstructure")
    print("mcstructure gravado:", dims, "paleta:", npal)
