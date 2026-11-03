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

def archive_source(identifier):
    """Best MP4 download URL of an Internet Archive item (trusted collections only)."""
    m = requests.get(f"https://archive.org/metadata/{identifier}", headers=UA, timeout=60).json()
    cols = m.get("metadata", {}).get("collection", [])
    cols = [cols] if isinstance(cols, str) else cols
    if not set(cols) & {"prelinger", "fedflix", "usnationalarchives"}:
        raise ValueError(f"collection not trusted: {cols}")
    lic = m.get("metadata", {}).get("licenseurl", "")
    files = [f for f in m.get("files", []) if f.get("name", "").lower().endswith((".mp4", ".mpeg", ".mpg", ".ogv"))]
    if not files:
        raise ValueError("no video file")
    pref = sorted(files, key=lambda f: (0 if "h.264" in f.get("format", "").lower() else 1 if "mpeg4" in f.get("format", "").lower() else 2,
                                        int(f.get("size", 1 << 40))))
    f = pref[0]
    title = m.get("metadata", {}).get("title", identifier)
    year = m.get("metadata", {}).get("year") or m.get("metadata", {}).get("date", "")[:4]
    return f"https://archive.org/download/{identifier}/{f['name']}", lic, title, year


def download(url, path):
    with requests.get(url, headers=UA, timeout=600, stream=True) as v:
        v.raise_for_status()
        with open(path, "wb") as fh:
            for chunk in v.iter_content(1 << 20):
                fh.write(chunk)


def preview_sheet(src, out):
    """Contact sheet: one thumbnail every N seconds, 6 per row, row-major, to pick clip start times."""
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src],
                               capture_output=True, text=True).stdout.strip() or 0)
    step = max(5, int(dur / 120) + 1)
    rows = max(1, -(-int(dur / step) // 6))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-vf",
                    f"fps=1/{step},scale=240:-2,tile=6x{rows}", "-frames:v", "1", "-q:v", "4", out], check=True)
    return step, round(dur)


for item in spec["images"]:
  if item.get("source") == "pixabay":
    try:
        vid = str(item["file"])
        out_dir = os.path.join("images", item["reel"])
        os.makedirs(out_dir, exist_ok=True)
        out = os.path.join(out_dir, f"pixabay_{vid}.mp4")
        if not os.path.exists(out):
            r = requests.get("https://pixabay.com/api/videos/", headers=UA, timeout=40,
                             params={"key": os.environ["PIXABAY_API_KEY"], "id": vid})
            r.raise_for_status()
            h = r.json()["hits"][0]
            src = h["videos"]["medium"]["url"] or h["videos"]["small"]["url"]
            download(src, "/tmp/pb_src")
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(item.get("start", 0)), "-i", "/tmp/pb_src",
                            "-t", str(item.get("dur", 8)), "-an", "-vf", "scale=-2:'min(1080,ih)',fps=30",
                            "-c:v", "libx264", "-preset", "veryfast", "-crf", "22", "-pix_fmt", "yuv420p", out], check=True)
            os.remove("/tmp/pb_src")
            credits[f'{item["reel"]}/pixabay_{vid}.mp4'] = {"path": out, "licence": "Pixabay Content License",
                "author": h.get("user", ""), "source": h.get("pageURL", ""), "use": item.get("use", "")}
        ok += 1
    except Exception as e:
        skipped.append((item["file"], f"error: {type(e).__name__}: {e}"[:300]))
    continue
  if item.get("source") == "archive":
    try:
        ident = item["file"]
        url, lic, title, year = archive_source(ident)
        tmp = f"/tmp/ia_{ident}"
        if item.get("preview"):
            os.makedirs("previews", exist_ok=True)
            out = f"previews/{ident}.jpg"
            if not os.path.exists(out):
                download(url, tmp)
                step, dur = preview_sheet(tmp, out)
                open(f"previews/{ident}.txt", "w").write(f"step={step}s duration={dur}s cols=6 title={title} year={year}\n")
        else:
            out_dir = os.path.join("images", item["reel"])
            os.makedirs(out_dir, exist_ok=True)
            out = os.path.join(out_dir, f"{ident}_{int(item.get('start', 0))}.mp4")
            if not os.path.exists(out):
                if not os.path.exists(tmp):
                    download(url, tmp)
                subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(item.get("start", 0)), "-i", tmp,
                                "-t", str(item.get("dur", 8)), "-an", "-vf", "scale=-2:'min(720,ih)',fps=30",
                                "-c:v", "libx264", "-preset", "veryfast", "-crf", "22", "-pix_fmt", "yuv420p", out], check=True)
            credits[f'{item["reel"]}/{os.path.basename(out)}'] = {
                "path": out, "licence": lic or "Public domain (Prelinger/US gov archive)", "author": title,
                "year": year, "source": f"https://archive.org/details/{ident}", "use": item.get("use", "")}
        if item.get("preview") and os.path.exists(tmp):
            os.remove(tmp)
        ok += 1
    except Exception as e:
        skipped.append((item["file"], f"error: {type(e).__name__}: {e}"[:300]))
    continue
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
