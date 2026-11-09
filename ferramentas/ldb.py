import struct, zlib, glob, os

def varint(b, i):
    r = 0; s = 0
    while True:
        c = b[i]; i += 1
        r |= (c & 0x7f) << s
        if not c & 0x80: return r, i
        s += 7

def decomp(data, t):
    if t == 0: return data
    if t == 2: return zlib.decompress(data)
    if t == 4: return zlib.decompress(data, -15)
    raise Exception('compression %d' % t)

def read_block(f, off, size):
    f.seek(off)
    raw = f.read(size + 5)
    return decomp(raw[:size], raw[size])

def iter_block(b):
    nrest = struct.unpack('<I', b[-4:])[0]
    end = len(b) - 4 - 4 * nrest
    i = 0; key = b''
    while i < end:
        sh, i = varint(b, i); ns, i = varint(b, i); vl, i = varint(b, i)
        key = key[:sh] + b[i:i + ns]; i += ns
        val = b[i:i + vl]; i += vl
        yield key, val

def read_table(path, out):
    with open(path, 'rb') as f:
        f.seek(-48, 2)
        foot = f.read(48)
        _, i = varint(foot, 0); _, i = varint(foot, i)
        io, i = varint(foot, i); isz, i = varint(foot, i)
        idx = read_block(f, io, isz)
        for _, h in iter_block(idx):
            o, j = varint(h, 0); s, j = varint(h, j)
            for k, v in iter_block(read_block(f, o, s)):
                uk = k[:-8]; tag = struct.unpack('<Q', k[-8:])[0]
                seq, typ = tag >> 8, tag & 0xff
                if uk not in out or out[uk][0] < seq:
                    out[uk] = (seq, typ, v)

def read_log(path, out):
    d = open(path, 'rb').read()
    i = 0; buf = b''
    while i + 7 <= len(d):
        ln = struct.unpack('<H', d[i + 4:i + 6])[0]; t = d[i + 6]
        chunk = d[i + 7:i + 7 + ln]; i += 7 + ln
        if t == 0 and ln == 0: continue
        buf += chunk
        if t in (1, 4):
            parse_batch(buf, out); buf = b''
        elif t == 0:
            buf = b''

def parse_batch(b, out):
    seq = struct.unpack('<Q', b[:8])[0]; n = struct.unpack('<I', b[8:12])[0]
    i = 12
    for _ in range(n):
        typ = b[i]; i += 1
        kl, i = varint(b, i); k = b[i:i + kl]; i += kl
        v = b''
        if typ == 1:
            vl, i = varint(b, i); v = b[i:i + vl]; i += vl
        if k not in out or out[k][0] <= seq:
            out[k] = (seq, typ, v)
        seq += 1

def load(d):
    out = {}
    for p in sorted(glob.glob(os.path.join(d, '*.ldb'))): read_table(p, out)
    for p in sorted(glob.glob(os.path.join(d, '*.log'))): read_log(p, out)
    return {k: v[2] for k, v in out.items() if v[1] == 1}

# ---- NBT little endian
def nbt_read(b, i, tag, name_needed=True):
    if tag == 1: return b[i], i + 1
    if tag == 2: return struct.unpack('<h', b[i:i + 2])[0], i + 2
    if tag == 3: return struct.unpack('<i', b[i:i + 4])[0], i + 4
    if tag == 4: return struct.unpack('<q', b[i:i + 8])[0], i + 8
    if tag == 5: return struct.unpack('<f', b[i:i + 4])[0], i + 4
    if tag == 6: return struct.unpack('<d', b[i:i + 8])[0], i + 8
    if tag == 7:
        n = struct.unpack('<i', b[i:i + 4])[0]; return b[i + 4:i + 4 + n], i + 4 + n
    if tag == 8:
        n = struct.unpack('<H', b[i:i + 2])[0]; return b[i + 2:i + 2 + n].decode('utf8', 'replace'), i + 2 + n
    if tag == 9:
        t = b[i]; n = struct.unpack('<i', b[i + 1:i + 5])[0]; i += 5; r = []
        for _ in range(n):
            v, i = nbt_read(b, i, t); r.append(v)
        return r, i
    if tag == 10:
        r = {}
        while True:
            t = b[i]; i += 1
            if t == 0: return r, i
            n = struct.unpack('<H', b[i:i + 2])[0]; nm = b[i + 2:i + 2 + n].decode('utf8'); i += 2 + n
            r[nm], i = nbt_read(b, i, t)
    if tag == 11:
        n = struct.unpack('<i', b[i:i + 4])[0]; return list(struct.unpack('<%di' % n, b[i + 4:i + 4 + 4 * n])), i + 4 + 4 * n
    if tag == 12:
        n = struct.unpack('<i', b[i:i + 4])[0]; return list(struct.unpack('<%dq' % n, b[i + 4:i + 4 + 8 * n])), i + 4 + 8 * n
    raise Exception('tag %d' % tag)

def nbt_root(b, i=0):
    t = b[i]; n = struct.unpack('<H', b[i + 1:i + 3])[0]; i += 3 + n
    return nbt_read(b, i, t)

def bkey(c):
    """canonical block string from compound with name/states"""
    st = c.get('states', {})
    return c['name'] + ('' if not st else '[' + ','.join('%s=%s' % (k, st[k]) for k in sorted(st)) + ']')
