import sys,collections,re
from world import World,norm
from cmp import orig
from filt import n2
W=World('world')
def strip(s): return re.sub(r'\[.*\]','',n2(s))
for n in map(int,sys.argv[1:]):
    name,(sz,ob,_)=orig(n)
    X0=70*((n-1)%10);Z0=70*((n-1)//10)
    chg=collections.Counter();ys=collections.Counter();origmat=collections.Counter();newmat=collections.Counter()
    for (x,y,z),b in ob.items():
        a=n2(norm(b));w=W.get(X0+x,100+y,Z0+z) or 'air';w=n2(w)
        if a!='air': origmat[strip(a)]+=1
        if w!='air': newmat[strip(w)]+=1
        if a==w or (a=='grass_block' and w=='dirt') or a.startswith('water') or w.startswith('water'): continue
        chg[(strip(a),strip(w))]+=1; ys[y]+=1
    print('=====',n,name,sz)
    print(' y-dist:',dict(sorted(ys.items())))
    print(' materiais novos (nao existiam):',{k:v for k,v in newmat.items() if k not in origmat})
    print(' materiais removidos:',{k:origmat[k] for k in origmat if k not in newmat})
    print(' trocas:',[('%s>%s'%k,c) for k,c in chg.most_common(22)])
