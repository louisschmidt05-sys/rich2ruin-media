"""v3 specs (style of the reference TikToks): full-bleed footage, stickers, dotted-grid boards, sentence-case captions."""
import json
def full(src, credit=None, items=None, **kw):
    d = {"type": "full", ("clip" if src.endswith(".mp4") else "img"): src}
    if credit: d["credit"] = credit
    if items: d["overlay"] = {"type": "stickers", "items": items}
    d.update(kw); return d
def S(text, style="yellow", y=880, at=0.15, size=64, x=540):
    return {"text": text, "style": style, "y": y, "at": at, "size": size, "x": x}
def L(text, shots, **kw): return {"text": text, "shots": shots, **kw}

# ---------------- 1929 ----------------
I = "images/03_crash_1929/"
BB = "The Big Board (NYSE film) · Prelinger Archives, public domain"
VT = "Valley Town (1940) · Prelinger Archives, public domain"
PD = " · public domain"
arch = dict(bw=True, grain=True)
DOW = [381.17, 260.64, 230.07, 41.22]
s1929 = {"id": "03d_crash_1929_v3", "style": "v3", "format": "THE CRASH", "lead_in": 0.06, "speed": 1.12, "lines": [
 L("October 29th, 1929. The day Wall Street broke.", [
   full(I + "big_board_721.mp4", BB, [S("OCT 29, 1929", "yellow", 820, 0.1, 76)], **arch),
   full(I + "Crowds_gathering_outside_New_York_Stock_Exchange_(3).jpg", "Crowd outside the NYSE, 1929" + PD, **arch)],
   hl=["broke"], sfx=[["slam", 0.05], ["whoosh", 1.6]]),
 L("Eight weeks earlier, the Dow had hit a record: 381.", [
   full(I + "big_board_63.mp4", BB, [S("RECORD", "yellow", 760, 0.6), S("DOW JONES: 381", "white", 900, 1.0)], **arch)],
   hl=["record"], sfx=[["whoosh", 0], ["cash", 1.2]]),
 L("Then, October 24th. Black Thursday.", [
   full(I + "Crowd_outside_nyse.jpg", "Crowd outside the NYSE, 1929" + PD, [S("BLACK THURSDAY", "red", 860, 0.6, 70)], **arch),
   full(I + "big_board_42.mp4", BB, **arch)], hl=["black", "thursday"]),
 L("Panic. 12.9 million shares change hands.", [
   full(I + "big_board_630.mp4", BB, [S("12.9M SHARES", "white", 860, 0.4, 72)], **arch),
   full(I + "big_board_672.mp4", BB, **arch)], hl=["panic"]),
 L("Monday: minus 12.8 percent.", [
   full(I + "big_board_686.mp4", BB, [S("BLACK MONDAY", "yellow", 760, 0.05), S("-12.8%", "red", 900, 0.6, 96)], **arch)],
   sfx=[["whoosh", 0], ["slam", 0.7]]),
 L("Tuesday: minus 11.7. Over 16 million shares traded in a single day.", [
   full(I + "19291030_Crash_of_'29_-_New_York_Times.jpg", "The New York Times, October 30, 1929" + PD,
        [S("-11.7%", "red", 900, 0.5, 96)], cx=0.35, cy=0.2, zoom=[1.0, 1.15], dim=0.4, **arch),
   full(I + "big_board_35.mp4", BB, [S("16.4M SHARES IN ONE DAY", "white", 880, 0.2, 60)], flash=0.15, **arch)],
   big=True, big_at=2.6, big_sfx="crash", drop=True, hl=["single"]),
 L("July 1932: the Dow sits at 41. Minus 89 percent.", [
   {"type": "board", "bg": I + "Crowd_outside_nyse.jpg", "points": DOW, "show_from": 0, "show_to": 3, "red_from": 0,
    "labels": {"0": "381", "3": "41"}, "items": [S("DOW JONES 1929 → 1932", "white", 420, 0.0, 50)]},
   full(I + "White_Angel_Breadline,_San_Francisco,_1932,_by_Dorothea_Lange,_3.jpg", "Dorothea Lange, 1932" + PD,
        [S("-89%", "red", 860, 0.2, 130)], cy=0.35, **arch)], sfx=[["whoosh", 0], ["slam", 2.4]]),
 L("The Great Depression sets in.", [
   full(I + "ValleyTo1940_832.mp4", VT, [S("THE GREAT DEPRESSION", "yellow", 860, 0.2, 62)], **arch),
   full(I + "ValleyTo1940_1274.mp4", VT, **arch), full(I + "ValleyTo1940_1053.mp4", VT, **arch)], hl=["great", "depression"]),
 L("It took until 1954, twenty-five years, to get back to the top.", [
   full(I + "big_board_56.mp4", BB, [S("25 YEARS", "yellow", 860, 0.6, 110)], **arch)], twist=True, hl=["twenty-five", "years,"]),
 {"text": "Follow for the next crash.", "scene": {"type": "outro"}}]}

# ---------------- Madoff ----------------
M = "images/05_madoff/pixabay_"
PB = "Footage: Pixabay"
sm = {"id": "05b_madoff_v3", "style": "v3", "format": "THE SCAM", "lead_in": 0.06, "speed": 1.12, "lines": [
 L("December 2008. A Wall Street legend tells his sons his fund is one big lie.", [
   full(M + "1044.mp4", PB, [S("DECEMBER 2008", "yellow", 820, 0.1, 72)], bw=True, grain=True),
   full(M + "6782.mp4", PB, [S("“ONE BIG LIE”", "red", 860, 0.5, 80)])], hl=["lie."], sfx=[["slam", 0.05], ["whoosh", 2.2]]),
 L("His name: Bernie Madoff. Former chairman of the Nasdaq.", [
   full(M + "42489.mp4", PB, [S("BERNIE MADOFF", "white", 860, 0.3, 76)]),
   full(M + "204306.mp4", PB, [S("EX-CHAIRMAN OF THE NASDAQ", "yellow", 860, 0.1, 54)])], hl=["madoff.", "nasdaq."]),
 L("On paper, his clients had almost 65 billion dollars.", [
   full(M + "50623.mp4", PB, [S("ON PAPER", "white", 740, 0.1, 56), S("$65 BILLION", "yellow", 880, 0.6, 100)]),
   full(M + "50623.mp4", PB, offset=3.5, zoom=[1.15, 1.3])], sfx=[["whoosh", 0], ["cash", 1.0]]),
 L("Much of it never existed.", [
   full(M + "15178.mp4", PB, [S("NEVER EXISTED", "red", 860, 0.4, 84)])], big=True, big_at=0.5, big_sfx="crash", drop=True, hl=["never", "existed."]),
 L("New investors' money paid the old ones.", [
   {"type": "board", "bg": M + "50630.mp4".replace(".mp4", ".mp4"), "items": [
     S("NEW INVESTORS", "white", 720, 0.1, 64), S("↓  pay  ↓", "yellow", 880, 0.6, 58), S("OLD INVESTORS", "white", 1040, 1.0, 64)]}],
   hl=["new", "old"]),
 L("Direct losses: around 18 billion.", [
   full(M + "166289.mp4", PB, [S("≈ $18 BILLION LOST", "red", 860, 0.3, 72)])], hl=["losses:"], sfx=[["whoosh", 0], ["slam", 0.5]]),
 L("He's arrested on December 11th.", [
   full(M + "231168.mp4", PB, [S("ARRESTED", "red", 780, 0.3, 84), S("DEC 11, 2008", "white", 920, 0.6, 56)])], hl=["arrested"]),
 L("The sentence: 150 years in prison.", [
   full(M + "162047.mp4", PB, [S("150 YEARS", "yellow", 860, 0.5, 120)])], sfx=[["whoosh", 0], ["slam", 0.6]]),
 L("He died in federal custody in 2021.", [
   full(M + "36713.mp4", PB, [S("2021", "white", 860, 0.3, 90)], dim=0.3)]),
 L("Victims have recovered over 14 billion dollars.", [
   full(M + "50630.mp4", PB, [S("$14B+ RECOVERED", "yellow", 860, 0.4, 76)])], twist=True, hl=["recovered"], sfx=[["whoosh", 0], ["cash", 0.6]]),
 {"text": "Follow for the next scam.", "scene": {"type": "outro"}}]}
for sp in (s1929, sm):
    json.dump(sp, open(f"specs/{sp['id']}.json", "w"), indent=1, ensure_ascii=False)
print("ok")
