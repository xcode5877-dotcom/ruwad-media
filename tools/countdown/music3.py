import numpy as np, wave
SR = 48000; DUR = 19.0; N = int(SR * DUR)
L = np.zeros(N); R = np.zeros(N)
rng = np.random.default_rng(7)
B = 0.5  # 120 bpm

def add(sig, t, gain=1.0, pan=0.0):
    i = int(t * SR); j = min(N, i + len(sig))
    if i >= N: return
    s = sig[:j - i] * gain
    L[i:j] += s * (1 - max(0, pan)); R[i:j] += s * (1 + min(0, pan))

def env(n, a=0.002, d=0.2):
    t = np.arange(n) / SR
    return np.minimum(1, t / a) * np.exp(-t / d)

def kick(big=False):
    n = int(SR * (0.9 if big else 0.45)); t = np.arange(n) / SR
    f = 45 + 110 * np.exp(-t * 30)
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) * np.exp(-t / (0.45 if big else 0.18))
    s += 0.3 * rng.standard_normal(n) * np.exp(-t / 0.004)
    return np.tanh(s * 1.8)

def clap():
    n = int(SR * 0.25); t = np.arange(n) / SR
    s = rng.standard_normal(n)
    e = np.exp(-t / 0.06) + 0.6 * np.exp(-np.maximum(0, t - 0.012) / 0.01) * (t > 0.012)
    s = np.convolve(s, np.ones(6) / 6, 'same') * e
    return s * 0.7

def hat(op=False):
    n = int(SR * (0.18 if op else 0.05)); t = np.arange(n) / SR
    s = np.diff(rng.standard_normal(n + 1)) * np.exp(-t / (0.06 if op else 0.012))
    return s * 0.35

def tick(hi=True):
    n = int(SR * 0.04); t = np.arange(n) / SR
    f = 2600 if hi else 1900
    return np.sin(2 * np.pi * f * t) * np.exp(-t / 0.006) * 0.6

def bass(freq, dur):
    n = int(SR * dur); t = np.arange(n) / SR
    s = np.sin(2 * np.pi * freq * t) + 0.5 * np.sin(2 * np.pi * freq * 2 * t + 0.3) + 0.25 * np.sign(np.sin(2 * np.pi * freq * t)) * 0.4
    e = np.minimum(1, t / 0.005) * np.exp(-t / (dur * 0.7))
    return np.tanh(s * e * 1.4) * 0.55

def riser(dur):
    n = int(SR * dur); t = np.arange(n) / SR
    noise = rng.standard_normal(n)
    # crude rising bandpass via cumulative mixing
    k = (t / dur) ** 2
    hp = noise - np.convolve(noise, np.ones(40) / 40, 'same')
    tone = np.sin(2 * np.pi * np.cumsum(200 + 1600 * k) / SR) * 0.25
    return (hp * 0.5 + tone) * k * 0.8

def boom():
    n = int(SR * 2.2); t = np.arange(n) / SR
    s = np.sin(2 * np.pi * np.cumsum(35 + 40 * np.exp(-t * 4)) / SR) * np.exp(-t / 0.9)
    crash = np.diff(rng.standard_normal(n + 1)) * np.exp(-t / 0.7) * 0.25
    return np.tanh(s * 1.5) * 0.9 + crash

def swoosh(dur=0.35):
    n = int(SR * dur); t = np.arange(n) / SR
    s = rng.standard_normal(n); s = np.convolve(s, np.ones(12) / 12, 'same')
    return s * np.sin(np.pi * t / dur) ** 2 * 1.4

def blip(freq):
    n = int(SR * 0.06); t = np.arange(n) / SR
    return np.sin(2 * np.pi * freq * t) * np.exp(-t / 0.02) * 0.35

def pad(freqs, dur):
    n = int(SR * dur); t = np.arange(n) / SR
    s = sum(np.sin(2 * np.pi * f * t + i) + 0.4 * np.sin(2 * np.pi * f * 1.005 * t) for i, f in enumerate(freqs))
    e = np.minimum(1, t / 0.6) * np.minimum(1, (dur - t) / 0.8)
    return s / len(freqs) * e * 0.22

A1, F1, G1, C2 = 55.0, 43.65, 49.0, 65.41


# 0-3: scroll tension (fast ticks accelerating), low drone
tt=0.0; gap=0.32
while tt<2.2: add(tick(True), tt, 0.6, 0.3); tt+=gap; gap=max(0.08,gap*0.88)
add(bass(A1*0.5*2, 2.9), 0.0, 0.45)
add(riser(1.0), 1.2, 0.9)
add(boom(), 2.2, 0.7); add(clap(), 2.2, 1.0)   # the X
# 3: reframe impact
add(kick(True), 3.0, 1.0); add(boom(), 3.0, 0.6)
for k in range(4):
    t = 3.0 + k * B
    if k: add(kick(), t, 0.8)
    add(tick(False), t + B/2, 0.5)
add(riser(0.5), 4.5, 0.9)
# 5-15.6 groove
add(boom(), 5.0, 0.8); add(kick(True), 5.0, 1.0)
k = 0; t = 5.0
while t < 15.5:
    if k: add(kick(), t, 0.95)
    if k % 2: add(clap(), t, 0.75)
    for h in range(4): add(hat(h == 2), t + h * B / 4, 0.55 if h % 2 else 0.3, 0.5 * (-1) ** h)
    add(bass([A1, A1, F1, G1][(k // 2) % 4], 0.22), t, 0.75)
    add(bass([A1, A1, F1, G1][(k // 2) % 4] * 2, 0.15), t + 0.25, 0.45)
    k += 1; t += B
for tt in [5.6, 7.7, 9.1, 10.9, 12.6, 14.1]:
    add(swoosh(0.3), tt - 0.15, 0.7)
    for j, f in enumerate([880, 1175, 1568]): add(blip(f), tt + j * 0.06, 0.75)
add(riser(0.7), 14.9, 1.0)
# 15.6 CTA
add(boom(), 15.6, 1.0); add(kick(True), 15.6, 1.0)
add(pad([220, 261.6, 329.6], 1.8), 15.6, 1.0); add(pad([174.6, 220, 261.6], 1.8), 17.2, 1.0)
for t in [16.6, 17.6]: add(kick(), t, 0.8)
for t in [16.1, 17.1, 18.1]: add(clap(), t, 0.5)
add(bass(A1, 1.6), 15.6, 0.6); add(bass(F1, 1.8), 17.2, 0.6)

# master: fade out tail, limit, normalize
t = np.arange(N) / SR
fade = np.clip((DUR - t) / 0.9, 0, 1)
mix = np.stack([L, R], 1) * fade[:, None]
mix = np.tanh(mix * 1.2)
mix = mix / np.max(np.abs(mix)) * 0.89
with wave.open('music3.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype('<i2').tobytes())
print('ok')
