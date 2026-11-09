"""QA da biblioteca: (1) links relativos entre .md que não existem; (2) IDs de bloco citados entre crases que não existem na lista oficial;
(3) documentos novos sem o cabeçalho de status. Uso (na raiz do repositório): python ferramentas/verificar_biblioteca.py"""
import pathlib
import re
import sys

R = pathlib.Path(__file__).resolve().parents[1]
validos = set((R / "ferramentas" / "construcao" / "blocos_validos.txt").read_text().split())
SUFIXOS = ("_planks", "_stairs", "_slab", "_bricks", "_brick", "_concrete", "_glass", "_pane", "_log", "_wool", "_wall", "_fence", "_trapdoor", "_door",
           "_leaves", "_carpet", "_terracotta", "_lantern", "_block", "_roots", "_stone", "_andesite", "_copper")
PASTAS = ("fundamentos", "estilos", "estruturas", "materiais", "ambientacao", "procedimentos", "tecnicas", "experimentos", "referencia")
# nomes que aparecem como identificadores de código/tecnica e não como bloco
IGNORAR = {"stone_slab", "cut_copper", "light_block", "iron_block", "stone_brick", "oak_door", "double_slab", "waxed_copper_block"}
problemas = 0
for md in sorted(R.rglob("*.md")):
    rel = md.relative_to(R)
    if rel.parts[0] not in PASTAS + ("README.md", "erros-e-licoes.md", "limitacoes-e-duvidas.md", "aulas", "ferramentas") and len(rel.parts) > 1:
        continue
    txt = md.read_text(encoding="utf-8")
    for m in re.finditer(r"\]\(([^)#\s]+\.md)(#[^)]*)?\)", txt):
        alvo = (md.parent / m.group(1)).resolve()
        if not alvo.exists():
            print("LINK QUEBRADO: %s -> %s" % (rel, m.group(1)))
            problemas += 1
    if rel.parts[0] in ("estilos", "estruturas", "materiais", "ambientacao", "fundamentos") and "> Status:" not in txt:
        print("SEM CABEÇALHO DE STATUS:", rel)
        problemas += 1
    if rel.parts[0] in ("estilos", "estruturas", "materiais", "ambientacao", "fundamentos", "procedimentos"):
        for m in re.finditer(r"`([a-z][a-z0-9_]{3,40})`", txt):
            t = m.group(1)
            if t in validos or t in IGNORAR:
                continue
            if t.startswith("light_block_") or t.startswith("construcao") or t.endswith(".py") or "." in t:
                continue
            if any(t.endswith(s) for s in SUFIXOS) and "_" in t:
                print("ID SUSPEITO (não está na lista oficial): %s em %s" % (t, rel))
                problemas += 1
print("problemas:", problemas)
sys.exit(1 if problemas else 0)
