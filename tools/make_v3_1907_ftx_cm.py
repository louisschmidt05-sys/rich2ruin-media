"""v3 specs (short cut, ~30 s): Panic of 1907, FTX (2022), Credit Mobilier (1872).
Facts checked 2026-11-15 on en.wikipedia.org (Panic_of_1907, Bankruptcy_of_FTX, Sam_Bankman-Fried,
Credit_Mobilier_scandal, Oakes_Ames, Golden_spike) and federalreservehistory.org (Panic of 1907).
New rules from the 15 Nov competitor study: 8 lines max, number + famous name in line 1, sticker on screen
from 0.1 s, one mechanism board, twist at the end, no extra SFX."""
import json


def full(src, credit=None, items=None, **kw):
    d = {"type": "full", ("clip" if src.endswith(".mp4") else "img"): src}
    if credit: d["credit"] = credit
    if items: d["overlay"] = {"type": "stickers", "items": items}
    d.update(kw); return d
def S(text, style="yellow", y=880, at=0.1, size=64, x=540):
    return {"text": text, "style": style, "y": y, "at": at, "size": size, "x": x}
def L(text, shots, **kw): return {"text": text, "shots": shots, **kw}

PB = "Footage: Pixabay"
arch = dict(bw=True, grain=True)
LOC = "Library of Congress, public domain"

# ---------------- Panic of 1907 ----------------
I = "images/16_panic1907/"
P = I + "pixabay_"
s1907 = {"id": "16_panic1907_v3", "style": "v3", "format": "THE CRASH", "lead_in": 0.06, "speed": 1.05, "voice": "af_heart", "pause": 0.25, "lines": [
 L("1907. Wall Street is collapsing. One man locks about 120 bankers in his library.", [
   full(I + "1907 Panic.png", "Wall Street crowd, 1907 · public domain", [S("1907", "white", 760, 0.1, 70), S("WALL STREET COLLAPSES", "red", 890, 0.3, 62)], zoom=[1.0, 1.1], **arch),
   full(I + "J.P. Morgan.jpg", "J. P. Morgan · public domain", [S("120 BANKERS LOCKED IN", "yellow", 900, 0.1, 64)], cy=0.3, zoom=[1.0, 1.08], **arch)],
   hl=["120 bankers"], sfx=[["slam", 0.05]],
   say="Nineteen-oh-seven. Wall Street is collapsing. One man locks about a hundred and twenty bankers in his library."),
 L("It starts with a failed bet on United Copper: from 60 dollars to 10.", [
   full(I + "Brokers signalling, curb market, New York City LCCN93508733.jpg", "Curb market brokers, New York · " + LOC, [S("OCTOBER 1907", "white", 760, 0.1, 60), S("UNITED COPPER", "yellow", 880, 0.3, 66)], **arch),
   {"type": "board", "bg": P + "151868.mp4", "points": [39, 60, 10], "show_from": 0, "show_to": 2, "red_from": 1,
    "labels": {"0": "$39", "1": "$60", "2": "$10"},
    "items": [S("UNITED COPPER · OCT 14–16, 1907", "white", 400, 0.0, 46)]}],
   hl=["60", "10."], say="It starts with a failed bet on United Copper: from sixty dollars to ten."),
 L("Panic. The Knickerbocker Trust loses 8 million dollars in under three hours.", [
   full(I + "Knickerbocker Trust Co., exterior view, New York LCCN2014680464.jpg", "Knickerbocker Trust Co., New York · " + LOC, [S("KNICKERBOCKER TRUST", "white", 760, 0.1, 58), S("-$8M IN < 3 HOURS", "red", 890, 0.35, 70)], zoom=[1.0, 1.1], **arch),
   full(P + "1694.mp4", PB, [S("OCTOBER 22", "yellow", 880, 0.1, 64)], **arch)],
   hl=["8 million"], say="Panic. The Knickerbocker Trust loses eight million dollars in under three hours."),
 L("Stocks fall almost 50 percent from their peak.", [
   full(I + "Stockexchange.jpg", "New York Stock Exchange floor, 1908 · public domain", [S("NYSE", "white", 760, 0.1, 60), S("≈ -50%", "red", 900, 0.4, 110)], zoom=[1.0, 1.12], flash=0.4, **arch)],
   big=True, big_at=0.4, big_sfx="crash", drop=True, hl=["50 percent"],
   say="Stocks fall almost fifty percent from their peak."),
 L("Morgan gets 14 bank presidents to pledge 23.6 million in minutes.", [
   full(I + "Edward Steichen - Photographic portrait of Pierpont Morgan (1837-1913).jpg", "J. P. Morgan by Edward Steichen, 1903 · public domain", [S("J. P. MORGAN", "white", 1000, 0.1, 62)], cy=0.35, zoom=[1.0, 1.08], **arch),
   {"type": "board", "bg": P + "164603.mp4", "items": [
     S("OCTOBER 24", "white", 640, 0.05, 54), S("14 BANK PRESIDENTS", "yellow", 760, 0.25, 62),
     S("↓", "white", 870, 0.45, 60), S("$23.6 MILLION", "red", 980, 0.6, 76), S("TO SAVE THE EXCHANGE", "white", 1100, 0.8, 50)]}],
   hl=["23.6 million"], say="Morgan gets fourteen bank presidents to pledge twenty-three point six million in minutes."),
 L("Nine days later, he locks them in his library until they pledge 25 million.", [
   full(P + "202823.mp4", PB, [S("NOVEMBER 2, 1907", "white", 760, 0.1, 58), S("DOOR LOCKED", "red", 890, 0.35, 70)], dim=0.2),
   full(P + "151868.mp4", PB, [S("3 A.M. · $25 MILLION", "yellow", 880, 0.1, 64)], **arch)],
   hl=["locks", "25 million."], say="Nine days later, he locks them in his library until they pledge twenty-five million."),
 L("The twist? This panic led America to create the Federal Reserve.", [
   full(I + "FederalReserveMap1914TheSun.png", "Federal Reserve districts, The Sun, 1914 · public domain", [S("1913", "yellow", 1000, 0.1, 76), S("THE FEDERAL RESERVE", "white", 1120, 0.35, 58)], cx=0.5, zoom=[1.0, 1.1], **arch)],
   twist=True, hl=["federal reserve."]),
 {"text": "Follow Rich to Ruin for the next crash.", "scene": {"type": "outro"}}]}

# ---------------- FTX 2022 ----------------
F = "images/17_ftx/pixabay_"
sftx = {"id": "17_ftx_v3", "style": "v3", "format": "THE SCAM", "lead_in": 0.06, "speed": 1.05, "voice": "af_heart", "pause": 0.25, "lines": [
 L("He was worth 16 billion dollars. Nine days later, his empire was bankrupt.", [
   full(F + "50352.mp4", PB, [S("$16 BILLION", "yellow", 860, 0.1, 96)]),
   full(F + "166289.mp4", PB, [S("9 DAYS LATER: BANKRUPT", "red", 880, 0.1, 62)])],
   hl=["16 billion", "bankrupt."], sfx=[["slam", 0.05]],
   say="He was worth sixteen billion dollars. Nine days later, his empire was bankrupt."),
 L("Sam Bankman-Fried founds the crypto exchange FTX in 2019.", [
   full(F + "134428.mp4", PB, [S("SAM BANKMAN-FRIED", "white", 760, 0.1, 58), S("FTX · 2019", "yellow", 890, 0.35, 72)], dim=0.3),
   full(F + "215751.mp4", PB, [S("41st RICHEST AMERICAN", "yellow", 880, 0.1, 60)])],
   hl=["ftx"], say="Sam Bankman-Fried founds the crypto exchange F T X in twenty nineteen."),
 L("November 2, 2022: a leak shows his trading firm runs on FTX's own token.", [
   full(F + "3176.mp4", PB, [S("NOV 2, 2022", "white", 760, 0.1, 60), S("COINDESK REPORT", "yellow", 890, 0.35, 62)]),
   {"type": "board", "bg": F + "20833.mp4", "items": [
     S("ALAMEDA RESEARCH", "white", 620, 0.05, 56), S("$14.6B IN ASSETS", "yellow", 740, 0.25, 66),
     S("40% =", "white", 880, 0.5, 60), S("FTT, FTX'S OWN TOKEN", "red", 1000, 0.65, 58)]}],
   hl=["own token."], say="November second, twenty twenty-two: a leak shows his trading firm runs on F T X's own token."),
 L("Binance says it will sell its FTT. Customers pull 6 billion dollars.", [
   full(F + "3180.mp4", PB, [S("NOV 7", "white", 760, 0.1, 60), S("BINANCE: SELLING ITS FTT", "yellow", 890, 0.3, 58)]),
   full(F + "142641.mp4", PB, [S("-$6 BILLION WITHDRAWN", "red", 880, 0.1, 62)])],
   hl=["6 billion"], say="Binance says it will sell its F T T. Customers pull six billion dollars."),
 L("November 11: bankruptcy. Alameda had taken 8 billion dollars.", [
   full(F + "377885.mp4", PB, [S("NOV 11, 2022", "white", 760, 0.1, 60), S("BANKRUPTCY", "red", 890, 0.3, 84)], flash=0.3),
   full(F + "13305.mp4", PB, [S("$8 BILLION HOLE", "red", 880, 0.1, 76)])],
   big=True, big_at=0.3, big_sfx="crash", drop=True, hl=["8 billion"],
   say="November eleventh: bankruptcy. Alameda had taken eight billion dollars."),
 L("Guilty on all seven counts. Sentence: 25 years in prison.", [
   full(F + "254922.mp4", PB, [S("GUILTY · 7 COUNTS", "white", 760, 0.1, 62), S("NOV 2, 2023", "yellow", 890, 0.3, 56)]),
   full(F + "93536.mp4", PB, [S("25 YEARS", "red", 880, 0.1, 96)], **arch)],
   hl=["guilty", "25 years"], say="Guilty on all seven counts. Sentence: twenty-five years in prison."),
 L("The twist? Customers are expected to get back over 100 percent of their claims.", [
   full(F + "23066.mp4", PB, [S("ESTIMATED RECOVERY", "white", 760, 0.1, 58), S("118% TO 142%", "yellow", 900, 0.35, 84)], dim=0.2)],
   twist=True, hl=["100 percent"],
   say="The twist? Customers are expected to get back over a hundred percent of their claims."),
 {"text": "Follow Rich to Ruin for the next scam.", "scene": {"type": "outro"}}]}

# ---------------- Credit Mobilier 1872 ----------------
C = "images/18_creditmobilier/"
Q = C + "pixabay_"
scm = {"id": "18_creditmobilier_v3", "style": "v3", "format": "THE SCAM", "lead_in": 0.06, "speed": 1.05, "voice": "af_heart", "pause": 0.25, "lines": [
 L("The railroad cost 50 million dollars to build. The bill: 94 million.", [
   full(Q + "57046.mp4", PB, [S("COST: $50 MILLION", "white", 760, 0.1, 64), S("BILLED: $94 MILLION", "red", 890, 0.35, 70)], **arch)],
   hl=["50 million", "94 million."], sfx=[["slam", 0.05]],
   say="The railroad cost fifty million dollars to build. The bill: ninety-four million."),
 L("1864: Union Pacific bosses create their own construction company.", [
   full(C + "Union pacific poster.jpg", "Union Pacific opening-day poster · public domain", [S("1864", "yellow", 1000, 0.1, 76)], cy=0.3, zoom=[1.0, 1.1], **arch),
   full(C + "Dale Creek Bridge Union Pacific Railroad Company by Andrew J Russell.jpg", "Dale Creek Bridge, A. J. Russell · public domain", [S("CRÉDIT MOBILIER OF AMERICA", "white", 880, 0.1, 50)], **arch)],
   hl=["their own"], say="Eighteen sixty-four: Union Pacific bosses create their own construction company."),
 L("They hire themselves at inflated prices and pocket the difference.", [
   {"type": "board", "bg": Q + "41146.mp4", "items": [
     S("CONGRESS FUNDS", "white", 560, 0.05, 54), S("↓", "yellow", 660, 0.2, 60),
     S("UNION PACIFIC", "white", 760, 0.3, 58), S("↓  PAYS INFLATED BILLS", "yellow", 870, 0.45, 50),
     S("CRÉDIT MOBILIER", "white", 980, 0.6, 58), S("= THE SAME MEN", "red", 1100, 0.8, 64)]}],
   hl=["inflated"]),
 L("Congressman Oakes Ames sells shares to colleagues, far below market price.", [
   full(C + "Oakes Ames - Brady-Handy (cropped).jpg", "Oakes Ames, Brady-Handy · public domain", [S("OAKES AMES", "white", 1000, 0.1, 64), S("CONGRESSMAN", "yellow", 1120, 0.3, 54)], cy=0.3, zoom=[1.0, 1.08], **arch),
   full(C + "Capitol, by E. & H.T. Anthony (Firm).jpg", "U.S. Capitol, E. & H.T. Anthony · public domain", [S("SHARES BELOW MARKET PRICE", "yellow", 880, 0.1, 54)], mode="fit", **arch)],
   hl=["below market"]),
 L("1872: The Sun exposes it. Union Pacific is left nearly bankrupt.", [
   full(Q + "41121.mp4", PB, [S("SEPT 4, 1872", "white", 760, 0.1, 60), S("“THE KING OF FRAUDS”", "red", 890, 0.35, 64)], flash=0.3, **arch),
   full(C + "East and West Shaking hands at the laying of last rail Union Pacific Railroad - .jpg", "Promontory Summit, 1869, A. J. Russell · public domain", [S("UNION PACIFIC: NEARLY BANKRUPT", "red", 880, 0.1, 52)], **arch)],
   big=True, big_at=0.3, big_sfx="crash", drop=True, hl=["nearly bankrupt."],
   say="Eighteen seventy-two: The Sun exposes it. Union Pacific is left nearly bankrupt."),
 L("Over 30 politicians got shares, including the Vice President.", [
   full(C + "Keppler Credit Mobilier Hari-Kari.png", "Credit Mobilier cartoon, J. Keppler · public domain", [S("30+ POLITICIANS", "yellow", 1050, 0.1, 70)], mode="fit", **arch),
   full(C + "Schuyler Colfax portrait (cropped).jpg", "Schuyler Colfax · public domain", [S("VICE PRESIDENT COLFAX", "white", 1000, 0.1, 54)], cy=0.3, **arch)],
   hl=["30", "vice president."], say="Over thirty politicians got shares, including the Vice President."),
 L("The twist? No one was ever charged. Ames was only censured.", [
   full(Q + "142723.mp4", PB, [S("CHARGES FILED: 0", "red", 760, 0.1, 70), S("AMES CENSURED · 1873", "white", 890, 0.4, 56)], **arch)],
   twist=True, hl=["charged.", "censured."], sfx=[["slam", 1.0]]),
 {"text": "Follow Rich to Ruin for the next scam.", "scene": {"type": "outro"}}]}

for sp in (s1907, sftx, scm):
    json.dump(sp, open(f"specs/{sp['id']}.json", "w"), indent=1, ensure_ascii=False)
    print("wrote", sp["id"])
