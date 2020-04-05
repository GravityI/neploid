#The purpose of this program is to convert ydk files to JSON format.
import json

def ydkToDeck(fp):
    deck = {"main":{}, "extra":{}, "side":{}}
    with open(fp, "r") as file:
        extraIdx = 0
        sideIdx = 0
        lines = list(map(lambda x : x.strip('\n'), file.readlines()))
        for x in range(len(lines)):
            if lines[x] == "#extra":
                extraIdx = x
            elif lines[x] == "!side":
                sideIdx = x
                break
        for y in lines[2:extraIdx]:
            if not y in deck["main"].keys():
                deck["main"][y] = 1
            else:
                deck["main"][y] += 1
        if extraIdx != 0:
            for z in lines[extraIdx+1:sideIdx]:
                if not z in deck["extra"].keys():
                    deck["extra"][z] = 1
                else:
                    deck["extra"][z] += 1
        if sideIdx != 0:
            for v in lines[sideIdx+1:]:
                if not v in deck["side"].keys():
                    deck["side"][v] = 1
                else:
                    deck["side"][v] += 1
        file.close()
    return deck

def deckToYdk(deck, fp):
    with open(fp, "w") as file:
        decklist = "#created by ...\n#main\n"
        for card in deck["main"].items():
            for _ in range(card[1]):
                decklist += card[0] + "\n"
        decklist += "#extra\n"
        for card in deck["extra"].items():
            for _ in range(card[1]):
                decklist += card[0] + "\n"
        decklist += "!side\n"
        for card in deck["side"].items():
            for _ in range(card[1]):
                decklist += card[0] + "\n"
        file.write(decklist)
        file.close()

deckToYdk(ydkToDeck("data/ydk/Cyber Dragon 04_19 (Exordio).ydk"), "data/ydk/testDeck.ydk")