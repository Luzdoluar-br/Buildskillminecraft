import collections
from world import World, norm
from cmp import load_struct, orig
import ldb

W = World('world')
tpl = {}
for k, v in W.d.items():
    if k.startswith(b'structuretemplate_'): tpl[int(k[-2:])] = load_struct(v)

print('n | nome | nao-ar orig | diff mundo | diff template')
res = {}
for n in range(1, 51):
    name, (sz, ob, _) = orig(n)
    X0 = 70 * ((n - 1) % 10); Z0 = 70 * ((n - 1) // 10)
    nonair = sum(1 for b in ob.values() if norm(b) != 'air')
    dw = collections.Counter(); miss = 0; tot = 0
    for (x, y, z), b in ob.items():
        w = W.get(X0 + x, 100 + y, Z0 + z)
        if w is None: miss += 1; w = 'air'
        a = norm(b)
        if a != w: dw[(a, w)] += 1; tot += 1
    dt = None
    if n in tpl:
        dt = collections.Counter()
        for p, b in tpl[n][1].items():
            a = norm(ob.get(p)); m = norm(b)
            if a != m: dt[(a, m)] += 1
    res[n] = (dw, dt)
    print('%02d | %s | %d | mundo=%d (vazio %d/%d) | tpl=%s' % (n, name[3:-12], nonair, tot, miss, len(ob), sum(dt.values()) if dt is not None else '-'))
import pickle; pickle.dump(res, open('res.pkl', 'wb'))
