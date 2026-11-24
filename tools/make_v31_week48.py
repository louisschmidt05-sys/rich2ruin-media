"""v3.1 specs (~30 s) for the week of 24 Nov - 8 Dec 2026: Florida land boom (1925-26), Overend Gurney (1866),
Panic of 1873 / Jay Cooke, Darien scheme (1698-1700), Great Salad Oil Swindle (1963).
Facts checked 2026-11-21 (en.wikipedia.org blocked in unattended runs, so other sources were used):
- Florida: wikiwand Florida_Land_Boom (Prinz Valdemar 10 Jan 1926), pbchistory.org (hurricane 18 Sep 1926,
  >390 dead; West Palm Beach real estate 1929->1930 -53% to $41.6M, $18.2M in 1935), cato.org (nearly 400 dead,
  40 Florida banks failed in 1926), moneyweek.com + fcit.usf.edu (binder = non-refundable deposit, balance in 30 days,
  binders flipped; lots resold up to ten times a day "some sources").
- Overend Gurney: Bank of England Quarterly Bulletin 2016 Q2 (largest discount house, larger than three next
  competitors combined; 1865 flotation, £15 paid per £50 share, >£25 Oct 1865, £12.25 just before collapse; help refused
  9 May; note on door 15:30 10 May 1866; 'Black Friday'; rate raised four times to 10%; Bagehot / lender of last resort),
  wikiwand ('the bankers' bank'), Illustrated London News 19 May 1866 via victorianweb.org (Lombard Street crowds).
- Panic of 1873: smithsonianmag.com (>$1.6B war bonds, Northern Pacific, NYSE shut 10 days first time, 18,000
  businesses, Utah silver mine, died wealthy 1905), federalreservehistory.org (bankruptcy 18 Sep, NYSE closed 20 Sep,
  depression 1873-79), pbs.org (14% unemployment by 1876, 18,000 businesses in two years).
- Darien: wikiwand Darien_scheme (£400,000 in a few weeks, about a fifth of Scotland's wealth, five ships July 1698,
  ~1,200 people, up to ten deaths a day, King William told colonies not to supply, abandoned July 1699, 300 of 1,200
  survived, £398,085 10s in 1707), nms.ac.uk (same 300/1,200, 2,000 lives, Equivalent partly compensation for Darien).
- Salad oil: TIME 4 Jun 1965 (Bayonne, 1.8 billion lbs receipts vs scarcely 100 million lbs found, water topped by a slick
  of oil, tanks connected by pipes, American Express Warehousing vouched, guilty plea), thereformedbroker.com and
  benzinga.com (bankruptcy 19 Nov 1963, soybean oil $9.875 -> $7.75 Nov 15-19, AmEx 65 -> 37, Buffett 5% for $20M,
  released 1972 after seven years)."""
import json


def full(src, credit="Footage: Pixabay", items=None, **kw):
    d = {"type": "full", ("clip" if src.endswith(".mp4") else "img"): src, "credit": credit}
    if items: d["overlay"] = {"type": "stickers", "items": items}
    d.update(kw); return d
def S(text, style="yellow", y=880, at=0.1, size=64, x=540):
    return {"text": text, "style": style, "y": y, "at": at, "size": size, "x": x}
def L(text, shots, **kw): return {"text": text, "shots": shots, **kw}
def board(bg, items, **kw):
    d = {"type": "board", "bg": bg, "items": items}; d.update(kw); return d
def OUT(kind): return {"text": f"Follow Rich to Ruin for the next {kind}.", "scene": {"type": "outro"}}
PD = " · public domain"
FM = " · State Archives of Florida, public domain"
LOC = " · Library of Congress, public domain"

# ---------------------------------------------------------------- 21 Florida land boom
F = "images/21_florida/"; FP = F + "pixabay_"
florida = {"id": "21_florida_v3", "style": "v3", "format": "THE CRASH", "lead_in": 0.06, "speed": 1.05, "voice": "af_heart", "pause": 0.25, "lines": [
 L("Miami, 1925: some lots reportedly sold ten times a day.", [
   full(F + "Miami Beach - Beach scene (1925).jpg", "Miami Beach postcard, 1925" + PD,
        [S("MIAMI, 1925", "white", 760, 0.1, 62), S("SOLD 10× A DAY", "yellow", 890, 0.3, 84)], bw=True, grain=True),
   full(FP + "154197.mp4", items=[S("THE FLORIDA LAND BOOM", "red", 880, 0.1, 62)])],
   hl=["ten times"], sfx=[["slam", 0.05]],
   say="Miami, nineteen twenty-five: some lots reportedly sold ten times a day."),
 L("Many buyers only paid a binder: a non-refundable deposit.", [
   full(FP + "41146.mp4", items=[S("THE BINDER", "yellow", 760, 0.1, 76), S("NON-REFUNDABLE DEPOSIT", "white", 890, 0.35, 56)])],
   hl=["binder:"]),
 L("The rest was due in 30 days. So they flipped it.", [
   full(F + "Aladdin City Florida Land Boom Map 1927.jpg", "Aladdin City lot plan, 1920s" + PD,
        [S("BALANCE DUE: 30 DAYS", "white", 760, 0.1, 60), S("FLIP IT FIRST", "yellow", 890, 0.35, 76)], grain=True),
   full(F + "Dammers, Gillette, and Burnes company bus- Coral Gables, Florida (8947514049).jpg",
        "Real estate bus, Coral Gables, 1922" + FM, [S("CORAL GABLES", "white", 880, 0.1, 62)], bw=True, grain=True)],
   hl=["30 days."], say="The rest was due in thirty days. So they flipped it."),
 L("January 1926: a sunken ship blocks Miami's harbour.", [
   full(FP + "200244.mp4", items=[S("JANUARY 10, 1926", "white", 760, 0.1, 60), S("PRINZ VALDEMAR SINKS", "red", 890, 0.35, 62)], dim=0.2),
   full(FP + "173725.mp4", items=[S("HARBOUR BLOCKED", "yellow", 880, 0.1, 70)])],
   hl=["sunken ship"], say="January nineteen twenty-six: a sunken ship blocks Miami's harbour."),
 L("September 1926: a hurricane hits Miami. Nearly 400 dead.", [
   full(F + "Miami hurricane weather map 9-18-1926 (3254801).jpg", "Weather map, 18 Sept 1926" + PD,
        [S("SEPTEMBER 18, 1926", "white", 760, 0.1, 60)], bw=True, grain=True, flash=0.3),
   full(F + "Home damaged by the 1926 hurricane- Miami Beach, Florida (8948510740).jpg",
        "Miami Beach, Sept 1926" + FM, [S("NEARLY 400 DEAD", "red", 890, 0.1, 80)], bw=True, grain=True)],
   big=True, big_at=0.3, big_sfx="crash", drop=True, hl=["Nearly 400"],
   say="September nineteen twenty-six: a hurricane hits Miami. Nearly four hundred dead."),
 L("In 1926 alone, 40 Florida banks fail.", [
   full(F + "Hollywood Beach Hotel after the 1926 hurricane (8901431154).jpg", "Hollywood Beach Hotel, Oct 1926" + FM,
        [S("1926", "white", 760, 0.1, 66), S("40 BANKS FAIL", "red", 890, 0.3, 84)], bw=True, grain=True),
   board(FP + "81359.mp4", [S("WEST PALM BEACH REAL ESTATE", "white", 400, 0.0, 44), S("1929 → 1930 → 1935", "yellow", 490, 0.2, 44)],
         points=[88.5, 41.6, 18.2], show_from=0, show_to=2, red_from=0,
         labels={"0": "1929", "1": "$41.6M", "2": "$18.2M"})],
   hl=["40"], say="In nineteen twenty-six alone, forty Florida banks fail."),
 L("The twist? This crash came three years before Wall Street's.", [
   full(FP + "59535.mp4", items=[S("FLORIDA: 1926", "red", 760, 0.1, 66), S("WALL STREET: 1929", "white", 890, 0.4, 66)], bw=True, dim=0.25)],
   twist=True, hl=["three years"], sfx=[["slam", 1.3]]),
 OUT("crash")]}

# ---------------------------------------------------------------- 22 Overend Gurney
O = "images/22_overend/"; OP = O + "pixabay_"
overend = {"id": "22_overend_v3", "style": "v3", "format": "RICH TO RUIN", "lead_in": 0.06, "speed": 1.05, "voice": "af_heart", "pause": 0.25, "lines": [
 L("London, 1866: the 'bankers' bank' collapses. Black Friday.", [
   full(O + "Political cartoon from Fun magazine about Overend Gurney.jpg", "\"A bank stock(ing)\", Fun magazine, 1866" + PD,
        [S("OVEREND, GURNEY & CO", "white", 760, 0.1, 58), S("BLACK FRIDAY", "red", 890, 0.3, 92)], grain=True),
   full(OP + "43562.mp4", items=[S("THE BANKERS' BANK", "yellow", 880, 0.1, 70)], bw=True, grain=True)],
   hl=["Black Friday."], sfx=[["slam", 0.05]],
   say="London, eighteen sixty-six: the bankers' bank collapses. Black Friday."),
 L("Overend Gurney was bigger than its next three rivals combined.", [
   full(O + "Aerial cutaway view of Soane's Bank of England by JM Gandy 1830.jpg", "Bank of England, J. M. Gandy, 1830" + PD,
        [S("LARGEST DISCOUNT HOUSE IN LONDON", "white", 760, 0.1, 50), S("> NEXT 3 RIVALS COMBINED", "yellow", 890, 0.35, 56)], grain=True)],
   hl=["three rivals"]),
 L("1865: it sells shares to the public at £15 paid.", [
   full(OP + "107240.mp4", items=[S("JULY 1865: GOES PUBLIC", "white", 760, 0.1, 58), S("£15 PAID PER SHARE", "yellow", 890, 0.35, 66)]),
   full(OP + "325497.mp4", items=[S("BY OCTOBER: OVER £25", "yellow", 880, 0.1, 66)])],
   hl=["£15"], say="Eighteen sixty-five: it sells shares to the public at fifteen pounds paid."),
 L("By May 1866, they're down to £12.25.", [
   board(OP + "111281.mp4", [S("OVEREND GURNEY SHARE", "white", 400, 0.0, 48), S("JULY 1865 → MAY 1866", "yellow", 490, 0.2, 44)],
         points=[15, 25, 12.25], show_from=0, show_to=2, red_from=1,
         labels={"0": "£15", "1": "£25+", "2": "£12.25"})],
   hl=["£12.25."], say="By May eighteen sixty-six, they're down to twelve pounds twenty-five."),
 L("It begs the Bank of England for help. Refused.", [
   full(O + "19th century Bank of England parlor.jpg", "Bank of England parlour, 19th century" + PD,
        [S("MAY 9, 1866", "white", 760, 0.1, 62), S("HELP REFUSED", "red", 890, 0.35, 84)], bw=True, grain=True)],
   hl=["Refused."]),
 L("May 10, 3:30 pm: a note on the door. Suspended.", [
   full(OP + "130878.mp4", items=[S("10 MAY 1866 · 15:30", "white", 760, 0.1, 60), S("PAYMENTS SUSPENDED", "red", 890, 0.3, 70)], flash=0.3, dim=0.2),
   full(OP + "1694.mp4", items=[S("LOMBARD STREET BESIEGED", "white", 760, 0.1, 54), S("BANK RATE → 10%", "red", 890, 0.35, 76)], bw=True, grain=True)],
   big=True, big_at=0.3, big_sfx="crash", drop=True, hl=["Suspended."],
   say="May tenth, three thirty p.m.: a note on the door. Suspended."),
 L("The twist? It taught the Bank to rescue banks in a panic.", [
   full(O + "Walter Bagehot NPG.jpg", "Walter Bagehot" + PD,
        [S("BAGEHOT, LOMBARD STREET, 1873", "white", 760, 0.1, 50), S("\"LEND FREELY, BOLDLY\"", "yellow", 890, 0.4, 66)], bw=True, grain=True)],
   twist=True, hl=["rescue"], sfx=[["slam", 1.3]]),
 OUT("fall")]}

# ---------------------------------------------------------------- 23 Panic of 1873
P = "images/23_panic1873/"; PP = P + "pixabay_"
panic = {"id": "23_panic1873_v3", "style": "v3", "format": "THE CRASH", "lead_in": 0.06, "speed": 1.05, "voice": "af_heart", "pause": 0.25, "lines": [
 L("He sold 1.6 billion dollars of war bonds. Then crashed.", [
   full(P + "Jay Cooke during Civil War.png", "Jay Cooke, Civil War era" + PD,
        [S("JAY COOKE", "white", 760, 0.1, 70), S("$1.6 BILLION OF WAR BONDS", "yellow", 890, 0.3, 60)], bw=True, grain=True, cy=0.35),
   full(P + "Scenes in Wall Street during the panic. Jay Cooke & Company's office LCCN9070711.jpg",
        "Jay Cooke & Co.'s office, 1873" + LOC, [S("BANKRUPT", "red", 880, 0.1, 96)], grain=True)],
   hl=["1.6 billion"], sfx=[["slam", 0.05]],
   say="He sold one point six billion dollars of war bonds. Then crashed."),
 L("Jay Cooke bets his bank on the Northern Pacific Railway.", [
   full(PP + "188828.mp4", items=[S("NORTHERN PACIFIC RAILWAY", "yellow", 760, 0.1, 58), S("HEAVILY INVESTED", "white", 890, 0.35, 70)], bw=True, grain=True),
   full(PP + "142723.mp4", items=[S("1870: COOKE FINANCES IT", "white", 880, 0.1, 62)], bw=True)],
   hl=["Northern Pacific"]),
 L("September 18, 1873: Jay Cooke & Company closes its doors.", [
   full(P + "Jay Cooke & Co. drawing.png", "Jay Cooke & Co., Philadelphia" + PD,
        [S("SEPTEMBER 18, 1873", "white", 760, 0.1, 60), S("DOORS CLOSED", "red", 890, 0.3, 84)], grain=True),
   full(PP + "20459.mp4", items=[S("BANKRUPT", "red", 880, 0.1, 90)], bw=True, dim=0.2)],
   hl=["closes"], say="September eighteenth, eighteen seventy-three: Jay Cooke and Company closes its doors."),
 L("Two days later, the Stock Exchange shuts. A first.", [
   full(P + "The Great Financial Panic of 1873 - Closing the door of the Stock Exchange on it.jpg",
        "Closing the Stock Exchange, 20 Sept 1873" + LOC,
        [S("NYSE CLOSED", "red", 760, 0.1, 80), S("FOR 10 DAYS", "white", 890, 0.3, 76)], grain=True, flash=0.3),
   full(P + "The Great Financial Panic - View in Broad St., near the Stock Exchange, on Satur.jpg",
        "Broad Street, 20 Sept 1873" + LOC, [S("FIRST TIME IN ITS HISTORY", "yellow", 880, 0.1, 58)], grain=True)],
   big=True, big_at=0.3, big_sfx="crash", drop=True, hl=["shuts."],
   say="Two days later, the Stock Exchange shuts. A first."),
 L("In two years, 18,000 businesses fail.", [
   full(P + "The Panic - Run on the Fourth National Bank, No. 20 Nassau Street (New York City.jpg",
        "Run on the Fourth National Bank, 1873" + LOC,
        [S("18,000 BUSINESSES", "red", 760, 0.1, 76), S("FAILED IN 2 YEARS", "white", 890, 0.35, 62)], grain=True)],
   hl=["18,000"], say="In two years, eighteen thousand businesses fail."),
 L("By 1876, unemployment hits 14 percent.", [
   full(PP + "214855.mp4", items=[S("1876: 14% UNEMPLOYED", "red", 760, 0.1, 66)], bw=True, dim=0.25),
   board(PP + "3639.mp4", [S("THE DEPRESSION", "white", 400, 0.0, 50), S("1873 → 1879", "yellow", 490, 0.2, 60),
                            S("6 YEARS", "red", 960, 0.6, 96)])],
   hl=["14 percent."], say="By eighteen seventy-six, unemployment hits fourteen percent."),
 L("The twist? Cooke got rich again, from a Utah silver mine.", [
   full(PP + "136660.mp4", items=[S("UTAH SILVER MINE", "white", 760, 0.1, 64), S("RICH AGAIN", "yellow", 890, 0.4, 84)])],
   twist=True, hl=["rich again,"], sfx=[["slam", 1.3]]),
 OUT("crash")]}

# ---------------------------------------------------------------- 24 Darien scheme
D = "images/24_darien/"; DP = D + "pixabay_"
DM = "A PLAN of the HARBOUR and Parts of adjacent on the ISTHMUS of DARIEN where the S.jpg"
darien = {"id": "24_darien_v3", "style": "v3", "format": "RICH TO RUIN", "lead_in": 0.06, "speed": 1.05, "voice": "af_heart", "pause": 0.25, "lines": [
 L("Scotland bets £400,000 on a colony in Panama. 300 survive.", [
   full(D + "Company of Scotland arms.png", "Arms of the Company of Scotland, 1698" + PD,
        [S("£400,000", "yellow", 760, 0.1, 96), S("SCOTLAND → PANAMA", "white", 890, 0.3, 66)], grain=True),
   full(DP + "223270.mp4", items=[S("ONLY 300 SURVIVE", "red", 880, 0.1, 76)], bw=True)],
   hl=["£400,000", "300"], sfx=[["slam", 0.05]],
   say="Scotland bets four hundred thousand pounds on a colony in Panama. Three hundred survive."),
 L("Raised in a few weeks: about a fifth of Scotland's wealth.", [
   full(D + "Minute book of the Company of Scotland's Court of Directors, 14 February 1696 to.jpg",
        "Company of Scotland minute book, 1696-98" + PD,
        [S("RAISED IN WEEKS", "white", 760, 0.1, 64), S("≈ 1/5 OF SCOTLAND'S WEALTH", "yellow", 890, 0.35, 56)], grain=True)],
   hl=["a fifth"]),
 L("July 1698: five ships, 1,200 settlers leave Leith.", [
   full(D + "Paul Hardy - Scene of the departure from Leith of the Darien expedition, AD 1698.jpg",
        "Departure from Leith, Paul Hardy" + PD,
        [S("JULY 1698", "white", 760, 0.1, 62), S("5 SHIPS · 1,200 SETTLERS", "yellow", 890, 0.3, 60)], grain=True),
   full(DP + "21528.mp4", items=[S("DESTINATION: DARIEN", "white", 880, 0.1, 62)])],
   hl=["1,200"], say="July sixteen ninety-eight: five ships, twelve hundred settlers leave Leith."),
 L("They build New Edinburgh. Then fever strikes.", [
   full(D + DM, "Plan of the Scots settlement, 1743" + PD,
        [S("NEW EDINBURGH", "yellow", 760, 0.1, 70)], grain=True),
   full(DP + "109726.mp4", items=[S("UP TO 10 DEATHS A DAY", "red", 880, 0.1, 64)], dim=0.2)],
   hl=["fever"]),
 L("England's king orders his colonies not to help.", [
   full(DP + "197439.mp4", items=[S("WILLIAM III", "white", 760, 0.1, 64), S("NO SUPPLIES FOR THE SCOTS", "red", 890, 0.35, 60)], bw=True, dim=0.2)],
   hl=["not to help."]),
 L("July 1699: abandoned. Only 300 of 1,200 survive.", [
   full(DP + "3588.mp4", items=[S("JULY 1699: ABANDONED", "red", 880, 0.1, 70)], bw=True, flash=0.3),
   board(DP + "39270.mp4", [S("FIRST EXPEDITION", "white", 400, 0.0, 50), S("SETTLERS", "yellow", 490, 0.2, 44)],
         points=[1200, 300], show_from=0, show_to=1, red_from=0, labels={"0": "1,200", "1": "300"})],
   big=True, big_at=0.3, big_sfx="crash", drop=True, hl=["300"],
   say="July sixteen ninety-nine: abandoned. Only three hundred of twelve hundred survive."),
 L("The twist? The 1707 Union paid out, partly for Darien.", [
   full(D + "Edinburgh in the 17thC (detail) by Wenceslas Hollar (1670).jpg", "Edinburgh, Wenceslas Hollar, 1670" + PD,
        [S("1707: ACT OF UNION", "white", 760, 0.1, 62), S("£398,085 \"EQUIVALENT\"", "yellow", 890, 0.4, 62)], bw=True, grain=True)],
   twist=True, hl=["paid out,"], sfx=[["slam", 1.3]],
   say="The twist? The seventeen-oh-seven Union paid out, partly for Darien."),
 OUT("fall")]}

# ---------------------------------------------------------------- 25 Salad oil swindle
A = "images/25_saladoil/"; AP = A + "pixabay_"
salad = {"id": "25_saladoil_v3", "style": "v3", "format": "THE SCAM", "lead_in": 0.06, "speed": 1.05, "voice": "af_heart", "pause": 0.25, "lines": [
 L("1.8 billion pounds of salad oil. Barely 100 million existed.", [
   full(AP + "342185.mp4", items=[S("1.8 BILLION LB CLAIMED", "yellow", 760, 0.1, 64), S("≈100 MILLION FOUND", "red", 890, 0.35, 70)]),
   full(A + "Constable Hook tanks jeh.jpg", "Oil tanks, Constable Hook, Bayonne (today)" + PD,
        [S("BAYONNE, NEW JERSEY", "white", 880, 0.1, 62)], dim=0.2)],
   hl=["1.8 billion", "100 million"], sfx=[["slam", 0.05]],
   say="One point eight billion pounds of salad oil. Barely a hundred million existed."),
 L("Tino De Angelis runs a vegetable oil refinery in Bayonne.", [
   full(A + "Anthony \"Tino\" De Angelis.png", "Tino De Angelis" + PD,
        [S("TINO DE ANGELIS", "white", 760, 0.1, 66), S("ALLIED CRUDE VEGETABLE OIL", "yellow", 890, 0.35, 54)], bw=True, grain=True, cy=0.35)],
   hl=["Bayonne."]),
 L("His tanks hold mostly water, with oil floating on top.", [
   full(AP + "190323.mp4", items=[S("MOSTLY WATER", "red", 760, 0.1, 76), S("A SLICK OF OIL ON TOP", "white", 890, 0.35, 58)], dim=0.15)],
   hl=["water,"]),
 L("Pipes move the same oil from tank to tank.", [
   full(AP + "43629.mp4", items=[S("TANKS LINKED BY PIPES", "white", 760, 0.1, 58), S("SAME OIL, COUNTED TWICE", "yellow", 890, 0.35, 58)])],
   hl=["same oil"]),
 L("An American Express subsidiary vouches for it. Loans follow.", [
   full(AP + "13047.mp4", items=[S("AMERICAN EXPRESS WAREHOUSING", "white", 760, 0.1, 50), S("WAREHOUSE RECEIPTS", "yellow", 890, 0.35, 64)]),
   full(A + "NY stock exchange traders floor LC-U9-10548-6.jpg", "NYSE floor, 1960s" + LOC,
        [S("BROKERS LEND ON THE OIL", "white", 880, 0.1, 58)], bw=True, grain=True)],
   hl=["vouches"]),
 L("November 1963: soybean oil cracks. His company goes bankrupt.", [
   full(AP + "33805.mp4", items=[S("NOVEMBER 19, 1963", "white", 760, 0.1, 60), S("BANKRUPT", "red", 890, 0.3, 96)], flash=0.3),
   board(AP + "274449.mp4", [S("SOYBEAN OIL PRICE", "white", 400, 0.0, 48), S("NOV 15 → NOV 19, 1963", "yellow", 490, 0.2, 44)],
         points=[9.875, 9, 7.75], show_from=0, show_to=2, red_from=0, labels={"0": "9.875", "1": "9", "2": "7.75"})],
   big=True, big_at=0.3, big_sfx="crash", drop=True, hl=["bankrupt."],
   say="November nineteen sixty-three: soybean oil cracks. His company goes bankrupt."),
 L("The twist? AmEx stock plunges, and Warren Buffett buys 5 percent.", [
   full(AP + "166289.mp4", items=[S("AMEX: $65 → $37", "red", 760, 0.1, 70), S("BUFFETT BUYS 5%", "yellow", 890, 0.4, 76)], dim=0.15)],
   twist=True, hl=["5 percent."], sfx=[["slam", 1.3]],
   say="The twist? Amex stock plunges, and Warren Buffett buys five percent."),
 OUT("scam")]}

for sp in (florida, overend, panic, darien, salad):
    json.dump(sp, open(f"specs/{sp['id']}.json", "w"), indent=1, ensure_ascii=False)
    print("wrote", sp["id"])
