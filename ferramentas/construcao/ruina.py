"""Deterioração de construções COM CAUSA (em vez de dano aleatório).

Princípio (documentado em estilos/ e ambientacao/ruinas-e-narrativa.md): uma ruína precisa mostrar COMO e POR QUE foi deteriorada.
Cada função aplica uma causa a uma caixa (x1,y1,z1,x2,y2,z2) de uma `Cena`:
  - abandono(c, caixa, ...)  : tempo + água: telhado e madeira falham primeiro, topos de muro erodem, musgo/rachaduras, vegetação nas arestas
  - impacto(c, caixa, centro, raio) : explosão/guerra: dano em gradiente a partir de um ponto, chamuscado, entulho abaixo
  - incendio(c, caixa) : madeira some, pedra fica enegrecida acima das aberturas, chaminés intactas
  - remover_flutuantes(c, caixa): colapso físico: tudo que perdeu ligação com o chão cai (vira entulho ou some)
Ordem física de falha usada (INTERPRETAÇÃO PRÓPRIA apoiada em guia de conservação de ruínas de alvenaria; ver ambientacao/ruinas-e-narrativa.md):
cobertura -> topos de muros -> pisos/madeiramento -> esquadrias -> cantos/empenas -> fachadas; pedra e tijolo sobrevivem mais que madeira.
"""
import math
import random

M = "minecraft:"
MADEIRA = ("planks", "_log", "_wood", "door", "trapdoor", "fence", "_stairs", "_slab", "bookshelf", "barrel", "crafting_table", "ladder")
PEDRAS = ("stone_bricks", "cobblestone", "andesite", "tuff_bricks", "polished_andesite", "deepslate_bricks", "bricks", "stone")
SEM_ESTRUTURA = ("grass", "fern", "flower", "tulip", "poppy", "vine", "moss_carpet", "leaves", "water", "lantern", "glass", "pane", "carpet", "berry", "azalea")


def _nome(b):
    return (b if isinstance(b, str) else b[0]).replace("minecraft:", "")


def _eh_madeira(n):
    base = n
    if "stairs" in n or "slab" in n:
        return any(t in n for t in ("oak", "spruce", "birch", "jungle", "acacia", "cherry", "mangrove", "bamboo", "crimson", "warped", "pale_oak"))
    return any(t in base for t in MADEIRA) and not any(s in n for s in ("stone", "brick", "deepslate", "tuff", "andesite", "cobble"))


def _dentro(p, caixa):
    x, y, z = p
    return caixa[0] <= x <= caixa[3] and caixa[1] <= y <= caixa[4] and caixa[2] <= z <= caixa[5]


def _envelhece(c, p, b, rnd, musgo=0.25, rachado=0.2):
    n = _nome(b)
    r = rnd.random()
    if n == "stone_bricks":
        c.blocos[p] = M + ("mossy_stone_bricks" if r < musgo else "cracked_stone_bricks" if r < musgo + rachado else "stone_bricks")
    elif n == "cobblestone":
        c.blocos[p] = M + ("mossy_cobblestone" if r < musgo else "cobblestone")


def remover_flutuantes(c, caixa, y_base, entulho=True, semente=1):
    """Remove componentes (vizinhança por face) que não tocam o chão (y <= y_base). Se `entulho`, parte vira bloco caído no chão logo abaixo."""
    rnd = random.Random(semente)
    pos = {p for p, b in c.blocos.items() if _dentro(p, caixa) and not any(s in _nome(b) for s in SEM_ESTRUTURA)}
    visto, ligados = set(), set()
    for p in list(pos):
        if p in visto:
            continue
        comp, pilha, toca = [], [p], False
        visto.add(p)
        while pilha:
            q = pilha.pop()
            comp.append(q)
            if q[1] <= y_base:
                toca = True
            for d in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
                r = (q[0] + d[0], q[1] + d[1], q[2] + d[2])
                if r in pos and r not in visto:
                    visto.add(r)
                    pilha.append(r)
        if toca:
            ligados.update(comp)
    removidos = 0
    for p in pos - ligados:
        b = c.blocos.pop(p)
        removidos += 1
        if entulho and rnd.random() < 0.35:                      # cai e para no primeiro apoio abaixo
            y = p[1]
            while y > y_base + 1 and (p[0], y - 1, p[2]) not in c.blocos:
                y -= 1
            if (p[0], y, p[2]) not in c.blocos and not _eh_madeira(_nome(b)):
                c.blocos[(p[0], y, p[2])] = M + rnd.choice(["cobblestone", "mossy_cobblestone", "andesite"])
    return removidos


def vegetar(c, caixa, y_base, semente=1, densidade=0.5):
    """Vegetação por umidade/exposição: musgo e grama no chão e nos topos de parede, trepadeiras nas faces úmidas, arbusto em entulho."""
    rnd = random.Random(semente)
    for (x, y, z), b in list(c.blocos.items()):
        if not _dentro((x, y, z), caixa) or any(s in _nome(b) for s in SEM_ESTRUTURA):
            continue
        acima = (x, y + 1, z) in c.blocos
        if not acima and rnd.random() < 0.25 * densidade and y > y_base:
            c.blocos[(x, y + 1, z)] = M + rnd.choice(["short_grass", "short_grass", "fern", "moss_carpet"])           # topo de muro
            if rnd.random() < 0.3:
                c.blocos[(x, y, z)] = M + "moss_block"
        if y == y_base + 1 and not acima and rnd.random() < 0.35 * densidade:
            c.blocos[(x, y + 1, z)] = M + rnd.choice(["short_grass", "tall_grass", "fern", "poppy", "dandelion"])
    return c


def limitar_balancos_de_madeira(c, caixa, maximo=3):
    """Madeira não segura vãos longos sem apoio: remove blocos de madeira a mais de `maximo` células (por face) de qualquer apoio de pedra/terra.
    Evita a 'cumeeira flutuando' depois que o telhado e as paredes de apoio caem."""
    pos = {p for p, b in c.blocos.items() if _dentro(p, caixa) and not any(s in _nome(b) for s in SEM_ESTRUTURA)}
    mad = {p for p in pos if _eh_madeira(_nome(c.blocos[p]))}
    apoio = pos - mad
    dist = {}
    fila = []
    for p in mad:
        for d in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
            if (p[0] + d[0], p[1] + d[1], p[2] + d[2]) in apoio:
                dist[p] = 1
                fila.append(p)
                break
    i = 0
    while i < len(fila):
        q = fila[i]
        i += 1
        for d in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
            r = (q[0] + d[0], q[1] + d[1], q[2] + d[2])
            if r in mad and r not in dist:
                dist[r] = dist[q] + 1
                fila.append(r)
    n = 0
    for p in mad:
        if dist.get(p, 99) > maximo:
            c.blocos.pop(p, None)
            n += 1
    return n


def abandono(c, caixa, y_base, y_piso_alto=None, semente=1, lado_exposto="norte", intensidade=0.7, musgo=0.3):
    rnd = random.Random(semente)
    x1, y1, z1, x2, y2, z2 = caixa
    for p, b in list(c.blocos.items()):
        if not _dentro(p, caixa):
            continue
        n = _nome(b)
        x, y, z = p
        alt = (y - y_base) / max(1, (y2 - y_base))
        expo = (z - z1) / max(1, (z2 - z1))
        if lado_exposto == "norte":
            expo = 1 - expo
        if _eh_madeira(n):
            if "door" in n or "trapdoor" in n or "pane" in n:
                if rnd.random() < 0.8:
                    c.blocos.pop(p, None)
            elif y > y_base + 4 or "stairs" in n or "slab" in n:                       # cobertura e madeiramento alto: some primeiro
                if rnd.random() < min(0.97, 0.45 + 0.6 * intensidade * (0.5 + 0.5 * expo)):
                    c.blocos.pop(p, None)
            elif rnd.random() < 0.55 * intensidade:                                    # piso/madeiramento baixo: apodrece
                c.blocos.pop(p, None)
        elif "glass" in n or "pane" in n:
            c.blocos.pop(p, None)
        elif any(t in n for t in PEDRAS):
            # topos de parede e cantos erodem: probabilidade cresce com a altura e com a exposição; base quase intacta
            if rnd.random() < 0.55 * intensidade * (alt ** 1.4) * (0.6 + 0.8 * expo):
                c.blocos.pop(p, None)
            else:
                _envelhece(c, p, b, rnd, musgo=musgo * (1.0 - 0.5 * alt) + 0.1, rachado=0.15 * alt + 0.05)
    limitar_balancos_de_madeira(c, caixa)
    remover_flutuantes(c, caixa, y_base, semente=semente)
    vegetar(c, caixa, y_base, semente=semente, densidade=1.0)
    return c


def impacto(c, caixa, centro, raio, y_base, semente=1, chamusco=0.5):
    rnd = random.Random(semente)
    cx, cy, cz = centro
    for p, b in list(c.blocos.items()):
        if not _dentro(p, caixa):
            continue
        d = math.sqrt((p[0] - cx) ** 2 + (p[1] - cy) ** 2 + (p[2] - cz) ** 2)
        if d <= raio:
            if rnd.random() < 1.0 - (d / raio) ** 1.6 * 0.8:
                c.blocos.pop(p, None)
                continue
        if d <= raio * 1.7 and any(t in _nome(b) for t in PEDRAS + MADEIRA) and rnd.random() < chamusco * (1 - d / (raio * 1.7)):
            c.blocos[p] = M + rnd.choice(["blackstone", "cracked_stone_bricks", "polished_blackstone_bricks"])
    n = remover_flutuantes(c, caixa, y_base, semente=semente)
    # entulho: pilha mais alta perto do centro projetado no chão
    for _ in range(int(raio * raio * 1.2)):
        a, r = rnd.random() * 2 * math.pi, abs(rnd.gauss(0, raio * 0.7))
        x, z = int(cx + math.cos(a) * r), int(cz + math.sin(a) * r)
        y = y_base + 1
        while (x, y, z) in c.blocos:
            y += 1
        if _dentro((x, y, z), caixa) and y <= y_base + 3:
            c.blocos[(x, y, z)] = M + rnd.choice(["cobblestone", "mossy_cobblestone", "andesite", "stone_bricks", "gravel"])
    return n


def incendio(c, caixa, y_base, semente=1):
    rnd = random.Random(semente)
    aberturas = []
    for p, b in list(c.blocos.items()):
        if _dentro(p, caixa) and _eh_madeira(_nome(b)) or ("pane" in _nome(b) and _dentro(p, caixa)):
            if "pane" in _nome(b):
                aberturas.append(p)
            c.blocos.pop(p, None)
    for (x, y, z) in aberturas:                                              # fuligem acima das aberturas
        for dy in (1, 2, 3):
            p = (x, y + dy, z)
            if p in c.blocos and any(t in _nome(c.blocos[p]) for t in PEDRAS) and rnd.random() < 0.8 - 0.2 * dy:
                c.blocos[p] = M + rnd.choice(["blackstone", "polished_blackstone_bricks"])
    for p, b in list(c.blocos.items()):
        if _dentro(p, caixa) and any(t in _nome(b) for t in PEDRAS) and rnd.random() < 0.12:
            c.blocos[p] = M + "cracked_stone_bricks"
    limitar_balancos_de_madeira(c, caixa)
    remover_flutuantes(c, caixa, y_base, semente=semente)
    return c
