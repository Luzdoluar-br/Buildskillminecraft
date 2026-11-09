"""X03: curvas e diagonais dentro do que o Minecraft permite.
 A) torres circulares de raio 2,5 / 3,5 / 5 / 7 / 10: a partir de que raio o círculo "lê" como círculo? (medida: erro máximo de circularidade em blocos)
 B) cúpulas: Cena.cupula (blocos cheios) x cúpula com lajes (resolução de meio bloco) nos raios 5, 8, 12
 C) rampas e diagonais: inclinações 1:1, 1:2 e 1:3 (escada, laje) e muro diagonal a 45 graus
Rode: python experimento.py"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from exp_util import *  # noqa: E402,F403

AQUI = Path(__file__).resolve().parent
c = Cena("x03_curvas", semente=11)
chao(c, -6, -14, 150, 14, y=0, bloco=M + "smooth_stone")
PEDRA = pal([("stone_bricks", 4), ("andesite", 2), ("polished_andesite", 1)], 3)
metricas = {}


def anel_circular(cx, cz, r, y0, y1, bloco):
    """Anel de 1 bloco: células cuja distância ao centro está em [r-0.5, r+0.5)."""
    cels = []
    for x in range(int(cx - r) - 2, int(cx + r) + 3):
        for z in range(int(cz - r) - 2, int(cz + r) + 3):
            d = math.hypot(x - cx, z - cz)
            if r - 0.5 <= d < r + 0.5:
                cels.append((x, z, d))
                for y in range(y0, y1 + 1):
                    c.ponto(x, y, z, bloco)
    return cels


# ---------------- A) torres circulares
x = 6
for r in (2.5, 3.5, 5.0, 7.0, 10.0):
    cels = anel_circular(x, -4, r, 1, 7, PEDRA)
    conj = {(a, b) for (a, b, _) in cels}
    def maior_corrida(chaves, eixo):
        melhor = 0
        for k in {t[1 - eixo] for t in conj}:
            vs = sorted(t[eixo] for t in conj if t[1 - eixo] == k)
            atual = 1
            for a, b in zip(vs, vs[1:]):
                atual = atual + 1 if b == a + 1 else 1
                melhor = max(melhor, atual)
            melhor = max(melhor, atual)
        return melhor
    reta = max(maior_corrida(conj, 0), maior_corrida(conj, 1))
    metricas["torre_r%s" % r] = {"diametro_blocos": int(2 * r + 1), "celulas_no_anel": len(cels), "maior_trecho_reto": reta, "reto/diametro": round(reta / (2 * r + 1), 2)}
    x += int(2 * r) + 6

# ---------------- B) cúpulas
x = 6
base_z = 8
for r in (5, 8, 12):
    # B1: Cena.cupula (blocos cheios, casca de 1)
    c.cupula(x, 1, base_z, r, M + "dark_oak_planks", espessura=1.0, altura_rel=0.7)
    metricas["cupula_blocos_r%d" % r] = {"blocos": sum(1 for (bx, by, bz) in c.blocos if abs(bx - x) <= r and abs(bz - base_z) <= r and by >= 1)}
    x += 2 * r + 4
for r in (5, 8, 12):
    # B2: casca com lajes: altura contínua h(d) = H*sqrt(1-(d/r)^2); parte inteira = bloco cheio, parte >= 0.5 = laje por cima
    H = r * 0.7
    n = 0
    for xx in range(x - r - 1, x + r + 2):
        for zz in range(base_z - r - 1, base_z + r + 2):
            d = math.hypot(xx - x, zz - base_z)
            if d > r:
                continue
            h = H * math.sqrt(max(0.0, 1 - (d / r) ** 2))
            ht = round(h * 2) / 2.0                                    # resolução de meio bloco
            # casca: só a camada de topo e 1 abaixo (oca por dentro)
            inteiro = int(ht)
            for y in range(max(1, inteiro - 1), inteiro + 1):
                c.ponto(xx, y + 1, zz, M + "spruce_planks"); n += 1
            if ht - inteiro >= 0.5:
                c.ponto(xx, inteiro + 2, zz, laje(M + "spruce_slab", False)); n += 1
    metricas["cupula_lajes_r%d" % r] = {"blocos": n}
    x += 2 * r + 4

# ---------------- C) rampas e diagonais (z = -12)
base = -12
for k, (nome, passo) in enumerate((("1:1", 1), ("1:2", 2), ("1:3", 3))):
    x0 = 6 + k * 24
    for i in range(0, 18):
        if passo == 1:
            h = i
            if h < 8:
                c.caixa(x0 + i, 1, base, x0 + i, h, base + 2, M + "stone_bricks")
                c.ponto(x0 + i, h + 1, base, escada(M + "stone_brick_stairs", LESTE)) if h < 7 else None
        elif passo == 2:
            h = i // 2
            if h < 8:
                c.caixa(x0 + i, 1, base, x0 + i, max(1, h), base + 2, M + "stone_bricks") if h >= 1 else None
                for z in range(base, base + 3):
                    c.ponto(x0 + i, h + 1, z, laje(M + "stone_brick_slab", False) if i % 2 == 0 else M + "stone_bricks") if False else None
        else:
            h = i // 3
    # rampa 1:2 e 1:3 com lajes: alturas de meio bloco; implementação genérica
    for i in range(0, 18):
        h2 = i / float(passo)
        inteiro = int(h2)
        for z in range(base, base + 3):
            if inteiro >= 1:
                c.caixa(x0 + i, 1, z, x0 + i, inteiro, z, M + "stone_bricks")
            if passo == 2 and h2 - inteiro >= 0.5:
                c.ponto(x0 + i, inteiro + 1, z, laje(M + "stone_brick_slab", False))
            elif passo == 1 and False:
                pass
            elif passo == 3:
                frac = h2 - inteiro
                if frac >= 0.66:
                    c.ponto(x0 + i, inteiro + 1, z, laje(M + "stone_brick_slab", False))
# muro diagonal a 45 graus: só blocos (z = -12 + passo, x + passo)
x0 = 6 + 3 * 24
for i in range(0, 14):
    for h in range(1, 7):
        c.ponto(x0 + i, h, base + i - 3, M + "stone_bricks")
        c.ponto(x0 + i + 1, h, base + i - 3, M + "stone_bricks")      # espessura 2 para fechar a diagonal

erros, dims, n, nb = fechar(c, AQUI, "x03_curvas", ignorar=("E-21",))
print("blocos:", nb, "dims:", dims, "paleta:", n)
for k, v in metricas.items():
    print(k, v)
print(relatorio(erros))
vistas = {"torres": ((20, 12, -16), (20, 3, -4)), "cupulas": ((30, 14, 22), (30, 5, 8)), "rampas": ((24, 12, -22), (24, 3, -12)), "cupulas_lajes": ((95, 14, 22), (95, 5, 8))}
fotos(c, AQUI, vistas, w=900, h=520, fov=65)
