import ldb, glob, os, sys, collections, json

BP = 'bp/x/structures/aula/'

def load_struct(b):
    root, _ = ldb.nbt_root(b)
    size = root['size']
    s = root['structure']
    pal = [ldb.bkey(p) for p in s['palette']['default']['block_palette']]
    idx = s['block_indices'][0]
    sx, sy, sz = size
    blocks = {}
    for x in range(sx):
        for y in range(sy):
            for z in range(sz):
                v = idx[(x * sy + y) * sz + z]
                blocks[(x, y, z)] = pal[v] if v >= 0 else None
    bpd = s['palette']['default'].get('block_position_data', {})
    return size, blocks, root

def orig(n):
    f = glob.glob(BP + '%02d_*.mcstructure' % n)[0]
    return os.path.basename(f), load_struct(open(f, 'rb').read())

if __name__ == '__main__':
    d = ldb.load('world')
    for k, v in sorted(d.items()):
        if k.startswith(b'structuretemplate_'):
            n = int(k[-2:])
            name, (osz, ob, oroot) = orig(n)
            msz, mb, mroot = load_struct(v)
            print('=== modificada_%02d vs %s | orig size %s | mod size %s' % (n, name, osz, msz))
            ch = collections.Counter(); tot = 0
            for p in set(ob) | set(mb):
                a = ob.get(p); b = mb.get(p)
                if a != b:
                    ch[(a, b)] += 1; tot += 1
            print('  blocos diferentes:', tot, 'de', len(mb))
            for (a, b), c in ch.most_common(25):
                print('   %4d  %s -> %s' % (c, a, b))
