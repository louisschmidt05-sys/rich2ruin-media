"""v3.1 specs (~30 s) for 10-16 Dec 2026: Japan's bubble (1989-90), Kerviel / Société Générale (2008),
Allen Stanford (2009-12), Northern Rock (2007-08), Medici Bank (1397-1494).
Facts checked 2026-11-28 (en.wikipedia.org not used; sources loaded through the web-fetch agent):
- Japan: nippon.com (record close 38,915.87 on 29 Dec 1989; first beaten 22 Feb 2024 at 39,098.68, "34 years and
  2 months"; post-bubble low 7,054.98 in March 2009 -> -81.9% computed), dawn.com/AFP (index quadrupled 1985-89, golf
  club memberships cost millions of dollars, Nikkei roughly halved in 1990, property prices fell sharply),
  qz.com (banks wrote off some 100 trillion yen of bad debts), japantimes.co.jp, aljazeera.com.
- Kerviel: societegenerale.com (positions ~€50bn, more than the bank's total capital; final loss €4.9bn),
  nbcnews.com (loss unwinding positions in January 2008; 5 Oct 2010 five years with two suspended, repay €4.9bn),
  cityam.com (forgery, breach of trust, unauthorised computer use), jurist.org (2014 Cour de cassation upheld the
  conviction, overruled the €4.9bn damages).
- Stanford: justice.gov (14 June 2012, 110 years; convicted 6 March 2012 on 13 of 14 counts; CDs from Stanford
  International Bank, Antigua, premium over US CDs; 112-foot yacht, six private planes; property value inflated
  5,000% to $3.1bn), aljazeera.com (30,000 investors in 100+ countries, knighted by Antigua 2006, SEC charged him
  Feb 2009), npr.org ($20 million paid to winners of one cricket tournament in Antigua), money.cnn.com ($7bn fraud).
- Northern Rock: wikiwand Northern_Rock (14 Sept 2007 liquidity support from the Bank of England; first UK run in
  150 years; borrowed short term on wholesale markets, lent long term; shares lost over 90% before nationalisation;
  nationalised 22 Feb 2008), irishtimes.com (fifth-largest UK mortgage lender; loans up to 125% of a home's value),
  britac.ac.uk (run stopped only when the government guaranteed deposits), thenationalnews.com (queues 14 Sept).
- Medici: wikiwand Medici_Bank (founding usually dated 1397, Giovanni di Bicci; largest bank in Europe in its prime;
  Rome branch held papal deposits; London liquidation 1478, losses 51,533 gold florins, Edward IV unable to repay
  after the Wars of the Roses; Bruges: bad debts of Charles the Bold, liquidated 1478; Lorenzo relied on Sassetti,
  interest in politics and art; 1494 invasion of Charles VIII, assets seized; central Florentine banco burned by a mob),
  brewminate.com (Rome branch managed papal finances; Piero's exile 1494)."""
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
def head(id_, fmt, lines):
    return {"id": id_, "style": "v3", "format": fmt, "lead_in": 0.06, "speed": 1.05, "voice": "af_heart", "pause": 0.25, "lines": lines}
PD = " · public domain"

# ---------------------------------------------------------------- 26 Japan
J = "images/26_japan/"; JP = J + "pixabay_"
japan = head("26_japan_v3", "THE CRASH", [
 L("Japan's stock market: 38,915 to 7,054. Over 80% gone.", [
   full(JP + "256109.mp4", items=[S("NIKKEI 38,915 (1989)", "white", 760, 0.1, 64), S("→ 7,054 (2009)", "red", 890, 0.3, 84)]),
   full(JP + "338956.mp4", items=[S("-80%", "red", 880, 0.1, 110)]),
   full(JP + "211067.mp4"),
   full(J + "Outside Tokyo Stock Exchange (98572).jpg", "Tokyo Stock Exchange (today)" + PD)],
   hl=["38,915", "7,054."], sfx=[["slam", 0.05]],
   say="Japan's stock market: thirty-eight thousand, to seven thousand. Over eighty percent gone."),
 L("1985 to 1989: Japanese stocks quadruple.", [
   full(JP + "246618.mp4", items=[S("1985 → 1989", "white", 760, 0.1, 64), S("STOCKS ×4", "yellow", 890, 0.3, 90)]),
   full(JP + "88697.mp4"),
   full(JP + "380567.mp4")],
   hl=["quadruple."], say="Nineteen eighty-five to eighty-nine: Japanese stocks quadruple."),
 L("Golf club memberships sold for millions of dollars.", [
   full(JP + "214267.mp4", items=[S("GOLF CLUB MEMBERSHIP", "white", 760, 0.1, 58), S("MILLIONS OF DOLLARS", "yellow", 890, 0.3, 66)]),
   full(JP + "41828.mp4"),
   full(JP + "52890.mp4")],
   hl=["millions"]),
 L("December 29, 1989: the Nikkei closes at a record.", [
   full(JP + "20851.mp4", items=[S("DECEMBER 29, 1989", "white", 760, 0.1, 60), S("RECORD: 38,915.87", "yellow", 890, 0.3, 70)]),
   full(JP + "204306.mp4"),
   full(J + "Inside Tokyo Stock Exchange (65002).jpg", "Tokyo Stock Exchange (today)" + PD),
   full(JP + "41957.mp4")],
   hl=["record."], say="December twenty-ninth, nineteen eighty-nine: the Nikkei closes at a record."),
 L("In 1990, it roughly halves. Property prices fall sharply.", [
   full(JP + "166289.mp4", items=[S("1990", "white", 760, 0.1, 70), S("NIKKEI ≈ HALVED", "red", 890, 0.3, 84)], flash=0.3),
   full(JP + "5278.mp4", items=[S("PROPERTY FALLS", "red", 880, 0.1, 76)], dim=0.15),
   full(JP + "154401.mp4"),
   full(JP + "147893.mp4")],
   big=True, big_at=0.3, big_sfx="crash", drop=True, hl=["halves."],
   say="In nineteen ninety, it roughly halves. Property prices fall sharply."),
 L("Banks write off about 100 trillion yen of bad debts.", [
   full(JP + "3134.mp4", items=[S("BAD DEBTS WRITTEN OFF", "white", 760, 0.1, 58), S("≈ ¥100 TRILLION", "red", 890, 0.3, 80)]),
   full(JP + "1046.mp4"),
   board(JP + "213815.mp4", [S("NIKKEI 225", "white", 400, 0.0, 48), S("1989 → 2009 → 2024", "yellow", 490, 0.2, 44)],
         points=[38915.87, 7054.98, 39098.68], show_from=0, show_to=2, red_from=0,
         labels={"0": "38,915", "1": "7,054", "2": "39,098"})],
   hl=["100 trillion"], say="Banks write off about a hundred trillion yen of bad debts."),
 L("The twist? The 1989 record only fell in February 2024.", [
   full(JP + "240973.mp4", items=[S("FEBRUARY 22, 2024", "white", 760, 0.1, 60), S("34 YEARS LATER", "yellow", 890, 0.4, 80)]),
   full(JP + "181114.mp4"),
   full(JP + "243075.mp4"),
   full(JP + "19627.mp4")],
   twist=True, hl=["February 2024."], sfx=[["slam", 1.3]],
   say="The twist? The nineteen eighty-nine record only fell in February twenty twenty-four."),
 OUT("crash")])

# ---------------------------------------------------------------- 27 Kerviel
K = "images/27_kerviel/"; KP = K + "pixabay_"
kerviel = head("27_kerviel_v3", "RICH TO RUIN", [
 L("One trader. €50 billion in secret bets. €4.9 billion lost.", [
   full(KP + "204291.mp4", items=[S("ONE TRADER", "white", 760, 0.1, 70), S("€4.9 BILLION LOST", "red", 890, 0.3, 80)]),
   full(KP + "263397.mp4", items=[S("€50 BILLION IN BETS", "yellow", 880, 0.1, 72)]),
   full(KP + "153455.mp4"),
   full(KP + "3819.mp4")],
   hl=["€50 billion", "€4.9 billion"], sfx=[["slam", 0.05]],
   say="One trader. Fifty billion euros in secret bets. Four point nine billion lost."),
 L("Jérôme Kerviel is a trader at Société Générale, Paris.", [
   full(KP + "8132.mp4", items=[S("SOCIÉTÉ GÉNÉRALE", "white", 760, 0.1, 64), S("LA DÉFENSE, PARIS", "yellow", 890, 0.3, 60)]),
   full(KP + "282564.mp4"),
   full(KP + "10822.mp4", items=[S("JÉRÔME KERVIEL", "white", 880, 0.1, 66)])],
   hl=["Société Générale,"], say="Jérôme Kerviel is a trader at Société Générale, in Paris."),
 L("His positions reach €50 billion: more than the bank's capital.", [
   full(KP + "133501.mp4", items=[S("≈ €50 BILLION", "yellow", 760, 0.1, 80), S("> THE BANK'S CAPITAL", "red", 890, 0.3, 70)]),
   board(KP + "14900.mp4", [S("ONE DESK", "white", 640, 0.05, 60), S("↓", "yellow", 760, 0.25, 60),
         S("€50 BILLION OF POSITIONS", "yellow", 880, 0.4, 58), S("↓", "yellow", 1000, 0.6, 60),
         S("> THE BANK'S TOTAL CAPITAL", "red", 1120, 0.75, 56)]),
   full(KP + "5395.mp4")],
   hl=["€50 billion:"], say="His positions reach fifty billion euros: more than the bank's capital."),
 L("January 2008: the bank finds them and unwinds them all.", [
   full(KP + "106217.mp4", items=[S("JANUARY 2008", "white", 760, 0.1, 66), S("SELL EVERYTHING", "red", 890, 0.3, 76)], dim=0.15),
   full(KP + "43559.mp4"),
   full(KP + "256977.mp4")],
   hl=["unwinds"], say="January two thousand eight: the bank finds them and unwinds them all."),
 L("The final bill: €4.9 billion.", [
   full(KP + "139336.mp4", items=[S("FINAL LOSS", "white", 760, 0.1, 70), S("€4.9 BILLION", "red", 890, 0.3, 100)], flash=0.3),
   full("images/26_japan/pixabay_166289.mp4"),
   full("images/25_saladoil/pixabay_33805.mp4")],
   big=True, big_at=0.3, big_sfx="crash", drop=True, hl=["€4.9 billion."],
   say="The final bill: four point nine billion euros."),
 L("2010: guilty, and ordered to repay €4.9 billion.", [
   full(KP + "162047.mp4", items=[S("OCTOBER 5, 2010: GUILTY", "white", 760, 0.1, 58), S("5 YEARS, 2 SUSPENDED", "yellow", 890, 0.3, 64)]),
   full(KP + "74491.mp4", items=[S("ORDERED TO REPAY €4.9 BILLION", "red", 880, 0.1, 54)]),
   full(KP + "1656.mp4")],
   hl=["guilty."], say="Twenty ten: guilty, and ordered to repay four point nine billion."),
 L("The twist? In 2014, France's top court scrapped that bill.", [
   full(KP + "188535.mp4", items=[S("COUR DE CASSATION, 2014", "white", 760, 0.1, 56), S("€4.9BN DAMAGES OVERTURNED", "yellow", 890, 0.4, 58)]),
   full(KP + "51721.mp4"),
   full(KP + "8246.mp4")],
   twist=True, hl=["scrapped"], sfx=[["slam", 1.3]],
   say="The twist? In twenty fourteen, France's top court scrapped that bill."),
 OUT("fall")])

# ---------------------------------------------------------------- 28 Stanford
T = "images/28_stanford/"; TP = T + "pixabay_"
stanford = head("28_stanford_v3", "THE SCAM", [
 L("Sentenced to 110 years for a $7 billion fraud.", [
   full(TP + "254922.mp4", items=[S("110 YEARS", "red", 760, 0.1, 100), S("$7 BILLION FRAUD", "yellow", 890, 0.3, 76)]),
   full(TP + "198751.mp4"),
   full(TP + "54904.mp4")],
   hl=["110 years", "$7 billion"], sfx=[["slam", 0.05]],
   say="Sentenced to a hundred and ten years, for a seven billion dollar fraud."),
 L("Allen Stanford's bank sits on the island of Antigua.", [
   full(TP + "7262.mp4", items=[S("STANFORD INTERNATIONAL BANK", "white", 760, 0.1, 52), S("ANTIGUA", "yellow", 890, 0.3, 84)]),
   full(T + "STJOHNS1", "St. John's, Antigua, postcard c. 1908" + PD, [S("ALLEN STANFORD", "white", 880, 0.1, 66)], grain=True),
   full(TP + "142213.mp4")],
   hl=["Antigua."]),
 L("Its CDs pay more than US banks. 30,000 investors buy.", [
   full(TP + "20857.mp4", items=[S("CERTIFICATES OF DEPOSIT", "white", 760, 0.1, 56), S("ABOVE US BANK RATES", "yellow", 890, 0.3, 62)]),
   full(TP + "7277.mp4", items=[S("30,000 INVESTORS", "yellow", 760, 0.1, 72), S("100+ COUNTRIES", "white", 890, 0.3, 66)]),
   board(TP + "164394.mp4", [S("INVESTORS BUY CDs", "white", 640, 0.05, 60), S("↓", "yellow", 760, 0.25, 60),
         S("STANFORD'S BANK", "yellow", 880, 0.4, 64), S("↓  DIVERTED (PROSECUTORS)", "yellow", 1000, 0.6, 52),
         S("HIS BUSINESSES & LIFESTYLE", "red", 1120, 0.75, 54)])],
   hl=["30,000"], say="Its CDs pay more than U.S. banks. Thirty thousand investors buy."),
 L("Antigua knights him. He pays $20 million to cricket winners.", [
   full(T + "STJOHNS2", "St. John's, Antigua, postcard c. 1908" + PD, [S("KNIGHTED BY ANTIGUA, 2006", "white", 880, 0.1, 58)], grain=True),
   full(TP + "139865.mp4", items=[S("ONE CRICKET TOURNAMENT", "white", 760, 0.1, 58), S("$20 MILLION TO WINNERS", "yellow", 890, 0.3, 66)]),
   full(TP + "189845.mp4")],
   hl=["$20 million"], say="Antigua knights him. He pays twenty million dollars to cricket winners."),
 L("Investors' money buys a yacht and six private planes.", [
   full(TP + "119442.mp4", items=[S("A YACHT...", "yellow", 880, 0.1, 76)]),
   full(TP + "51021.mp4", items=[S("SIX PRIVATE PLANES", "yellow", 880, 0.1, 72)]),
   full(TP + "31660.mp4"),
   full(TP + "119436.mp4")],
   hl=["six private planes."], say="Investors' money buys a yacht, and six private planes."),
 L("February 2009: the SEC charges him with fraud.", [
   full(TP + "208082.mp4", items=[S("FEBRUARY 2009", "white", 760, 0.1, 66), S("CHARGED WITH FRAUD", "red", 890, 0.3, 74)], flash=0.3, dim=0.15),
   full(TP + "198755.mp4"),
   full(TP + "110737.mp4", items=[S("MARCH 2012: GUILTY, 13 OF 14 COUNTS", "white", 880, 0.1, 50)])],
   big=True, big_at=0.3, big_sfx="crash", drop=True, hl=["fraud."],
   say="February two thousand nine: the S.E.C. charges him with fraud."),
 L("The twist? One property was inflated 5,000%, to $3.1 billion.", [
   full(TP + "154199.mp4", items=[S("VALUE INFLATED 5,000%", "red", 760, 0.1, 66), S("→ $3.1 BILLION", "yellow", 890, 0.4, 76)]),
   full(TP + "154197.mp4"),
   full(TP + "315758.mp4"),
   full(T + "Antigua - Market Wharf, St. Johns.jpg", "Market Wharf, St. John's, Antigua, c. 1908" + PD, grain=True),
   full(TP + "37885.mp4")],
   twist=True, hl=["5,000%,"], sfx=[["slam", 1.3]],
   say="The twist? One property was inflated five thousand percent, to three point one billion dollars."),
 OUT("scam")])

# ---------------------------------------------------------------- 29 Northern Rock
N = "images/29_northernrock/"; NP = N + "pixabay_"
rock = head("29_northernrock_v3", "THE CRASH", [
 L("September 2007: Britain's first bank run in 150 years.", [
   full(NP + "6387.mp4", items=[S("SEPTEMBER 14, 2007", "white", 760, 0.1, 60), S("FIRST UK BANK RUN IN 150 YEARS", "red", 890, 0.3, 54)]),
   full(NP + "28227.mp4", items=[S("NORTHERN ROCK", "yellow", 880, 0.1, 80)]),
   full(NP + "149927.mp4")],
   hl=["150 years."], sfx=[["slam", 0.05]],
   say="September two thousand seven: Britain's first bank run in a hundred and fifty years."),
 L("Northern Rock is the UK's fifth-biggest mortgage lender.", [
   full(NP + "1400.mp4", items=[S("NEWCASTLE UPON TYNE", "white", 760, 0.1, 60), S("Nº5 UK MORTGAGE LENDER", "yellow", 890, 0.3, 62)]),
   full(NP + "189742.mp4"),
   full(NP + "216041.mp4")],
   hl=["fifth-biggest"], say="Northern Rock is the U.K.'s fifth-biggest mortgage lender."),
 L("It borrows short-term on money markets, not from savers.", [
   full(NP + "315480.mp4", items=[S("SHORT-TERM WHOLESALE MONEY", "yellow", 880, 0.1, 56)]),
   board(NP + "177850.mp4", [S("SHORT-TERM MONEY MARKETS", "white", 640, 0.05, 54), S("↓", "yellow", 760, 0.25, 60),
         S("NORTHERN ROCK", "yellow", 880, 0.4, 66), S("↓", "yellow", 1000, 0.6, 60),
         S("LONG-TERM MORTGAGES", "white", 1120, 0.75, 58)]),
   full(NP + "108296.mp4")],
   hl=["short-term"], say="It borrows short-term on money markets, not from savers."),
 L("Some of its loans reach 125% of a home's value.", [
   full(NP + "125777.mp4", items=[S("UP TO 125%", "red", 760, 0.1, 90), S("OF THE HOME'S VALUE", "white", 890, 0.3, 64)]),
   full(NP + "9486.mp4"),
   full(NP + "114254.mp4")],
   hl=["125%"], say="Some of its loans reach a hundred and twenty-five percent of a home's value."),
 L("September 14: it needs emergency help from the Bank of England.", [
   full(NP + "176408.mp4", items=[S("SEPTEMBER 14, 2007", "white", 760, 0.1, 60), S("BANK OF ENGLAND SUPPORT", "yellow", 890, 0.3, 62)]),
   full(NP + "291720.mp4"),
   full(NP + "27023.mp4")],
   hl=["emergency help"], say="September fourteenth: it needs emergency help from the Bank of England."),
 L("Savers queue outside branches. Shares lose over 90%.", [
   full(NP + "3627.mp4", items=[S("QUEUES AT THE BRANCHES", "white", 760, 0.1, 60), S("SHARES -90%", "red", 890, 0.3, 90)], flash=0.3),
   full(NP + "36510.mp4"),
   full(NP + "21543.mp4"),
   full(NP + "174262.mp4")],
   big=True, big_at=0.3, big_sfx="crash", drop=True, hl=["over 90%."],
   say="Savers queue outside branches. Shares lose over ninety percent."),
 L("The twist? By February 2008, taxpayers own the bank.", [
   full(NP + "1204.mp4", items=[S("FEBRUARY 22, 2008", "white", 760, 0.1, 60), S("NATIONALISED", "yellow", 890, 0.4, 84)]),
   full(NP + "28693.mp4"),
   full(NP + "28226.mp4")],
   twist=True, hl=["taxpayers"], sfx=[["slam", 1.3]],
   say="The twist? By February two thousand eight, taxpayers own the bank."),
 OUT("crash")])

# ---------------------------------------------------------------- 30 Medici
M = "images/30_medici/"; MP = M + "pixabay_"
medici = head("30_medici_v3", "RICH TO RUIN", [
 L("Europe's biggest bank lost 51,533 gold florins in London alone.", [
   full(M + "EDWARD", "King Edward IV, c. 1540" + PD, [S("KING EDWARD IV", "white", 760, 0.1, 66), S("MEDICI LOSS: 51,533 FLORINS", "red", 890, 0.3, 60)], grain=True, cy=0.3),
   full(MP + "29731.mp4", items=[S("EUROPE'S BIGGEST BANK", "yellow", 880, 0.1, 66)]),
   full(MP + "13679.mp4")],
   hl=["51,533"], sfx=[["slam", 0.05]],
   say="Europe's biggest bank lost fifty-one thousand gold florins in London alone."),
 L("Florence, 1397: Giovanni di Bicci de' Medici founds it.", [
   full(M + "GIOVANNI", "Giovanni di Bicci, Bronzino workshop" + PD, [S("FLORENCE, 1397", "white", 760, 0.1, 66), S("GIOVANNI DI BICCI", "yellow", 890, 0.3, 64)], cy=0.3),
   full(MP + "292819.mp4"),
   full(M + "KETTENPLAN", "View of Florence, c. 1500" + PD, grain=True)],
   hl=["1397:"], say="Florence, thirteen ninety-seven: Giovanni di Bicci de' Medici founds it."),
 L("It banks for the Pope, from London to Bruges.", [
   full(MP + "107189.mp4", items=[S("BANKER TO THE POPE", "yellow", 880, 0.1, 70)]),
   board(MP + "207982.mp4", [S("ROME · VENICE · MILAN · PISA", "white", 680, 0.05, 54), S("GENEVA · LYON · AVIGNON", "white", 800, 0.3, 54),
         S("LONDON · BRUGES", "yellow", 920, 0.55, 64)]),
   full(MP + "56452.mp4")],
   hl=["the Pope,"]),
 L("Then Lorenzo the Magnificent prefers politics and art.", [
   full(M + "LORENZO", "Lorenzo de' Medici, Vasari" + PD, [S("LORENZO THE MAGNIFICENT", "white", 880, 0.1, 58)], cy=0.3),
   full(MP + "143419.mp4", items=[S("THE BANK IS NEGLECTED", "red", 880, 0.1, 62)]),
   full(MP + "325497.mp4")],
   hl=["politics and art."]),
 L("Kings default: Edward IV in London, Charles the Bold in Bruges.", [
   full(M + "CAXTON", "Edward IV, presentation miniature, c. 1480" + PD, [S("LONDON CLOSED, 1478", "red", 880, 0.1, 66)]),
   full(M + "CHARLES", "Charles the Bold, Rogier van der Weyden" + PD, [S("CHARLES THE BOLD", "white", 760, 0.1, 64), S("BRUGES: BAD DEBTS", "red", 890, 0.3, 66)], cy=0.3),
   full(MP + "192011.mp4")],
   hl=["Kings default:"]),
 L("1494: France invades. The Medici flee. The bank is seized.", [
   full(M + "GRANACCI", "Entry of Charles VIII into Florence, Granacci" + PD, [S("1494", "white", 760, 0.1, 76), S("BANK SEIZED", "red", 890, 0.3, 90)], flash=0.3),
   full(MP + "38998.mp4"),
   full(M + "BEZZUOLI", "Entry of Charles VIII into Florence, Bezzuoli, 1829" + PD, [S("THE MEDICI FLEE", "yellow", 880, 0.1, 70)]),
   full(MP + "53834.mp4")],
   big=True, big_at=0.3, big_sfx="crash", drop=True, hl=["seized."],
   say="Fourteen ninety-four: France invades. The Medici flee. The bank is seized."),
 L("The twist? A mob burned its Florence headquarters.", [
   full(MP + "236711.mp4", items=[S("FLORENCE HEADQUARTERS", "white", 760, 0.1, 60), S("BURNED BY A MOB", "red", 890, 0.4, 76)]),
   full(MP + "2173.mp4"),
   full(MP + "210104.mp4")],
   twist=True, hl=["burned"], sfx=[["slam", 1.3]]),
 OUT("fall")])

if __name__ == "__main__":
    import sys
    names = json.load(open(sys.argv[1])) if len(sys.argv) > 1 else {}
    for spec in (japan, kerviel, stanford, rock, medici):
        txt = json.dumps(spec, indent=1, ensure_ascii=False)
        for k, v in names.items():
            txt = txt.replace(f'/{k}"', "/" + json.dumps(v)[1:])
        json.dump(json.loads(txt), open(f"specs/{spec['id']}.json", "w"), indent=1, ensure_ascii=False)
        print("wrote", spec["id"])
