"""Search Wikimedia Commons for files matching queries in media_queries.json and report the ones whose
licence is public domain or CC0. Writes media_search.json (read it, then copy chosen files into images.json).
media_queries.json: {"queries": [{"reel": "...", "q": "wall street 1929", "type": "video"|"image", "max": 15}]}"""
import json, os, re, time, io
import requests

API = "https://commons.wikimedia.org/w/api.php"
UA = {"User-Agent": "rich2ruin-media-bot/1.2 (https://github.com/louisschmidt05-sys/rich2ruin-media) python-requests"}
ALLOWED = re.compile(r"(public domain|^pd|cc0)", re.I)

spec = json.load(open("media_queries.json"))
out = {"results": []}
def search_archive(q):
    """Internet Archive (Prelinger and other collections): keep items whose licenseurl is public domain / CC0."""
    query = f'({q["q"]}) AND mediatype:movies AND (licenseurl:*publicdomain* OR licenseurl:*zero*)'
    # only collections whose public-domain status is curated (Prelinger, US government archives)
    query += f' AND collection:({q.get("collection", "prelinger OR fedflix OR usnationalarchives")})'
    r = requests.get("https://archive.org/advancedsearch.php", headers=UA, timeout=60, params={
        "q": query, "fl[]": ["identifier", "title", "year", "licenseurl", "description", "collection"],
        "rows": q.get("max", 15), "output": "json", "sort[]": "downloads desc"})
    r.raise_for_status()
    rows = []
    for d in r.json()["response"]["docs"]:
        desc = d.get("description", "")
        desc = " ".join(desc) if isinstance(desc, list) else desc
        rows.append({"reel": q["reel"], "q": q["q"], "source": "archive", "file": d["identifier"],
                     "title": d.get("title", "")[:120], "year": d.get("year"), "licence": d.get("licenseurl", ""),
                     "ok": True, "desc": re.sub("<[^>]+>", "", desc)[:220]})
    return rows


def search_pixabay(q):
    """Pixabay videos (free licence, commercial use OK, credit the source). Needs PIXABAY_API_KEY secret."""
    key = os.environ.get("PIXABAY_API_KEY")
    if not key:
        raise RuntimeError("PIXABAY_API_KEY missing")
    r = requests.get("https://pixabay.com/api/videos/", headers=UA, timeout=40, params={
        "key": key, "q": q["q"][:100], "per_page": max(3, min(q.get("max", 12), 50)), "safesearch": "true"})
    r.raise_for_status()
    rows = []
    for h in r.json().get("hits", []):
        v = h["videos"]
        rows.append({"reel": q["reel"], "q": q["q"], "source": "pixabay", "file": str(h["id"]), "ok": True,
                     "licence": "Pixabay Content License", "duration_s": h.get("duration"), "tags": h.get("tags"),
                     "user": h.get("user"), "page": h.get("pageURL"),
                     "w": v["medium"]["width"], "h": v["medium"]["height"],
                     "thumb": v["tiny"].get("thumbnail") or v["small"].get("thumbnail")})
    return rows


def pixabay_sheets(results):
    """One labelled contact sheet per reel with every Pixabay hit, to choose clips by eye."""
    from PIL import Image, ImageDraw
    by = {}
    for x in results:
        if x.get("source") == "pixabay" and x.get("thumb"):
            by.setdefault(x["reel"], []).append(x)
    os.makedirs("previews", exist_ok=True)
    for reel, xs in by.items():
        seen, ims = set(), []
        for x in xs:
            if x["file"] in seen:
                continue
            seen.add(x["file"])
            try:
                im = Image.open(io.BytesIO(requests.get(x["thumb"], headers=UA, timeout=30).content)).convert("RGB")
            except Exception:
                continue
            im.thumbnail((320, 180))
            c = Image.new("RGB", (320, 200), (20, 20, 20))
            c.paste(im, (0, 0))
            ImageDraw.Draw(c).text((4, 182), f'{x["file"]} {x["duration_s"]}s {x["q"][:22]}', fill=(255, 220, 0))
            ims.append(c)
        cols = 5
        sheet = Image.new("RGB", (320 * cols, 200 * (-(-len(ims) // cols))), (0, 0, 0))
        for i, c in enumerate(ims):
            sheet.paste(c, ((i % cols) * 320, (i // cols) * 200))
        sheet.save(f"previews/pixabay_{reel}.jpg", quality=85)


for q in spec["queries"]:
    kind = q.get("type", "video")
    if q.get("source") == "pixabay":
        try:
            out["results"] += search_pixabay(q)
        except Exception as e:
            out["results"].append({"reel": q["reel"], "q": q["q"], "error": str(e)[:200]})
        time.sleep(1)
        continue
    if q.get("source") == "archive":
        try:
            out["results"] += search_archive(q)
        except Exception as e:
            out["results"].append({"reel": q["reel"], "q": q["q"], "error": str(e)[:200]})
        time.sleep(1)
        continue
    srsearch = q["q"] + (" filetype:video" if kind == "video" else " filetype:bitmap")
    try:
        r = requests.get(API, headers=UA, timeout=40, params={
            "action": "query", "format": "json", "generator": "search", "gsrsearch": srsearch,
            "gsrnamespace": 6, "gsrlimit": q.get("max", 15),
            "prop": "imageinfo", "iiprop": "url|size|mime|extmetadata"})
        r.raise_for_status()
        pages = r.json().get("query", {}).get("pages", {})
    except Exception as e:
        out["results"].append({"reel": q["reel"], "q": q["q"], "error": str(e)[:200]})
        continue
    for p in pages.values():
        ii = (p.get("imageinfo") or [{}])[0]
        meta = ii.get("extmetadata", {})
        lic = meta.get("LicenseShortName", {}).get("value", "")
        desc = re.sub("<[^>]+>", "", meta.get("ImageDescription", {}).get("value", ""))[:220]
        date = re.sub("<[^>]+>", "", meta.get("DateTimeOriginal", {}).get("value", ""))[:40]
        out["results"].append({
            "reel": q["reel"], "q": q["q"], "file": p["title"].removeprefix("File:"),
            "licence": lic, "ok": bool(ALLOWED.search(lic)), "mime": ii.get("mime"),
            "mb": round(ii.get("size", 0) / 1e6, 1), "w": ii.get("width"), "h": ii.get("height"),
            "duration_s": round(ii.get("duration", 0) or 0), "date": date, "desc": desc})
    time.sleep(1)

pixabay_sheets(out["results"])
json.dump(out, open("media_search.json", "w"), indent=1, ensure_ascii=False)
print(len(out["results"]), "results;", sum(1 for x in out["results"] if x.get("ok")), "public domain/CC0")
