import playGround
import human
import copy
import time
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

# Expecti but max at the very top

INDEX_FILE_RED = "INDEX/ROBOT1/INDEX_RED.txt"
INDEX_FILE_YEL = "INDEX/ROBOT1/INDEX_YEL.txt"

def ifMyTurn(mySide):
    f = open(TXTpaths[0], 'r')
    line = f.readline()
    temp = eval(line)
    if temp == -mySide:
        return True
    return False

chooseSide = human.chooseSide

deepest_search_level = 6
GAMMA = 2

def fargmax(array):
    array = list(array)
    return array.index(max(array))

def fargmin(array):
    array = list(array)
    return array.index(min(array))

def getGAMMA(turn):
    return GAMMA ** (-((turn + 1) // 2))

def chooseColumn(mySide, gS):
    dict = []
    method = 0
    if mySide == 1:
        method = playGround.putRed
    elif mySide == -1:
        method = playGround.putYel
    else:
        return 0
    for i in range(0, 7):
        temp = copy.deepcopy(gS)
        newGS = method(temp, i)
        if newGS:
            tp = evalFunc(newGS, 0, -mySide, mySide)
            toIndex(newGS, tp, mySide)
            print(i)
            print(tp)
            dict.append(tp)
        else:
            if mySide == 1:
                dict.append(-2.0)
            else:
                dict.append(2.0)
    col = None
    if mySide == 1:
        col = fargmax(dict)
    else:
        col = fargmin(dict)
    return col, method(gS, col)

def getSuccessors(gS, sideOfThisTurn):
    lst = []
    method = None
    if sideOfThisTurn == 1:
        method = playGround.putRed
    elif sideOfThisTurn == -1:
        method = playGround.putYel
    else:
        return lst
    for i in range(0, 7):
        temp = copy.deepcopy(gS)
        temp = method(temp, i)
        lst.append(temp)
    return lst

def evalFunc(gS, turn, sideOfThisTurn, mySide):
    if turn == deepest_search_level + 1:
        return 0.0

    gamma = getGAMMA(turn)
    wOT = playGround.isWin(gS)
    if wOT != 0:
        return gamma * wOT

    count = 0
    temp = 0.0
    flag_4_0TurnLost = False
    for i in getSuccessors(gS, sideOfThisTurn):
        if i:
            if turn == 0:
                seeOpWin = playGround.isWin(i)
                if seeOpWin != 0:
                    if mySide * seeOpWin < 0:
                        flag_4_0TurnLost = True
            temp += evalFunc(i, turn + 1, -sideOfThisTurn, mySide)
            count += 1
        else:
            temp += 0.0

    if count == 0:
        return 0.0
    else:
        if flag_4_0TurnLost:
            return (temp + (count * -mySide * 1.0)) / (count * 1.0)
        else:
            return temp / (count * 1.0)

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

def toIndex(gS, expectedValue, mySide):
    if mySide == 0:
        return None

    new_LIST = [gS, expectedValue, mySide]
    # Right after the red played
    if mySide == 1:
        rf = open(INDEX_FILE_RED, "r")
        line = rf.readline()
        while line:
            if eval(line)[0] == new_LIST[0]:
                return None
        f = open(INDEX_FILE_RED, "a")
        f.write((str)(new_LIST))
    # Right after the yellow played
    elif mySide == -1:
        rf = open(INDEX_FILE_YEL, "r")
        line = rf.readline()
        while line:
            if eval(line)[0] == new_LIST[0]:
                return None
        f = open(INDEX_FILE_YEL, "a")
        f.write((str)(new_LIST))
    return None

    # print("<<<<<<<<<<<<<<<< GAME OVER >>>>>>>>>>>>>>>\n\n\n\n\n")

if __name__ == "__main__":
    terms = sys.argv[1:]
    roomNum = terms[0]
    playerTurn = terms[1]
    playerTurn = eval(playerTurn)

    chooseRoomNum(roomNum)
    args = chooseSide(playerTurn)
    f1 = open(INDEX_FILE_RED, 'a')
    f2 = open(INDEX_FILE_YEL, 'a')
    play(args)
