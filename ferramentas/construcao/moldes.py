"""Moldes locais (coordenadas da construção com giro de 180 graus), orientação de blocos e telhados. Genérico: sem paletas de projeto."""
import math
import random
import sys

from .cena import Cena, Paleta, escada, laje, LESTE, OESTE, SUL, NORTE  # noqa: E402,F401

M = "minecraft:"
ESCADAS = []        # lances de escada interna: (molde, [(lx,ly,lz,dir_local)...], (lx,ly,lz) célula à frente do último degrau); a auditoria confere cada um
FLIP = {LESTE: OESTE, OESTE: LESTE, SUL: NORTE, NORTE: SUL}


def pal(itens, s=1):
    """Paleta ponderada: lista de (nome_sem_prefixo, peso). Ex.: pal([("stone_bricks", 3), ("andesite", 2)])."""
    return Paleta([(M + n if ":" not in n else n, p) for n, p in itens], s)


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

    def porta_dir(self, x, y, z, madeira, frente_local):
        """Porta cuja FRENTE (lado de fora) olha para `frente_local`; gira com a casa."""
        card = self.CARD[self.dirm(frente_local)]
        base = {"door_hinge_bit": False, "minecraft:cardinal_direction": card, "open_bit": False}
        self.p(x, y, z, (M + madeira + "_door", {**base, "upper_block_bit": False}))
        self.p(x, y + 1, z, (M + madeira + "_door", {**base, "upper_block_bit": True}))

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


