import pickle,re,collections
res=pickle.load(open('res.pkl','rb'))
def n2(s):
    s=re.sub(r'corner=[a-z_]+,?','',s); s=re.sub(r'wood_type=[a-z_]+,?','',s); s=re.sub(r'hanging=\d,?','',s)
    s=re.sub(r'liquid_depth=\d+,?','',s); s=s.replace(',]',']').replace('[]','')
    return s
def sub(dw):
    out=collections.Counter()
    for (a,b),c in dw.items():
        a=n2(a);b=n2(b)
        if a==b: continue
        if a=='grass_block' and b=='dirt': continue
        if a.startswith('water') or b.startswith('water'): continue
        out[(a,b)]+=c
    return out
if __name__=='__main__':
    for n in range(1,51):
        s=sub(res[n][0]); t=sum(s.values())
        lv=sum(c for (a,b),c in s.items() if 'leaves' in a and b=='air')
        print('%02d subst=%d (folhas->ar %d)'%(n,t,lv))
