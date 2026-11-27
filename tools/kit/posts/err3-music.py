import numpy as np, wave, sys, json
D=json.loads(sys.argv[1]); X=0.35
starts=[];t=0
for i,d in enumerate(D): starts.append(t); t+=d-X
DUR=t+X; SR=48000; N=int(SR*DUR); L=np.zeros(N); rng=np.random.default_rng(7)
def T(d): return np.arange(int(SR*d))/SR
def nf(m): return 440*2**((m-69)/12)
def add(s,t,g=1):
    i=int(t*SR)
    if i>=N: return
    j=min(N,i+len(s)); L[i:j]+=s[:j-i]*g
def kick():
    t=T(.35); f=45+110*np.exp(-t*35); return np.tanh(1.8*np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t/.15))*.8
def hat(): t=T(.05); return np.diff(rng.standard_normal(len(t)+1))*np.exp(-t/.01)*.1
def snap(): t=T(.15); return np.diff(rng.standard_normal(len(t)+1))*np.exp(-t/.035)*.25
def pluck(m,d=.4):
    t=T(d); f=nf(m); s=sum(np.sin(2*np.pi*f*k*t)/k**1.6 for k in range(1,6)); return s*np.exp(-t/(d*.35))*np.minimum(1,t/.002)*.28
def bass(m,d=.3):
    t=T(d); f=nf(m); return np.tanh(2*(np.sin(2*np.pi*f*t)+.4*np.sin(4*np.pi*f*t)))*np.exp(-t/(d*.5))*.35
def whoosh(d=.45):
    t=T(d); n=np.convolve(rng.standard_normal(len(t)),np.ones(30)/30,'same'); return n*np.sin(np.pi*t/d)**2*.9
def hit():
    t=T(.8); return (np.sin(2*np.pi*nf(76)*t)+.5*np.sin(2*np.pi*nf(83)*t))*np.exp(-t/.25)*.25
bpm=100; b=60/bpm; prog=[[57,60,64],[53,57,60],[48,52,55],[55,59,62]]; mel=[69,72,76,72,67,71,74,71]
k=0;tt=0.0
while tt<DUR-0.5:
    bar=int(k/4)%4; beat=k%4
    add(kick(),tt) if beat in (0,2) else add(snap(),tt)
    add(hat(),tt+b/2); add(bass(prog[bar][0]-12),tt)
    add(pluck(prog[bar][beat%3]+12),tt+b/2,.8)
    if k%2==0: add(pluck(mel[(k//2)%8],.6),tt,.6)
    k+=1; tt+=b
for i,s in enumerate(starts):
    if i: add(whoosh(),s-0.25,.6)
    if i in (2,4,6): add(hit(),s+0.1)
L/=np.max(np.abs(L))*1.15
fo=int(SR*1.2); L[-fo:]*=np.linspace(1,0,fo); L[:int(SR*.05)]*=np.linspace(0,1,int(SR*.05))
st=np.stack([L,L],1); w=wave.open('music.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st*32767).astype('<i2').tobytes()); w.close()
print(DUR)
