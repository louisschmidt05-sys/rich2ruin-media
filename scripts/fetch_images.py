"""Download images listed in images.json from Wikimedia Commons, keeping only files
whose Commons licence is public domain or CC0. Writes images/<reel>/<file> and credits.json."""
import json, os, re, sys, time
import requests

API = "https://commons.wikimedia.org/w/api.php"
UA = {"User-Agent": "rich2ruin-media-bot/1.1 (https://github.com/louisschmidt05-sys/rich2ruin-media; educational history reels) python-requests"}
ALLOWED = re.compile(r"(public domain|^pd|cc0)", re.I)

spec = json.load(open("images.json"))
credits = json.load(open("credits.json")) if os.path.exists("credits.json") else {}
ok, skipped = 0, []

for item in spec["images"]:
  try:
    name = item["file"]
    key = f'{item["reel"]}/{name}'
    r = requests.get(API, headers=UA, timeout=30, params={
        "action": "query", "format": "json", "titles": f"File:{name}",
        "prop": "imageinfo", "iiprop": "url|extmetadata", "iiurlwidth": 1600})
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
    url = info.get("thumburl") or info["url"]
    out_dir = os.path.join("images", item["reel"])
    os.makedirs(out_dir, exist_ok=True)
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
