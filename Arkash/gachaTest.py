import json
import random

def roll(box):
    with open("droprates.json", 'r') as file:
        data = json.load(file)
        boxData = data[box]
        file.close()
    randomGen = random.random()
    probability = 0
    for drop in boxData:
        if probability <= randomGen <= probability + drop["droprate"]:
            print(drop["battler"])
            break
        else:
            probability += drop["droprate"]

for _ in range(100):
    roll("box1")