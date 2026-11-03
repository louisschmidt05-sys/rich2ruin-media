import sys; sys.path.insert(0, 'engine')
import engine
for rid in sys.argv[1:]:
    r = engine.Reel(f'specs/{rid}.json'); r._words()
    wins = r.windows(); ts = []
    for i, (a, b) in enumerate(wins):
        n = len(r.spec['lines'][i].get('shots') or [1])
        for j in range(n): ts.append(round(a + (b - a) * (j + 0.75) / n, 2))
    print(rid, round(r.timing['total'], 1), 's', r.stills(ts), flush=True)
