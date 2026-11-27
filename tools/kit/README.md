# RUWAD content kit (Claude)

Everything needed to keep the RUWAD page (ruwad.academy / FB page 102371038845741) posting daily.

## Rules (from Fawaz)
- Story order: space a day's stories 10 min apart (13:00 question, 13:10 answer, 13:20 CTA). 1-min gaps got published out of order on 19.11.
- Post EVERY day: stories daily + a reel or carousel at least every 2 days; always keep 48h scheduled ahead in Metricool (brand id 7641800, timezone Asia/Jerusalem). APPROVAL RULE (Fawaz, 25.11.2026): prepare everything, but do NOT schedule until Fawaz replies «موافق» on the `[موافقة] محتوى رواد` issue in xcode5877-dotcom/nmd-hub (see AGENTS-RUNBOOK.md there). The 18.11 blanket permission is replaced.
- Goal: grow organic followers in Daburiyya and the surrounding area; exam season (1.11–20.12.2026).
- Style: dark teal brand (#1A433F / #FFD84D / #3EE08A), Lalezar headlines + Rubik, every post with a visual hook. No clichés (no results posts, no testimonials). Never claim "guaranteed" results.
- Voice-overs: synthetic voice ONLY in fusha (edge-tts ar-JO-TaimNeural), and NO word containing ج (the voice says it like Egyptian g). Dialect voices sound wrong — never use them. On-screen text can be Palestinian dialect.
- Content facts must come from the RUWAD platform (repo xcode5877-dotcom/ruwad-os, src/lib/play/...) — real curriculum, real features (diagnosis, plan, dynamic questions, error report, parent portal).
- WhatsApp CTA: 0546111668, keyword «امتحان».

## Files
- posts/: HTML templates rendered with shot.py (playwright). car.html (4:5 carousel), qday.html (question-of-the-day stories 9:16), how.html, story.html. Copy fonts/ next to the HTML.
- reel/: "الامتحان يتكلّم" series (talking exam paper). Edit captions in reel.html, lines in vo/gen.py, then: timeline.py → music.py → mix → render.py video → concat (see previous runs). v9.wav = fusha narrator outro.
- ad/: direct parents ad (no voice).
- Publish media via raw.githubusercontent.com/xcode5877-dotcom/ruwad-media/main/<path>.

## Series so far
Episodes: 1 math g8, 2 English g9 (British voice + Arabic subtitles), 3 Arabic g7. Next ideas: 4 science/physics g8–9, 5 "exams hold an emergency meeting about RUWAD", finale "the exam surrenders".
Episode 4 physics g8 forces (reels/exam-talks-ep4.mp4, files in reel/ep4) → 23.11 19:00.
Stories: question of the day per grade (q-a phys9 speed, q-b phys8 rocket, q-c chem9 H2O, q-d math7 clock angle 4:00 → 22.11, q-e g5 divisible-by-9 digit-sum 2,718 → 23.11, q-f g10 parallel 6Ω‖3Ω=2Ω → 24.11, q-g g4 rounding: smallest number that rounds to 4,700 = 4,650 → 25.11), financial-literacy g9 (fin9). Carousel fact9 «امتحان التحليل حاطط 5 فخاخ» (posts/fact9, template car-fact9.html) → 25.11 19:00. Episode 5 chemistry g9 (reels/exam-talks-ep5.mp4, files in reel/ep5 incl. mix.py = music*0.45 + VO at timeline offsets; render 3 scenes in parallel with ONLY=0/1/2) → 27.11 19:00. Stories q-i g6 science series circuit (one bulb burns → the other goes off; home = parallel) → 27.11. Next ideas: carousel ~29.11; ep6 "emergency meeting". shot.py: use /home/claude/work-style abs path of cwd (fixed copy in run).

## Ads
Account retalbox (act 1430002849233135), campaign "RUWAD | امتحانات | واتساب أهالي". Region ad set paused 18.11; Daburiyya ad set running (25₪/day; raising budget needs a verified advertiser identity on the ad set).

## Log
- 24.11: 26.11 stories q-h (g3 order of operations 6+4×2=14) were scheduled by the 10:23 run, whose GitHub push failed; images recovered from Metricool into stories/qday/q-h1..3.jpg. Next due: reel 27.11 19:00 (ep5) + stories 27.11.
- 25.11: someone else scheduled 2 reels on 25.11 (17:00 math g8 3 mistakes, 21:00 English 3 mistakes). Added 27.11 stories q-i + 27.11 19:00 reel ep5 (chem g9). Next due: stories 28.11 + carousel 29.11 19:00.
- 26.11: prepared (NOT scheduled, waiting for Fawaz approval): stories q-j g7 temperature −3+8=5 → 28.11 13:00/13:10/13:20; stories q-k g2 sun/moon lam (الشّمس) → 29.11 13:00/13:10/13:20; carousel chem10tf «صح ولا غلط؟ 5 جمل عن الذرّة» (g10 chem: A=p+n, Na⁺ lost e⁻, Cl⁻>Cl, Cl-35/37 isotopes, period radius shrinks) → 29.11 19:00. Run had no access to nmd-hub, so no approval issue was opened; approval requested via message to Fawaz.
- 27.11: 26.11 set (q-j 28.11, q-k 29.11 stories) still pending approval; chem10tf carousel DROPPED for 29.11 because the approved December plan (26.11) puts «3 أخطاء» عربي إعراب سابع on Sunday 29.11 and info carousels perform worst. Made reel err3-ar7 (reels/err3-ar7.mp4, 24.5s, music only, frames from tools/kit/posts/err3-ar7.html, music err3-music.py, assembled with zoompan+xfade): يكتبون (النون مش فاعل) / كتبَتْ vs كتبْتُ / زارَنا الطبيبُ (نا مفعول) — content from ruwad-os g5/arabic-guide.ts → 29.11 19:00. Stories q-l g8 net force tug-of-war 70N vs 50N = 20N toward the stronger (qday-g8-tug.html) → 30.11. Approval issue opened in nmd-hub.
