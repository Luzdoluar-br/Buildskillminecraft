import ldb, struct, collections, re, glob, os
from cmp import load_struct, orig

DROP = {'update_bit', 'persistent_bit'}
def norm(s):
    if s is None: return 'air'
    m = re.match(r'([^\[]+)(?:\[(.*)\])?$', s)
    name = m.group(1).replace('minecraft:', '')
    st = []
    if m.group(2):
        for kv in m.group(2).split(','):
            k, v = kv.split('=', 1)
            k = k.replace('minecraft:', '')
            if k in DROP or k.startswith('connection_') or k.startswith('wall_connection') or k == 'wall_post_bit': continue
            if (k, v) in (('corner', 'none'), ('pillar_axis', 'y'), ('vertical_half', 'bottom'), ('liquid_depth', '0'), ('upside_down_bit', '0')): continue
            st.append(k + '=' + v)
    if name in ('air', 'cave_air', 'void_air', 'structure_void'): return 'air'
    return name + ('[' + ','.join(st) + ']' if st else '')

class World:
    def __init__(self, d):
        self.d = ldb.load(d); self.cache = {}
    def sub(self, cx, cz, sy):
        k = (cx, cz, sy)
        if k in self.cache: return self.cache[k]
        key = struct.pack('<ii', cx, cz) + b'\x2f' + struct.pack('<b', sy)
        v = self.d.get(key)
        r = None
        if v is not None:
            ver = v[0]; ns = v[1]; i = 2
            if ver == 9: i = 3
            storages = []
            for _ in range(ns):
                hdr = v[i]; i += 1
                bits = hdr >> 1
                bpw = 32 // bits; nw = -(-4096 // bpw)
                words = struct.unpack('<%dI' % nw, v[i:i + 4 * nw]); i += 4 * nw
                n = struct.unpack('<i', v[i:i + 4])[0]; i += 4
                pal = []
                for _ in range(n):
                    c, i = ldb.nbt_root(v, i); pal.append(norm(ldb.bkey(c)))
                mask = (1 << bits) - 1
                idx = []
                for w in words:
                    for j in range(bpw):
                        idx.append((w >> (j * bits)) & mask)
                storages.append((pal, idx))
            r = storages[0]
        self.cache[k] = r
        return r
    def get(self, x, y, z):
        s = self.sub(x >> 4, z >> 4, y >> 4)
        if s is None: return None
        pal, idx = s
        return pal[idx[(((x & 15) * 16) + (z & 15)) * 16 + (y & 15)]]
