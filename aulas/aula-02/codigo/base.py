"""Base da Vila Pedra-Musgo: moldes locais (com giro de 180 graus), paletas e terreno."""
import math
import random
import sys

sys.path.insert(0, r"C:\Users\Desktop\Desktop\Projetos\BotVulpus\addon\tools")
from construcao.cena import Cena, Paleta, escada, laje, LESTE, OESTE, SUL, NORTE  # noqa: E402,F401

M = "minecraft:"
ESCADAS = []        # lances de escada interna: (molde, x0, y0, z0, degraus, direção local); a auditoria confere cada um
FLIP = {LESTE: OESTE, OESTE: LESTE, SUL: NORTE, NORTE: SUL}


# ---------------------------------------------------------------- paletas (T1: um material dominante + 2 a 3 tons vizinhos)
def pal(itens, s=1):
    return Paleta([(M + n if ":" not in n else n, p) for n, p in itens], s)


PEDRA = pal([("stone_bricks", 3), ("andesite", 3), ("tuff_bricks", 2.5), ("polished_andesite", 1.2), ("mossy_stone_bricks", 0.8), ("cobblestone", 1)], 1)
PEDRA_ESCURA = pal([("stone_bricks", 3), ("andesite", 2), ("cobblestone", 2), ("mossy_cobblestone", 1), ("polished_tuff", 1)], 2)
REBOCO = pal([("calcite", 4), ("diorite", 2), ("light_gray_concrete", 1.2), ("smooth_quartz", 0.6)], 3)
REBOCO_CINZA = pal([("light_gray_concrete", 5), ("andesite", 1.5), ("calcite", 1)], 4)
GRAMA = pal([("grass_block", 9), ("moss_block", 1.3), ("podzol", 0.4)], 5)
TERRA = pal([("dirt", 6), ("coarse_dirt", 2), ("dirt_with_roots", 0.3)], 6)
CAMINHO = pal([("andesite", 3), ("cobblestone", 3), ("gravel", 2), ("grass_path", 3), ("coarse_dirt", 1), ("stone_bricks", 1)], 7)
PRACA = pal([("stone_bricks", 3), ("andesite", 3), ("cobblestone", 2), ("tuff_bricks", 1.5), ("mossy_stone_bricks", 1), ("gravel", 0.4)], 8)


def tr(nome, direcao=0, aberto=False, invertido=True):
    return (M + nome, {"direction": direcao, "open_bit": aberto, "upside_down_bit": invertido})


class Molde:
    """Coordenadas locais: x leste, y cima, z para a FRENTE (a fachada com a porta). flip=True gira 180 graus (fachada para o norte)."""

    def __init__(self, c, x, z, w, d, y, flip=False):
        self.c, self.w, self.d, self.y0, self.flip = c, w, d, y, flip
        self.ox = x + (w - 1 if flip else 0)
        self.oz = z + (d - 1 if flip else 0)

    def mundo(self, x, y, z):
        return (self.ox - x, self.y0 + y, self.oz - z) if self.flip else (self.ox + x, self.y0 + y, self.oz + z)

    def dirm(self, d):
        return FLIP[d] if self.flip else d

    def p(self, x, y, z, b):
        self.c.ponto(*self.mundo(x, y, z), b)

    def box(self, x1, y1, z1, x2, y2, z2, b):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                for z in range(min(z1, z2), max(z1, z2) + 1):
                    self.p(x, y, z, b)

    def oca(self, x1, y1, z1, x2, y2, z2, b):
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                for z in range(z1, z2 + 1):
                    if x in (x1, x2) or z in (z1, z2):
                        self.p(x, y, z, b)

    def limpar(self, x1, y1, z1, x2, y2, z2):
        self.box(x1, y1, z1, x2, y2, z2, M + "air")

    CARD = {LESTE: "east", OESTE: "west", SUL: "south", NORTE: "north"}

    def maq(self, x, y, z, nome, frente_local):
        """Forno/defumador/alto-forno/atril/bigorna/abóbora: a FRENTE olha para `frente_local` (SUL = para a frente da casa). Gira junto com a casa (flip)."""
        self.p(x, y, z, (M + nome, {"minecraft:cardinal_direction": self.CARD[self.dirm(frente_local)]}))

    def esc(self, nome):
        if isinstance(nome, list):
            tot = sum(p for _, p in nome)
            r = self.c.rnd.random() * tot
            for n, p in nome:
                r -= p
                if r <= 0:
                    return n
            return nome[-1][0]
        return nome

    def st(self, x, y, z, nome, d, inv=False):
        self.p(x, y, z, escada(M + self.esc(nome), self.dirm(d), inv))

    def sl(self, x, y, z, nome, topo=False):
        self.p(x, y, z, laje(M + (nome if nome.endswith('_slab') else nome + '_slab'), topo))

    def tr(self, x, y, z, nome, d=0, aberto=False, inv=True):
        dd = {0: 0, 1: 1, 2: 2, 3: 3}[d]
        if self.flip:
            dd = {0: 1, 1: 0, 2: 3, 3: 2}[d]
        self.p(x, y, z, tr(nome, dd, aberto, inv))

    def log(self, x, y, z, nome, eixo="y"):
        self.p(x, y, z, (M + nome, {"pillar_axis": eixo}))

    def porta(self, x, y, z, madeira, aberta=False):
        """Porta voltada para a FRENTE (+z local)."""
        card = "north" if self.flip else "south"
        base = {"door_hinge_bit": False, "minecraft:cardinal_direction": card, "open_bit": aberta}
        self.p(x, y, z, (M + madeira + "_door", {**base, "upper_block_bit": False}))
        self.p(x, y + 1, z, (M + madeira + "_door", {**base, "upper_block_bit": True}))

    def lanterna(self, x, y, z, pendurada=True):
        self.p(x, y, z, (M + "lantern", {"hanging": pendurada}))

    def cama(self, x, y, z, d_cabeceira):
        """Cama simulada (o bloco `bed` e descartado ao carregar a estrutura sem entidade de bloco): travesseiro branco + colcha de la azul."""
        vx, vz = {LESTE: (1, 0), OESTE: (-1, 0), SUL: (0, 1), NORTE: (0, -1)}[d_cabeceira]
        self.p(x, y, z, M + "white_wool")
        self.p(x - vx, y, z - vz, M + "light_blue_wool")

    def _laje_de(self, nome):
        n = nome[0][0] if isinstance(nome, list) else nome
        return M + n.replace("_stairs", "_slab")

    def telhado_x(self, x1, x2, z1, z2, y, nome, empena, beiral=1, beiral_x=0, cumeeira=None, esconder_empena=False):
        """Duas águas com a cumeeira ao longo de x; fecha as empenas com o bloco `empena`. Largura (z2-z1+1+2*beiral) deve ser ímpar."""
        za, zb, xa, xb = z1 - beiral, z2 + beiral, x1 - beiral_x, x2 + beiral_x
        i = 0
        while za + i <= zb - i:
            for x in range(xa, xb + 1):
                if za + i == zb - i:
                    self.p(x, y + i, za + i, cumeeira or self._laje_de(nome))
                else:
                    self.st(x, y + i, za + i, nome, SUL)
                    self.st(x, y + i, zb - i, nome, NORTE)
            if not esconder_empena:
                for x in (x1, x2):
                    for z in range(za + i + 1, zb - i):
                        self.p(x, y + i, z, empena)
            i += 1
        return y + i - 1  # altura da cumeeira

    def telhado_z(self, x1, x2, z1, z2, y, nome, empena, beiral=1, beiral_z=0, cumeeira=None):
        xa, xb, za, zb = x1 - beiral, x2 + beiral, z1 - beiral_z, z2 + beiral_z
        i = 0
        while xa + i <= xb - i:
            for z in range(za, zb + 1):
                if xa + i == xb - i:
                    self.p(xa + i, y + i, z, cumeeira or self._laje_de(nome))
                else:
                    self.st(xa + i, y + i, z, nome, LESTE)
                    self.st(xb - i, y + i, z, nome, OESTE)
            for z in (z1, z2):
                for x in range(xa + i + 1, xb - i):
                    self.p(x, y + i, z, empena)
            i += 1
        return y + i - 1

    def tenda(self, x1, x2, z1, z2, y, nome, beiral=1, linhas=99):
        """Telhado de quatro águas (pirâmide de escadas) sobre o retângulo; termina em ponta ou em cumeeira."""
        xa, xb, za, zb = x1 - beiral, x2 + beiral, z1 - beiral, z2 + beiral
        i = 0
        while xa + i <= xb - i and za + i <= zb - i and i < linhas:
            for x in range(xa + i, xb - i + 1):
                self.st(x, y + i, za + i, nome, SUL) if za + i < zb - i else self.p(x, y + i, za + i, self._laje_de(nome))
                if zb - i != za + i:
                    self.st(x, y + i, zb - i, nome, NORTE)
            for z in range(za + i + 1, zb - i):
                self.st(xa + i, y + i, z, nome, LESTE) if xa + i < xb - i else self.p(xa + i, y + i, z, self._laje_de(nome))
                if xb - i != xa + i:
                    self.st(xb - i, y + i, z, nome, OESTE)
            i += 1
        return y + i - 1


# ---------------------------------------------------------------- terreno
def gerar_terreno(c, W, D, pads, rel_ruido, semente=11, fixas=None):
    rnd = random.Random(semente)
    fase = [rnd.random() * 6 for _ in range(4)]
    H = [[0] * D for _ in range(W)]
    fixo = [[False] * D for _ in range(W)]
    for x in range(W):
        for z in range(D):
            v = 1.2 + 0.7 * math.sin(x * 0.11 + fase[0]) + 0.6 * math.sin(z * 0.09 + fase[1]) + 0.4 * math.sin((x + z) * 0.06 + fase[2])
            H[x][z] = max(0, min(3, round(v * rel_ruido)))
    for (x1, z1, x2, z2, nivel, margem) in pads:
        for x in range(x1 - margem, x2 + margem + 1):
            for z in range(z1 - margem, z2 + margem + 1):
                if not (0 <= x < W and 0 <= z < D):
                    continue
                dentro = x1 <= x <= x2 and z1 <= z <= z2
                if dentro:
                    H[x][z] = nivel
                    fixo[x][z] = True
                elif not fixo[x][z]:
                    dist = max(x1 - x, x - x2, z1 - z, z - z2)
                    t = dist / (margem + 1)
                    H[x][z] = round(nivel * (1 - t) + H[x][z] * t)
    for (fx, fz), nivel in (fixas or {}).items():
        H[fx][fz] = nivel
        fixo[fx][fz] = True
    for _ in range(40):
        for x in range(W):
            for z in range(D):
                if fixo[x][z]:
                    continue
                viz = [H[a][b] for a, b in ((x + 1, z), (x - 1, z), (x, z + 1), (x, z - 1)) if 0 <= a < W and 0 <= b < D]
                lo, hi = max(viz) - 1, min(viz) + 1
                H[x][z] = min(max(H[x][z], lo), hi) if lo <= hi else round(sum(viz) / len(viz))
    return H, fixo


def preencher_terreno(c, H, W, D, agua=None):
    for x in range(W):
        for z in range(D):
            h = H[x][z]
            for y in range(-4, h):
                c.ponto(x, y, z, TERRA if y >= h - 3 else pal([("stone", 4), ("andesite", 2), ("tuff", 2)], 9))
            c.ponto(x, h, z, GRAMA)
