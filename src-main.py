import os, json, urllib.request, random
V=[0,100,320,330,500,900,20000]
PAWN=[0,0,0,0,0,0,0,0, 5,10,10,-20,-20,10,10,5, 5,-5,-10,0,0,-10,-5,5, 0,0,0,20,20,0,0,0, 5,5,10,25,25,10,5,5, 10,10,20,30,30,20,10,10, 50,50,50,50,50,50,50,50, 0,0,0,0,0,0,0,0]
KNIGHT=[-50,-40,-30,-30,-30,-30,-40,-50, -40,-20,0,5,5,0,-20,-40, -30,5,10,15,15,10,5,-30, -30,0,15,20,20,15,0,-30, -30,5,15,20,20,15,5,-30, -30,0,10,15,15,10,0,-30, -40,-20,0,0,0,0,-20,-40, -50,-40,-30,-30,-30,-30,-40,-50]
BISHOP=[-20,-10,-10,-10,-10,-10,-10,-20, -10,5,0,0,0,0,5,-10, -10,10,10,10,10,10,10,-10, -10,0,10,10,10,10,0,-10, -10,5,5,10,10,5,5,-10, -10,0,5,10,10,5,0,-10, -10,0,0,0,0,0,0,-10, -20,-10,-10,-10,-10,-10,-10,-20]
ROOK=[0,0,0,5,5,0,0,0, -5,0,0,0,0,0,0,-5, -5,0,0,0,0,0,0,-5, -5,0,0,0,0,0,0,-5, -5,0,0,0,0,0,0,-5, -5,0,0,0,0,0,0,-5, 5,10,10,10,10,10,10,5, 0,0,0,0,0,0,0,0]
QUEEN=[-20,-10,-10,-5,-5,-10,-10,-20, -10,0,5,0,0,0,0,-10, -10,5,5,5,5,5,0,-10, 0,0,5,5,5,5,0,-5, -5,0,5,5,5,5,0,-5, -10,0,5,5,5,5,0,-10, -10,0,0,0,0,0,0,-10, -20,-10,-10,-5,-5,-10,-10,-20]
KINGM=[20,30,10,0,0,10,30,20, 20,20,0,0,0,0,20,20, -10,-20,-20,-20,-20,-20,-20,-10, -20,-30,-30,-40,-40,-30,-30,-20, -30,-40,-40,-50,-50,-40,-40,-30, -30,-40,-40,-50,-50,-40,-40,-30, -30,-40,-40,-50,-50,-40,-40,-30, -30,-40,-40,-50,-50,-40,-40,-30]
KINGE=[-50,-30,-30,-30,-30,-30,-30,-50, -30,-30,0,0,0,0,-30,-30, -30,-10,20,30,30,20,-10,-30, -30,-10,30,40,40,30,-10,-30, -30,-10,30,40,40,30,-10,-30, -30,-10,20,30,30,20,-10,-30, -30,-20,-10,0,0,-10,-20,-30, -50,-40,-30,-20,-20,-30,-40,-50]
PST=[None,PAWN,KNIGHT,BISHOP,ROOK,QUEEN,KINGM]
ND=[-33,-31,-18,-14,14,18,31,33]
KD=[-17,-16,-15,-1,1,15,16,17]
BD=[-17,-15,15,17]
RD=[-16,-1,1,16]
_r=random.Random(12345)
Z=[[ _r.getrandbits(64) for _ in range(128)] for _ in range(13)]
ZS=_r.getrandbits(64)
ZC=[_r.getrandbits(64) for _ in range(16)]
ZE=[_r.getrandbits(64) for _ in range(8)]
NODES=100000
INF=30000
MATE=29000
class E:
    def __init__(s):
        s.b=[0]*128; s.t=1; s.c=0; s.e=-1; s.h=0; s.k=[0,0]; s.u=[]
        s.tt={}; s.kl=[[0,0] for _ in range(64)]; s.hh={}
        s.nd=0; s.stop=False
    def fen(s,f):
        p=f.split()
        s.b=[0]*128; s.t=1 if p[1]=='w' else -1; s.c=0; s.e=-1
        if 'K' in p[2]: s.c|=1
        if 'Q' in p[2]: s.c|=2
        if 'k' in p[2]: s.c|=4
        if 'q' in p[2]: s.c|=8
        if p[3]!='-': s.e=(ord(p[3][0])-97)+(int(p[3][1])-1)*16
        mp={'P':1,'N':2,'B':3,'R':4,'Q':5,'K':6,'p':-1,'n':-2,'b':-3,'r':-4,'q':-5,'k':-6}
        r=7; f=0
        for ch in p[0]:
            if ch=='/': r-=1; f=0
            elif ch.isdigit(): f+=int(ch)
            else:
                sq=r*16+f; pc=mp[ch]; s.b[sq]=pc
                if abs(pc)==6: s.k[0 if pc>0 else 1]=sq
                f+=1
        s.h=0
        for i in range(128):
            if s.b[i]: s.h^=Z[s.b[i]+6][i]
        if s.t<0: s.h^=ZS
        s.h^=ZC[s.c]
        if s.e>=0: s.h^=ZE[s.e&7]
    def att(s,sq,by):
        b=s.b
        if by>0:
            if not (sq-15)&0x88 and b[sq-15]==1: return 1
            if not (sq-17)&0x88 and b[sq-17]==1: return 1
        else:
            if not (sq+15)&0x88 and b[sq+15]==-1: return 1
            if not (sq+17)&0x88 and b[sq+17]==-1: return 1
        for d in ND:
            q=sq+d
            if 0<=q<128 and not q&0x88 and b[q]==2*by: return 1
        for d in KD:
            q=sq+d
            if 0<=q<128 and not q&0x88 and b[q]==6*by: return 1
        for d in BD:
            q=sq+d
            while 0<=q<128 and not q&0x88:
                p=b[q]
                if p:
                    if p==3*by or p==5*by: return 1
                    break
                q+=d
        for d in RD:
            q=sq+d
            while 0<=q<128 and not q&0x88:
                p=b[q]
                if p:
                    if p==4*by or p==5*by: return 1
                    break
                q+=d
        return 0
    def gen(s,cap):
        b=s.b; t=s.t; mv=[]
        for f in range(128):
            if f&0x88: continue
            p=b[f]
            if not p or (p>0)!=(t>0): continue
            a=abs(p)
            if a==1:
                d=16*t; t1=f+d
                if not cap and not b[t1]:
                    r=f>>4
                    if (t>0 and r==6) or (t<0 and r==1):
                        for q in (5,4,3,2): mv.append(f|(t1<<7)|(q<<14))
                    else:
                        mv.append(f|(t1<<7))
                        if (t>0 and r==1) or (t<0 and r==6):
                            if not b[f+2*d]: mv.append(f|((f+2*d)<<7))
                for dd in (d-1,d+1):
                    t2=f+dd
                    if t2&0x88: continue
                    q=b[t2]
                    if q and (q>0)!=(t>0):
                        r=f>>4
                        if (t>0 and r==6) or (t<0 and r==1):
                            for pr in (5,4,3,2): mv.append(f|(t2<<7)|(pr<<14))
                        else: mv.append(f|(t2<<7))
                    elif t2==s.e:
                        mv.append(f|(t2<<7))
            elif a==2:
                for d in ND:
                    q=f+d
                    if 0<=q<128 and not q&0x88:
                        v=b[q]
                        if not v and cap: continue
                        if not v or (v>0)!=(t>0): mv.append(f|(q<<7))
            elif a==6:
                for d in KD:
                    q=f+d
                    if 0<=q<128 and not q&0x88:
                        v=b[q]
                        if not v and cap: continue
                        if not v or (v>0)!=(t>0): mv.append(f|(q<<7))
                if not cap:
                    if t>0:
                        if s.c&1 and not b[5] and not b[6] and b[7]==4 and not s.att(4,-1) and not s.att(5,-1) and not s.att(6,-1): mv.append(4|(6<<7))
                        if s.c&2 and not b[3] and not b[2] and not b[1] and b[0]==4 and not s.att(4,-1) and not s.att(3,-1) and not s.att(2,-1): mv.append(4|(2<<7))
                    else:
                        if s.c&4 and not b[117] and not b[118] and b[119]==-4 and not s.att(116,1) and not s.att(117,1) and not s.att(118,1): mv.append(116|(118<<7))
                        if s.c&8 and not b[115] and not b[114] and not b[113] and b[112]==-4 and not s.att(116,1) and not s.att(115,1) and not s.att(114,1): mv.append(116|(114<<7))
            else:
                ds=BD if a==3 else RD if a==4 else BD+RD
                for d in ds:
                    q=f+d
                    while 0<=q<128 and not q&0x88:
                        v=b[q]
                        if not v:
                            if not cap: mv.append(f|(q<<7))
                        else:
                            if (v>0)!=(t>0): mv.append(f|(q<<7))
                            break
                        q+=d
        return mv
    def mk(s,m):
        f=m&127; t=(m>>7)&127; pr=(m>>14)&7
        b=s.b; pc=b[f]; cap=b[t]
        s.u.append((m,cap,s.c,s.e,s.h))
        s.h^=Z[pc+6][f]; s.h^=Z[pc+6][t]
        if cap: s.h^=Z[cap+6][t]
        s.h^=ZC[s.c]
        if s.e>=0: s.h^=ZE[s.e&7]
        if abs(pc)==1 and t==s.e and not cap:
            cpsq=t-16*s.t; cp=b[cpsq]
            s.h^=Z[cp+6][cpsq]; b[cpsq]=0
        b[t]=pc; b[f]=0
        if pr:
            b[t]=pr*s.t; s.h^=Z[pr*s.t+6][t]; s.h^=Z[pc+6][t]
        ep=-1
        if abs(pc)==6:
            s.k[0 if pc>0 else 1]=t
            if abs(t-f)==2:
                if t>f: rs,rd=f+3,f+1
                else: rs,rd=f-4,f-1
                rp=b[rs]; b[rd]=rp; b[rs]=0
                s.h^=Z[rp+6][rs]; s.h^=Z[rp+6][rd]
            s.c&= ~(3 if pc>0 else 12)
        if abs(pc)==1 and abs(t-f)==32: ep=f+16*s.t
        if f==0 or t==0: s.c&=~2
        if f==7 or t==7: s.c&=~1
        if f==112 or t==112: s.c&=~8
        if f==119 or t==119: s.c&=~4
        s.e=ep
        s.h^=ZC[s.c]
        if s.e>=0: s.h^=ZE[s.e&7]
        s.h^=ZS; s.t=-s.t
    def un(s):
        m,cap,cs,ep,h=s.u.pop()
        f=m&127; t=(m>>7)&127; pr=(m>>14)&7
        b=s.b; s.t=-s.t; s.h=h; s.c=cs; s.e=ep
        pc=b[t]
        if pr: pc=1*s.t
        b[f]=pc; b[t]=cap
        if abs(pc)==1 and t==ep and not cap:
            b[t-16*s.t]=-1*s.t
        if abs(pc)==6:
            s.k[0 if pc>0 else 1]=f
            if abs(t-f)==2:
                if t>f: rs,rd=f+3,f+1
                else: rs,rd=f-4,f-1
                b[rs]=b[rd]; b[rd]=0
    def ev(s):
        b=s.b; mg=0; eg=0; ph=0
        wpf=[0]*8; bpf=[0]*8; wb=0; bb=0; wk=0; bk=0
        for sq in range(128):
            if sq&0x88: continue
            p=b[sq]
            if not p: continue
            a=abs(p); r=sq>>4; fl=sq&7
            if p>0:
                i=r*8+fl
                if a==6:
                    mg+=V[a]+KINGM[i]; eg+=V[a]+KINGE[i]; wk=sq
                else:
                    mg+=V[a]+PST[a][i]; eg+=V[a]+PST[a][i]
                    if a==1: wpf[fl]|=1<<r
                    elif a==3: wb+=1
                if a in (2,3): ph+=1
                elif a==4: ph+=2
                elif a==5: ph+=4
            else:
                i=(7-r)*8+fl
                if a==6:
                    mg-=V[a]+KINGM[i]; eg-=V[a]+KINGE[i]; bk=sq
                else:
                    mg-=V[a]+PST[a][i]; eg-=V[a]+PST[a][i]
                    if a==1: bpf[fl]|=1<<r
                    elif a==3: bb+=1
                if a in (2,3): ph+=1
                elif a==4: ph+=2
                elif a==5: ph+=4
        if ph>24: ph=24
        if wb>=2: mg+=30; eg+=30
        if bb>=2: mg-=30; eg-=30
        for fl in range(8):
            w=wpf[fl]; bl=bpf[fl]
            if w:
                if w&(w-1): mg-=8; eg-=8
                adj=(wpf[fl-1] if fl>0 else 0)|(wpf[fl+1] if fl<7 else 0)
                if not adj: mg-=10; eg-=10
                # passed: no black pawn ahead on this/adjacent files
                r=0
                while r<8:
                    if w>>r & 1:
                        ok=True
                        for ff in (fl-1,fl,fl+1):
                            if 0<=ff<8:
                                for rr in range(r+1,8):
                                    if bpf[ff]>>rr & 1: ok=False
                        if ok: mg+=12+8*r; eg+=15+10*r
                    r+=1
            if bl:
                if bl&(bl-1): mg+=8; eg+=8
                adj=(bpf[fl-1] if fl>0 else 0)|(bpf[fl+1] if fl<7 else 0)
                if not adj: mg+=10; eg+=10
                r=0
                while r<8:
                    if bl>>r & 1:
                        ok=True
                        for ff in (fl-1,fl,fl+1):
                            if 0<=ff<8:
                                for rr in range(0,r):
                                    if wpf[ff]>>rr & 1: ok=False
                        if ok: mg-=12+8*(7-r); eg-=15+10*(7-r)
                    r+=1
        sc=(mg*ph+eg*(24-ph))//24
        return sc if s.t>0 else -sc
    def qs(s,a,be,ply):
        s.nd+=1
        if s.nd>=NODES: s.stop=True; return 0
        st=s.ev()
        if st>=be: return be
        if st>a: a=st
        inch=s.att(s.k[0 if s.t>0 else 1], -s.t)
        ms=s.gen(0) if inch else s.gen(1)
        ms.sort(key=lambda m: V[abs(s.b[(m>>7)&127])]*10-V[abs(s.b[m&127])], reverse=True)
        for m in ms:
            if not inch:
                v=s.b[(m>>7)&127]
                if st+V[abs(v)]+200<a: continue
            s.mk(m)
            if s.att(s.k[0 if s.t<0 else 1], s.t):
                s.un(); continue
            v=-s.qs(-be,-a,ply+1)
            s.un()
            if s.stop: return 0
            if v>=be: return be
            if v>a: a=v
        return a
    def ab(s,d,a,be,ply):
        s.nd+=1
        if s.nd>=NODES: s.stop=True; return 0
        if d<=0: return s.qs(a,be,ply)
        inch=s.att(s.k[0 if s.t>0 else 1], -s.t)
        tt=s.tt.get(s.h); ttm=0
        if tt and tt[0]>=d:
            if tt[1]==0: return tt[2]
            if tt[1]==1 and tt[2]>=be: return be
            if tt[1]==2 and tt[2]<=a: return a
            ttm=tt[3]
        if d>=3 and not inch and be<INF-100:
            has=False
            for sq in range(128):
                if sq&0x88: continue
                p=s.b[sq]
                if p and (p>0)==(s.t>0) and abs(p) not in (1,6): has=True; break
            if has:
                oe=s.e; oh=s.h
                s.h^=ZS
                if oe>=0: s.h^=ZE[oe&7]
                s.e=-1; s.t=-s.t
                v=-s.ab(d-3,-be,-be+1,ply+1)
                s.t=-s.t; s.e=oe; s.h=oh
                if s.stop: return 0
                if v>=be: return be
        ms=s.gen(0)
        def os(m):
            if m==ttm: return 1<<28
            v=s.b[(m>>7)&127]
            if v: return (1<<24)+V[abs(v)]*10-V[abs(s.b[m&127])]
            if m==s.kl[ply][0]: return 1<<22
            if m==s.kl[ply][1]: return 1<<21
            return s.hh.get(m,0)
        ms.sort(key=os, reverse=True)
        best=-INF; bm=0; flag=2
        for i,m in enumerate(ms):
            t=(m>>7)&127
            iscap=(s.b[t]!=0) or ((m>>14)&7) or (abs(s.b[m&127])==1 and t==s.e)
            s.mk(m)
            if s.att(s.k[0 if s.t<0 else 1], s.t):
                s.un(); continue
            if d>=3 and i>=3 and not iscap and not inch:
                r=1 if i<8 else 2
                v=-s.ab(d-1-r,-a-1,-a,ply+1)
                if v>a:
                    v=-s.ab(d-1,-a-1,-a,ply+1)
                    if v>a and v<be: v=-s.ab(d-1,-be,-a,ply+1)
            elif i==0:
                v=-s.ab(d-1,-be,-a,ply+1)
            else:
                v=-s.ab(d-1,-a-1,-a,ply+1)
                if v>a and v<be: v=-s.ab(d-1,-be,-a,ply+1)
            s.un()
            if s.stop: return 0
            if v>best: best=v; bm=m
            if v>=be:
                flag=1
                if not iscap:
                    if m!=s.kl[ply][0]:
                        s.kl[ply][1]=s.kl[ply][0]; s.kl[ply][0]=m
                    s.hh[m]=min(s.hh.get(m,0)+d*d,6000)
                break
            if v>a: a=v; flag=0
        if best==-INF:
            return -MATE+ply if inch else 0
        s.tt[s.h]=(d,flag,best,bm)
        return best
    def root(s,legal):
        s.nd=0; s.stop=False; s.tt={}
        best=legal[0]; done=0
        for d in range(1,64):
            s.stop=False
            ms=s.gen(0)
            def os(m):
                if m==best: return 1<<28
                v=s.b[(m>>7)&127]
                if v: return (1<<24)+V[abs(v)]*10-V[abs(s.b[m&127])]
                return s.hh.get(m,0)
            ms.sort(key=os, reverse=True)
            a=-INF; be=INF; cur=best; sc=-INF; ok=True
            for j,m in enumerate(ms):
                s.mk(m)
                if s.att(s.k[0 if s.t<0 else 1], s.t):
                    s.un(); continue
                if j==0:
                    v=-s.ab(d-1,-be,-a,1)
                else:
                    v=-s.ab(d-1,-a-1,-a,1)
                    if v>a and v<be: v=-s.ab(d-1,-be,-a,1)
                s.un()
                if s.stop: ok=False; break
                if v>sc: sc=v; cur=m
                if v>a: a=v
            if not ok: break
            best=cur; done=d
            if sc>=MATE-100: break
        return best
def uci(m):
    f=m&127; t=(m>>7)&127; pr=(m>>14)&7
    s='abcdefgh'[f&7]+str((f>>4)+1)+'abcdefgh'[t&7]+str((t>>4)+1)
    if pr: s+='nbrq'[pr-2]
    return s
def parse_uci(u):
    f=(ord(u[0])-97)+(int(u[1])-1)*16
    t=(ord(u[2])-97)+(int(u[3])-1)*16
    pr=0
    if len(u)>4: pr={'n':2,'b':3,'r':4,'q':5}[u[4]]
    return f|(t<<7)|(pr<<14)
URL=os.environ['MAKEFUN_ENV_URL']
def call(p,o):
    q=urllib.request.Request(URL+p, data=json.dumps(o).encode(), headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(q) as r: return json.load(r)
def main():
    e=E()
    while True:
        g=call('/game',{})
        if g.get('status')=='done': break
        while g.get('status')=='your_move':
            e.fen(g['fen'])
            legal=[parse_uci(u) for u in g['legal_moves']]
            m=e.root(legal)
            if m not in legal: m=legal[0]
            g=call('/move',{'game':g['game'],'move':uci(m)})
if __name__=='__main__': main()
