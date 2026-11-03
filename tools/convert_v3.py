"""Convert an old (v1) spec into a v3 spec: same verified narration, full-bleed media + stickers + boards.
usage: python3 tools/convert_v3.py <old_id> <new_id> <archive:0|1> [pixabay ids in preferred order...]"""
import json, sys, os, glob
old_id, new_id, archive = sys.argv[1], sys.argv[2], sys.argv[3] == "1"
order = sys.argv[4:]
o = json.load(open(f"specs/{old_id}.json"))
reel_dir = None
photos = []
for l in o["lines"]:
    sc = l["scene"]
    if sc.get("img"):
        photos.append((sc["img"], sc.get("credit", "")))
        reel_dir = sc["img"].split("/")[1]
reel_dir = reel_dir or os.environ.get("REEL_DIR")
clips = [f"images/{reel_dir}/pixabay_{i}.mp4" for i in order if os.path.exists(f"images/{reel_dir}/pixabay_{i}.mp4")]
# media pool: photos (each once) interleaved with clips
pool, pi, ci = [], 0, 0
# photos already shown on their own line are never reused elsewhere (a portrait on the wrong sentence misleads)
direct = {l["scene"]["img"] for l in o["lines"] if l["scene"]["type"] == "photo"}
seen_ph = []
for ph in photos:
    if ph[0] not in direct and ph[0] not in [x[0] for x in seen_ph]:
        seen_ph.append(ph)
while pi < len(seen_ph) or ci < len(clips):
    if ci < len(clips):
        pool.append(("clip", clips[ci], "Footage: Pixabay")); ci += 1
    if pi < len(seen_ph):
        pool.append(("img", seen_ph[pi][0], seen_ph[pi][1])); pi += 1
cursor = [0]


def next_media(avoid=None):
    for _ in range(len(pool)):
        m = pool[cursor[0] % len(pool)]
        cursor[0] += 1
        if m[1] != avoid:
            return m
    return pool[0]


def S(text, style="yellow", y=880, at=0.15, size=64):
    return {"text": str(text), "style": style, "y": y, "at": at, "size": size}


COL = {"gold": "yellow", "red": "red", "cream": "white", "green": "yellow", "grey": "white"}


def fmt(sc):
    v = sc["value"]
    return f'{sc.get("prefix", "")}{v:,.{sc.get("dec", 0)}f}{sc.get("suffix", "")}'.strip()


def stickers(sc):
    t = sc["type"]
    if t == "year":
        it = [S(sc["big"], "red" if sc.get("color") == "red" else "yellow", 800, 0.1, 100)]
        if sc.get("sub"): it.append(S(sc["sub"], "white", 940, 0.5, 50))
        return it
    if t == "text":
        return [S(tx, COL.get(c, "white"), 760 + i * 135, 0.1 + 0.3 * i, 70) for i, (tx, c) in enumerate(sc["lines"][:3])]
    if t == "stat":
        it = []
        if sc.get("label"): it.append(S(sc["label"], "white", 760, 0.1, 50))
        it.append(S(fmt(sc), "red" if sc.get("color") == "red" else "yellow", 900, 0.5, 104))
        if sc.get("sub") and len(sc["sub"]) <= 30: it.append(S(sc["sub"], "white", 1030, 0.9, 40))
        return it
    if t == "name":
        it = [S(sc["name"], "white", 800, 0.2, 76)]
        if sc.get("tag") or sc.get("sub"): it.append(S(sc.get("tag") or sc.get("sub"), "yellow", 930, 0.6, 50))
        return it
    if t == "compare":
        return [S(sc["a"], "white", 760, 0.1, 60), S(f'{sc["b1"]} {sc["b2"]}', "yellow", 900, 0.6, 56)]
    if t == "icons":
        it = []
        if sc.get("title"): it.append(S(sc["title"], "white", 780, 0.1, 56))
        if sc.get("badge"): it.append(S(sc["badge"], "yellow", 910, 0.5, 72))
        return it
    return []


def chunks(text, n=20):
    out, cur = [], ""
    for w in text.split():
        if cur and len(cur) + 1 + len(w) > n:
            out.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur: out.append(cur)
    return out


def board(sc, bg):
    t = sc["type"]
    b = {"type": "board", "bg": bg}
    if t == "chart":
        pts = [v for _, v in sc["points"]]
        b.update({"points": pts, "show_from": sc.get("show_from", 0), "show_to": sc.get("show_to", len(pts) - 1),
                  "red_from": sc.get("red_from", 99), "illustrative": sc.get("illustrative", False)})
        labs = {}
        for i in sc.get("tag", []):
            labs[str(i)] = f'{sc.get("prefix", "")}{pts[i]:,.{sc.get("dec", 0)}f}{sc.get("suffix", "")}'
        b["labels"] = labs
        items = []
        if sc.get("title"): items.append(S(sc["title"], "white", 400, 0.0, 50))
        if sc.get("big"): items.append(S(sc["big"], "red", 1080, sc.get("big_at", 1.0), 80))
        b["items"] = items
    elif t == "news":
        items = [S(sc.get("date", ""), "yellow", 640, 0.1, 46)] if sc.get("date") else []
        for i, c in enumerate(chunks(sc["headline"])[:3]):
            items.append(S(c, "white", 790 + i * 125, 0.35 + 0.3 * i, 64))
        b["items"] = items
    elif t == "myth":
        b["items"] = [S(sc.get("kicker", "THE TWIST"), "yellow", 600, 0.0, 56), S(sc["myth"], "white", 760, 0.4, 64),
                      S("MYTH", "red", 880, 1.0, 50), S(sc["reality"], "yellow", 1030, 1.6, 80)]
    return b


def full(m, items, **kw):
    kind, src, cred = m
    d = {"type": "full", ("clip" if kind == "clip" else "img"): src, "credit": cred}
    if archive:
        d.update(bw=True, grain=True)
    if items:
        d["overlay"] = {"type": "stickers", "items": items}
    d.update(kw)
    return d


new = {"id": new_id, "style": "v3", "format": o.get("format"), "lead_in": 0.06, "speed": 1.12, "lines": []}
last = None
for l in o["lines"]:
    sc = l["scene"]
    if sc["type"] == "outro":
        new["lines"].append({"text": l["text"], "scene": {"type": "outro"}})
        continue
    words = len(l["text"].split())
    shots = []
    core = sc.get("overlay") if sc["type"] == "photo" else sc
    core = core or {}
    if sc["type"] == "photo":
        m = ("img", sc["img"], sc.get("credit", ""))
        shots.append(full(m, stickers(core) if core else []))
        last = sc["img"]
    elif core.get("type") in ("chart", "news", "myth"):
        bgm = next((m for m in pool if m[0] == "clip"), None) or next_media(last)
        shots.append(board(core, bgm[1]))
    else:
        m = next_media(last)
        last = m[1]
        shots.append(full(m, stickers(core)))
    if words > 7:
        m = next_media(last)
        last = m[1]
        shots.append(full(m, []))
    nl = {"text": l["text"], "shots": shots}
    for k in ("big", "big_at", "big_sfx", "drop", "twist", "say", "pause"):
        if k in l: nl[k] = l[k]
    new["lines"].append(nl)
json.dump(new, open(f"specs/{new_id}.json", "w"), indent=1, ensure_ascii=False)
print(new_id, len(new["lines"]), "lines, pool", len(pool))
