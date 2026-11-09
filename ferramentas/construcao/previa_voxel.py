# Cópia VENDORIZADA de BotVulpus/addon/tools/previa_voxel.py (código do próprio dono do projeto). Alterações: imports ajustados para funcionar dentro deste repositório.
#!/usr/bin/env python3
"""Prévia isométrica de estruturas de blocos (sem Minecraft, sem Java): serve para CONFERIR forma, escala, paleta e composição
antes de construir no jogo. Usa as texturas vanilla do Bedrock (Mojang/bedrock-samples, baixadas uma vez para tools/.cache_blocos).

Uso como biblioteca:
    from previa_voxel import Cena
    c = Cena()
    c.caixa(0, 0, 0, 9, 4, 9, "stone_bricks")          # sólida
    c.oca(0, 0, 0, 9, 4, 9, "planks_oak")             # só as paredes, piso e teto
    c.ponto(4, 1, 0, "air")                           # tira um bloco (porta)
    c.salvar("previa.png", azimutes=(45, 135, 225, 315))

Coordenadas: x leste, y cima, z sul. Os nomes são os de textures/blocks do pacote de recursos (ou cores da tabela COR).
Limites honestos: não mostra blocos customizados do addon, nem luz e sombra reais, nem estados (portas, escadas) além de bloco inteiro.
"""
from __future__ import annotations

import math
import urllib.request
from pathlib import Path

from PIL import Image

CACHE = Path(__file__).resolve().parent / ".cache_blocos"
URL = "https://cdn.jsdelivr.net/gh/Mojang/bedrock-samples@main/resource_pack/textures/blocks/{}.png"

# (topo, lado) por nome, quando diferem; senão vale o próprio nome nos dois.
PARES: dict[str, tuple[str, str]] = {
    "grass": ("grass_top", "dirt"),
    "log_oak": ("log_oak_top", "log_oak"),
    "log_spruce": ("log_spruce_top", "log_spruce"),
    "log_birch": ("log_birch_top", "log_birch"),
    "crafting_table": ("crafting_table_top", "crafting_table_front"),
    "bookshelf": ("planks_oak", "bookshelf"),
    "tnt": ("tnt_top", "tnt_side"),
}

# nome do bloco Bedrock -> (textura do topo, textura do lado) no pacote de recursos; variantes enceradas valem como as normais
ALIAS: dict[str, tuple[str, str]] = {
    "deepslate_tiles": ("deepslate_tiles", "deepslate_tiles"), "polished_deepslate": ("polished_deepslate", "polished_deepslate"), "deepslate_bricks": ("deepslate_bricks", "deepslate_bricks"),
    "cracked_deepslate_bricks": ("cracked_deepslate_bricks", "cracked_deepslate_bricks"), "chiseled_polished_blackstone": ("chiseled_polished_blackstone", "chiseled_polished_blackstone"),
    "smooth_basalt": ("smooth_basalt", "smooth_basalt"), "mossy_cobblestone": ("cobblestone_mossy", "cobblestone_mossy"), "dark_oak_planks": ("planks_big_oak", "planks_big_oak"),
    "dark_oak_log": ("log_big_oak_top", "log_big_oak"), "green_concrete": ("concrete_green", "concrete_green"), "red_concrete": ("concrete_red", "concrete_red"),
    "blue_concrete": ("concrete_blue", "concrete_blue"), "brown_terracotta": ("hardened_clay_stained_brown", "hardened_clay_stained_brown"), "yellow_terracotta": ("hardened_clay_stained_yellow", "hardened_clay_stained_yellow"),
    "smooth_sandstone": ("sandstone_top", "sandstone_top"), "sandstone": ("sandstone_top", "sandstone_normal"), "snow_block": ("snow", "snow"),
    "yellow_concrete_powder": ("concrete_powder_yellow", "concrete_powder_yellow"), "yellow_stained_glass": ("glass_yellow", "glass_yellow"), "red_stained_glass": ("glass_red", "glass_red"),
    "dark_oak_leaves": ("leaves_big_oak", "leaves_big_oak"), "dark_oak_fence": ("planks_big_oak", "planks_big_oak"),
    "grass_block": ("grass_top", "grass_side_carried"), "dirt": ("dirt", "dirt"), "coarse_dirt": ("coarse_dirt", "coarse_dirt"),
    "podzol": ("dirt_podzol_top", "dirt_podzol_side"), "rooted_dirt": ("dirt_with_roots", "dirt_with_roots"), "moss_block": ("moss_block", "moss_block"),
    "stone": ("stone", "stone"), "andesite": ("stone_andesite", "stone_andesite"), "diorite": ("stone_diorite", "stone_diorite"), "granite": ("stone_granite", "stone_granite"),
    "polished_diorite": ("stone_diorite_smooth", "stone_diorite_smooth"), "polished_andesite": ("stone_andesite_smooth", "stone_andesite_smooth"),
    "cobblestone": ("cobblestone", "cobblestone"), "stone_bricks": ("stonebrick", "stonebrick"), "mossy_stone_bricks": ("stonebrick_mossy", "stonebrick_mossy"),
    "cracked_stone_bricks": ("stonebrick_cracked", "stonebrick_cracked"), "tuff": ("tuff", "tuff"), "calcite": ("calcite", "calcite"), "dripstone_block": ("dripstone_block", "dripstone_block"),
    "quartz_block": ("quartz_block_top", "quartz_block_side"), "smooth_quartz": ("quartz_block_bottom", "quartz_block_bottom"), "quartz_pillar": ("quartz_pillar_top", "quartz_pillar"),
    "chiseled_quartz_block": ("quartz_block_chiseled_top", "quartz_block_chiseled"), "copper_block": ("copper_block", "copper_block"), "weathered_copper": ("weathered_copper", "weathered_copper"),
    "exposed_copper": ("exposed_copper", "exposed_copper"), "oxidized_copper": ("oxidized_copper", "oxidized_copper"), "gold_block": ("gold_block", "gold_block"),
    "sea_lantern": ("sea_lantern", "sea_lantern"), "oak_fence": ("planks_oak", "planks_oak"), "oak_planks": ("planks_oak", "planks_oak"), "spruce_planks": ("planks_spruce", "planks_spruce"),
    "cherry_log": ("cherry_log_top", "cherry_log_side"), "cherry_leaves": ("cherry_leaves", "cherry_leaves"), "cherry_planks": ("cherry_planks", "cherry_planks"),
    "deepslate": ("deepslate", "deepslate"), "blackstone": ("blackstone", "blackstone"), "polished_blackstone": ("polished_blackstone", "polished_blackstone"),
    "obsidian": ("obsidian", "obsidian"), "glowstone": ("glowstone", "glowstone"), "amethyst_block": ("amethyst_block", "amethyst_block"),
    "white_concrete": ("concrete_white", "concrete_white"), "pink_concrete": ("concrete_pink", "concrete_pink"), "magenta_concrete": ("concrete_magenta", "concrete_magenta"),
    "light_blue_concrete": ("concrete_light_blue", "concrete_light_blue"), "orange_concrete": ("concrete_orange", "concrete_orange"), "purple_concrete": ("concrete_purple", "concrete_purple"),
    "black_concrete": ("concrete_black", "concrete_black"), "yellow_concrete": ("concrete_yellow", "concrete_yellow"), "cyan_concrete": ("concrete_cyan", "concrete_cyan"),
    "pink_terracotta": ("hardened_clay_stained_pink", "hardened_clay_stained_pink"), "white_terracotta": ("hardened_clay_stained_white", "hardened_clay_stained_white"),
    "pink_wool": ("wool_colored_pink", "wool_colored_pink"), "white_wool": ("wool_colored_white", "wool_colored_white"), "purple_wool": ("wool_colored_purple", "wool_colored_purple"),
    "light_blue_wool": ("wool_colored_light_blue", "wool_colored_light_blue"), "yellow_wool": ("wool_colored_yellow", "wool_colored_yellow"),
    "pink_stained_glass": ("glass_pink", "glass_pink"), "light_blue_stained_glass": ("glass_light_blue", "glass_light_blue"), "white_stained_glass": ("glass_white", "glass_white"),
    "purple_stained_glass": ("glass_purple", "glass_purple"), "magenta_stained_glass": ("glass_magenta", "glass_magenta"), "orange_stained_glass": ("glass_orange", "glass_orange"),
    "smooth_stone": ("stone_slab_top", "stone_slab_top"), "bookshelf": ("planks_oak", "bookshelf"), "glass": ("glass", "glass"), "ice": ("ice", "ice"), "packed_ice": ("ice_packed", "ice_packed"),
    "sand": ("sand", "sand"), "sandstone": ("sandstone_top", "sandstone_normal"), "red_sandstone": ("red_sandstone_top", "red_sandstone_normal"), "bone_block": ("bone_block_top", "bone_block_side"),
    "end_stone": ("end_stone", "end_stone"), "lantern": ("lantern", "lantern"), "lightning_rod": ("lightning_rod", "lightning_rod"), "gravel": ("gravel", "gravel"),
}
# coisas que não são cubos (plantas, hastes, placas): somem na prévia leve
NAO_CUBO = ("light_block", "end_rod", "tulip", "allium", "azure", "short_grass", "tall_grass", "hanging_roots", "poppy", "dandelion", "fern", "candle", "carpet", "pane", "_fence", "lightning_rod", "sapling", "vine", "flower", "petals", "torch")
COR_BLOCO = {"vulpus:maquina_skybound_baixo": (255, 150, 190), "vulpus:maquina_skybound_topo": (255, 190, 215), "vulpus:maquina_backrooms_baixo": (200, 180, 80), "vulpus:maquina_backrooms_topo": (225, 210, 110), "vulpus:maquina_hunter_baixo": (40, 80, 50), "vulpus:maquina_hunter_topo": (70, 40, 40), "lantern": (255, 200, 90), "light_blue_stained_glass": (150, 200, 255), "pink_stained_glass": (255, 170, 210), "glass": (210, 230, 240)}
# cor de reserva quando a textura não existe (r, g, b)
COR: dict[str, tuple[int, int, int]] = {
    "grass": (96, 160, 64), "leaves": (60, 120, 50), "water": (60, 100, 220), "air": (0, 0, 0),
    "wool_pink": (240, 150, 190), "wool_yellow": (240, 210, 70), "wool_white": (235, 235, 235), "wool_purple": (130, 60, 170),
    "carpet_yellow": (240, 210, 70), "concrete_white": (235, 238, 240), "concrete_yellow": (240, 200, 40), "concrete_pink": (235, 140, 180),
}
# não bloqueiam a vista (transparentes ou luminosos que não ocultam o que está atrás)
VAZADOS = {"air", "yellow_stained_glass", "red_stained_glass", "glass", "glass_pane", "leaves", "water", "ice", "barrier", "pink_stained_glass", "light_blue_stained_glass", "white_stained_glass", "purple_stained_glass", "magenta_stained_glass", "orange_stained_glass", "short_grass", "hanging_roots"}
EMISSIVOS = {"lantern", "sea_lantern", "glowstone", "lantern", "shroomlight", "froglight", "redstone_lamp_on", "lit_redstone_lamp", "beacon"}


def _textura(nome: str) -> Image.Image:
    """Textura 16x16 RGBA do nome; sem textura, cor sólida da tabela (ou cinza)."""
    CACHE.mkdir(exist_ok=True)
    arq = CACHE / f"{nome.replace(':', '_')}.png"
    if not arq.exists() and ":" in nome:
        arq.write_bytes(b"")  # bloco do addon: não existe no pacote vanilla, usa a cor da tabela
    if not arq.exists():
        try:
            req = urllib.request.Request(URL.format(nome), headers={"User-Agent": "VulpusPrevia/1.0"})
            arq.write_bytes(urllib.request.urlopen(req, timeout=20).read())
        except Exception:
            arq.write_bytes(b"")
    if arq.stat().st_size:
        img = Image.open(arq).convert("RGBA")
        return img.crop((0, 0, min(img.width, img.height), min(img.width, img.height))).resize((16, 16), Image.NEAREST)
    return Image.new("RGBA", (16, 16), COR_BLOCO.get(nome, COR.get(nome, (150, 150, 160))) + (255,))


def _tingir(img: Image.Image, nome: str) -> Image.Image:
    """Grama e folhas vêm em cinza no pacote: pinta de verde."""
    if nome in ("grass_top", "leaves_oak", "leaves_spruce", "leaves_birch", "leaves", "grass_side_carried"):
        cor = (110, 170, 70) if nome == "grass_top" else (70, 130, 50)
        px = img.load()
        for y in range(img.height):
            for x in range(img.width):
                r, g, b, a = px[x, y]
                px[x, y] = (r * cor[0] // 255, g * cor[1] // 255, b * cor[2] // 255, a)
    return img


class Cena:
    """Um conjunto de blocos nomeados, com ajudas para montar (caixa, oca, linha)."""

    def __init__(self) -> None:
        self.blocos: dict[tuple[int, int, int], str] = {}

    def ponto(self, x: int, y: int, z: int, nome: str) -> None:
        if nome == "air":
            self.blocos.pop((x, y, z), None)
        else:
            self.blocos[(x, y, z)] = nome

    def caixa(self, x1: int, y1: int, z1: int, x2: int, y2: int, z2: int, nome: str) -> None:
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                for z in range(min(z1, z2), max(z1, z2) + 1):
                    self.ponto(x, y, z, nome)

    def oca(self, x1: int, y1: int, z1: int, x2: int, y2: int, z2: int, nome: str, teto: bool = True, piso: bool = True) -> None:
        xa, xb, ya, yb, za, zb = min(x1, x2), max(x1, x2), min(y1, y2), max(y1, y2), min(z1, z2), max(z1, z2)
        for x in range(xa, xb + 1):
            for y in range(ya, yb + 1):
                for z in range(za, zb + 1):
                    borda = x in (xa, xb) or z in (za, zb) or (piso and y == ya) or (teto and y == yb)
                    if borda:
                        self.ponto(x, y, z, nome)

    def linha(self, a: tuple[int, int, int], b: tuple[int, int, int], nome: str) -> None:
        n = max(abs(b[i] - a[i]) for i in range(3)) or 1
        for i in range(n + 1):
            self.ponto(*(round(a[k] + (b[k] - a[k]) * i / n) for k in range(3)), nome)

    # ------------------------------------------------------------------ desenho
    def desenhar(self, azimute: int = 45, s: int = 16, margem: int = 24) -> Image.Image:
        """Isométrica 2:1 vista de um dos quatro cantos (azimute 45, 135, 225 ou 315)."""
        if not self.blocos:
            return Image.new("RGBA", (64, 64), (24, 22, 32, 255))
        giro = (azimute // 90) % 4
        xs = [p[0] for p in self.blocos]
        zs = [p[2] for p in self.blocos]
        x0, z0, x1, z1 = min(xs), min(zs), max(xs), max(zs)

        def rot(x: int, z: int) -> tuple[int, int]:
            rx, rz = x - x0, z - z0
            w, d = x1 - x0, z1 - z0
            for _ in range(giro):
                rx, rz = rz, w - rx
                w, d = d, w
            return rx, rz

        giradas = {(*rot(x, z), y): n for (x, y, z), n in self.blocos.items() for _ in [0]}
        # ordem de pintura: do mais longe (menor rx + rz + y) para o mais perto
        itens = sorted(giradas.items(), key=lambda kv: (kv[0][0] + kv[0][1] + kv[0][2], kv[0][2], kv[0][0]))
        # caixa da imagem: projeta os cantos de todos os blocos e desloca para caber com margem
        mx, my, Mx, My = 1e9, 1e9, -1e9, -1e9
        for (rx, rz, y) in giradas:
            for dx in (0, 1):
                for dz in (0, 1):
                    for dy in (0, 1):
                        px_, py_ = (rx + dx - rz - dz) * s, (rx + dx + rz + dz) * s / 2 - (y + dy) * s
                        mx, my, Mx, My = min(mx, px_), min(my, py_), max(Mx, px_), max(My, py_)
        larg, alto = int(Mx - mx) + margem * 2 + 1, int(My - my) + margem * 2 + 1
        img = Image.new("RGBA", (larg, alto), (24, 22, 32, 255))
        origem_x, base_y = margem - mx, margem - my

        def tela(rx: float, rz: float, y: float) -> tuple[float, float]:
            return origem_x + (rx - rz) * s, base_y + (rx + rz) * s / 2 - y * s

        def vazado(rx: int, rz: int, y: int) -> bool:
            n = giradas.get((rx, rz, y))
            return n is None or n in VAZADOS or (n.replace("waxed_", "") not in ALIAS and any(k in n for k in NAO_CUBO))

        cache: dict[tuple[str, str], Image.Image] = {}
        for (rx, rz, y), nome in itens:
            if nome in VAZADOS and nome != "glass":
                continue
            base_n = nome.replace("waxed_", "")
            if any(k in base_n for k in NAO_CUBO) and base_n not in ALIAS:
                continue
            topo_n, lado_n = ALIAS.get(base_n) or ALIAS.get(base_n.replace("_slab", "").replace("_stairs", "")) or PARES.get(nome, (nome, nome))
            for face in ("topo", "esq", "dir"):
                viz = {"topo": (rx, rz, y + 1), "esq": (rx, rz + 1, y), "dir": (rx + 1, rz, y)}[face]
                if not vazado(*viz):
                    continue
                if nome == "glass" and giradas.get(viz) == "glass":
                    continue
                chave = (topo_n if face == "topo" else lado_n, face)
                if chave not in cache:
                    t = _tingir(_textura(chave[0]), chave[0])
                    if nome in EMISSIVOS:
                        brilho = 1.0
                    else:
                        brilho = {"topo": 1.0, "esq": 0.78, "dir": 0.58}[face]
                    px = t.load()
                    for yy in range(16):
                        for xx in range(16):
                            r, g, b, a = px[xx, yy]
                            px[xx, yy] = (min(255, int(r * brilho)), min(255, int(g * brilho)), min(255, int(b * brilho)), a)
                    cache[chave] = t
                tex = cache[chave]
                if face == "topo":
                    o = tela(rx, rz, y + 1)
                    a_ = (s, s / 2)
                    b_ = (-s, s / 2)
                elif face == "esq":
                    o = tela(rx, rz + 1, y + 1)
                    a_ = (s, s / 2)
                    b_ = (0, s)
                else:
                    o = tela(rx + 1, rz, y + 1)
                    a_ = (-s, s / 2)
                    b_ = (0, s)
                _face(img, tex, o, a_, b_)
        return img

    def salvar(self, caminho: str | Path, azimutes: tuple[int, ...] = (45, 135, 225, 315), s: int = 12) -> Path:
        """Salva as vistas lado a lado (2 por linha) em um PNG."""
        vistas = [self.desenhar(a, s) for a in azimutes]
        colunas = 2 if len(vistas) > 1 else 1
        linhas = (len(vistas) + colunas - 1) // colunas
        lw = max(v.width for v in vistas)
        lh = max(v.height for v in vistas)
        folha = Image.new("RGBA", (lw * colunas, lh * linhas), (24, 22, 32, 255))
        for i, v in enumerate(vistas):
            folha.alpha_composite(v, ((i % colunas) * lw, (i // colunas) * lh))
        caminho = Path(caminho)
        caminho.parent.mkdir(parents=True, exist_ok=True)
        folha.convert("RGB").save(caminho)
        return caminho


def _face(img: Image.Image, tex: Image.Image, o: tuple[float, float], a: tuple[float, float], b: tuple[float, float]) -> None:
    """Cola a textura (16x16) num paralelogramo: ponto o, vetores a (textura x) e b (textura y)."""
    xs = [o[0], o[0] + a[0], o[0] + b[0], o[0] + a[0] + b[0]]
    ys = [o[1], o[1] + a[1], o[1] + b[1], o[1] + a[1] + b[1]]
    ex, ey = math.floor(min(xs)), math.floor(min(ys))
    w, h = math.ceil(max(xs)) - ex + 1, math.ceil(max(ys)) - ey + 1
    det = a[0] * b[1] - a[1] * b[0]
    if abs(det) < 1e-6:
        return
    # inverso: (X, Y) da tela -> (u, v) em 0..1 -> pixel da textura
    inv = ((b[1] / det, -b[0] / det), (-a[1] / det, a[0] / det))
    coef = (
        inv[0][0] * 16, inv[0][1] * 16, (-(o[0] - ex) * inv[0][0] - (o[1] - ey) * inv[0][1]) * 16,
        inv[1][0] * 16, inv[1][1] * 16, (-(o[0] - ex) * inv[1][0] - (o[1] - ey) * inv[1][1]) * 16,
    )
    saida = tex.transform((w, h), Image.AFFINE, coef, Image.NEAREST)
    # fora do paralelogramo a amostra cai fora da textura e vem transparente
    img.alpha_composite(saida, (ex, ey)) if ex >= 0 and ey >= 0 else None


if __name__ == "__main__":
    c = Cena()
    c.caixa(0, 0, 0, 12, 0, 12, "stone")
    c.oca(2, 1, 2, 10, 5, 10, "planks_oak", piso=False)
    c.ponto(6, 1, 2, "air")
    c.ponto(6, 2, 2, "air")
    c.caixa(4, 3, 10, 8, 4, 10, "glass")
    c.linha((2, 1, 2), (2, 6, 2), "log_oak")
    c.linha((10, 1, 2), (10, 6, 2), "log_oak")
    c.ponto(6, 1, 6, "sea_lantern")
    print(c.salvar(Path(__file__).resolve().parent / ".cache_blocos" / "teste_previa.png", azimutes=(45, 135)))
