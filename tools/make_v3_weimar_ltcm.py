"""v3 specs: Weimar hyperinflation (1923) and Long-Term Capital Management (1998). Facts checked 2026-11-07
(Wikipedia + mises.org for Weimar; Wikipedia + WSJ 16 Nov 1998 reprint for LTCM)."""
import json, sys
sys.path.insert(0, "tools")


def full(src, credit=None, items=None, **kw):
    d = {"type": "full", ("clip" if src.endswith(".mp4") else "img"): src}
    if credit: d["credit"] = credit
    if items: d["overlay"] = {"type": "stickers", "items": items}
    d.update(kw); return d
def S(text, style="yellow", y=880, at=0.15, size=64, x=540):
    return {"text": text, "style": style, "y": y, "at": at, "size": size, "x": x}
def L(text, shots, **kw): return {"text": text, "shots": shots, **kw}

PB = "Footage: Pixabay"
arch = dict(bw=True, grain=True)

# ---------------- Weimar 1923 ----------------
I = "images/14_weimar/"
RB = "Reichsbank note · public domain"
sw = {"id": "14_weimar_v3", "style": "v3", "format": "THE CRASH", "lead_in": 0.06, "speed": 1.12, "lines": [
 L("A loaf of bread for 200 billion marks. Berlin, 1923.", [
   full(I + "pixabay_63066.mp4", PB, [S("1 LOAF OF BREAD", "white", 760, 0.1, 62), S("200,000,000,000 MARKS", "yellow", 900, 0.5, 66)], **arch),
   full(I + "note_100_trillion.jpg", "100 trillion mark note, 1924 · " + RB, [S("BERLIN · 1923", "red", 1000, 0.1, 64)], zoom=[1.0, 1.06], dim=0.0)],
   hl=["200 billion"], sfx=[["slam", 0.05], ["whoosh", 2.0]],
   say="A loaf of bread for two hundred billion marks. Berlin, 1923."),
 L("A year earlier: about 160.", [
   full(I + "pixabay_14239.mp4", PB, [S("END OF 1922", "white", 760, 0.1, 60), S("≈ 160 MARKS", "yellow", 900, 0.5, 90)], **arch)],
   hl=["160."], sfx=[["whoosh", 0], ["cash", 1.0]]),
 L("Before the war, one dollar bought 4.2 marks.", [
   full(I + "note_100000.jpg", "100,000 mark note, 1923 · " + RB, [S("1914", "white", 960, 0.1, 60), S("$1 = 4.2 MARKS", "yellow", 1090, 0.4, 76)], dim=0.0, zoom=[1.0, 1.05])],
   hl=["4.2"]),
 L("Then France and Belgium occupy the Ruhr.", [
   full(I + "French enter Essen.jpg", "French troops enter Essen, 1923 · public domain", [S("JANUARY 1923", "yellow", 780, 0.1, 62), S("THE RUHR IS OCCUPIED", "red", 910, 0.5, 62)], **arch),
   full(I + "Ruhr01181923.png", "Map of the occupied Ruhr, 1923 · public domain", cx=0.5, dim=0.45, zoom=[1.0, 1.12], **arch)],
   hl=["ruhr."], sfx=[["slam", 0.05]]),
 L("Workers strike. The state pays them with printed money.", [
   full(I + "Protest meeting Berlin 1923.jpg", "Protest meeting, Berlin, 1923 · public domain", [S("PASSIVE RESISTANCE", "white", 860, 0.1, 62)], **arch),
   {"type": "board", "bg": I + "pixabay_152728.mp4", "items": [
     S("RUHR WORKERS STRIKE", "white", 640, 0.05, 56), S("↓", "yellow", 760, 0.3, 64),
     S("STATE PAYS THEM", "white", 880, 0.45, 56), S("↓", "yellow", 1000, 0.65, 64), S("PRINT MORE MARKS", "red", 1120, 0.8, 60)]}],
   hl=["printed"]),
 L("Millions. Then billions. Then trillions.", [
   full(I + "note_10_million.jpg", "10 million mark note, 1923 · " + RB, [S("10 MILLION", "white", 980, 0.1, 76)], dim=0.0, zoom=[1.0, 1.06]),
   full(I + "note_500_billion.jpg", "500 billion mark note, 1923 · " + RB, [S("500 BILLION", "yellow", 980, 0.1, 76)], dim=0.0, zoom=[1.0, 1.06]),
   full(I + "note_100_trillion.jpg", "100 trillion mark note, 1924 · " + RB, [S("100 TRILLION", "red", 980, 0.1, 76)], dim=0.0, zoom=[1.05, 1.12])],
   hl=["millions.", "billions.", "trillions."], sfx=[["whoosh", 0], ["whoosh", 0.9], ["slam", 1.8]]),
 L("November 1923: one dollar, 4.2 trillion marks.", [
   full(I + "In a Berlin Bank LCCN2014716642.jpg", "“In a Berlin Bank” · Library of Congress, public domain",
        [S("$1 = 4,200,000,000,000 MARKS", "red", 880, 0.4, 58)], cx=0.55, zoom=[1.0, 1.12], flash=0.5, **arch),
   {"type": "board", "bg": I + "In a Berlin Bank LCCN2014716642.jpg", "points": [4.2, 7.9, 4.2e12], "show_from": 0, "show_to": 2,
    "red_from": 1, "labels": {"0": "4.2", "2": "4.2 TRILLION"},
    "items": [S("MARKS PER DOLLAR", "white", 380, 0.0, 50), S("1914 · 1918 · NOV 1923", "yellow", 470, 0.2, 44)]}],
   big=True, big_at=2.2, big_sfx="crash", drop=True, hl=["4.2 trillion"],
   say="November 1923: one dollar, four point two trillion marks."),
 L("Savings became almost worthless. The middle class, impoverished.", [
   full(I + "pixabay_207982.mp4", PB, [S("SAVINGS", "white", 780, 0.1, 64), S("≈ WORTHLESS", "red", 910, 0.45, 72)], **arch),
   full(I + "Notgeld fritz quant 10 millionen mark.jpg", "Emergency money, Trier, 1923 · public domain", [S("THE MIDDLE CLASS", "yellow", 880, 0.2, 62)], cy=0.25, **arch)],
   hl=["worthless.", "impoverished."]),
 L("The fix? A new currency: the Rentenmark.", [
   full(I + "note_1_rentenmark.jpg", "1 Rentenmark, 1923 · public domain", [S("NOVEMBER 1923", "white", 960, 0.1, 58), S("THE RENTENMARK", "yellow", 1090, 0.4, 72)], dim=0.0, zoom=[1.0, 1.06])],
   hl=["rentenmark."], sfx=[["whoosh", 0], ["cash", 1.2]]),
 L("One Rentenmark for one trillion old marks. Twelve zeros, gone.", [
   full(I + "note_1_rentenmark.jpg", "1 Rentenmark, 1923 · public domain", [S("1 RENTENMARK", "yellow", 960, 0.1, 70), S("= 1,000,000,000,000 MARKS", "white", 1090, 0.5, 58)], dim=0.0, zoom=[1.08, 1.16]),
   full(I + "pixabay_34594.mp4", PB, [S("12 ZEROS", "red", 880, 0.2, 110)], **arch)],
   twist=True, hl=["trillion", "twelve"], sfx=[["slam", 2.0]]),
 {"text": "Follow Rich to Ruin for the next crash.", "scene": {"type": "outro"}}]}

# ---------------- LTCM 1998 ----------------
T = "images/15_ltcm/pixabay_"
sl = {"id": "15_ltcm_v3", "style": "v3", "format": "RICH TO RUIN", "lead_in": 0.06, "speed": 1.12, "lines": [
 L("Two Nobel winners. One hedge fund. A 3.6 billion dollar rescue.", [
   full(T + "278200.mp4", PB, [S("2 NOBEL PRIZE WINNERS", "yellow", 860, 0.1, 64)]),
   full(T + "338956.mp4", PB, [S("ONE HEDGE FUND", "white", 760, 0.0, 62), S("$3.6B RESCUE", "red", 900, 0.4, 84)])],
   hl=["nobel", "rescue."], sfx=[["slam", 0.05], ["whoosh", 1.9]],
   say="Two Nobel winners. One hedge fund. A three point six billion dollar rescue."),
 L("Its name: Long-Term Capital Management.", [
   full(T + "42489.mp4", PB, [S("FOUNDED 1994", "white", 760, 0.1, 64), S("BY JOHN MERIWETHER", "yellow", 890, 0.4, 56)]),
   full(T + "3132.mp4", PB, [S("LONG-TERM CAPITAL MANAGEMENT", "yellow", 820, 0.0, 50), S("LTCM · 1994", "white", 940, 0.3, 64)])],
   hl=["long-term"]),
 L("Partners Myron Scholes and Robert Merton win the 1997 Nobel.", [
   full(T + "5373.mp4", PB, [S("MYRON SCHOLES", "white", 760, 0.1, 64), S("ROBERT MERTON", "white", 890, 0.4, 64)], dim=0.3),
   full(T + "19459.mp4", PB, [S("NOBEL PRIZE · 1997", "yellow", 860, 0.1, 70)], bw=True)],
   hl=["nobel."]),
 L("1995: plus 43 percent. 1996: plus 41.", [
   full(T + "88697.mp4", PB, [S("1995: +43%", "yellow", 760, 0.2, 80), S("1996: +41%", "yellow", 900, 0.6, 80)])],
   hl=["43", "41."], sfx=[["cash", 0.6], ["cash", 1.8]], say="Nineteen ninety-five: plus forty-three percent. Ninety-six: plus forty-one."),
 L("The secret? Over 25 borrowed dollars for every dollar of capital.", [
   {"type": "board", "bg": T + "204306.mp4", "items": [
     S("CAPITAL", "white", 620, 0.05, 54), S("$4.7 BILLION", "yellow", 740, 0.25, 70),
     S("BORROWED", "white", 900, 0.5, 54), S("$124.5 BILLION", "red", 1020, 0.7, 70), S("OVER 25 TO 1", "white", 1180, 0.9, 54)]}],
   hl=["borrowed"], sfx=[["whoosh", 0]]),
 L("August 1998: Russia defaults.", [
   full(T + "291425.mp4", PB, [S("AUG 17, 1998", "white", 760, 0.1, 60), S("RUSSIA DEFAULTS", "red", 890, 0.4, 72)]),
   full(T + "41884.mp4", PB, bw=True, dim=0.4)],
   hl=["defaults"], sfx=[["slam", 0.5]]),
 L("LTCM loses 4.6 billion in under four months.", [
   full(T + "338955.mp4", PB, [S("-$4.6 BILLION", "red", 880, 0.3, 96)], flash=0.4),
   {"type": "board", "bg": T + "166289.mp4", "points": [4.7, 2.3, 0.4], "show_from": 0, "show_to": 2, "red_from": 0,
    "labels": {"0": "$4.7B", "2": "$0.4B"},
    "items": [S("LTCM CAPITAL · 1998", "white", 400, 0.0, 50), S("JAN · SEPT 1 · SEPT 25", "yellow", 490, 0.2, 44)]}],
   big=True, big_at=0.6, big_sfx="crash", drop=True, hl=["4.6 billion"],
   say="LTCM loses four point six billion in under four months."),
 L("The New York Fed gets 14 banks to rescue it.", [
   full(T + "231168.mp4", PB, [S("NEW YORK FED", "white", 760, 0.1, 64), S("14 BANKS · $3.625B", "yellow", 890, 0.4, 66)]),
   full(T + "8252.mp4", PB, [S("NO PUBLIC MONEY", "white", 880, 0.2, 62)], bw=True)],
   hl=["14 banks"]),
 L("The twist? A fund called Long-Term, liquidated by 2000.", [
   full(T + "32384.mp4", PB, [S("“LONG-TERM”", "yellow", 760, 0.1, 76), S("LIQUIDATED · 2000", "red", 900, 0.5, 66)], dim=0.3)],
   twist=True, hl=["long-term"], sfx=[["slam", 2.0]]),
 {"text": "Follow Rich to Ruin for the next fall.", "scene": {"type": "outro"}}]}

for sp in (sw, sl):
    json.dump(sp, open(f"specs/{sp['id']}.json", "w"), indent=1, ensure_ascii=False)
print("ok")
