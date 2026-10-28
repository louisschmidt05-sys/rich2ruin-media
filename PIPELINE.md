# Rich 2 Ruin — weekly production runbook

Read this file and `EDITORIAL.md` fully before doing anything. The owner asked for full autonomy:
produce and schedule without asking for approval. Stop and report only on the blockers listed at the end.

## 0. Setup (every fresh session)
```bash
bash scripts/setup.sh          # deps + Kokoro voice model into ~/.cache/rich2ruin
```
ffmpeg must exist. Fonts are in `engine/fonts`.

## 1. Pick this week's 3 topics
- Open `topics.json`. Take the first 3 entries with `"status": "backlog"`, keeping the format mix
  (never 3 of the same format in one week if avoidable).
- Skip any topic that breaks the rules in `EDITORIAL.md` (mark it `"status": "rejected"` with a reason).
- If fewer than 6 backlog topics remain, add new ones (verified real events) to keep the queue ≥ 10.

## 2. Research and write each script
- Verify every number, date and name on at least one solid source (Wikipedia article + its citations is the minimum).
  Use WebFetch on en.wikipedia.org. If a figure is disputed, either drop it or say "around"/"estimated".
- Write the spec in `specs/<NN>_<slug>.json` copying the structure of existing specs:
  10 narration lines + outro, 35–48 s, hook in the first line, one `big` + `drop` line (the crash moment),
  one `twist` line, CTA "Follow Rich to Ruin for the next crash/scam/fall."
- Scene types: year, text, stat, compare, icons, chart, myth, name, news, photo (with `overlay`), outro.
  Charts with invented shapes must set `"illustrative": true`.

## 3. Images (for "archive" style reels)
- Archive style is for stories before ~1930 (public-domain material exists). Modern stories use graphic style.
- Find 6–8 Wikimedia Commons files (WebSearch with allowed_domains commons.wikimedia.org), add them to
  `images.json` under the reel id, commit, push. The `Fetch archive images` workflow downloads them and
  keeps only public domain / CC0 (see `fetch_log.txt`, `credits.json`). Wait for the run to finish
  (`gh api repos/louisschmidt05-sys/rich2ruin-media/actions/runs`), then `git pull`.
- Each image is used once; alternate photo scenes with black graphic scenes. Use `"mode": "fit"` for
  landscape or small images. Put a short credit + " · public domain" on every photo scene.
- If fewer than 5 usable images: make the reel in graphic style instead.

## 4. Render
```bash
python3 engine/engine.py specs/<id>.json voice      # TTS (bm_george, speed 1.06)
python3 engine/engine.py specs/<id>.json stills     # contact sheet -> build/<id>/sheet.png
# LOOK at the sheet (Read the png): text overlaps, unreadable overlays, wrong images -> fix spec
python3 engine/engine.py specs/<id>.json render     # -> reels/<id>.mp4
```
Check: duration 30–55 s, `ffprobe` shows h264 1080x1920 + aac. Pull 3 frames at key moments and look at them.

## 5. Publish
- `git add reels/<id>.mp4 specs/<id>.json`, commit, push. Public URL:
  `https://raw.githubusercontent.com/louisschmidt05-sys/rich2ruin-media/main/reels/<id>.mp4`
- Metricool brand id `7707098` (rich.2ruin), timezone Europe/Paris. Schedule with `createScheduledPost`:
  Mon / Wed / Fri of the following week at 17:43, providers instagram + tiktok + youtube,
  `instagramData.type=REEL`, `isAiGenerated=true`; `tiktokData.isAigc=true` + title;
  `youtubeData` type `short`, title ending `#shorts`, `madeForKids=false`, `isAiGeneratedContent=true`,
  category `EDUCATION`; `videoCoverMilliseconds: 1500`.
- Caption: 1–2 punchy lines, "Follow for history's greatest crashes/scams/falls.", credits line
  ("Artworks/Photos: public domain. AI voiceover."), 5 hashtags. No financial advice, no promotion of
  any financial product.
- Before scheduling, `getScheduledPosts` for the target week so nothing is doubled.

## 6. Learn
- Pull last 2 weeks of Instagram/TikTok/YouTube metrics (`getAnalyticsAvailableMetrics`, then
  `getAnalyticsDataByMetrics`). Append a short dated line to `LEARNINGS.md`: what performed, what to change
  (hook style, format, length). Apply clear lessons to the next scripts.

## 7. Bookkeeping
- Update `topics.json` statuses (`scheduled` + date + reel id) and commit with a clear message.

## Stop and report (do not improvise) when
- Metricool rejects a post or a quota/plan limit is hit.
- A topic needs facts you cannot verify.
- GitHub push/workflow fails twice.
- Any platform warning, strike or copyright claim appears in analytics/notifications.
