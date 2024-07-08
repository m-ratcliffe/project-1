from random import Random

def getPosition():
    var = Random()

    hole = var.choice(["A1", "A2", "A3", "A4", "B1", "B2", "B3", "B4", "C1", "C2", "C3", "C4", "D1", "D2", "D3", "D4"])
    stick = var.choice(["Blue", "Green", "Red", "Yellow"])
    position = "Place the " + stick + " Stick in Hole " + hole

    return position