"""Download images listed in images.json from Wikimedia Commons, keeping only files
whose Commons licence is public domain or CC0. Writes images/<reel>/<file> and credits.json."""
import json, os, re, subprocess, sys, time
import requests

API = "https://commons.wikimedia.org/w/api.php"
UA = {"User-Agent": "rich2ruin-media-bot/1.1 (https://github.com/louisschmidt05-sys/rich2ruin-media; educational history reels) python-requests"}
ALLOWED = re.compile(r"(public domain|^pd|cc0)", re.I)



def pick_video_source(name):
    """Smallest-reasonable transcode (<=720p) from Commons derivatives, else None."""
    try:
        r = requests.get(API, headers=UA, timeout=30, params={
            "action": "query", "format": "json", "titles": f"File:{name}",
            "prop": "videoinfo", "viprop": "derivatives"})
        page = next(iter(r.json()["query"]["pages"].values()))
        ders = page["videoinfo"][0].get("derivatives", [])
        ders = [d for d in ders if d.get("height") and d["height"] <= 720 and "src" in d]
        if not ders:
            return None
        return max(ders, key=lambda d: d["height"])["src"]
    except Exception:
        return None


spec = json.load(open("images.json"))
credits = json.load(open("credits.json")) if os.path.exists("credits.json") else {}
ok, skipped = 0, []

for item in spec["images"]:
  try:
    name = item["file"]
    key = f'{item["reel"]}/{name}'
    r = requests.get(API, headers=UA, timeout=30, params={
        "action": "query", "format": "json", "titles": f"File:{name}",
        "prop": "imageinfo", "iiprop": "url|extmetadata", "iiurlwidth": 2400})
    r.raise_for_status()
    pages = r.json()["query"]["pages"]
    page = next(iter(pages.values()))
    if "imageinfo" not in page:
        skipped.append((name, "not found on Commons"))
        continue
    info = page["imageinfo"][0]
    meta = info.get("extmetadata", {})
    lic = meta.get("LicenseShortName", {}).get("value", "")
    if not ALLOWED.search(lic):
        skipped.append((name, f"licence not public domain: {lic}"))
        continue
    is_video = name.lower().endswith((".webm", ".ogv", ".mpg", ".mpeg", ".mp4"))
    out_dir = os.path.join("images", item["reel"])
    os.makedirs(out_dir, exist_ok=True)
    if is_video:
        out = os.path.join(out_dir, os.path.splitext(name)[0][:80] + ".mp4")
        if not os.path.exists(out):
            src = pick_video_source(name) or info["url"]
            tmp = "/tmp/clip_src"
            with requests.get(src, headers=UA, timeout=300, stream=True) as v:
                v.raise_for_status()
                with open(tmp, "wb") as fh:
                    for chunk in v.iter_content(1 << 20):
                        fh.write(chunk)
            ss, dur = str(item.get("start", 0)), str(item.get("dur", 90))
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", ss, "-i", tmp, "-t", dur, "-an",
                            "-vf", "scale=-2:'min(720,ih)',fps=30", "-c:v", "libx264", "-preset", "veryfast",
                            "-crf", "24", "-pix_fmt", "yuv420p", out], check=True)
            os.remove(tmp)
            time.sleep(1)
    else:
        url = info.get("thumburl") or info["url"]
        ext = os.path.splitext(url.split("?")[0])[1].lower() or ".jpg"
        out = os.path.join(out_dir, os.path.splitext(name)[0][:80] + ext)
        if not os.path.exists(out):
            img = requests.get(url, headers=UA, timeout=60)
            img.raise_for_status()
            open(out, "wb").write(img.content)
            time.sleep(1)
    credits[key] = {
        "path": out, "licence": lic,
        "author": re.sub("<[^>]+>", "", meta.get("Artist", {}).get("value", "")).strip(),
        "source": info.get("descriptionurl"), "use": item.get("use", "")}
    ok += 1
  except Exception as e:
    skipped.append((item["file"], f"error: {type(e).__name__}: {e}"[:300]))

json.dump(credits, open("credits.json", "w"), indent=1, ensure_ascii=False)
report = [f"kept {ok} images"] + [f"SKIPPED {n} -> {why}" for n, why in skipped]
print("\n".join(report))
open("fetch_log.txt", "w").write("\n".join(report) + "\n")
