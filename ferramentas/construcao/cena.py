# Cópia VENDORIZADA de BotVulpus/addon/tools/construcao/cena.py (código do próprio dono do projeto). Alterações: imports ajustados para funcionar dentro deste repositório.
"""Biblioteca de construção da VULPUS: monta estruturas de blocos por código, valida, gera `.mcstructure` e renderiza uma imagem real.

Fluxo (ver a skill `construcao-minecraft`):
    from construcao.cena import Cena, Paleta, laje, escada
    c = Cena("coreto")
    c.caixa(0, 0, 0, 8, 0, 8, "minecraft:stone_bricks")
    c.cupula(4, 4, 4, 5, "minecraft:copper_block")
    c.construir(saida)        # -> .mcstructure + .png (render do Minecraft Creator Tools) + relatório de validação

Coordenadas: x leste, y cima, z sul (como no jogo). Nomes de bloco no formato achatado do Bedrock moderno ("minecraft:oak_planks",
"minecraft:pink_stained_glass"). Estados entram como dicionário: ("minecraft:oak_stairs", {"weirdo_direction": 0, "upside_down_bit": False}).
"""
from __future__ import annotations

import json
import math
import os
import random
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Sequence, Union

Bloco = Union[str, tuple]  # "minecraft:stone" ou ("minecraft:oak_stairs", {"weirdo_direction": 0})
AR = "minecraft:air"
LIMITE_RENDER_MCT = 4500  # acima disso o render do Creator Tools estoura o tempo de montagem da cena

# direções dos blocos com orientação no Bedrock (weirdo_direction das escadas: 0 leste, 1 oeste, 2 sul, 3 norte)
LESTE, OESTE, SUL, NORTE = 0, 1, 2, 3


def escada(nome: str, direcao: int = 0, invertida: bool = False) -> tuple:
    return (nome, {"weirdo_direction": direcao, "upside_down_bit": invertida})


def laje(nome: str, em_cima: bool = False) -> tuple:
    return (nome, {"minecraft:vertical_half": "top" if em_cima else "bottom"})


def _norm(b: Bloco) -> tuple[str, tuple]:
    if isinstance(b, str):
        return b, ()
    nome, props = b
    return nome, tuple(sorted(props.items()))


@dataclass
class Paleta:
    """Mistura ponderada de blocos: o antídoto contra paredes de um bloco só (veja 'misturar texturas' na skill)."""

    itens: list[tuple[Bloco, float]]
    semente: int = 1

    def __post_init__(self) -> None:
        self._rnd = random.Random(self.semente)

    def sortear(self) -> Bloco:
        total = sum(p for _, p in self.itens)
        r = self._rnd.random() * total
        for b, p in self.itens:
            r -= p
            if r <= 0:
                return b
        return self.itens[-1][0]


def _resolver(b: Union[Bloco, Paleta]) -> Bloco:
    return b.sortear() if isinstance(b, Paleta) else b


class Cena:
    def __init__(self, nome: str = "estrutura", semente: int = 7) -> None:
        self.nome = nome
        self.blocos: dict[tuple[int, int, int], Bloco] = {}
        self.rnd = random.Random(semente)

    # ------------------------------------------------------------------ básicos
    def ponto(self, x: int, y: int, z: int, b: Union[Bloco, Paleta]) -> None:
        b = _resolver(b)
        if _norm(b)[0] == AR:
            self.blocos.pop((x, y, z), None)
        else:
            self.blocos[(x, y, z)] = b

    def pegar(self, x: int, y: int, z: int) -> Bloco | None:
        return self.blocos.get((x, y, z))

    def caixa(self, x1: int, y1: int, z1: int, x2: int, y2: int, z2: int, b: Union[Bloco, Paleta]) -> None:
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                for z in range(min(z1, z2), max(z1, z2) + 1):
                    self.ponto(x, y, z, b)

    def oca(self, x1: int, y1: int, z1: int, x2: int, y2: int, z2: int, b: Union[Bloco, Paleta], piso: bool = True, teto: bool = True) -> None:
        xa, xb, ya, yb, za, zb = min(x1, x2), max(x1, x2), min(y1, y2), max(y1, y2), min(z1, z2), max(z1, z2)
        for x in range(xa, xb + 1):
            for y in range(ya, yb + 1):
                for z in range(za, zb + 1):
                    if x in (xa, xb) or z in (za, zb) or (piso and y == ya) or (teto and y == yb):
                        self.ponto(x, y, z, b)

    def linha(self, a: tuple[int, int, int], b: tuple[int, int, int], bloco: Union[Bloco, Paleta]) -> None:
        n = max(abs(b[i] - a[i]) for i in range(3)) or 1
        for i in range(n + 1):
            self.ponto(*(round(a[k] + (b[k] - a[k]) * i / n) for k in range(3)), bloco)

    def limpar(self, x1: int, y1: int, z1: int, x2: int, y2: int, z2: int) -> None:
        self.caixa(x1, y1, z1, x2, y2, z2, AR)

    def copiar(self, outra: "Cena", dx: int = 0, dy: int = 0, dz: int = 0) -> None:
        """Carimba os blocos de outra cena deslocados (módulos: construa uma vez, carimbe várias)."""
        for (x, y, z), b in outra.blocos.items():
            self.ponto(x + dx, y + dy, z + dz, b)

    def espelhar_x(self, centro_x: float) -> None:
        """Espelha tudo em torno de um eixo x (simetria que NÃO parece copiada só vale em arquitetura formal)."""
        novos = {(int(2 * centro_x - x), y, z): b for (x, y, z), b in self.blocos.items()}
        self.blocos.update(novos)

    # ------------------------------------------------------------------ formas
    def cilindro(self, cx: int, cy: int, cz: int, raio: float, altura: int, b: Union[Bloco, Paleta], oco: bool = False) -> None:
        for y in range(cy, cy + altura):
            for x in range(int(cx - raio) - 1, int(cx + raio) + 2):
                for z in range(int(cz - raio) - 1, int(cz + raio) + 2):
                    d = math.hypot(x - cx, z - cz)
                    if d <= raio + 0.35 and (not oco or d > raio - 0.65):
                        self.ponto(x, y, z, b)

    def esfera(self, cx: int, cy: int, cz: int, raio: float, b: Union[Bloco, Paleta], oca: bool = False, meia: bool = False) -> None:
        r = int(math.ceil(raio))
        for x in range(cx - r - 1, cx + r + 2):
            for y in range(cy - (0 if meia else r) - 1, cy + r + 2):
                for z in range(cz - r - 1, cz + r + 2):
                    d = math.sqrt((x - cx) ** 2 + (y - cy) ** 2 + (z - cz) ** 2)
                    if d <= raio + 0.3 and (not oca or d > raio - 1.0):
                        self.ponto(x, y, z, b)

    def cupula(self, cx: int, cy: int, cz: int, raio: float, b: Union[Bloco, Paleta], espessura: float = 1.0, altura_rel: float = 1.0) -> None:
        """Meia esfera oca (a base fica em cy). altura_rel < 1 achata (cúpula de coreto), > 1 alonga (cebola)."""
        r = int(math.ceil(raio))
        ry = raio * altura_rel
        for x in range(cx - r - 1, cx + r + 2):
            for y in range(cy, cy + int(math.ceil(ry)) + 2):
                for z in range(cz - r - 1, cz + r + 2):
                    d = math.sqrt((x - cx) ** 2 + ((y - cy) / altura_rel) ** 2 + (z - cz) ** 2)
                    if raio - espessura < d <= raio + 0.3:
                        self.ponto(x, y, z, b)

    def pendentes(self, quantidade: int, comp_min: int, comp_max: int, b: Union[Bloco, Paleta], semente: int = 9) -> None:
        """Estalactites cônicas penduradas no fundo do que já foi construído: base de 3x3 que afina em ponta de 1 bloco."""
        rnd = random.Random(semente)
        fundos: dict[tuple[int, int], int] = {}
        for (x, y, z) in self.blocos:
            if (x, z) not in fundos or y < fundos[(x, z)]:
                fundos[(x, z)] = y
        colunas = [k for k in fundos.items() if all((k[0][0] + dx, k[0][1] + dz) in fundos for dx in (-1, 0, 1) for dz in (-1, 0, 1))]
        rnd.shuffle(colunas)
        for (x, z), y in colunas[:quantidade]:
            comp = rnd.randint(comp_min, comp_max)
            for i in range(1, comp + 1):
                larg = 1 if i > comp * 0.45 else 2  # 1 = só o centro; 2 = cruz
                self.ponto(x, y - i, z, b)
                if larg == 2:
                    for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        if rnd.random() < 0.7 and (x + dx, y - i, z + dz) not in self.blocos:
                            self.ponto(x + dx, y - i, z + dz, b)

    def piramide(self, cx: int, cy: int, cz: int, meio_lado: int, b: Union[Bloco, Paleta], oca: bool = False) -> None:
        for i in range(meio_lado + 1):
            l = meio_lado - i
            y = cy + i
            if oca and l > 0:
                self.oca(cx - l, y, cz - l, cx + l, y, cz + l, b, piso=False, teto=False)
            else:
                self.caixa(cx - l, y, cz - l, cx + l, y, cz + l, b)

    def telhado_duas_aguas(self, x1: int, z1: int, x2: int, z2: int, y: int, escada_nome: str, cheio: Bloco, eixo: str = "x", beiral: int = 1) -> None:
        """Telhado de escadas ('x': a cumeeira corre ao longo de x). Sobe 1 bloco a cada 1 de largura; fecha as empenas."""
        xa, xb, za, zb = min(x1, x2) - (beiral if eixo == "z" else 0), max(x1, x2) + (beiral if eixo == "z" else 0), min(z1, z2) - (beiral if eixo == "x" else 0), max(z1, z2) + (beiral if eixo == "x" else 0)
        if eixo == "x":
            largura = zb - za + 1
            for i in range(largura // 2 + 1):
                for x in range(xa, xb + 1):
                    if za + i <= zb - i:
                        self.ponto(x, y + i, za + i, escada(escada_nome, SUL))   # lado norte sobe para o sul
                        if zb - i != za + i:
                            self.ponto(x, y + i, zb - i, escada(escada_nome, NORTE))
                        else:
                            self.ponto(x, y + i, za + i, cheio)
        else:
            largura = xb - xa + 1
            for i in range(largura // 2 + 1):
                for z in range(za, zb + 1):
                    if xa + i <= xb - i:
                        self.ponto(xa + i, y + i, z, escada(escada_nome, LESTE))
                        if xb - i != xa + i:
                            self.ponto(xb - i, y + i, z, escada(escada_nome, OESTE))
                        else:
                            self.ponto(xa + i, y + i, z, cheio)

    def arco_redondo(self, cx: int, y_base: int, z: int, meia_largura: int, b: Union[Bloco, Paleta], eixo: str = "x", espessura: int = 1) -> None:
        """Arco de meio círculo (vão livre) no plano x-y (eixo 'x') ou z-y ('z'): os blocos do arco, sem preencher o vão."""
        for ang in range(0, 181, 3):
            a = math.radians(ang)
            dx, dy = round(math.cos(a) * meia_largura), round(math.sin(a) * meia_largura)
            for e in range(espessura):
                if eixo == "x":
                    self.ponto(cx + dx, y_base + dy, z + e, b)
                else:
                    self.ponto(z + e, y_base + dy, cx + dx, b)

    def escada_reta(self, x: int, y: int, z: int, passos: int, dx: int, dz: int, st: str, enchimento: Bloco | None = None) -> None:
        """Escada reta subindo de (x, y, z) na direção (dx, dz): um degrau por bloco, com o enchimento por baixo (se dado)."""
        d = {(1, 0): LESTE, (-1, 0): OESTE, (0, 1): SUL, (0, -1): NORTE}[(dx, dz)]
        for i in range(passos):
            self.ponto(x + dx * i, y + i, z + dz * i, escada(st, d))
            if enchimento is not None:
                for yy in range(y, y + i):
                    self.ponto(x + dx * i, yy, z + dz * i, enchimento)

    def helice(self, cx: int, cy: int, cz: int, raio: int, altura: int, degrau: Bloco, miolo: Bloco | None = None) -> None:
        """Escada em espiral: um degrau a cada bloco de altura, girando 45 graus."""
        if miolo is not None:
            self.caixa(cx, cy, cz, cx, cy + altura, cz, miolo)
        for i in range(altura):
            a = math.radians(i * 45)
            self.ponto(cx + round(math.cos(a) * raio), cy + i, cz + round(math.sin(a) * raio), degrau)
            a2 = math.radians(i * 45 + 22)
            self.ponto(cx + round(math.cos(a2) * (raio - 1)), cy + i, cz + round(math.sin(a2) * (raio - 1)), degrau)

    # ------------------------------------------------------------------ orgânico
    def ilha_flutuante(self, cx: int, cy: int, cz: int, raio: float, profundidade: int, topo: Union[Bloco, Paleta], solo: Union[Bloco, Paleta], rocha: Union[Bloco, Paleta], ruido: float = 0.35, semente: int = 3, espessura_solo: int = 3) -> None:
        """Ilha em gota: topo quase plano e irregular, uma capa de solo e, por baixo, rocha que afunila em ponta (nada de bloco retangular).

        topo = camada de cima (grama), solo = as `espessura_solo` camadas seguintes (terra), rocha = o resto (pedra misturada)."""
        rnd = random.Random(semente)
        fase = [rnd.random() * 6.28 for _ in range(4)]

        def raio_em(ang: float) -> float:
            return raio * (1 + ruido * (math.sin(ang * 2 + fase[0]) * 0.5 + math.sin(ang * 3 + fase[1]) * 0.3 + math.sin(ang * 5 + fase[2]) * 0.2))

        r = int(raio * (1 + ruido)) + 2
        for x in range(cx - r, cx + r + 1):
            for z in range(cz - r, cz + r + 1):
                d = math.hypot(x - cx, z - cz)
                R = raio_em(math.atan2(z - cz, x - cx))
                if d > R:
                    continue
                f = d / R  # 0 no centro, 1 na borda
                fundo = int(profundidade * (1 - f ** 1.35) * (0.7 + 0.3 * math.sin(x * 0.7 + z * 0.5 + fase[3])))
                topo_y = cy + (1 if f < 0.35 and rnd.random() < 0.18 else 0)
                for y in range(topo_y - fundo, topo_y + 1):
                    if y == topo_y:
                        self.ponto(x, y, z, topo)
                    elif y > topo_y - 1 - espessura_solo + (1 if f > 0.8 else 0):
                        self.ponto(x, y, z, solo)
                    else:
                        self.ponto(x, y, z, rocha)

    def chao(self, x: int, z: int, y_max: int | None = None) -> int | None:
        """Y do bloco sólido mais alto da coluna (x, z), ignorando plantas e luz invisível; None se não há chão."""
        melhor = None
        for (bx, by, bz), b in self.blocos.items():
            if bx == x and bz == z and (y_max is None or by <= y_max):
                n = _norm(b)[0]
                if any(k in n for k in ("light_block", "tulip", "allium", "azure", "short_grass", "petals", "flower", "poppy", "dandelion", "hanging_roots")):
                    continue
                if melhor is None or by > melhor:
                    melhor = by
        return melhor

    def arvore(self, x: int, y: int | None, z: int, altura: int, tronco: Bloco, folha: Union[Bloco, Paleta], copa: float = 2.6) -> bool:
        """Árvore que NASCE NO CHÃO: se y é None (ou não há bloco sólido embaixo) procura o chão da coluna; sem chão, não planta e devolve False."""
        base = self.chao(x, z)
        if base is None:
            return False
        y = base + 1
        for i in range(altura):
            self.ponto(x, y + i, z, tronco)
        for dx in range(-int(copa) - 1, int(copa) + 2):
            for dy in range(-1, int(copa) + 1):
                for dz in range(-int(copa) - 1, int(copa) + 2):
                    d = math.sqrt(dx * dx + (dy * 1.2) ** 2 + dz * dz)
                    if d <= copa + self.rnd.random() * 0.6 and (dx or dz or dy > 0):
                        if self.pegar(x + dx, y + altura - 1 + dy, z + dz) is None:
                            self.ponto(x + dx, y + altura - 1 + dy, z + dz, folha)
        return True

    def poste(self, x: int, z: int, altura: int = 4, direcao: tuple[int, int] = (1, 0), braco: int = 2, base: Bloco = "minecraft:stone_brick_wall", haste: str = "minecraft:spruce_fence", ponta: Bloco = "minecraft:spruce_planks") -> bool:
        """Poste de lampada "pescoço de ganso" (como o dono desenhou): pé de pedra, haste de cerca e, no topo, um braço de tábuas que sai para o lado
        com a lanterna PENDURADA na ponta. Sempre sobre o chão da coluna; sem chão, não constrói (nada de poste flutuando)."""
        g = self.chao(x, z)
        if g is None:
            return False
        dx, dz = direcao
        lado = {(1, 0): "east", (-1, 0): "west", (0, 1): "south", (0, -1): "north"}[(dx, dz)]
        madeira = haste.split(":")[-1].replace("_fence", "")
        y = g + 1
        self.ponto(x, y, z, base)
        for i in range(1, altura - 1):
            self.ponto(x, y + i, z, (haste, {"wood_type": madeira}))
        topo = y + altura - 1
        liga = {f"minecraft:connection_{k}": k == lado for k in ("east", "west", "north", "south")}
        self.ponto(x, topo, z, (haste, {**liga, "wood_type": madeira}))
        for i in range(1, braco + 1):
            self.ponto(x + dx * i, topo, z + dz * i, ponta)
        self.ponto(x + dx * braco, topo - 1, z + dz * braco, ("minecraft:lantern", {"hanging": True}))
        return True

    # ------------------------------------------------------------------ medidas e validação
    def pecas_soltas(self, ignorar: tuple = ("light_block", "end_rod", "amethyst_cluster", "hanging_roots", "vine", "petals", "tulip", "allium", "azure", "short_grass", "poppy", "dandelion")) -> list[tuple[int, tuple, str]]:
        """Componentes (6-vizinhança) fora da maior peça: [(tamanho, (x1,y1,z1,x2,y2,z2), exemplo)], maiores primeiro. Plantas e luz invisível não contam."""
        sol = {p: b for p, b in self.blocos.items() if not any(k in _norm(b)[0] for k in ignorar)}
        visto: set = set()
        comps: list[list] = []
        vizinhos = tuple((dx, dy, dz) for dx in (-1, 0, 1) for dy in (-1, 0, 1) for dz in (-1, 0, 1) if (dx, dy, dz) != (0, 0, 0) and abs(dx) + abs(dy) + abs(dz) <= 2)  # face e aresta (escada de telhado encosta na diagonal)
        for ini in sol:
            if ini in visto:
                continue
            fila, comp = [ini], []
            visto.add(ini)
            while fila:
                x, y, z = fila.pop()
                comp.append((x, y, z))
                for dx, dy, dz in vizinhos:
                    q = (x + dx, y + dy, z + dz)
                    if q in sol and q not in visto:
                        visto.add(q)
                        fila.append(q)
            comps.append(comp)
        if len(comps) <= 1:
            return []
        comps.sort(key=len, reverse=True)
        saida = []
        for comp in comps[1:]:
            xs, ys, zs = zip(*comp)
            ex = _norm(sol[comp[0]])[0].replace("minecraft:", "")
            saida.append((len(comp), (min(xs), min(ys), min(zs), max(xs), max(ys), max(zs)), ex))
        return saida

    def caixa_limite(self) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
        xs, ys, zs = zip(*self.blocos) if self.blocos else ((0,), (0,), (0,))
        return (min(xs), min(ys), min(zs)), (max(xs), max(ys), max(zs))

    def validar(self, luz_emissores: Iterable[str] = ("lantern", "sea_lantern", "glowstone", "shroomlight", "torch", "end_rod", "froglight", "candle", "campfire", "redstone_lamp")) -> list[str]:
        """Checagens objetivas (o que um revisor de arquitetura Minecraft pega). Devolve avisos em texto."""
        avisos: list[str] = []
        if not self.blocos:
            return ["Cena vazia."]
        (x0, y0, z0), (x1, y1, z1) = self.caixa_limite()
        w, h, d = x1 - x0 + 1, y1 - y0 + 1, z1 - z0 + 1
        if w > 64 or d > 64 or h > 256:
            avisos.append(f"Tamanho {w}x{h}x{d} passa de 64x256x64: divida em módulos (limite do structure block/load).")
        # monocultura: nenhum bloco acima de 70% da superfície visível
        contagem: dict[str, int] = {}
        for (x, y, z), b in self.blocos.items():
            if any((x + dx, y + dy, z + dz) not in self.blocos for dx, dy, dz in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))):
                contagem[_norm(b)[0]] = contagem.get(_norm(b)[0], 0) + 1
        total = sum(contagem.values())
        for nome, n in sorted(contagem.items(), key=lambda kv: -kv[1])[:1]:
            if total > 40 and n / total > 0.7:
                avisos.append(f"Monocultura: {nome} é {n * 100 // total}% da superfície visível (misture 3 a 5 blocos parecidos).")
        # peças soltas no ar: componentes de blocos que não encostam (por face) na maior peça. Pega poste sem chão, árvore sem pé, ilhota perdida.
        for tamanho, caixa, amostra in self.pecas_soltas():
            avisos.append(f"PEÇA SOLTA: {tamanho} bloco(s) sem encostar no resto, em x{caixa[0]}..{caixa[3]} y{caixa[1]}..{caixa[4]} z{caixa[2]}..{caixa[5]} (ex.: {amostra}). Falta chão embaixo?")
        # luz: sem nenhuma fonte, a cena fica escura e os mobs nascem
        if not any(any(k in _norm(b)[0] for k in luz_emissores) for b in self.blocos.values()):
            avisos.append("Nenhuma fonte de luz na cena (luminária, lanterna, vidro luminoso).")
        return avisos

    # ------------------------------------------------------------------ saída
    def para_volume(self) -> dict:
        """IBlockVolume do Minecraft Creator Tools: camadas de baixo para cima, chaves de uma letra."""
        (x0, y0, z0), (x1, y1, z1) = self.caixa_limite()
        simbolos = ".#ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@%&*+=~^<>?"
        chaves: dict[tuple[str, tuple], str] = {}
        key: dict[str, dict] = {".": {"typeId": AR}}
        for b in self.blocos.values():
            n = _norm(b)
            if n not in chaves:
                s = simbolos[len(chaves) + 1]  # pula o "."
                chaves[n] = s
                key[s] = {"typeId": n[0], **({"properties": dict(n[1])} if n[1] else {})}
        camadas = []
        for y in range(y0, y1 + 1):
            linhas = []
            for z in range(z0, z1 + 1):
                linhas.append("".join(chaves[_norm(self.blocos[(x, y, z)])] if (x, y, z) in self.blocos else "." for x in range(x0, x1 + 1)))
            camadas.append(linhas)
        return {"southWestBottom": {"x": 0, "y": 0, "z": 0}, "blockLayersBottomToTop": camadas, "key": key}

    def construir(self, pasta: Union[str, Path], renderizar: bool = True, mct: Union[str, Path, None] = None, visao: str = "all", ambiente: str = "plains", hora: str = "noon", largura: int = 1024) -> dict:
        """Gera <pasta>/<nome>.volume.json, .mcstructure e (opcional) .png pelo Minecraft Creator Tools. Devolve caminhos e avisos.

        visao: "all" (4 vistas em 2x2), "three-quarter", "front", "side" ou "back"; ambiente: "neutral", "plains", "desert", "snowy";
        hora: "noon", "sunset" ou "night" (o render de noite mostra como a iluminação da construção funciona)."""
        pasta = Path(pasta).resolve()
        pasta.mkdir(parents=True, exist_ok=True)
        base = pasta / self.nome
        volume = base.with_suffix(".volume.json")
        volume.write_text(json.dumps(self.para_volume()), encoding="utf-8")
        mct_dir = Path(mct or os.environ.get("MCT_DIR") or Path.home() / ".vulpus_tools" / "mct")
        saida = {"avisos": self.validar(), "volume": volume, "mcstructure": base.with_suffix(".mcstructure"), "png": None}
        if not (mct_dir / "node_modules" / ".bin").exists():
            saida["avisos"].append("O Minecraft Creator Tools não está instalado em %s (npm install @minecraft/creator-tools): só gerei o volume JSON." % mct_dir)
            return saida
        npx = shutil.which("npx") or "npx"
        subprocess.run([npx, "mct", "buildstructure", str(volume), str(saida["mcstructure"]), "--overwrite"], cwd=mct_dir, check=True, capture_output=True, timeout=300)
        if renderizar:
            png = base.with_suffix(".png")
            # o render do Creator Tools tem limite de ~30 s para montar a cena: estruturas com mais de ~4.500 blocos estouram.
            # Nelas uso a prévia isométrica própria (previa_voxel) e, para conferir detalhes, render_recorte().
            if len(self.blocos) <= LIMITE_RENDER_MCT:
                try:
                    self._render_mct(mct_dir, npx, saida["mcstructure"], png, visao, ambiente, hora, largura)
                    saida["png"] = png
                    return saida
                except Exception as e:  # noqa: BLE001
                    saida["avisos"].append(f"Render do Creator Tools falhou ({type(e).__name__}); usei a prévia isométrica.")
            saida["png"] = self.previa_leve(png)
        return saida

    def _render_mct(self, mct_dir: Path, npx: str, estrutura: Path, png: Path, visao: str, ambiente: str, hora: str, largura: int) -> None:
        tmp = mct_dir / f"{self.nome}.mcstructure"  # o render lê a estrutura de dentro da pasta de entrada (-i)
        shutil.copyfile(estrutura, tmp)
        args = [npx, "mct", "render", "structure", tmp.name, str(png), "-i", ".", "--environment", ambiente, "--time-of-day", hora, "--width", str(largura), "--height", str(largura), "--no-grid"]
        args += ["--all-views"] if visao == "all" else ["--view", visao]
        subprocess.run(args, cwd=mct_dir, check=True, capture_output=True, timeout=400)
        if not png.exists():
            raise RuntimeError("sem imagem")

    def previa_leve(self, png: Path, azimutes: tuple = (45, 135, 225, 315)) -> Path:
        """Prévia isométrica própria (rápida, sem limite de tamanho). Texturas vanilla, sem sombras reais."""
        import sys
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from previa_voxel import Cena as CenaLeve  # noqa: PLC0415

        leve = CenaLeve()
        for (x, y, z), b in self.blocos.items():
            leve.ponto(x, y, z, _norm(b)[0].replace("minecraft:", ""))  # blocos do addon ficam com o prefixo (cor da tabela)
        return leve.salvar(png, azimutes=azimutes, s=8 if len(self.blocos) > 6000 else 12)

    def recorte(self, x1: int, y1: int, z1: int, x2: int, y2: int, z2: int, nome: str | None = None) -> "Cena":
        """Sub-cena só com os blocos de uma caixa (para renderizar um detalhe de uma estrutura grande)."""
        sub = Cena(nome or f"{self.nome}_recorte")
        for (x, y, z), b in self.blocos.items():
            if min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2) and min(z1, z2) <= z <= max(z1, z2):
                sub.blocos[(x, y, z)] = b
        return sub
