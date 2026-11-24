"""Audit visual variety: seconds per shot and repeated sources per reel (needs build/<id>/timing.json)."""
import json, os, sys, collections
def src(sh):
    return sh.get("clip") or sh.get("img") or sh.get("bg")
def audit(i):
    s = json.load(open(f"specs/{i}.json"))
    tp = f"build/{i}/timing.json"
    tm = json.load(open(tp))["lines"] if os.path.exists(tp) else None
    used = collections.Counter(src(sh) for l in s["lines"] for sh in l.get("shots", []) if src(sh))
    rep = {k: v for k, v in used.items() if v > 1}
    worst = []
    for n, l in enumerate(s["lines"]):
        if "shots" not in l or not tm: continue
        a = tm[n]["start"]; b = tm[n + 1]["start"] if n + 1 < len(tm) else tm[n]["end"]
        worst.append(round((b - a) / len(l["shots"]), 1))
    folder = os.path.dirname(next(iter(used))) if used else ""
    pool = [os.path.join(folder, f) for f in sorted(os.listdir(folder))] if folder and os.path.isdir(folder) else []
    unused = [p for p in pool if p not in used and not p.endswith((".txt", ".json"))]
    return dict(id=i, shots=sum(len(l.get("shots", [])) for l in s["lines"]), unique=len(used), repeats=len(rep), sec_per_shot=worst, unused=len(unused))
if __name__ == "__main__":
    for i in sys.argv[1:]:
        print(audit(i))
