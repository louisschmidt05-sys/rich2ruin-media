"""v3.1 specs (~30 s): Hunt brothers & Silver Thursday (1980), dot-com bubble (2000).
Facts checked 2026-11-15 on en.wikipedia.org (Silver_Thursday, Nelson_Bunker_Hunt, Dot-com_bubble, Pets.com)."""
import json


def full(src, credit="Footage: Pixabay", items=None, **kw):
    d = {"type": "full", ("clip" if src.endswith(".mp4") else "img"): src, "credit": credit}
    if items: d["overlay"] = {"type": "stickers", "items": items}
    d.update(kw); return d
def S(text, style="yellow", y=880, at=0.1, size=64, x=540):
    return {"text": text, "style": style, "y": y, "at": at, "size": size, "x": x}
def L(text, shots, **kw): return {"text": text, "shots": shots, **kw}
OUT = {"text": "Follow Rich to Ruin for the next fall.", "scene": {"type": "outro"}}

H = "images/19_hunt/pixabay_"
hunt = {"id": "19_hunt_v3", "style": "v3", "format": "RICH TO RUIN", "lead_in": 0.06, "speed": 1.12, "lines": [
 L("Silver goes from under 10 dollars to over 50. Two brothers are buying it all.", [
   full(H + "12751.mp4", items=[S("SILVER: UNDER $10", "white", 760, 0.1, 64), S("→ OVER $50", "yellow", 890, 0.35, 84)]),
   full(H + "3134.mp4", items=[S("THE HUNT BROTHERS", "red", 880, 0.1, 66)])],
   hl=["10", "50."], sfx=[["slam", 0.05]],
   say="Silver goes from under ten dollars to over fifty. Two brothers are buying it all."),
 L("Bunker and Herbert Hunt's group controls about 195 million ounces.", [
   full(H + "200104.mp4", items=[S("BUNKER & HERBERT HUNT", "white", 760, 0.1, 58), S("≈ 195 MILLION OZ", "yellow", 890, 0.35, 76)])],
   hl=["195 million"], say="Bunker and Herbert Hunt's group controls about a hundred and ninety-five million ounces."),
 L("On paper, their silver jumps from 1.1 to 6.8 billion dollars.", [
   {"type": "board", "bg": H + "307616.mp4", "points": [1.1, 6.8], "show_from": 0, "show_to": 1,
    "labels": {"0": "$1.1B", "1": "$6.8B"}, "items": [S("VALUE OF THE HUNT POSITION", "white", 400, 0.0, 46), S("1979 → JAN 1980", "yellow", 490, 0.2, 44)]}],
   hl=["6.8 billion"], say="On paper, their silver jumps from one point one to six point eight billion dollars."),
 L("January 1980: the exchange changes the rules. Only selling allowed.", [
   full(H + "308080.mp4", items=[S("JANUARY 21, 1980", "white", 760, 0.1, 60), S("COMEX: SELL ORDERS ONLY", "red", 890, 0.35, 60)], dim=0.2)],
   hl=["selling"], say="January nineteen-eighty: the exchange changes the rules. Only selling allowed."),
 L("March 27, 1980: Silver Thursday. Silver closes at 10.80.", [
   full(H + "204306.mp4", items=[S("SILVER THURSDAY", "white", 760, 0.1, 64), S("$10.80", "red", 900, 0.3, 110)], flash=0.3),
   {"type": "board", "bg": H + "20857.mp4", "points": [50, 29.75, 10.8], "show_from": 0, "show_to": 2, "red_from": 0,
    "labels": {"0": "$50+", "1": "$29.75", "2": "$10.80"}, "items": [S("SILVER, $ PER OUNCE", "white", 400, 0.0, 46), S("JAN · MAR 10 · MAR 27, 1980", "yellow", 490, 0.2, 42)]}],
   big=True, big_at=0.3, big_sfx="crash", drop=True, hl=["10.80."],
   say="March twenty-seventh, nineteen-eighty: Silver Thursday. Silver closes at ten eighty."),
 L("Thirteen banks arrange a 1.1 billion dollar loan to a Hunt company.", [
   full(H + "6714.mp4", items=[S("13 BANKS", "white", 760, 0.1, 66), S("$1.1 BILLION LOAN", "yellow", 890, 0.35, 70)], dim=0.2)],
   hl=["1.1 billion"], say="Thirteen banks arrange a one point one billion dollar loan to a Hunt company."),
 L("The twist? In 1988, a jury finds they conspired. That year, they go bankrupt.", [
   full(H + "3612.mp4", items=[S("1988: LIABLE FOR CONSPIRACY", "white", 760, 0.1, 54), S("CHAPTER 11", "red", 890, 0.4, 84)], bw=True, grain=True)],
   twist=True, hl=["conspired.", "bankrupt."], say="The twist? In nineteen eighty-eight, a jury finds they conspired. That year, they go bankrupt."),
 OUT]}

D = "images/20_dotcom/pixabay_"
dot = {"id": "20_dotcom_v3", "style": "v3", "format": "THE CRASH", "lead_in": 0.06, "speed": 1.12, "lines": [
 L("March 10, 2000: the Nasdaq hits 5,048. Then 5 trillion dollars vanish.", [
   full(D + "338956.mp4", items=[S("NASDAQ: 5,048", "yellow", 760, 0.1, 80), S("MARCH 10, 2000", "white", 890, 0.35, 58)]),
   full(D + "166289.mp4", items=[S("-$5 TRILLION", "red", 880, 0.1, 96)])],
   hl=["5,048.", "5 trillion"], sfx=[["slam", 0.05]],
   say="March tenth, two thousand: the Nasdaq hits five thousand and forty-eight. Then five trillion dollars vanish."),
 L("In 1999 alone, the Nasdaq rises 85.6 percent.", [
   full(D + "314558.mp4", items=[S("1999", "white", 760, 0.1, 70), S("NASDAQ +85.6%", "yellow", 900, 0.35, 84)])],
   hl=["85.6"], say="In nineteen ninety-nine alone, the Nasdaq rises eighty-five point six percent."),
 L("Pets.com spends 1.2 million dollars on one Super Bowl ad.", [
   full(D + "156318.mp4", items=[S("PETS.COM", "yellow", 760, 0.1, 76), S("SUPER BOWL AD: $1.2M", "white", 890, 0.35, 62)])],
   hl=["1.2 million"], say="Pets dot com spends one point two million dollars on one Super Bowl ad."),
 L("February 2000: its stock market debut raises 82.5 million.", [
   full(D + "5631.mp4", items=[S("IPO · FEB 2000", "white", 760, 0.1, 62), S("$82.5 MILLION", "yellow", 890, 0.35, 80)])],
   hl=["82.5 million."], say="February two thousand: its stock market debut raises eighty-two point five million."),
 L("Nine months later, it's out of business.", [
   full(D + "37417.mp4", items=[S("NOVEMBER 2000", "white", 760, 0.1, 62), S("OUT OF BUSINESS", "red", 890, 0.35, 76)], bw=True)],
   hl=["nine months"]),
 L("October 2002: the Nasdaq-100 is down 78 percent.", [
   full(D + "204306.mp4", items=[S("OCT 9, 2002", "white", 760, 0.1, 60), S("NASDAQ-100: -78%", "red", 900, 0.3, 90)], flash=0.3),
   {"type": "board", "bg": D + "14900.mp4", "points": [100, 22], "show_from": 0, "show_to": 1, "red_from": 0,
    "labels": {"0": "PEAK", "1": "-78%"}, "items": [S("NASDAQ-100", "white", 400, 0.0, 50), S("MARCH 2000 → OCT 2002", "yellow", 490, 0.2, 44)]}],
   big=True, big_at=0.3, big_sfx="crash", drop=True, hl=["78 percent."],
   say="October two thousand two: the Nasdaq one hundred is down seventy-eight percent."),
 L("The twist? Amazon crashed too, and survived.", [
   full(D + "726.mp4", items=[S("AMAZON CRASHED TOO", "white", 760, 0.1, 62), S("…AND SURVIVED", "yellow", 890, 0.45, 76)], dim=0.2)],
   twist=True, hl=["survived."], sfx=[["slam", 1.2]]),
 {"text": "Follow Rich to Ruin for the next crash.", "scene": {"type": "outro"}}]}

for sp in (hunt, dot):
    json.dump(sp, open(f"specs/{sp['id']}.json", "w"), indent=1, ensure_ascii=False)
    print("wrote", sp["id"])
