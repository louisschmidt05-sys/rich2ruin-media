import json
I = "images/03_crash_1929/"
BB = "The Big Board, NYSE film · Prelinger Archives, public domain"
VT = "Valley Town (1940) · Prelinger Archives, public domain"
pd = " · public domain"
def clip(name, credit, ov=None, **kw):
    d = {"type": "clip", "clip": I + name + ".mp4", "credit": credit, "y": 760, "zoom": [1.0, 1.12]}
    if ov: d["overlay"] = ov
    d.update(kw); return d
def photo(name, credit, ov=None, **kw):
    d = {"type": "photo", "img": I + name, "mode": "fit", "y": 760, "from": [0.5, 0.5, 1.0], "to": [0.5, 0.5, 1.12],
         "credit": credit + pd, "dim": 0.1}
    if ov: d["overlay"] = ov
    d.update(kw); return d
def txt(lines, size=120, y=1150, sub=None):
    d = {"type": "text", "lines": lines, "size": size, "y": y}
    if sub: d["sub"] = sub
    return d
def stat(label, value, **kw):
    d = {"type": "stat", "label": label, "label_y": 1090, "value": value, "y": 1200}
    d.update(kw); return d
DOW = [["SEP 1929", 381.17], ["OCT 28", 260.64], ["OCT 29", 230.07], ["JUL 1932", 41.22]]
L = lambda text, shots, **kw: {"text": text, "shots": shots, **kw}
spec = {"id": "03c_crash_1929_v2", "format": "THE CRASH", "lead_in": 0.08, "speed": 1.12,
 "headline": "THE 1929 CRASH\n-89% IN 3 YEARS",
 "lines": [
  L("October 29th, 1929. The day Wall Street broke.", [
      clip("big_board_721", BB, txt([["OCT 29, 1929", "gold"]], 130)),
      photo("Crowds_gathering_outside_New_York_Stock_Exchange_(3).jpg", "Crowd outside the NYSE, 1929")],
      sfx=[["slam", 0.05], ["whoosh", 1.6]]),
  L("Eight weeks earlier, the Dow had hit a record: 381.", [
      clip("big_board_63", BB, stat("DOW JONES · SEP 3, 1929", 381.17, dec=2, end_sfx="cash"))]),
  L("Then, October 24th. Black Thursday.", [
      photo("Crowd_outside_nyse.jpg", "Crowd outside the NYSE, 1929", txt([["BLACK THURSDAY", "red"]], 110)),
      clip("big_board_42", BB)]),
  L("Panic. 12.9 million shares change hands.", [
      clip("big_board_630", BB, stat("SHARES TRADED · OCT 24", 12.9, dec=1, suffix="M", color="cream", end_sfx="slam")),
      clip("big_board_672", BB)]),
  L("Monday: minus 12.8 percent.", [
      clip("big_board_686", BB, stat("BLACK MONDAY · OCT 28", -12.82, dec=2, suffix="%", color="red", end_sfx="slam"), bw=True)]),
  L("Tuesday: minus 11.7. Over 16 million shares traded in a single day.", [
      photo("19291030_Crash_of_'29_-_New_York_Times.jpg", "The New York Times, October 30, 1929",
            stat("BLACK TUESDAY · OCT 29", -11.73, dec=2, suffix="%", color="red"),
            mode="cover", **{"from": [0.4, 0.25, 1.6], "to": [0.38, 0.32, 1.9]}, bw=True, dim=0.45),
      clip("big_board_35", BB, txt([["16.4M SHARES", "cream"]], 120), bw=True, flash=0.15)],
      big=True, big_at=2.6, big_sfx="crash", drop=True),
  L("July 1932: the Dow sits at 41. Minus 89 percent.", [
      clip("ValleyTo1940_1209", VT, stat("JULY 8, 1932", 41.22, **{"from": 381.17}, dec=2, color="red", end_sfx="slam")),
      photo("White_Angel_Breadline,_San_Francisco,_1932,_by_Dorothea_Lange,_3.jpg", "Dorothea Lange, White Angel Breadline, 1932",
            txt([["-89%", "red"]], 240), mode="cover", **{"from": [0.5, 0.35, 1.0], "to": [0.5, 0.4, 1.12]}, dim=0.3)],
      sfx=[["whoosh", 0], ["slam", 2.2]]),
  L("The Great Depression sets in.", [
      clip("ValleyTo1940_832", VT, txt([["GREAT DEPRESSION", "gold"]], 100)),
      clip("ValleyTo1940_1274", VT), clip("ValleyTo1940_1053", VT)]),
  L("It took until 1954, twenty-five years, to get back to the top.", [
      clip("big_board_56", BB, txt([["25 YEARS", "gold"]], 170))], twist=True),
  {"text": "Follow for the next crash.", "scene": {"type": "outro"}}]}
json.dump(spec, open("specs/03c_crash_1929_v2.json", "w"), indent=1, ensure_ascii=False)
print("ok")
