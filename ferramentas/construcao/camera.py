# Cópia VENDORIZADA de BotVulpus/addon/tools/construcao/camera.py (código do próprio dono do projeto). Alterações: imports ajustados para funcionar dentro deste repositório.
"""Câmera livre para as construções: tira "fotos" de qualquer ponto, inclusive com os olhos de um jogador (1,62 acima do chão), sem abrir o jogo.

Raycast em numpy sobre a grade de blocos (DDA), com as texturas vanilla do Bedrock. Serve para eu ANDAR pela construção e conferir por partes,
como no Blockbench: `foto(cena, pos=(x, y, z), alvo=(x, y, z))`.

    from construcao.camera import foto, ronda, olhos
    foto(cena, (30, 3, 40), (30, 3, 20), "hall.png")            # câmera em pos, olhando para alvo
    olhos(cena, (30, 1, 50), "norte", "entrada.png")            # de pé em (x, y, z) olhando para o norte (jogador: y é o piso)
    ronda(cena, centro=(30, 5, 30), raio=40, altura=25, pasta=".../fotos")   # 8 fotos ao redor, de cima

Honesto: blocos que não são cubos (cerca, escada, laje, lanterna) aparecem como cubos inteiros e plantas somem; luz e sombra são simples.
Para conferir forma, escala, o que está no chão e o que está no ar, serve. Para detalhes finos, `Cena.construir()` com render do Creator Tools.
"""
from __future__ import annotations

import math
from pathlib import Path

import numpy as np
from PIL import Image

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from previa_voxel import ALIAS, EMISSIVOS, NAO_CUBO, PARES, VAZADOS, _textura, _tingir  # noqa: E402

DIRECOES = {"norte": (0.0, -1.0), "sul": (0.0, 1.0), "leste": (1.0, 0.0), "oeste": (-1.0, 0.0)}
ALTURA_OLHOS = 1.62


def _nome(b) -> str:
    n = b if isinstance(b, str) else b[0]
    return n.replace("minecraft:", "").replace("waxed_", "")


MADEIRAS = {"oak": "planks_oak", "spruce": "planks_spruce", "birch": "planks_birch", "jungle": "planks_jungle", "acacia": "planks_acacia", "dark_oak": "planks_big_oak", "cherry": "cherry_planks", "mangrove": "mangrove_planks", "bamboo": "bamboo_planks", "crimson": "crimson_planks", "warped": "warped_planks"}
SUFIXOS = ("_fence_gate", "_pressure_plate", "_stairs", "_slab", "_fence", "_wall", "_trapdoor", "_door", "_button")


def _nomes_textura(n: str) -> tuple[str, str]:
    """(topo, lado) do pacote de recursos para o bloco; derivados (escada, laje, cerca...) usam o material do bloco inteiro."""
    if n in ALIAS:
        return ALIAS[n]
    if n.startswith("stripped_") and n.endswith("_log"):
        return n + "_top", n
    if n in ("grass_path", "dirt_path"):
        return "grass_path_top", "grass_path_side"
    base = n
    for suf in SUFIXOS:
        if n.endswith(suf):
            base = n[: -len(suf)]
            break
    if base in ALIAS:
        return ALIAS[base]
    if base in MADEIRAS:
        return MADEIRAS[base], MADEIRAS[base]
    if base == "stone_brick":
        return ALIAS["stone_bricks"]
    if base in ("nether_brick", "red_nether_brick"):
        return base, base
    return PARES.get(n, (n, n))


COR_PROPRIA = {"lantern": (255, 168, 64), "soul_lantern": (90, 210, 230), "chain": (64, 70, 84), "iron_chain": (64, 70, 84), "end_rod": (250, 245, 255), "lightning_rod": (200, 120, 70), "ladder": (150, 110, 60), "campfire": (230, 120, 40)}


def _cor_solida(c: tuple[int, int, int]) -> np.ndarray:
    a = np.zeros((16, 16, 4), np.float32)
    a[..., :3] = np.array(c, np.float32) / 255.0
    a[..., 3] = 1.0
    # moldura escura (cara de lanterna) para não virar um bloco chapado
    a[0, :, :3] *= 0.45
    a[-1, :, :3] *= 0.45
    a[:, 0, :3] *= 0.45
    a[:, -1, :3] *= 0.45
    return a


def _texturas(nome: str) -> tuple[np.ndarray, np.ndarray]:
    if nome in COR_PROPRIA:
        s = _cor_solida(COR_PROPRIA[nome])
        return s, s
    topo, lado = _nomes_textura(nome)
    a = np.array(_tingir(_textura(topo), topo), dtype=np.float32) / 255.0
    b = np.array(_tingir(_textura(lado), lado), dtype=np.float32) / 255.0
    return a, b


ESC = 4  # a grade é 4x mais fina que a de blocos: laje, escada, cerca, parede, alçapão e lanterna ganham a forma de verdade


def _cx(x0, x1, y0, y1, z0, z1):
    m = np.zeros((ESC, ESC, ESC), dtype=bool)
    m[x0:x1, y0:y1, z0:z1] = True
    return m


_CHEIO = _cx(0, 4, 0, 4, 0, 4)


def _forma(n: str, props: dict) -> np.ndarray | None:
    """Máscara 4x4x4 (x, y, z) do bloco, ou None se não deve aparecer."""
    topo = props.get("minecraft:vertical_half") == "top" or props.get("top_slot_bit") is True or props.get("upside_down_bit") is True
    if n.endswith("double_slab") or n.endswith("_double_slab"):
        return _CHEIO
    if n.endswith("_slab"):
        return _cx(0, 4, 2, 4, 0, 4) if topo else _cx(0, 4, 0, 2, 0, 4)
    if n.endswith("_stairs"):
        d = int(props.get("weirdo_direction", 0))
        base = _cx(0, 4, 2, 4, 0, 4) if topo else _cx(0, 4, 0, 2, 0, 4)
        alto = (0, 2) if topo else (2, 4)
        degrau = {0: _cx(2, 4, alto[0], alto[1], 0, 4), 1: _cx(0, 2, alto[0], alto[1], 0, 4), 2: _cx(0, 4, alto[0], alto[1], 2, 4), 3: _cx(0, 4, alto[0], alto[1], 0, 2)}[d % 4]
        return base | degrau
    if n.endswith("_fence") or n == "nether_brick_fence":
        return _cx(1, 3, 0, 4, 1, 3)
    if n.endswith("_wall"):
        return _cx(1, 3, 0, 4, 1, 3)
    if n.endswith("_trapdoor"):
        if props.get("open_bit") is True:
            return _cx(0, 4, 0, 4, 0, 1)
        return _cx(0, 4, 3, 4, 0, 4) if topo else _cx(0, 4, 0, 1, 0, 4)
    if n.endswith("_door"):
        return _cx(0, 4, 0, 4, 0, 1)
    if n in ("lantern", "soul_lantern"):
        if props.get("hanging") is True:
            return _cx(1, 3, 0, 3, 1, 3)  # pendurada: o corpo desce a partir do topo do bloco
        return _cx(1, 3, 0, 2, 1, 3)
    if n in ("chain", "iron_chain"):
        return _cx(1, 2, 0, 4, 1, 2)
    if n == "end_rod" or n == "lightning_rod":
        return _cx(1, 2, 0, 4, 1, 2)
    if n == "ladder":
        return _cx(0, 4, 0, 4, 3, 4)
    if "button" in n or "pressure_plate" in n:
        return _cx(1, 3, 0, 1, 1, 3)
    if "carpet" in n or n == "moss_carpet":
        return _cx(0, 4, 0, 1, 0, 4)
    if "candle" in n:
        return _cx(1, 3, 0, 2, 1, 3)
    if any(k in n for k in ("tulip", "allium", "azure", "short_grass", "tall_grass", "hanging_roots", "poppy", "dandelion", "fern", "sapling", "vine", "flower", "petals", "light_block", "torch", "air")):
        return None
    if n == "grass_path" or n == "dirt_path":
        return _cx(0, 4, 0, 3, 0, 4)
    return _CHEIO


class Mundo:
    """Grade de blocos (4x mais fina que a do jogo) pronta para o raycast."""

    def __init__(self, blocos: dict) -> None:
        xs, ys, zs = zip(*blocos)
        self.min = np.array([min(xs) - 1, min(ys) - 1, min(zs) - 1])
        self.max = np.array([max(xs) + 2, max(ys) + 2, max(zs) + 2])
        self.dim_blocos = tuple(int(v) for v in (self.max - self.min))
        self.dim = tuple(d * ESC for d in self.dim_blocos)
        self.grade = np.zeros(self.dim, dtype=np.uint16)
        self.nomes = ["ar"]
        self.topo = [np.zeros((16, 16, 4), np.float32)]
        self.lado = [np.zeros((16, 16, 4), np.float32)]
        self.vidro = [False]
        self.luz = [False]
        indice = {}
        for (x, y, z), b in blocos.items():
            n = _nome(b)
            props = b[1] if isinstance(b, tuple) and len(b) > 1 and isinstance(b[1], dict) else {}
            forma = _forma(n, props)
            if forma is None:
                continue
            if n not in indice:
                indice[n] = len(self.nomes)
                self.nomes.append(n)
                tx, lx = _texturas(n)
                self.topo.append(tx)
                self.lado.append(lx)
                self.vidro.append(n in VAZADOS and "leaves" not in n)
                self.luz.append(n in EMISSIVOS or n in ("lantern", "end_rod"))
            bx, by, bz = (x - self.min[0]) * ESC, (y - self.min[1]) * ESC, (z - self.min[2]) * ESC
            sub = self.grade[bx : bx + ESC, by : by + ESC, bz : bz + ESC]
            sub[forma] = indice[n]
        self._bracos(blocos, indice)
        self.topo = np.stack(self.topo)
        self.lado = np.stack(self.lado)
        self.vidro = np.array(self.vidro)
        self.luz = np.array(self.luz)

    def _bracos(self, blocos: dict, indice: dict) -> None:
        """Cercas e paredes ligam com a vizinha da mesma família e com bloco inteiro: desenha os braços (como o jogo faz sozinho)."""
        familia = lambda n: "fence" if n.endswith("fence") else ("wall" if n.endswith("_wall") else None)  # noqa: E731
        cheios = {p for p, b in blocos.items() if _forma(_nome(b), b[1] if isinstance(b, tuple) and len(b) > 1 and isinstance(b[1], dict) else {}) is _CHEIO}
        for (x, y, z), b in blocos.items():
            n = _nome(b)
            f = familia(n)
            if not f:
                continue
            bx, by, bz = (x - self.min[0]) * ESC, (y - self.min[1]) * ESC, (z - self.min[2]) * ESC
            idx = indice[n]
            props = b[1] if isinstance(b, tuple) and len(b) > 1 and isinstance(b[1], dict) else {}
            for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                lado = {(1, 0): "east", (-1, 0): "west", (0, 1): "south", (0, -1): "north"}[(dx, dz)]
                chave = f"minecraft:connection_{lado}"
                if chave in props:  # o próprio bloco diz com quem liga
                    vizinha = props[chave] is True
                else:
                    v = (x + dx, y, z + dz)
                    vizinha = v in blocos and (familia(_nome(blocos[v])) == f or v in cheios)
                if not vizinha:
                    continue
                if f == "fence":
                    xs = slice(2, 4) if dx > 0 else slice(0, 2) if dx < 0 else slice(1, 3)
                    zs = slice(2, 4) if dz > 0 else slice(0, 2) if dz < 0 else slice(1, 3)
                    for ya, yb in ((1, 2), (3, 4)):
                        self.grade[bx + xs.start : bx + xs.stop, by + ya : by + yb, bz + zs.start : bz + zs.stop] = idx
                else:
                    xs = slice(2, 4) if dx > 0 else slice(0, 2) if dx < 0 else slice(1, 3)
                    zs = slice(2, 4) if dz > 0 else slice(0, 2) if dz < 0 else slice(1, 3)
                    self.grade[bx + xs.start : bx + xs.stop, by : by + 3, bz + zs.start : bz + zs.stop] = idx


def _raios(pos, alvo, fov, w, h):
    pos = np.array(pos, dtype=np.float64)
    f = np.array(alvo, dtype=np.float64) - pos
    f /= np.linalg.norm(f)
    cima = np.array([0.0, 1.0, 0.0])
    d = np.cross(f, cima)
    if np.linalg.norm(d) < 1e-6:
        d = np.array([1.0, 0.0, 0.0])
    d /= np.linalg.norm(d)
    u = np.cross(d, f)
    asp = w / h
    tf = math.tan(math.radians(fov) / 2)
    xs = (np.arange(w) + 0.5) / w * 2 - 1
    ys = 1 - (np.arange(h) + 0.5) / h * 2
    gx, gy = np.meshgrid(xs * tf * asp, ys * tf)
    dirs = f[None, None, :] + gx[..., None] * d[None, None, :] + gy[..., None] * u[None, None, :]
    dirs /= np.linalg.norm(dirs, axis=-1, keepdims=True)
    return pos, dirs.reshape(-1, 3)


def renderizar(mundo: Mundo, pos, alvo, fov: float = 70, w: int = 800, h: int = 500, hora: str = "dia", passos: int = 1500) -> Image.Image:
    pos_, dirs = _raios(pos, alvo, fov, w, h)
    n = len(dirs)
    ceu_a, ceu_b = ((125, 175, 245), (205, 225, 255)) if hora == "dia" else ((8, 8, 24), (36, 30, 60))
    t = np.clip(dirs[:, 1] * 1.4 + 0.5, 0, 1)[:, None]
    cor = np.array(ceu_b)[None] * (1 - t) + np.array(ceu_a)[None] * t
    cor = cor.astype(np.float32) / 255.0
    o = (pos_ - mundo.min) * ESC  # origem no espaço da grade fina (1 unidade = 1/4 de bloco)
    inv = np.where(np.abs(dirs) < 1e-9, 1e9, 1.0 / np.where(np.abs(dirs) < 1e-9, 1e-9, dirs))
    passo = np.sign(dirs).astype(np.int32)
    passo[passo == 0] = 1
    vox = np.floor(np.tile(o, (n, 1))).astype(np.int32)
    t_delta = np.abs(inv)
    prox = np.where(passo > 0, vox + 1 - o, o - vox)
    t_max = prox * t_delta
    ativo = np.ones(n, dtype=bool)
    # a câmera pode estar fora da caixa: avança o raio até entrar na caixa (slab test)
    dim = np.array(mundo.dim)
    t0 = np.zeros(n)
    fora = np.any((o < 0) | (o >= dim))
    if fora:
        a = (0 - o) * inv
        b = (dim - o) * inv
        tmin = np.max(np.minimum(a, b), axis=1)
        tmax = np.min(np.maximum(a, b), axis=1)
        ok = (tmax >= np.maximum(tmin, 0)) & (tmax > 0)
        ativo &= ok
        t0 = np.where(ok, np.maximum(tmin, 0) + 1e-4, 0)
        p = o[None] + dirs * t0[:, None]
        vox = np.floor(p).astype(np.int32)
        vox = np.clip(vox, 0, dim - 1)
        prox = np.where(passo > 0, vox + 1 - p, p - vox)
        t_max = prox * t_delta
    rgb = cor.copy()
    feito = ~ativo
    trans = np.ones(n, dtype=np.float32)  # luz que ainda passa (vidro)
    acum = np.zeros((n, 3), np.float32)
    ultimo = np.zeros(n, np.int32)  # eixo do último passo (0 x, 1 y, 2 z): diz qual face foi atingida
    t_ent = t0.astype(np.float64).copy()  # distância até a entrada no voxel atual
    if fora:
        ultimo = np.argmax(np.minimum(a, b), axis=1).astype(np.int32)
    for _ in range(passos):
        idx = np.nonzero(~feito)[0]
        if idx.size == 0:
            break
        v = vox[idx]
        dentro = np.all((v >= 0) & (v < dim), axis=1)
        feito[idx[~dentro]] = True
        idx = idx[dentro]
        if idx.size == 0:
            break
        v = vox[idx]
        bl = mundo.grade[v[:, 0], v[:, 1], v[:, 2]]
        bate = bl > 0
        if np.any(bate):
            ii = idx[bate]
            bb = bl[bate]
            ult = ultimo[ii]
            p = o[None] + dirs[ii] * t_ent[ii][:, None]
            fr = ((p - vox[ii] + (vox[ii] % ESC)) % ESC) / ESC  # posição dentro do bloco (0..1)
            sgn = passo[ii, ult]
            u = np.where(ult == 0, fr[:, 2], fr[:, 0])
            vv = np.where(ult == 1, fr[:, 2], 1 - fr[:, 1])
            ui = (np.clip(u, 0, 0.999) * 16).astype(int)
            vi_ = (np.clip(vv, 0, 0.999) * 16).astype(int)
            de_cima = (ult == 1) & (sgn < 0)
            tex = np.where(de_cima[:, None], mundo.topo[bb, vi_, ui], mundo.lado[bb, vi_, ui])
            brilho = np.where(ult == 1, np.where(sgn < 0, 1.0, 0.5), np.where(ult == 0, 0.8, 0.65))
            brilho = np.where(mundo.luz[bb], 1.2, brilho)
            neblina = np.clip(1 - (t_ent[ii] / ESC) / 400.0, 0.35, 1.0)
            c = tex[:, :3] * brilho[:, None]
            c = c * neblina[:, None] + np.array([0.7, 0.8, 1.0])[None] * (1 - neblina[:, None]) * (0.6 if hora == "dia" else 0.1)
            vid = mundo.vidro[bb]
            op = ~vid & (tex[:, 3] > 0.4)
            rgb[ii[op]] = c[op] * trans[ii[op]][:, None] + acum[ii[op]]
            feito[ii[op]] = True
            sel = ~op
            vi = ii[sel]
            if vi.size:
                acum[vi] += c[sel] * 0.25 * trans[vi][:, None]
                trans[vi] *= 0.75
        ativos = np.nonzero(~feito)[0]
        if ativos.size == 0:
            break
        eixo = np.argmin(t_max[ativos], axis=1)
        ultimo[ativos] = eixo
        t_ent[ativos] = t_max[ativos, eixo] + t0[ativos]
        vox[ativos, eixo] += passo[ativos, eixo]
        t_max[ativos, eixo] += t_delta[ativos, eixo]
    # raios que passaram só por vidro e nada mais: céu com a névoa do vidro
    sobra = (~np.any(rgb != cor, axis=1)) & (acum.sum(axis=1) > 0)
    rgb[sobra] = cor[sobra] * trans[sobra][:, None] + acum[sobra]
    img = (np.clip(rgb, 0, 1) * 255).astype(np.uint8).reshape(h, w, 3)
    return Image.fromarray(img)


def foto(cena, pos, alvo, destino, fov: float = 70, w: int = 800, h: int = 500, hora: str = "dia") -> Path:
    mundo = Mundo(cena.blocos)
    img = renderizar(mundo, pos, alvo, fov, w, h, hora)
    destino = Path(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)
    img.save(destino)
    return destino


def olhos(cena, pe, direcao, destino, fov: float = 80, w: int = 800, h: int = 500, hora: str = "dia", pitch: float = 0.0) -> Path:
    """De pé em `pe` = (x, y_do_piso, z), olhando para norte/sul/leste/oeste (ou um ângulo em graus: 0 = norte, 90 = leste)."""
    if isinstance(direcao, str):
        dx, dz = DIRECOES[direcao]
    else:
        a = math.radians(direcao)
        dx, dz = math.sin(a), -math.cos(a)
    pos = (pe[0] + 0.5, pe[1] + ALTURA_OLHOS, pe[2] + 0.5)
    alvo = (pos[0] + dx * 10, pos[1] + math.tan(math.radians(pitch)) * 10, pos[2] + dz * 10)
    return foto(cena, pos, alvo, destino, fov, w, h, hora)


def ronda(cena, centro, raio, altura, pasta, n: int = 8, fov: float = 60, w: int = 800, h: int = 500) -> list[Path]:
    """n fotos em volta (de fora, de cima), todas olhando para o centro."""
    mundo = Mundo(cena.blocos)
    pasta = Path(pasta)
    pasta.mkdir(parents=True, exist_ok=True)
    saida = []
    for i in range(n):
        a = 2 * math.pi * i / n
        pos = (centro[0] + math.sin(a) * raio, centro[1] + altura, centro[2] - math.cos(a) * raio)
        arq = pasta / f"ronda_{i}.png"
        renderizar(mundo, pos, centro, fov, w, h).save(arq)
        saida.append(arq)
    return saida
