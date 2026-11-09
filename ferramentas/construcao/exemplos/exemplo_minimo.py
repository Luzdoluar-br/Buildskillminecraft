"""Exemplo mínimo executável: casa pequena com porta, escada interna, cama com entidade de bloco; exporta, relê e audita.
Rode a partir da pasta `ferramentas/`:   python construcao/exemplos/exemplo_minimo.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))      # pasta ferramentas/
from construcao.cena import Cena, escada, SUL, NORTE, LESTE, OESTE
from construcao.moldes import Molde, pal, ESCADAS, M
from construcao.exportar import gravar, ler, Byte
from construcao.auditoria_geral import auditar, relatorio

c = Cena("casa_minima", semente=1)
c.caixa(-2, -1, -2, 12, 0, 10, M + "grass_block")
m = Molde(c, 0, 0, 9, 7, 1)                    # pegada 9x7, piso em y=1
m.box(0, 0, 0, 8, 0, 6, pal([("stone_bricks", 3), ("andesite", 2)]))
m.oca(0, 1, 0, 8, 4, 6, pal([("stripped_spruce_log", 1)]))
m.limpar(4, 1, 6, 4, 3, 6)
m.porta(4, 1, 6, "spruce")
m.st(4, 3, 6, "stone_brick_stairs", NORTE, True)          # verga em escada invertida
m.box(0, 5, 0, 8, 5, 6, M + "spruce_planks")              # forro
m.st(7, 1, 2, "spruce_stairs", SUL)
m.cama(2, 1, 2, SUL)                                       # cama simulada com lã (o bloco `bed` exige entidade de bloco)
m.p(1, 1, 5, (M + "bed", {"direction": 0, "head_piece_bit": True, "occupied_bit": False}))   # cama real...
m.p(1, 1, 4, (M + "bed", {"direction": 0, "head_piece_bit": False, "occupied_bit": False}))

saida = Path(__file__).resolve().parent / "saida"
saida.mkdir(exist_ok=True)
caixa0 = c.caixa_limite()[0]
cabeca = m.mundo(1, 1, 5)
pe = m.mundo(1, 1, 4)
dims, n = gravar(c, saida / "casa_minima.mcstructure",
                 entidades={cabeca: {"id": "Bed", "color": Byte(14), "BlockEntityVersion": 0}, pe: {"id": "Bed", "color": Byte(14), "BlockEntityVersion": 0}})
blocos, ents, size = ler(saida / "casa_minima.mcstructure")
print("estrutura:", dims, "paleta:", n, "| relida:", size, len(blocos), "blocos,", len(ents), "entidades de bloco")
print(relatorio(auditar(c)))
