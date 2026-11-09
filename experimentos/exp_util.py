"""Utilitário comum dos experimentos: cena de teste, fotos, auditoria e exportação. Cada experimento roda isolado (não toca nas construções das aulas)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ferramentas"))
from construcao.cena import Cena, Paleta, escada, laje, LESTE, OESTE, SUL, NORTE  # noqa: E402,F401
from construcao.moldes import Molde, pal, M, ESCADAS  # noqa: E402,F401
from construcao.exportar import gravar  # noqa: E402,F401
from construcao.auditoria_geral import auditar, relatorio  # noqa: E402,F401
from construcao import camera  # noqa: E402


def chao(c, x0, z0, x1, z1, y=0, bloco=None):
    bloco = bloco or pal([("grass_block", 8), ("moss_block", 1)], 3)
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            c.ponto(x, y - 1, z, M + "dirt")
            c.ponto(x, y, z, bloco)


def fotos(c, pasta, vistas, w=900, h=560, fov=65):
    """vistas = {nome: (posicao, alvo)}. Grava PNG em <pasta>/imagens/<nome>.png"""
    pasta = Path(pasta) / "imagens"
    pasta.mkdir(parents=True, exist_ok=True)
    for nome, (pos, alvo) in vistas.items():
        camera.foto(c, pos, alvo, pasta / (nome + ".png"), fov=fov, w=w, h=h)
    return pasta


def fechar(c, pasta, nome, ignorar=(), entidades=None):
    """Audita (regras genéricas), grava o .mcstructure em <pasta>/saida/ e devolve (erros, dims)."""
    pasta = Path(pasta) / "saida"
    pasta.mkdir(parents=True, exist_ok=True)
    erros = auditar(c, ignorar=ignorar)
    dims, n = gravar(c, pasta / (nome + ".mcstructure"), entidades=entidades)
    return erros, dims, n, len(c.blocos)
