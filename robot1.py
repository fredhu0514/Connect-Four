import playGround
import human
import copy
import time

ifMyTurn = human.ifMyTurn
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
    playGround.initProcessorTXT()
    mySide = args
    isWin = False
    while not isWin:
        time.sleep(3)
        if ifMyTurn(mySide):
            f = open(playGround.path_current_game_state, 'r')
            f.readline()
            curTurn = eval(f.readline())
            gS = eval(f.readline())

            sideSTR = ""
            if mySide == 1:
                sideSTR = "=================== RED ==================\n"
            elif mySide == -1:
                sideSTR = "================== YELLOW ================\n"
            # print(sideSTR + "Turn " + (str)(curTurn) + ".\n")
            playGround.printGS(gS)
            chooseCol, updatedGS = chooseColumn(mySide, gS)

            # Write the game.txt file
            playGround.updateFileInfo(curTurn + 1, chooseCol, mySide, updatedGS, playGround.path_all_games)

            # Judge who wins
            winner = playGround.isWin(updatedGS)
            if winner != 0:
                isWin = True
                playGround.gameEnds(winner, updatedGS)
                break

            # If no winners but the board is full
            if playGround.isFull(updatedGS):
                playGround.writeDraw()
                break

    # print("<<<<<<<<<<<<<<<< GAME OVER >>>>>>>>>>>>>>>\n\n\n\n\n")

if __name__ == "__main__":
    args = chooseSide()
    play(args)

# def test2():
#     putYel = playGround.putYel
#     putRed = playGround.putRed
#     gS = playGround.init_gameState()
#     gS = putYel(gS, 1)
#     gS = putYel(gS, 1)
#     gS = putYel(gS, 1)
#
#     gS = putRed(gS, 2)
#     gS = putRed(gS, 2)
#     gS = putRed(gS, 2)
#     gS = putYel(gS, 2)
#     gS = putRed(gS, 2)
#
#     gS = putRed(gS, 3)
#     gS = putRed(gS, 3)
#     gS = putYel(gS, 3)
#     gS = putYel(gS, 3)
#     gS = putYel(gS, 3)
#     gS = putRed(gS, 3)
#
#     gS = putYel(gS, 4)
#     gS = putYel(gS, 4)
#     gS = putYel(gS, 4)
#     gS = putRed(gS, 4)
#
#     gS = putRed(gS, 5)
#     gS = putRed(gS, 5)
#     gS = putRed(gS, 5)
#     gS = putYel(gS, 5)
#     playGround.printGS(gS)
#     chooseColumn(1, gS)
