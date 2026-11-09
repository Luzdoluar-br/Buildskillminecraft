"""Escritor próprio de .mcstructure (NBT little-endian) no mesmo formato dos arquivos do add-on da Aula 01 (version 18161159)."""
import struct

VERSAO = 18161159


def _s(txt):
    b = txt.encode("utf-8")
    return struct.pack("<H", len(b)) + b


def _tag(tid, nome, payload):
    return bytes([tid]) + _s(nome) + payload


def _estado(v):
    if isinstance(v, bool):
        return 1, struct.pack("<B", 1 if v else 0)
    if isinstance(v, int):
        return 3, struct.pack("<i", v)
    return 8, _s(str(v))


def _compound(itens):
    return b"".join(itens) + b"\x00"


def gravar(cena, caminho):
    (x0, y0, z0), (x1, y1, z1) = cena.caixa_limite()
    sx, sy, sz = x1 - x0 + 1, y1 - y0 + 1, z1 - z0 + 1
    pal = {}
    lista = []

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
    camada0 = struct.pack("<%di" % len(dados), *dados)
    camada1 = struct.pack("<%di" % len(dados), *([-1] * len(dados)))
    paleta = b""
    for nome, props in lista:
        est = b""
        for k, v in props:
            tid, pl = _estado(v)
            est += _tag(tid, k, pl)
        est += b"\x00"
        paleta += _compound([_tag(8, "name", _s(nome)), _tag(10, "states", est), _tag(3, "version", struct.pack("<i", VERSAO))])
    block_palette = _tag(9, "block_palette", bytes([10]) + struct.pack("<i", len(lista)) + paleta)
    default = _tag(10, "default", _compound([block_palette, _tag(10, "block_position_data", b"\x00")]))
    palette = _tag(10, "palette", _compound([default]))
    indices = _tag(9, "block_indices", bytes([9]) + struct.pack("<i", 2)
                   + bytes([3]) + struct.pack("<i", len(dados)) + camada0
                   + bytes([3]) + struct.pack("<i", len(dados)) + camada1)
    entidades = _tag(9, "entities", bytes([0]) + struct.pack("<i", 0))
    estrutura = _tag(10, "structure", _compound([indices, entidades, palette]))
    raiz = _compound([
        _tag(3, "format_version", struct.pack("<i", 1)),
        _tag(9, "size", bytes([3]) + struct.pack("<i", 3) + struct.pack("<3i", sx, sy, sz)),
        estrutura,
        _tag(9, "structure_world_origin", bytes([3]) + struct.pack("<i", 3) + struct.pack("<3i", 0, 0, 0)),
    ])
    with open(caminho, "wb") as f:
        f.write(bytes([10]) + _s("") + raiz)
    return (sx, sy, sz), len(lista)
