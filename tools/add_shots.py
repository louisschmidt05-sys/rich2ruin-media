"""Add extra shots to v3 specs so a new visual appears every ~1.5 s and no source repeats.
Usage: python3 tools/add_shots.py plan.json
plan.json: {"<spec id>": {"<line index>": ["images/<reel>/file.jpg" | "images/<reel>/pixabay_123.mp4", ...]}}
- Duplicate sources inside a spec are replaced first by the planned assets of the same line (when any).
- Extra assets are inserted after the line's existing shots (stickers stay on the first shots).
- Archive photos get bw + grain; credits are built from the file name (Commons) or "Footage: Pixabay"."""
import json, os, re, sys


def credit_for(path):
    f = os.path.basename(path)
    if f.startswith("pixabay_"):
        return "Footage: Pixabay"
    name = os.path.splitext(f)[0]
    name = re.sub(r"\bLCCN\w*", "", name)
    name = re.sub(r"\(\d{6,}\)", "", name)
    name = re.sub(r"[_]+", " ", name)
    name = re.sub(r"\s+", " ", name).strip(" -.,")
    if len(name) > 60:
        name = name[:57].rsplit(" ", 1)[0] + "…"
    return name + " · public domain"


def shot(path, archive=True):
    d = {"type": "full", "credit": credit_for(path)}
    if path.endswith(".mp4"):
        d["clip"] = path
    else:
        d["img"] = path
        if archive:
            d["bw"], d["grain"] = True, True
    return d


def src(sh):
    return sh.get("clip") or sh.get("img") or sh.get("bg")


def apply(spec_id, plan):
    p = f"specs/{spec_id}.json"
    s = json.load(open(p))
    # last lines first, so a repeated source is replaced in its later occurrence
    for li, assets in sorted(plan.items(), key=lambda kv: -int(kv[0])):
        ln = s["lines"][int(li)]
        for a in assets:
            assert os.path.exists(a), a
        ln.setdefault("shots", [])
        pending = list(assets)
        # replace repeated sources in this line
        used_elsewhere = [src(sh) for j, l in enumerate(s["lines"]) if j != int(li) for sh in l.get("shots", [])]
        seen = set()
        for k, sh in enumerate(ln["shots"]):
            if sh.get("type") == "full" and (src(sh) in used_elsewhere or src(sh) in seen) and pending:
                a = pending.pop(0)
                new = shot(a)
                for key in ("overlay", "dim", "flash", "cy", "cx"):
                    if key in sh:
                        new[key] = sh[key]
                ln["shots"][k] = new
            seen.add(src(ln["shots"][k]))
        ln["shots"] += [shot(a) for a in pending]
    json.dump(s, open(p, "w"), indent=1, ensure_ascii=False)
    used = [src(sh) for l in s["lines"] for sh in l.get("shots", []) if src(sh)]
    dup = sorted({u for u in used if used.count(u) > 1})
    print(spec_id, "shots", len(used), "repeats", dup)


if __name__ == "__main__":
    plan = json.load(open(sys.argv[1]))
    for sid, pl in plan.items():
        apply(sid, pl)
