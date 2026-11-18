import json
d = json.load(open('vo/dur.json'))
OLD = [0,1.9,3.4,5.6,8.0,9.0,11.0,14.0,16.6,19.0,22.0,25.5]
segs = [('v0',.35,.15),('v1',.1,.3),('v2',.1,.3),('v3',.1,.3),(None,0,0),('v4',.1,.25),('v5',.1,.3),('v6',.1,.3),('v7',.1,.4),('v8',.15,.65),('v9',.5,.8)]
NEW=[0.0]; VO=[]
for v,lead,tail in segs:
    dur = 1.0 if v is None else max(lead + d[v] + tail, 2.6 if v=='v8' else 0)
    if v: VO.append((v, round(NEW[-1]+lead,3)))
    NEW.append(round(NEW[-1]+dur,3))
json.dump({'old':OLD,'new':NEW,'vo':VO}, open('timeline.json','w'), indent=1)
open('timeline.js','w').write(f"const TL_OLD={OLD},TL_NEW={NEW};\nfunction remap(t){{for(let i=0;i<TL_NEW.length-1;i++){{if(t<TL_NEW[i+1]||i==TL_NEW.length-2){{const k=(t-TL_NEW[i])/(TL_NEW[i+1]-TL_NEW[i]);return TL_OLD[i]+k*(TL_OLD[i+1]-TL_OLD[i])}}}}}}\n")
print(NEW); print(VO)
