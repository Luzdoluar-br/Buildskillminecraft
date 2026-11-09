"""Auditoria genérica de construções (regras aprendidas em erros-e-licoes.md). Funciona sobre qualquer `Cena`; regras de terreno são opcionais.

Uso mínimo:
    from construcao.auditoria_geral import auditar, relatorio
    erros = auditar(cena)                      # regras que só dependem dos blocos
    erros += auditar(cena, contexto=ctx)       # + regras de terreno/ocupação, se você tiver um contexto (ver `Contexto`)
    print(relatorio(erros))                    # meta: TOTAL 0

Cada erro = (código, posição, detalhe). Os códigos E-xx são os do registro `erros-e-licoes.md`.
Lances de escada interna: registrar com `moldes.ESCADAS` (ver moldes.py / casas da Aula 02).
"""
import collections
import math
import pathlib
from dataclasses import dataclass, field

from .moldes import ESCADAS, SUL, NORTE, LESTE, OESTE

VALIDOS = set((pathlib.Path(__file__).with_name("blocos_validos.txt")).read_text().split()) | {"air"}      # 1187 IDs oficiais (referencia/blocos-bedrock.md)
PRECISA_APOIO = ("barrel", "smoker", "furnace", "crafting_table", "bookshelf", "lectern", "anvil", "hay_block", "melon_block", "pumpkin", "carpet",
                 "_door", "fence", "lantern", "carrots", "potatoes", "wheat", "short_grass", "tall_grass", "fern", "tulip", "poppy", "cornflower",
                 "bluet", "daisy", "valley", "dandelion", "berry", "azalea", "waterlily", "farmland", "stone_brick_wall")
TERRENO = ("grass", "dirt", "moss", "podzol", "path", "gravel", "cobble", "andesite", "stone", "tuff", "polished")
import json
ESTADOS = json.loads((pathlib.Path(__file__).with_name("estados_validos.json")).read_text(encoding="utf-8"))   # {bloco: {estado: [valores]}} OFICIAL (bedrock-samples)
MAQUINAS = ("smoker", "blast_furnace", "furnace", "lectern", "anvil")


def nome(b):
    return "air" if b is None else (b if isinstance(b, str) else b[0]).replace("minecraft:", "")


def estado(b):
    return {} if b is None or isinstance(b, str) else b[1]


def passavel(n):
    return n == "air" or any(k in n for k in ("grass", "fern", "tulip", "poppy", "cornflower", "bluet", "daisy", "valley", "dandelion", "berry",
                                              "azalea", "carpet", "lily_pad", "farmland", "stairs", "slab", "lantern", "rose", "waterlily"))


def solido(n):
    return not passavel(n) and not any(k in n for k in ("pane", "door", "water"))


@dataclass
class Contexto:
    """Dados opcionais de terreno e ocupação para as regras E-12/E-14/E-15/E-16/E-19."""
    H: list = None                      # H[x][z] = y do bloco de topo do terreno
    W: int = 0
    D: int = 0
    rede: set = field(default_factory=set)         # células (x,z) por onde se anda (ruas, praça)
    isentas: set = field(default_factory=set)      # células da rede onde objetos sólidos são intencionais
    objetos: list = field(default_factory=list)    # (nome, "disco"/"ret", geometria, raio_do_objeto, largura_do_anel)
    conflitos: list = field(default_factory=list)  # (novo, existente, célula) do registro de ocupação
    arvores: list = field(default_factory=list)    # [(x, z)] troncos plantados
    agua: set = field(default_factory=set)


def regra_ids(c):
    return [("E-01 ID inexistente no Bedrock", p, nome(b)) for p, b in c.blocos.items() if nome(b) not in VALIDOS]


def regra_estados(c):
    """E-31: cada estado e valor de cada bloco deve existir na lista oficial (ex.: `facing_direction` não vale em smoker; `wood_type` não existe em cerca)."""
    erros = []
    vistos = set()
    for p, b in c.blocos.items():
        if isinstance(b, str) or not b[1]:
            continue
        n = nome(b)
        for k, v in b[1].items():
            chave = (n, k, str(v))
            if chave in vistos:
                continue
            ok = n in ESTADOS and k in ESTADOS[n] and (int(v) if isinstance(v, bool) else v) in ESTADOS[n][k]
            if not ok:
                vistos.add(chave)
                motivo = "bloco sem estados na lista" if n not in ESTADOS else ("estado inexistente" if k not in ESTADOS[n] else "valor fora de %s" % ESTADOS[n][k])
                erros.append(("E-31 estado inválido: %s (%s)" % (k, motivo), p, "%s=%r em %s" % (k, v, n)))
    return erros


def _grupos_de_cerca(c):
    """Agrupa cercas ligadas por face e diz se cada grupo toca em algum bloco que NÃO seja cerca (torre, chão, parede). Cabos presos a torres passam."""
    cercas = {p for p, b in c.blocos.items() if "fence" in nome(b) and "gate" not in nome(b)}
    grupo = {}
    firmes = set()
    for p in cercas:
        if p in grupo:
            continue
        gid, pilha, membros, toca = len(set(grupo.values())), [p], [], False
        grupo[p] = gid
        while pilha:
            q = pilha.pop()
            membros.append(q)
            for d in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
                r = (q[0] + d[0], q[1] + d[1], q[2] + d[2])
                if r in cercas:
                    if r not in grupo:
                        grupo[r] = gid
                        pilha.append(r)
                elif r in c.blocos and nome(c.blocos[r]) not in ("air",) and "lantern" not in nome(c.blocos[r]) and "water" not in nome(c.blocos[r]):
                    toca = True
        if toca:
            firmes.add(gid)
    return {p: (g in firmes) for p, g in grupo.items()}


def regra_apoio(c):
    erros = []
    firme = _grupos_de_cerca(c)
    for (x, y, z), b in c.blocos.items():
        n = nome(b)
        if not any(k in n for k in PRECISA_APOIO) or (n == "lantern" and estado(b).get("hanging")):
            continue
        abaixo = nome(c.pegar(x, y - 1, z))
        if abaixo == "air" or (abaixo == "water" and "waterlily" not in n):
            if "fence" in n and "gate" not in n and firme.get((x, y, z)):
                continue          # cabo/guarda-corpo ligado a estrutura sólida: aceito (elemento suspenso intencional)
            erros.append(("E-21 bloco sem apoio (flutuando): %s sobre %s" % (n, abaixo), (x, y, z), n))
    return erros


def regra_portas(c):
    erros = []
    for (x, y, z), b in c.blocos.items():
        if not (isinstance(b, tuple) and nome(b).endswith("_door") and not b[1].get("upper_block_bit")):
            continue
        if nome(c.pegar(x, y + 1, z)) != nome(b):
            erros.append(("E-03 porta sem metade de cima", (x, y, z), nome(b)))
        if c.pegar(x, y + 2, z) is None:
            erros.append(("E-10 vão acima da porta (falta verga)", (x, y, z), nome(b)))
        card = b[1].get("minecraft:cardinal_direction")
        d = {"north": (0, -1), "south": (0, 1), "east": (1, 0), "west": (-1, 0)}.get(card, (0, 1))      # lado de FORA
        for lado, s in (("fora", 1), ("dentro", -1)):
            for dy in (0, 1):
                n = nome(c.pegar(x + d[0] * s, y + dy, z + d[1] * s))
                if solido(n):
                    erros.append(("E-02 porta barrada (%s)" % lado, (x + d[0] * s, y + dy, z + d[1] * s), n))
        lat = (1, 0) if d[0] == 0 else (0, 1)           # batentes: ao longo da parede
        for s in (-1, 1):
            for dy in (0, 1, 2):
                n = nome(c.pegar(x + lat[0] * s, y + dy, z + lat[1] * s))
                if n == "air" or "pane" in n or "glass" in n:
                    erros.append(("E-11 porta desconexa da parede (batente %s)" % ("vidro" if n != "air" else "vazio"), (x + lat[0] * s, y + dy, z + lat[1] * s), n))
    return erros


def regra_lanternas(c):
    return [("E-05 lanterna pendurada sem suporte", p, "lantern") for p, b in c.blocos.items()
            if nome(b) == "lantern" and estado(b).get("hanging") and c.pegar(p[0], p[1] + 1, p[2]) is None]


def regra_agua(c):
    return [("E-06 água com ar ao lado (pode vazar)", p, "water") for p, b in c.blocos.items()
            if nome(b) == "water" and any(c.pegar(p[0] + dx, p[1], p[2] + dz) is None for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)))]


def regra_troncos(c):
    """E-23: tronco 'stripped' horizontal com a ponta no ar (a não ser que haja lanterna pendurada logo abaixo: ponta de viga intencional)."""
    erros = []
    for (x, y, z), b in c.blocos.items():
        n = nome(b)
        eixo = estado(b).get("pillar_axis")
        if n.startswith("stripped_") and n.endswith("_log") and eixo in ("x", "z"):
            d = (1, 0) if eixo == "x" else (0, 1)
            for s in (1, -1):
                if nome(c.pegar(x + d[0] * s, y, z + d[1] * s)) == "air" and nome(c.pegar(x, y - 1, z)) != "lantern":
                    erros.append(("E-23 ponta de tronco exposta (canto/encontro errado)", (x, y, z), "%s axis=%s" % (n, eixo)))
                    break
    return erros


def regra_maquinas(c):
    erros = []
    ve = {"north": (0, -1), "south": (0, 1), "east": (1, 0), "west": (-1, 0)}
    for (x, y, z), b in c.blocos.items():
        n = nome(b)
        card = estado(b).get("minecraft:cardinal_direction")
        if n in MAQUINAS and card and solido(nome(c.pegar(x + ve[card][0], y, z + ve[card][1]))):
            erros.append(("E-24 máquina virada para a parede", (x, y, z), "%s frente=%s" % (n, card)))
        if n in MAQUINAS + ("pumpkin",) and not card:
            erros.append(("E-24 máquina sem orientação (cardinal_direction)", (x, y, z), n))
        if n == "lightning_rod" and estado(b).get("facing_direction") != 1:
            erros.append(("E-25 para-raios não aponta para cima (facing_direction=1)", (x, y, z), n))
        if n == "bed":
            erros.append(("E-04 cama sem entidade de bloco (o jogo remove); use entidades={'id':'Bed','color':...} ao exportar", (x, y, z), n))
    return erros


def regra_escadas(c, escadas=None):
    erros = []
    for (m, passos, frente) in (ESCADAS if escadas is None else escadas):
        for (lx, ly, lz, d) in passos:
            b = c.pegar(*m.mundo(lx, ly, lz))
            if "stairs" not in nome(b) or estado(b).get("weirdo_direction") != m.dirm(d) or estado(b).get("upside_down_bit"):
                erros.append(("E-29 degrau faltando ou virado errado", m.mundo(lx, ly, lz), nome(b)))
            for h in (1, 2):
                n_ = nome(c.pegar(*m.mundo(lx, ly + h, lz)))
                if solido(n_):
                    erros.append(("E-29 sem altura livre sobre o degrau", m.mundo(lx, ly + h, lz), n_))
        topo = nome(c.pegar(*m.mundo(*frente)))
        if not solido(topo):
            erros.append(("E-29 escada não chega ao piso (falta piso à frente do último degrau)", m.mundo(*frente), topo))
    return erros


def regras_de_terreno(c, ctx):
    erros = []
    H = ctx.H
    for (x, y, z), b in c.blocos.items():                      # E-14 poste sobre terreno
        if nome(b) == "stone_brick_wall" and nome(c.pegar(x, y + 1, z)) == "spruce_fence":
            abaixo = nome(c.pegar(x, y - 1, z))
            if abaixo == "air" or not any(k in abaixo for k in TERRENO) or y - 1 != H[x][z]:
                erros.append(("E-14 poste fora do terreno (sobre %s)" % abaixo, (x, y, z), "poste"))
    for (x, z) in ctx.arvores:
        abaixo = nome(c.pegar(x, H[x][z], z))
        if not any(k in abaixo for k in TERRENO):
            erros.append(("E-14 árvore fora do terreno (sobre %s)" % abaixo, (x, H[x][z], z), "árvore"))
    for conf in ctx.conflitos:                                  # E-16 colisões
        erros.append(("E-16 objetos colidindo/posição inválida", conf[2], "%s x %s" % (conf[0], conf[1])))
    for (nm, tipo, geo, r_obj, anel) in ctx.objetos:           # E-15 caminho ao redor
        if tipo == "disco":
            cels = [(x, z) for x in range(int(geo[0] - anel) - 1, int(geo[0] + anel) + 2) for z in range(int(geo[1] - anel) - 1, int(geo[1] + anel) + 2)
                    if r_obj < math.hypot(x - geo[0], z - geo[1]) <= anel]
        else:
            x1, z1, x2, z2 = geo
            cels = [(x, z) for x in range(x1 - anel, x2 + anel + 1) for z in range(z1 - anel, z2 + anel + 1) if not (x1 <= x <= x2 and z1 <= z <= z2)]
        for (x, z) in cels:
            if not (0 <= x < ctx.W and 0 <= z < ctx.D):
                continue
            for dy in (1, 2):
                n = nome(c.pegar(x, H[x][z] + dy, z))
                if solido(n):
                    erros.append(("E-15 sem caminho livre ao redor de %s" % nm, (x, H[x][z] + dy, z), n))
            if (x, z) in ctx.agua:
                erros.append(("E-15 água no anel de %s" % nm, (x, z), "água"))
    rede = {k for k in ctx.rede if 0 <= k[0] < ctx.W and 0 <= k[1] < ctx.D}
    for (x, z) in rede - ctx.isentas:                           # E-12 obstáculo na rede
        for dy in (1, 2):
            n = nome(c.pegar(x, H[x][z] + dy, z))
            if solido(n) and not (n == "spruce_fence" and "lantern" in nome(c.pegar(x, H[x][z] + dy + 1, z))) \
                    and not (n == "stone_brick_wall" and nome(c.pegar(x, H[x][z] + dy + 1, z)) == "spruce_fence"):
                erros.append(("E-12 obstáculo no caminho/praça", (x, H[x][z] + dy, z), n))
    for (x, z) in rede:                                         # E-19 degrau alto
        for dx, dz in ((1, 0), (0, 1)):
            q = (x + dx, z + dz)
            if q in rede and abs(H[x][z] - H[q[0]][q[1]]) > 1:
                erros.append(("E-19 degrau alto no caminho", (x, z), "dH=%d" % abs(H[x][z] - H[q[0]][q[1]])))
    return erros


REGRAS = (regra_ids, regra_estados, regra_apoio, regra_portas, regra_lanternas, regra_agua, regra_troncos, regra_maquinas)


def auditar(c, contexto=None, escadas=None, ignorar=()):
    """Roda todas as regras. `ignorar` = prefixos de código a omitir, ex.: ('E-21',)."""
    erros = []
    for r in REGRAS:
        erros += r(c)
    erros += regra_escadas(c, escadas)
    if contexto is not None:
        erros += regras_de_terreno(c, contexto)
    return [e for e in erros if not any(e[0].startswith(p) for p in ignorar)]


def relatorio(erros, max_por_regra=6):
    linhas = ["TOTAL: %d" % len(erros)]
    for k, v in collections.Counter(e[0] for e in erros).most_common():
        linhas.append("%4d  %s" % (v, k))
        for e in [e for e in erros if e[0] == k][:max_por_regra]:
            linhas.append("         %s %s" % (e[1], e[2]))
    return "\n".join(linhas)
