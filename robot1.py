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

INDEX_FILE_RED = "INDEX/ROBOT1/4ROUND_INDEX_RED.txt"
INDEX_FILE_YEL = "INDEX/ROBOT1/4ROUND_INDEX_YEL.txt"
QUEUES = "INDEX/ROBOT1/__Files__/QUEUES.txt"
TOTALLINES = "INDEX/ROBOT1/__Files__/TOTALLINES.txt"
CURHEADER = "INDEX/ROBOT1/__Files__/CURHEADER.txt"

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
            tp = 0
            flag = False

            if mySide == 1:
                rf = open(INDEX_FILE_RED, 'r')
                line = rf.readline()
                while line:
                    line = eval(line)
                    if line[0] == newGS:
                        tp = line[1]
                        flag = True
                        break
                    line = rf.readline()
            elif mySide == -1:
                rf = open(INDEX_FILE_YEL, 'r')
                line = rf.readline()
                while line:
                    line = eval(line)
                    if line[0] == newGS:
                        tp = line[1]
                        flag = True
                        break
                    line = rf.readline()

            if flag:
                print("--==READ==--")
                print(i)
                print(tp)
                dict.append(tp)
            else:
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
            # tp = 0
            # flag = False
            # if sideOfThisTurn == 1:
            #     rf = open(INDEX_FILE_RED, 'r')
            #     line = rf.readline()
            #     while line:
            #         line = eval(line)
            #         if line[0] == i:
            #             tp = line[1]
            #             flag = True
            #             break
            #         line = rf.readline()
            # elif sideOfThisTurn == -1:
            #     rf = open(INDEX_FILE_YEL, 'r')
            #     line = rf.readline()
            #     while line:
            #         line = eval(line)
            #         if line[0] == i:
            #             tp = line[1]
            #             flag = True
            #             break
            #         line = rf.readline()
            # if not flag:
            #     tp = evalFunc(i, turn + 1, -sideOfThisTurn, mySide)
            #     toIndex(i, tp, sideOfThisTurn)
            tp = evalFunc(i, turn + 1, -sideOfThisTurn, mySide)
            temp += tp
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
            line = rf.readline()
        f = open(INDEX_FILE_RED, "a")
        f.write((str)(new_LIST) + "\n")
        rf.close()
        f.close()
    # Right after the yellow played
    elif mySide == -1:
        rf = open(INDEX_FILE_YEL, "r")
        line = rf.readline()
        while line:
            if eval(line)[0] == new_LIST[0]:
                return None
            line = rf.readline()
        f = open(INDEX_FILE_YEL, "a")
        f.write((str)(new_LIST) + "\n")
        rf.close()
        f.close()
    return None

    # print("<<<<<<<<<<<<<<<< GAME OVER >>>>>>>>>>>>>>>\n\n\n\n\n")
headerPTR = [0]
totalLines = [0]
def getCurHeader():
    f = open(CURHEADER, 'r')
    value = f.readline()
    if value:
        value = eval(value)
    else:
        value = 0
    headerPTR[0] = value

def writeCurHeader():
    f = open(CURHEADER, 'w')
    f.write((str)(headerPTR[0]) + '\n')

def getTotalLines():
    f = open(TOTALLINES, 'r')
    value = f.readline()
    if value:
        value = eval(value)
    else:
        value = 0
    totalLines[0] = value

def writeTotalLines():
    f = open(TOTALLINES, 'w')
    f.write((str)(totalLines[0]) + '\n')

def helperBFS(gS, side):
    print("In BFS helper")
    children = getSuccessors(gS, side)
    if children:
        for i in children:
            if i:
                if not prePureIndex(i, side):
                    q = open(QUEUES, 'a')
                    q.write((str)([i, side]) + "\n")
                    totalLines[0] += 1
                    writeTotalLines()
    print("Out BFS helper")

def getLineN(n, path):
    print("In getLineN")
    l = open(path, 'r')
    for i in range(0, headerPTR[0]):
        l.readline()
    line = l.readline()
    line = eval(line)
    headerPTR[0] += 1
    print("Out getLineN " + (str)(headerPTR[0]))
    return line


def ifFileEmpty():
    print("In ifFileEmpty")
    print("HEADPTR " + (str)(headerPTR[0]))
    print("TotalLINE " + (str)(totalLines[0]))
    if headerPTR[0] >= totalLines[0]:
        print("Out ifFileEmpty True")
        return True
    print("Out ifFileEmpty False")
    return False

def hasTheSate(tempGSandSide):
    side = tempGSandSide[1]
    if side == 1:
        rf = open(INDEX_FILE_RED, "r")
        line = rf.readline()
        while line:
            if eval(line)[0] == tempGSandSide[0]:
                return True
            line = rf.readline()
    else:
        rf = open(INDEX_FILE_YEL, "r")
        line = rf.readline()
        while line:
            if eval(line)[0] == tempGSandSide[0]:
                return True
            line = rf.readline()
    return False

SOME_PATH_RED = "RED.txt"
SOME_PATH_YEL = "YEL.txt"
def hasTheStateInPast(tempGSandSide):
    if tempGSandSide[1] == 1:
        f = open(SOME_PATH_RED, 'r')
        line = f.readline()
        while line:
            tempS = eval(line)
            if tempGSandSide[0] == tempS[0]:
                return tempS[1]
            line = f.readline()
    elif tempGSandSide[1] == -1:
        f = open(SOME_PATH_YEL, 'r')
        line = f.readline()
        while line:
            tempS = eval(line)
            if tempGSandSide[0] == tempS[0]:
                return tempS[1]
            line = f.readline()
    return None

def indexCreatorBFS(gS, side):
    print("In BFS indexCreator")
    helperBFS(gS, side)
    while not ifFileEmpty():
        tempGSandSide = getLineN(headerPTR[0], QUEUES)
        tp = "PLACE_HOLDER"
        if not hasTheSate(tempGSandSide):
            # When passes, the next line can be noted
            # tp = hasTheStateInPast(tempGSandSide)
            tp = None
            if tp == None:
                tp = evalFunc(tempGSandSide[0], 0, -tempGSandSide[1], tempGSandSide[1])
            print(tp)
            pureIndex(tempGSandSide[0], tp, tempGSandSide[1])
        if not (tp == 1 or tp == -1 or tp == 0):
            helperBFS(tempGSandSide[0], -tempGSandSide[1])
        writeCurHeader()
    print("Out BFS indexCreator")

def prePureIndex(gS, mySide):
    print("In pre check")
    if mySide == 1:
        rf = open(QUEUES, "r")
        line = rf.readline()
        for i in range(7):
            if eval(line)[0] == gS:
                print("Out pre check True")
                return True
            line = rf.readline()
        for i in range(headerPTR[0] - 7):
            rf.readline()
        while line:
            if eval(line)[0] == gS:
                print("Out pre check True")
                return True
            line = rf.readline()
    # Right after the yellow played
    elif mySide == -1:
        rf = open(QUEUES, "r")
        line = rf.readline()
        for i in range(7):
            if eval(line)[0] == gS:
                print("Out pre check True")
                return True
            line = rf.readline()
        for i in range(headerPTR[0] - 7):
            rf.readline()
        while line:
            if eval(line)[0] == gS:
                print("Out pre check True")
                return True
            line = rf.readline()
    print("Out pre check False")
    return False

def pureIndex(gS, expectedValue, mySide):
        if mySide == 0:
            return None

        new_LIST = [gS, expectedValue, mySide]
        # Right after the red played
        if mySide == 1:
            f = open(INDEX_FILE_RED, "a")
            f.write((str)(new_LIST) + "\n")
            f.close()
        # Right after the yellow played
        elif mySide == -1:
            f = open(INDEX_FILE_YEL, "a")
            f.write((str)(new_LIST) + "\n")
            f.close()
        return None

def indexCreatorDFS(gS, side):
    print("In DFS indexCreator")
    children = getSuccessors(gS, side)
    if len(children) != 0:
        for i in children:
            if i != None:
                tp = evalFunc(i, 0, -side, side)
                print(tp)
                if tp != 0:
                    toIndex(i, tp, side)
                    if tp == 1 or tp == -1:
                        continue
                    indexCreator(i, -side)
    print("Out DFS indexCreator")

# def repeatIndex(gS, expectedValue, mySide):
#     if mySide == 0:
#         return None
#
#     new_LIST = [gS, expectedValue, mySide]
#     # Right after the red played
#     if mySide == 1:
#         f = open(INDEX_FILE_RED, "a")
#         f.write((str)(new_LIST) + "\n")
#         rf.close()
#         f.close()
#     # Right after the yellow played
#     elif mySide == -1:
#         f = open(INDEX_FILE_YEL, "a")
#         f.write((str)(new_LIST) + "\n")
#         rf.close()
#         f.close()
#     return None

def runIndexCreator():
    getCurHeader()
    getTotalLines()
    gS = playGround.init_gameState()
    indexCreatorBFS(gS, 1)

if __name__ == "__main__":
    terms = sys.argv[1:]
    roomNum = terms[0]
    playerTurn = terms[1]
    playerTurn = eval(playerTurn)

    chooseRoomNum(roomNum)
    args = chooseSide(playerTurn)
    f1 = open(INDEX_FILE_RED, 'a')
    f2 = open(INDEX_FILE_YEL, 'a')
    f3 = open(QUEUES, 'a')
    f4 = open(TOTALLINES, 'a')
    f4 = open(CURHEADER, 'a')
    runIndexCreator()
    # play(args)
