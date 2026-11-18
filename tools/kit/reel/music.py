import numpy as np, wave
import json
TL=json.load(open('timeline.json'))
def remap(t):
    O,Nw=TL['old'],TL['new']
    for i in range(len(O)-1):
        if t<O[i+1] or i==len(O)-2:
            return Nw[i]+(t-O[i])/(O[i+1]-O[i])*(Nw[i+1]-Nw[i])
SR = 48000; DUR = TL['new'][-1]; N = int(SR * DUR)
L = np.zeros(N); R = np.zeros(N)
rng = np.random.default_rng(11)

def add(sig, t, gain=1.0, pan=0.0):
    i = int(remap(t) * SR)
    if i >= N or i < 0: return
    j = min(N, i + len(sig)); s = sig[:j - i] * gain
    L[i:j] += s * (1 - max(0, pan)); R[i:j] += s * (1 + min(0, pan))

def T(d): return np.arange(int(SR * d)) / SR
def nf(m): return 440 * 2 ** ((m - 69) / 12)

def pluck(m, d=0.35, bright=1.0):
    t = T(d); f = nf(m)
    s = sum(np.sin(2*np.pi*f*k*t) / k**(1.6/bright) for k in range(1, 6))
    return s * np.exp(-t / (d*0.35)) * np.minimum(1, t/0.002) * 0.35

def bass(m, d=0.22):
    t = T(d); f = nf(m)
    s = np.tanh(2.2*(np.sin(2*np.pi*f*t) + 0.4*np.sin(2*np.pi*2*f*t)))
    return s * np.exp(-t / (d*0.5)) * np.minimum(1, t/0.004) * 0.5

def kick():
    t = T(0.4); f = 45 + 120*np.exp(-t*35)
    return np.tanh(1.8*np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-t/0.16)) * 0.9

def snap():
    t = T(0.15); s = np.diff(rng.standard_normal(len(t)+1))
    return s * np.exp(-t/0.03) * 0.28

def hat():
    t = T(0.05); return np.diff(rng.standard_normal(len(t)+1)) * np.exp(-t/0.01) * 0.12

def knock():
    t = T(0.18)
    s = np.sin(2*np.pi*190*t)*np.exp(-t/0.035) + 0.5*np.sin(2*np.pi*410*t)*np.exp(-t/0.02)
    s += np.convolve(rng.standard_normal(len(t)), np.ones(20)/20, 'same') * np.exp(-t/0.01) * 2
    return np.tanh(s*2) * 0.9

def whoosh(d, up=True):
    t = T(d); n = rng.standard_normal(len(t))
    k = np.sin(np.pi * t / d) ** 2
    hp = n - np.convolve(n, np.ones(30)/30, 'same')
    return hp * k * 0.35

def thud():
    t = T(0.5); f = 60 + 60*np.exp(-t*20)
    return np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-t/0.15) * 0.9

def stamp():
    return np.concatenate([kick()[:int(SR*0.2)]*0.7]) + 0 if False else (kick()*0.6 + np.pad(snap()*2, (0, len(kick())-len(snap()))))

def ding(m, d=1.2):
    t = T(d); f = nf(m)
    s = np.sin(2*np.pi*f*t) + 0.5*np.sin(2*np.pi*2.76*f*t)*np.exp(-t/0.15) + 0.3*np.sin(2*np.pi*5.4*f*t)*np.exp(-t/0.08)
    return s * np.exp(-t/0.45) * 0.3

def tick():
    t = T(0.03); return np.sin(2*np.pi*2400*t)*np.exp(-t/0.005)*0.35

def riser(d):
    t = T(d); k = (t/d)**2
    tone = np.sin(2*np.pi*np.cumsum(150 + 900*k)/SR) * 0.2
    n = rng.standard_normal(len(t)); hp = n - np.convolve(n, np.ones(20)/20, 'same')
    return (tone + hp*0.25) * k

def trombone(m, d, vib=False, slide=0):
    t = T(d); f = nf(m) * (1 + slide*(t/d))
    if vib: f = f * (1 + 0.03*np.sin(2*np.pi*6*t) * np.minimum(1, t/0.3))
    ph = 2*np.pi*np.cumsum(f)/SR
    s = sum(np.sin(k*ph) / k for k in range(1, 9))
    e = np.minimum(1, t/0.05) * np.minimum(1, (d-t)/0.12)
    return np.tanh(s*1.3) * e * 0.28

def boom():
    t = T(1.8); f = 38 + 50*np.exp(-t*5)
    s = np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-t/0.7)
    s += np.diff(rng.standard_normal(len(t)+1)) * np.exp(-t/0.5) * 0.2
    return s * 0.9

# ---------- 0 - 3.4 : drop + quirky pluck
add(whoosh(0.7), 0.0, 1.2)
add(thud(), 0.68, 1.0)
B = 0.3  # 100bpm-ish 8ths
mel = [72, 76, 79, 76, 74, 71, 72, -1, 72, 76, 79, 81, 79, -1]
for i, m in enumerate(mel):
    if m > 0: add(pluck(m), 0.8 + i*B*0.62, 0.9, pan=0.2 if i % 2 else -0.2)
add(ding(84, 0.6), 1.9, 0.8); add(ding(91, 0.5), 1.97, 0.5)  # gasp stinger
for i in range(8): add(pluck(60 if i % 2 == 0 else 55, 0.25), 1.95 + i*0.18, 0.6)

# ---------- 3.4 - 8.0 : villain groove (minor, 120bpm)
b = 0.25
line = [45, 45, 48, 45, 50, 49, 48, 44]
t0 = 3.4
k = 0
while t0 + k*b < 7.95:
    tt = t0 + k*b
    add(bass(line[k % 8] - 12, 0.22), tt, 0.9)
    if k % 4 == 0: add(kick(), tt, 0.8)
    if k % 4 == 2: add(snap(), tt, 1.0)
    add(hat(), tt + b/2, 0.8)
    if k % 8 in (0, 3, 6): add(pluck(line[k % 8] + 12, 0.2, 1.5), tt, 0.5)
    k += 1
for s in [3.9, 4.4, 5.0, 5.7, 6.3]: add(stamp(), s, 0.8)

# ---------- 8.0 knocks, silence
add(knock(), 8.0, 1.0); add(knock(), 8.18, 0.8)
add(knock(), 8.6, 1.0); add(knock(), 8.78, 0.9)
# ---------- 9.0 - 14 : suspense
add(whoosh(0.5), 9.05, 1.0)
add(ding(76, 1.5), 9.5, 0.6)
for i in range(int((14.0-9.2)/0.5)):
    add(tick(), 9.2 + i*0.5, 0.9)
    add(bass(33, 0.45), 9.2 + i*1.0, 0.5) if i % 2 == 0 else None
add(riser(2.4), 11.6, 0.9)
add(ding(79, 0.8), 11.6, 0.4)
# ---------- 14 - 19 : tense fast pulse + checks
b = 0.2
for k in range(int(5.0/b)):
    tt = 14.0 + k*b
    add(bass(38 if (k//8) % 2 == 0 else 37, 0.15), tt, 0.7)
    if k % 2 == 0: add(kick(), tt, 0.5)
    add(hat(), tt + b/2, 0.9)
for i, s in enumerate([14.4, 15.4, 16.4]): add(ding(84 + i*2, 0.9), s, 0.9)
add(ding(91, 1.4), 17.6, 1.0); add(ding(88, 1.4), 17.62, 0.6)
add(riser(1.0), 18.0, 0.7)
# ---------- 19 - 22 : sad trombone
add(trombone(55, 0.55), 19.05, 1.0)
add(trombone(54, 0.55), 19.65, 1.0)
add(trombone(53, 0.55), 20.25, 1.0)
add(trombone(52, 1.4, vib=True, slide=-0.03), 20.85, 1.0)
# ---------- 22 - 25.5 : boom + bright outro
add(whoosh(0.4), 21.75, 1.3)
add(boom(), 22.05, 0.9)
add(ding(84, 1.6), 22.25, 0.8); add(ding(91, 1.6), 22.27, 0.5)
b = 0.25
chords = [[60, 64, 67, 72], [65, 69, 72, 77], [67, 71, 74, 79], [65, 69, 72, 77]]
for k in range(int(3.2/b)):
    tt = 22.3 + k*b
    c = chords[(k//4) % 4]
    add(pluck(c[k % 4] + 12, 0.3, 1.4), tt, 0.6, pan=0.3 if k % 2 else -0.3)
    if k % 4 == 0: add(kick(), tt, 0.6); add(bass(c[0]-24, 0.3), tt, 0.7)
    if k % 4 == 2: add(snap(), tt, 0.9)
    add(hat(), tt + b/2, 0.7)
add(ding(79, 1.2), 23.7, 0.6)  # WA

# master
fade = np.ones(N); fl = int(SR*0.6); fade[-fl:] = np.linspace(1, 0, fl)
L *= fade; R *= fade
peak = max(np.abs(L).max(), np.abs(R).max())
L = np.tanh(L / peak * 1.3) * 0.7; R = np.tanh(R / peak * 1.3) * 0.7
st = (np.stack([L, R], 1) * 32767).astype(np.int16)
with wave.open('music.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())
print('ok')
