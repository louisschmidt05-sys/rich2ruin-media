"""Procedural sound effects + music bed, all generated here (no third-party rights)."""
import numpy as np

SR = 44100
_rng = np.random.default_rng(11)


def _env(L, attack, decay):
    x = np.arange(L) / SR
    return np.minimum(1, x / max(attack, 1e-4)) * np.exp(-x / decay)


def _lp(sig, k):
    return np.convolve(sig, np.ones(k) / k, mode="same")


def whoosh(dur=0.45, up=True):
    L = int(dur * SR)
    x = np.arange(L) / SR
    n = _rng.standard_normal(L)
    dark = _lp(n, 40)
    bright = _lp(n, 5) - dark
    f = x / dur if up else 1 - x / dur
    out = dark * (1 - f) * 3 + bright * f * 0.8
    return out * np.sin(np.pi * x / dur) ** 2 * 0.6


def lerp(a, b, t):
    return a + (b - a) * t


def impact(vol=1.0):
    L = int(0.6 * SR)
    x = np.arange(L) / SR
    f = 45 + 110 * np.exp(-x * 28)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(L, 0.001, 0.18)
    click = _rng.standard_normal(L) * _env(L, 0.0005, 0.012) * 0.6
    return (body + click) * vol


def boom(vol=1.0):
    L = int(2.6 * SR)
    x = np.arange(L) / SR
    f = 32 + 70 * np.exp(-x * 7)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x * 1.3)
    rumble = _lp(_rng.standard_normal(L), 30) * np.exp(-x * 2.2) * 2.5
    return (s * 1.1 + rumble) * vol


def crash():
    """Falling 'market crash' tone + noise burst + boom."""
    L = int(1.4 * SR)
    x = np.arange(L) / SR
    f = 900 * np.exp(-x * 2.2) + 60
    tone = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.25 * np.exp(-x * 1.5)
    tone = _lp(tone, 6)
    burst = _rng.standard_normal(L) * np.exp(-x * 5) * 0.35
    out = np.zeros(int(2.6 * SR))
    out[:L] += tone + burst
    out += boom(0.9)[: len(out)]
    return out


def riser(dur=1.3):
    L = int(dur * SR)
    x = np.arange(L) / SR
    n = _rng.standard_normal(L)
    hp = np.diff(np.concatenate([[0], n]))
    tone = np.sin(2 * np.pi * np.cumsum(200 + 900 * (x / dur) ** 2) / SR) * 0.15
    return (hp * 0.35 + tone) * (x / dur) ** 2.2


def ding(vol=0.7):
    L = int(1.2 * SR)
    x = np.arange(L) / SR
    s = (np.sin(2 * np.pi * 1318 * x) + 0.5 * np.sin(2 * np.pi * 2637 * x) + 0.25 * np.sin(2 * np.pi * 3951 * x))
    return s * _env(L, 0.002, 0.35) * 0.35 * vol


def cash():
    """Cash-register style: two quick dings + drawer thud."""
    out = np.zeros(int(1.0 * SR))
    d = ding(0.6)
    out[: len(d)] += d[: len(out)]
    i = int(0.09 * SR)
    out[i:] += ding(0.5)[: len(out) - i]
    return out


def ticks(dur):
    L = int(dur * SR)
    out = np.zeros(L)
    t = 0.0
    gap = 0.075
    while t < dur - 0.02:
        i = int(t * SR)
        c = _rng.standard_normal(int(0.012 * SR)) * _env(int(0.012 * SR), 0.0003, 0.003)
        c = np.diff(np.concatenate([[0], c]))
        out[i:i + len(c)] += c[: L - i] * 0.5
        t += gap
    return out


def paper():
    L = int(0.35 * SR)
    x = np.arange(L) / SR
    n = np.diff(np.concatenate([[0], _rng.standard_normal(L)]))
    return n * np.sin(np.pi * x / 0.35) ** 3 * 0.35


def slam():
    L = int(0.6 * SR)
    return impact(1.0) + ding(0.3)[:L]


LIB = {"whoosh": lambda: whoosh(0.45), "whoosh_down": lambda: whoosh(0.5, up=False), "impact": impact,
       "boom": boom, "crash": crash, "riser": riser, "ding": ding, "cash": cash, "paper": paper, "slam": slam}


def music(total, drop=None, twist=None, accents=()):
    """Pulse bed in D minor: build until `drop`, heartbeat until `twist`, lighter after.
    `accents` = times of big moments: music cuts briefly before and swells after."""
    n = int(total * SR)
    mix = np.zeros(n)
    beat = 60 / 120

    def add(sig, start):
        i = int(start * SR)
        if i >= n or i + len(sig) <= 0:
            return
        j = min(n, i + len(sig))
        mix[max(i, 0):j] += sig[max(0, -i): j - i]

    def kick():
        L = int(0.4 * SR)
        x = np.arange(L) / SR
        f = 50 + 90 * np.exp(-x * 30)
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(L, 0.002, 0.15)

    def hat():
        L = int(0.05 * SR)
        h = np.diff(np.concatenate([[0], _rng.standard_normal(L)]))
        return h * _env(L, 0.0005, 0.012) * 0.22

    def bass(fq, dur):
        L = int(dur * SR)
        x = np.arange(L) / SR
        s = np.sign(np.sin(2 * np.pi * fq * x)) * 0.5 + np.sin(2 * np.pi * fq * x)
        return _lp(s, 40) * _env(L, 0.005, dur * 0.6) * 0.33

    def pad(freqs, dur, vol):
        L = int(dur * SR)
        x = np.arange(L) / SR
        s = sum(np.sin(2 * np.pi * f * x + 0.8 * np.sin(2 * np.pi * 0.25 * x)) for f in freqs)
        fade = np.minimum(1, np.minimum(x / 1.2, (dur - x) / 1.2))
        return s / len(freqs) * np.clip(fade, 0, 1) * vol

    drop = drop if drop is not None else total * 0.55
    twist = twist if twist is not None else min(total - 4, drop + 6)
    prog = [73.42, 73.42, 87.31, 65.41]
    t, b = 0.0, 0
    while t < drop - 0.05:
        k = 0.5 + 0.5 * (t / max(drop, 1))
        add(kick() * 0.9 * k, t)
        if t > 2:
            add(hat() * k, t + beat / 2)
            if t > drop * 0.5:
                add(hat() * k * 0.7, t + beat / 4 * 3)
        add(bass(prog[(b // 4) % 4], beat * 0.9) * k, t)
        t += beat
        b += 1
    add(pad([146.83, 174.61, 220.0], drop, 0.10), 0)
    t = drop + 1.4
    while t < twist - 0.1:
        add(kick() * 0.5, t)
        add(kick() * 0.3, t + 0.22)
        t += beat * 2
    add(pad([73.42, 110.0, 138.59], max(1.5, twist - drop), 0.09), drop + 0.4)
    t = twist
    b = 0
    while t < total - 1.0:
        add(kick() * 0.65, t)
        add(hat() * 0.8, t + beat / 2)
        add(bass([73.42, 87.31, 98.0, 87.31][(b // 4) % 4], beat * 0.8) * 0.6, t)
        t += beat
        b += 1
    add(pad([146.83, 185.0, 220.0, 293.66], max(1.5, total - twist), 0.09), twist)

    gain = np.ones(n)
    for a in accents:
        # brief cut right before the hit, then a swell
        i0, i1 = int((a - 0.28) * SR), int(a * SR)
        if i0 > 0 and i1 < n:
            gain[i0:i1] = np.linspace(1, 0.15, i1 - i0)
            j1 = min(n, i1 + int(1.6 * SR))
            gain[i1:j1] = np.linspace(1.6, 1.0, j1 - i1)
    mix *= gain
    fo = int(1.2 * SR)
    mix[-fo:] *= np.linspace(1, 0, fo)
    mix[: int(0.3 * SR)] *= np.linspace(0, 1, int(0.3 * SR))
    return mix / (np.abs(mix).max() + 1e-9) * 0.95
