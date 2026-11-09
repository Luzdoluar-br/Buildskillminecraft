"""X04: ruína COM CAUSA x dano aleatório, sobre a mesma casa de pedra (15 x 11, dois pisos, telhado de duas águas).
 R0 intacta | R1 controle: 40% dos blocos removidos ao acaso | R2 abandono (tempo e água) | R3 impacto (explosão, raio 6) | R4 incêndio
Métrica objetiva: blocos FLUTUANTES (sem ligação por face com o chão) após o dano. Dano aleatório deixa muitos; as causas físicas deixam 0.
Avaliação visual: ver imagens/ e README.md (a "legibilidade da causa" é julgamento visual, não número).
Rode: python experimento.py"""
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from exp_util import *  # noqa: E402,F403
from construcao import ruina  # noqa: E402

AQUI = Path(__file__).resolve().parent
c = Cena("x04_ruinas", semente=21)
chao(c, -6, -8, 5 * 26 + 6, 18)
PEDRA = pal([("stone_bricks", 4), ("andesite", 2), ("tuff_bricks", 1.5)], 7)
BASE_Y = 1     # y do primeiro bloco da casa (fundação); tudo que toca y<=BASE_Y está apoiado no chão


def casa(x0):
    m = Molde(c, x0, 0, 15, 11, 1)
    m.box(0, 0, 0, 14, 0, 10, PEDRA)
    m.oca(0, 1, 0, 14, 8, 10, PEDRA)
    m.box(1, 4, 1, 13, 4, 9, M + "spruce_planks")                            # piso do andar de cima
    m.limpar(10, 4, 1, 12, 4, 3)
    for k in range(1, 5):
        m.st(11, k, k, "spruce_stairs", SUL)
    for lx in (3, 7, 11):
        for ly in (2, 6):
            m.p(lx, ly, 10, M + "glass_pane"); m.p(lx, ly + 1 if ly == 2 else ly, 10, M + "glass_pane")
    m.limpar(7, 1, 10, 7, 2, 10)
    m.porta(7, 1, 10, "spruce")
    m.box(1, 8, 1, 13, 8, 9, M + "spruce_planks")
    m.telhado_x(0, 14, 0, 10, 9, "dark_oak_stairs", PEDRA, beiral=1, beiral_x=1)
    m.box(12, 9, 1, 12, 14, 2, PEDRA)                                          # chaminé
    m.p(3, 1, 2, M + "crafting_table"); m.p(4, 1, 2, M + "barrel")
    m.box(2, 5, 8, 4, 5, 8, M + "bookshelf")
    return (x0 - 1, 1, -1, x0 + 15, 14, 11)


def flutuantes(cena, caixa, y_base):
    pos = {p for p, b in cena.blocos.items() if ruina._dentro(p, caixa) and not any(s in ruina._nome(b) for s in ruina.SEM_ESTRUTURA)}
    visto, f = set(), 0
    for p in pos:
        if p in visto:
            continue
        comp, pilha, toca = [], [p], False
        visto.add(p)
        while pilha:
            q = pilha.pop(); comp.append(q)
            if q[1] <= y_base:
                toca = True
            for d in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
                r = (q[0] + d[0], q[1] + d[1], q[2] + d[2])
                if r in pos and r not in visto:
                    visto.add(r); pilha.append(r)
        if not toca:
            f += len(comp)
    return f


caixas = [casa(i * 26) for i in range(5)]
resultado = {}
resultado["R0_intacta"] = {"blocos": sum(1 for p in c.blocos if ruina._dentro(p, caixas[0])), "flutuantes": flutuantes(c, caixas[0], BASE_Y)}

# R1 controle: remoção aleatória uniforme
rnd = random.Random(3)
for p in [p for p in c.blocos if ruina._dentro(p, caixas[1]) and p[1] > BASE_Y]:
    if rnd.random() < 0.40:
        c.blocos.pop(p)
resultado["R1_aleatoria"] = {"blocos": sum(1 for p in c.blocos if ruina._dentro(p, caixas[1])), "flutuantes": flutuantes(c, caixas[1], BASE_Y)}

# R2 abandono
ruina.abandono(c, caixas[2], BASE_Y, semente=5, lado_exposto="norte", intensidade=0.85)
resultado["R2_abandono"] = {"blocos": sum(1 for p in c.blocos if ruina._dentro(p, caixas[2])), "flutuantes": flutuantes(c, caixas[2], BASE_Y)}

# R3 impacto: ponto na fachada leste, nível do andar de cima
x0 = 3 * 26
ruina.impacto(c, caixas[3], (x0 + 15, 6, 5), 6.0, BASE_Y, semente=8)
resultado["R3_impacto"] = {"blocos": sum(1 for p in c.blocos if ruina._dentro(p, caixas[3])), "flutuantes": flutuantes(c, caixas[3], BASE_Y)}

# R4 incêndio
ruina.incendio(c, caixas[4], BASE_Y, semente=2)
resultado["R4_incendio"] = {"blocos": sum(1 for p in c.blocos if ruina._dentro(p, caixas[4])), "flutuantes": flutuantes(c, caixas[4], BASE_Y)}

erros, dims, n, nb = fechar(c, AQUI, "x04_ruinas", ignorar=("E-21", "E-23", "E-05", "E-10", "E-11", "E-02", "E-03", "E-29"))
print("blocos:", nb, "dims:", dims, "paleta:", n)
for k, v in resultado.items():
    print(k, v)
print(relatorio(erros))
vistas = {}
for i in range(5):
    x = i * 26
    vistas["r%d_frente" % i] = ((x + 7, 10, -17), (x + 7, 6, 5))
    vistas["r%d_obliqua" % i] = ((x + 26, 11, -12), (x + 6, 5, 5))
fotos(c, AQUI, vistas, w=640, h=420, fov=62)
