import certifi_patch, asyncio, edge_tts, subprocess, json
VOICE="ar-JO-TaimNeural"
LINES=[
 ("v0","أنا امْتِحانُ الكيمْياء، لِلصَّفِّ التّاسِع!","+15%","+0Hz"),
 ("v1","لَمْ يَهْزِمْني طالِبٌ، مُنْذُ قُرون!","+10%","-8Hz"),
 ("v2","أُرْبِكُهُمْ بِالصِّيَغ، وَأُحَيِّرُهُمْ بِمُوازَنَةِ المُعادَلات!","+18%","-4Hz"),
 ("v3","وَأَنْتَظِرُ الخَطَأَ، في قانونِ حِفْظِ الكُتْلَة.","+5%","-14Hz"),
 ("v4","لكِنْ هذا العام، وَصَلَ طُلّابٌ مِنْ رُوّاد!","+15%","+6Hz"),
 ("v5","يُوازِنونَ المُعادَلات، كَأَنَّها لُعْبَة!","+15%","+10Hz"),
 ("v6","وَكُلَّ مَرَّة، أَسْئِلَةٌ لَمْ يَرَوْها مِنْ قَبْل، وَيَحُلّونَها!","+20%","+14Hz"),
 ("v7","وَمُعَلِّمٌ يُتابِعُهُمْ، كُلَّ يَوْم!","+15%","+18Hz"),
 ("v8","كُتْلَتي مَحْفوظَة، لكِنَّ كَرامَتي ضاعَت!!","+5%","+26Hz"),
]
async def main():
    for n,t,r,p in LINES:
        assert 'ج' not in t, n
        await edge_tts.Communicate(t,VOICE,rate=r,pitch=p).save(f"{n}.mp3")
        subprocess.run(["ffmpeg","-v","error","-y","-i",f"{n}.mp3","-af","silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse","-ar","48000","-ac","1",f"{n}.wav"],check=True)
    d={n:float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f"{n}.wav"])) for n in [l[0] for l in LINES]+["v9"]}
    json.dump(d,open("dur.json","w"),indent=1); print(d)
asyncio.run(main())
