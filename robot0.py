# Most stupid robot
import playGround
import human
import copy
import time
import random
import sys

TXTpaths = [playGround.path_current_game_state, playGround.path_all_games, playGround.txt_file]

def chooseRoomNum(term=""):
    if term == "":
        term = input("Input your Room Number: ")
        print("\n")
        print("\n")
        print("\n")

        TXTpaths[0] += term + TXTpaths[2]
        TXTpaths[1] += term + TXTpaths[2]
        return None
    else:
        TXTpaths[0] += term + TXTpaths[2]
        TXTpaths[1] += term + TXTpaths[2]

def ifMyTurn(mySide):
    f = open(TXTpaths[0], 'r')
    line = f.readline()
    temp = eval(line)
    if temp == -mySide:
        return True
    return False

chooseSide = human.chooseSide

deepest_search_level = 0
GAMMA = 2

def fargmax(array):
    array = list(array)
    return array.index(max(array))

def fargmin(array):
    array = list(array)
    return array.index(min(array))

def getGAMMA(turn):
    return GAMMA ** (-((turn + 1) // 2))

def method(mySide):
    if mySide == 1:
        return playGround.putRed
    elif mySide == -1:
        return playGround.putYel
    else:
        return None

def nextStepWins(mySide, gS):
    print("Into nextStepWins 0")
    put = method(mySide)
    if not put:
        print("Out of nextStepWins 1")
        return []

    lst = []
    for i in range(0, 7):
        tempGS = put(copy.deepcopy(gS), i)
        if tempGS:
            if playGround.isWin(tempGS) == mySide:
                lst.append(i)
    print("Out of nextStepWins 2")
    return lst

def nextStepOpWins(mySide, gS):
    print("Into nextStepOpWins 0")
    put = method(-mySide)
    if not put:
        print("Out of nextStepOpWins 1")
        return []

    lst = []
    for i in range(0, 7):
        tempGS = put(copy.deepcopy(gS), i)
        if tempGS:
            if playGround.isWin(tempGS) == -mySide:
                lst.append(i)
    print("Out of nextStepOpWins 2")
    return lst

def nextnextStepOpWins(mySide, gS):
    print("Into nextnextStepOpWins 0")
    put = method(mySide)
    opPut = method(-mySide)
    if not (put and opPut):
        print("Out of nextnextStepOpWins 1")
        return []

    lst = []
    for i in range(0, 7):
        tempGS = put(copy.deepcopy(gS), i)
        if tempGS:
            for j in range(0, 7):
                newTempGS = put(copy.deepcopy(tempGS), j)
                if newTempGS:
                    if not nextStepOpWins(mySide, gS) and nextStepOpWins(mySide, tempGS):
                        lst.append(i)
    print("Out of nextnextStepOpWins 2")
    return lst

def randomlyChooseLegal(mySide, gS):
    print("Into randomlyChooseLegal 0")
    put = method(mySide)
    if not put:
        print("Out of randomlyChooseLegal 1")
        return None
    lst = []
    for i in range(0, 7):
        if put(copy.deepcopy(gS), i):
            lst.append(i)
    if len(lst) == 0:
        print("Out of randomlyChooseLegal 2")
        return None
    temp = random.randint(0, len(lst) - 1)
    print("Out of randomlyChooseLegal 3")
    return lst[temp]

def chooseColumnRAW(mySide, gS):
    print("Into randomlyChooseLegal 0")
    put = method(mySide)
    nextTurnWins = nextStepWins(mySide, gS)
    nextTurnOPWins = nextStepOpWins(mySide, gS)
    nextnextTurnOPWins = nextnextStepOpWins(mySide, gS)

    if nextTurnWins:
        colIndex = random.randint(0, len(nextTurnWins) - 1)
        print("Out of chooseColumnRAW 1")
        return nextTurnWins[colIndex]
    elif nextTurnOPWins:
        colIndex = random.randint(0, len(nextTurnOPWins) - 1)
        print("Out of chooseColumnRAW 2")
        return nextTurnOPWins[colIndex]
    elif nextnextTurnOPWins:
        if len(nextnextTurnOPWins) == 7:
            print("Out of chooseColumnRAW 3")
            return randomlyChooseLegal(mySide, gS)
        else:
            avaiLST = []
            for i in range(0, 7):
                if i not in nextnextTurnOPWins:
                    avaiLST.append(i)
            possibleLST = []
            for i in avaiLST:
                if put(copy.deepcopy(gS), i):
                    possibleLST.append(i)
            if len(possibleLST):
                temp = random.randint(0, len(possibleLST) - 1)
                print("Out of chooseColumnRAW 4")
                return possibleLST[temp]
            else:
                print("Out of chooseColumnRAW 5")
                return randomlyChooseLegal(mySide, gS)
    else:
        print("Out of chooseColumnRAW 6")
        return randomlyChooseLegal(mySide, gS)

def chooseColumn(mySide, gS):
    print("Into of chooseColumnRAW 0")
    put = method(mySide)
    col = chooseColumnRAW(mySide, gS)
    print("Out of chooseColumnRAW 1")
    return col, put(gS, col)


def play(args=""):
    # Main Function
    playGround.initProcessorTXT(TXTpaths[0])
    mySide = args
    isWin = False
    while not isWin:
        time.sleep(3)
        if ifMyTurn(mySide):
            f = open(TXTpaths[0], 'r')
            f.readline()
            curTurn = eval(f.readline())
            gS = eval(f.readline())

            sideSTR = ""
            if mySide == 1:
                sideSTR = "=================== RED ==================\n"
            elif mySide == -1:
                sideSTR = "================== YELLOW ================\n"
            playGround.printGS(gS)
            chooseCol, updatedGS = chooseColumn(mySide, gS)

            # Write the game.txt file
            playGround.updateFileInfo(curTurn + 1, chooseCol, mySide, updatedGS, TXTpaths[1], TXTpaths[0])

            # Judge who wins
            winner = playGround.isWin(updatedGS)
            if winner != 0:
                isWin = True
                playGround.gameEnds(winner, updatedGS, TXTpaths[0])
                break

            # If no winners but the board is full
            if playGround.isFull(updatedGS):
                playGround.writeDraw(TXTpaths[0], TXTpaths[1])
                break

if __name__ == "__main__":
    terms = sys.argv[1:]
    roomNum = terms[0]
    playerTurn = terms[1]
    playerTurn = eval(playerTurn)

    chooseRoomNum(roomNum)
    args = chooseSide(playerTurn)

    play(args)
