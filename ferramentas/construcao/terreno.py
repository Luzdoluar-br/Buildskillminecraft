"""Terreno por mapa de alturas: pads planos com margem, relaxamento de inclinação (<=1 entre vizinhos) e preenchimento."""
import math
import random

from .moldes import pal
from .cena import Cena, Paleta


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


def preencher_terreno(c, H, W, D, topo, solo, rocha=None, fundo=-4):
    """Preenche o terreno: `topo` (ex.: grama), `solo` (3 camadas abaixo do topo) e `rocha` (resto até `fundo`). Cada um pode ser bloco ou Paleta."""
    for x in range(W):
        for z in range(D):
            h = H[x][z]
            for y in range(fundo, h):
                c.ponto(x, y, z, solo if y >= h - 3 else (rocha or pal([("stone", 4), ("andesite", 2), ("tuff", 2)], 9)))
            c.ponto(x, h, z, topo)
