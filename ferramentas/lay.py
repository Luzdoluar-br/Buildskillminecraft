import sys,re
from world import World,norm
from cmp import orig
from filt import n2
W=World('world')
n=int(sys.argv[1]); ys=list(map(int,sys.argv[2:]))
name,(sz,ob,_)=orig(n)
X0=70*((n-1)%10);Z0=70*((n-1)//10)
leg={}
def sym(s):
    s=re.sub(r'\[.*\]','',n2(s))
    if s=='air': return '.'
    if s not in leg: leg[s]='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'[len(leg)%62]
    return leg[s]
for y in ys:
    print('--- y=%d  (esq=original | dir=mundo)  x vertical, z horizontal'%y)
    for x in range(sz[0]):
        a=''.join(sym(norm(ob[(x,y,z)])) for z in range(sz[2]))
        b=''.join(sym(W.get(X0+x,100+y,Z0+z) or 'air') for z in range(sz[2]))
        print(a+'   '+b)
print({v:k for k,v in leg.items()})
