# RUWAD content kit (Claude)

Everything needed to keep the RUWAD page (ruwad.academy / FB page 102371038845741) posting daily.

## Rules (from Fawaz)
- Post EVERY day: stories daily + a reel or carousel at least every 2 days; always keep 48h scheduled ahead in Metricool (brand id 7641800, timezone Asia/Jerusalem). Fawaz gave full permission (18.11.2026) to create and schedule without per-post approval.
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
Stories: question of the day per grade (q-a phys9 speed, q-b phys8 rocket, q-c chem9 H2O, q-d math7 clock angle 4:00 → 22.11), financial-literacy g9 (fin9). Next reel due 23.11 19:00 (ep4 science).

## Ads
Account retalbox (act 1430002849233135), campaign "RUWAD | امتحانات | واتساب أهالي". Region ad set paused 18.11; Daburiyya ad set running (25₪/day; raising budget needs a verified advertiser identity on the ad set).
