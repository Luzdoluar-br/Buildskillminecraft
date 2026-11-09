"""Escritor de `.mcstructure` (NBT little-endian) com suporte a entidades de bloco e leitor para conferência.

Formato conferido contra uma estrutura gravada pelo próprio jogo (ver referencia/mcstructure-formato.md):
índice linear = x*(Y*Z) + y*Z + z; booleano = byte; inteiro = int; texto = string; `block_position_data` indexado pelo índice linear.

Uso:
    from construcao.exportar import gravar, ler
    dims, n_paleta = gravar(cena, "saida/minha.mcstructure", entidades={(x, y, z): {"id": "Bed", "color": Byte(0)}})
    cena2 = ler("saida/minha.mcstructure")   # devolve dict {(x,y,z): (nome, estados)} para auditoria/conferência

Tipos NBT explícitos quando necessário: Byte(1), Short(1), Int(1), Long(1), Float(1.0). `bool` vira byte, `int` vira int, `str` vira string,
dict vira compound, list vira lista (tipo do 1º elemento).
"""
import struct

VERSAO_PALETA = 18168865      # valor gravado pelo jogo atual do dono (a wiki.bedrock.dev cita o mesmo)
FORMATO = 1                   # o jogo grava 2 (com compression=0), mas CARREGA o 1 (testado)


class Byte(int):
    pass


class Short(int):
    pass


class Int(int):
    pass


class Long(int):
    pass


class Float(float):
    pass


def _s(txt):
    b = txt.encode("utf-8")
    return struct.pack("<H", len(b)) + b


def _tipo(v):
    if isinstance(v, bool) or isinstance(v, Byte):
        return 1
    if isinstance(v, Short):
        return 2
    if isinstance(v, Long):
        return 4
    if isinstance(v, Float) or isinstance(v, float):
        return 5
    if isinstance(v, int):
        return 3
    if isinstance(v, str):
        return 8
    if isinstance(v, dict):
        return 10
    if isinstance(v, (list, tuple)):
        return 9
    raise TypeError("tipo NBT não suportado: %r" % type(v))


def _payload(v):
    t = _tipo(v)
    if t == 1:
        return struct.pack("<b", int(v))
    if t == 2:
        return struct.pack("<h", int(v))
    if t == 3:
        return struct.pack("<i", int(v))
    if t == 4:
        return struct.pack("<q", int(v))
    if t == 5:
        return struct.pack("<f", float(v))
    if t == 8:
        return _s(v)
    if t == 10:
        return b"".join(bytes([_tipo(x)]) + _s(k) + _payload(x) for k, x in v.items()) + b"\x00"
    if t == 9:
        if not v:
            return bytes([0]) + struct.pack("<i", 0)
        te = _tipo(v[0])
        return bytes([te]) + struct.pack("<i", len(v)) + b"".join(_payload(x) for x in v)
    raise TypeError(t)


def _estado(v):
    return Byte(1 if v else 0) if isinstance(v, bool) else v


def gravar(cena, caminho, entidades=None):
    """Grava `cena` (blocos em cena.blocos) em `caminho`. `entidades` = {(x, y, z): dict NBT} (coordenadas da cena); x,y,z da entidade são preenchidos."""
    (x0, y0, z0), (x1, y1, z1) = cena.caixa_limite()
    sx, sy, sz = x1 - x0 + 1, y1 - y0 + 1, z1 - z0 + 1
    pal, lista = {}, []

    def idx(b):
        nome, props = (b, ()) if isinstance(b, str) else (b[0], tuple(sorted(b[1].items())))
        k = (nome, props)
        if k not in pal:
            pal[k] = len(lista)
            lista.append(k)
        return pal[k]

    ar = idx("minecraft:air")
    dados = [ar] * (sx * sy * sz)
    for (x, y, z), b in cena.blocos.items():
        dados[((x - x0) * sy + (y - y0)) * sz + (z - z0)] = idx(b)
    paleta = []
    for nome, props in lista:
        paleta.append({"name": nome, "states": {k: _estado(v) for k, v in props}, "version": Int(VERSAO_PALETA)})
    posdata = {}
    for (x, y, z), ent in (entidades or {}).items():
        if (x, y, z) not in cena.blocos:
            raise ValueError("entidade em bloco inexistente: %r" % ((x, y, z),))
        li = ((x - x0) * sy + (y - y0)) * sz + (z - z0)
        posdata[str(li)] = {"block_entity_data": {**ent, "x": Int(x), "y": Int(y), "z": Int(z)}}
    raiz = {
        "format_version": Int(FORMATO),
        "size": [Int(sx), Int(sy), Int(sz)],
        "structure": {
            "block_indices": [[Int(v) for v in dados], [Int(-1)] * len(dados)],
            "entities": [],
            "palette": {"default": {"block_palette": paleta, "block_position_data": posdata}},
        },
        "structure_world_origin": [Int(0), Int(0), Int(0)],
    }
    corpo = b"".join(bytes([_tipo(v)]) + _s(k) + _payload(v) for k, v in raiz.items()) + b"\x00"
    with open(caminho, "wb") as f:
        f.write(bytes([10]) + _s("") + corpo)
    return (sx, sy, sz), len(lista)


# ------------------------------------------------------------------ leitura (para conferir o que foi gravado ou o que o jogo gravou)
def _ler(b, i, tag):
    if tag == 1:
        return struct.unpack("<b", b[i:i + 1])[0], i + 1
    if tag == 2:
        return struct.unpack("<h", b[i:i + 2])[0], i + 2
    if tag == 3:
        return struct.unpack("<i", b[i:i + 4])[0], i + 4
    if tag == 4:
        return struct.unpack("<q", b[i:i + 8])[0], i + 8
    if tag == 5:
        return struct.unpack("<f", b[i:i + 4])[0], i + 4
    if tag == 6:
        return struct.unpack("<d", b[i:i + 8])[0], i + 8
    if tag == 8:
        n = struct.unpack("<H", b[i:i + 2])[0]
        return b[i + 2:i + 2 + n].decode("utf-8", "replace"), i + 2 + n
    if tag == 9:
        t = b[i]
        n = struct.unpack("<i", b[i + 1:i + 5])[0]
        i += 5
        r = []
        for _ in range(n):
            v, i = _ler(b, i, t)
            r.append(v)
        return r, i
    if tag == 10:
        r = {}
        while True:
            t = b[i]
            i += 1
            if t == 0:
                return r, i
            n = struct.unpack("<H", b[i:i + 2])[0]
            nome = b[i + 2:i + 2 + n].decode("utf-8")
            i += 2 + n
            r[nome], i = _ler(b, i, t)
    raise ValueError("tag %d" % tag)


def ler_nbt(caminho):
    b = open(caminho, "rb").read()
    n = struct.unpack("<H", b[1:3])[0]
    raiz, _ = _ler(b, 3 + n, b[0])
    return raiz


def ler(caminho):
    """Devolve ({(x,y,z): (nome, estados)} , entidades {(x,y,z): dict}, size) em coordenadas relativas ao canto mínimo."""
    raiz = ler_nbt(caminho)
    sx, sy, sz = raiz["size"]
    s = raiz["structure"]
    pal = s["palette"]["default"]["block_palette"]
    idx = s["block_indices"][0]
    blocos = {}
    for x in range(sx):
        for y in range(sy):
            for z in range(sz):
                v = idx[(x * sy + y) * sz + z]
                if v >= 0 and pal[v]["name"] != "minecraft:air":
                    blocos[(x, y, z)] = (pal[v]["name"], pal[v].get("states", {}))
    ent = {}
    for k, v in s["palette"]["default"].get("block_position_data", {}).items():
        li = int(k)
        x, rem = divmod(li, sy * sz)
        y, z = divmod(rem, sz)
        ent[(x, y, z)] = v.get("block_entity_data", {})
    return blocos, ent, (sx, sy, sz)
