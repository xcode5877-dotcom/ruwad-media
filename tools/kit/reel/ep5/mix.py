import numpy as np, wave, json
def rd(p):
    w=wave.open(p); n=w.getnframes(); ch=w.getnchannels(); a=np.frombuffer(w.readframes(n),np.int16).astype(float)/32768
    return a.reshape(-1,ch), w.getframerate()
m,sr=rd('music.wav'); out=m*0.45
for v,t in json.load(open('timeline.json'))['vo']:
    a,s2=rd(f'vo/{v}.wav'); assert s2==sr; a=a[:,0]
    i=int(t*sr); j=min(len(out),i+len(a))
    out[i:j]+= a[:j-i,None]*1.0
out=np.tanh(out/np.abs(out).max()*1.2)*0.85
w=wave.open('mix.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes((out*32767).astype(np.int16).tobytes()); w.close(); print('ok', len(out)/sr)
