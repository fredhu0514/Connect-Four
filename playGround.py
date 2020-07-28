import copy
import time

redVal = 1
yelVal = -1

path_current_game_state = "Current/process.txt"
path_all_games = "Current/game.txt"

def init_gameState():
    lst = []
    for i in range(0, 6):
        temp = []
        for j in range(0, 7):
            temp.append(0)
        lst.append(temp)
    return lst

def isFull(gS):
    for row in range(0, len(gS)):
        for col in range(0, len(gS[row])):
            if col == 0:
                return False
    return True

def isWin(gameState):
    for row in range(0, 6):
        for col in range(0, 7):
            curColor = gameState[row][col]
            if curColor == 0:
                continue
            flag = False
            # See same col to the right dir
            if col <= 3:
                for cPTR in range(col + 1, col + 4):
                    if gameState[row][cPTR] != curColor:
                        break
                    if cPTR == col + 3:
                        flag = True
            # See same row to the upper dir
            if row <= 2:
                for rPTR in range(row + 1, row + 4):
                    if gameState[rPTR][col] != curColor:
                        break
                    if rPTR == row + 3:
                        flag = True
            # See same row to down vertical
            if row <= 2 and col <= 3:
                for t in range(1, 4):
                    if gameState[row + t][col + t] != curColor:
                        break
                    if t == 3:
                        flag = True
            # See same row to up vertical
            if row >= 3 and col <= 3:
                for t in range(1, 4):
                    if gameState[row - t][col + t] != curColor:
                        break
                    if t == 3:
                        flag = True
            # if any of these scene happens, the game ends with return the winning side
            if flag:
                return curColor
    # If no one wins, return 0
    return 0

def test():
    gS = init_gameState()
    gS = putRed(gS, 2)
    gS = putRed(gS, 3)
    gS = putRed(gS, 5)
    gS = putYel(gS, 1)
    gS = putYel(gS, 4)

    gS = putRed(gS, 1)
    gS = putRed(gS, 2)
    gS = putRed(gS, 3)
    gS = putRed(gS, 5)
    gS = putYel(gS, 4)

    gS = putRed(gS, 2)
    gS = putYel(gS, 1)
    gS = putYel(gS, 3)
    gS = putYel(gS, 4)
    gS = putYel(gS, 5)

    gS = putRed(gS, 4)
    gS = putYel(gS, 2)
    gS = putYel(gS, 3)

    gS = putYel(gS, 3)

    gS = putRed(gS, 3)

    gS = putRed(gS, 0)

    gS = putYel(gS, 0)
    printGS(gS)

    print(isWin(gS))

def printGS(gS, displayF=True):
    result = ""
    for i in range(0, 6):
        for j in range(0, 7):
            if gS[i][j] == 0:
                result += "O"
            elif gS[i][j] == 1:
                result += "R"
            elif gS[i][j] == -1:
                result += "Y"
            # result += "\t"
            result += " "
        result += "\n"
    if displayF:
        print(result)
    else:
        return result

def putRed(gameState, a):
    if not (a >= 0 and a <= 6):
        print("Your column choice is invalid!")
        return None
    ptr = 0
    for i in range(0, 6):
        if gameState[i][a] != 0:
            ptr = i
            break
        if i == 5:
            ptr = 6
    if ptr - 1 < 0:
        # print("This column is full, choose another one!")
        return None
    else:
        gameState[ptr - 1][a] = redVal
        return gameState

def putYel(gameState, a):
    if not (a >= 0 and a <= 6):
        print("Your column choice is invalid!")
        return None
    ptr = 0
    for i in range(0, 6):
        if gameState[i][a] != 0:
            ptr = i
            break
        if i == 5:
            ptr = 6
    if ptr - 1 < 0:
        # print("This column is full, choose another one!")
        return None
    else:
        gameState[ptr - 1][a] = yelVal
        return gameState

def initProcessorTXT():
    # palyer; turn; game state
    temp = (str)(-1) + "\n"
    temp += (str)(0) + "\n"
    temp += (str)(init_gameState()) + "\n"
    f = open(path_current_game_state,'w')
    f.write(temp)

def writeDraw():
    # Processor.txt should be empty then
    temp = ""
    f = open(path_current_game_state,'w')
    f.write(temp)

    # Write winner infomation to the folder
    temp == "<<<<<<<<<<<<<\\\\\\\\\\ DRAW /////>>>>>>>>>>>>>\n"
    temp += printGS(gS, False)
    temp += "<<<<<<<<<<<<<<<< GAME OVER >>>>>>>>>>>>>>>\n\n\n\n\n"
    f = open(path_all_games,'a')
    f.write(temp)

    t = time.strftime("Games/%Y-%m-%d %H-%M-%S_", time.localtime())
    newFileName = t + "GAME.txt"

    f = open(path_all_games,'r')
    for line in f:
        w = open(newFileName,'a')
        w.write(line)

    f = open(path_all_games,'w')
    f.write("")

def gameEnds(winner, gS):
    # Processor.txt should be empty then
    temp = ""
    f = open(path_current_game_state,'w')
    f.write(temp)

    # Write winner infomation to the folder
    if winner == 1:
        temp = "\n<<<<<<<<<<<<\\\\\\\\\\ RED WINS /////>>>>>>>>>>>>>>>\n"
    elif winner == -1:
        temp = "\n<<<<<<<<<<\\\\\\\\\\ YELLOW WINS /////>>>>>>>>>\n"
    temp += printGS(gS, False)
    temp += "<<<<<<<<<<<<<<<< GAME OVER >>>>>>>>>>>>>>>\n\n\n\n\n"
    f = open(path_all_games,'a')
    f.write(temp)

    t = time.strftime("Games/%Y-%m-%d %H-%M-%S_", time.localtime())
    newFileName = t + "GAME.txt"

    f = open(path_all_games,'r')
    for line in f:
        w = open(newFileName,'a')
        w.write(line)

    f = open(path_all_games,'w')
    f.write("")



def updateFileInfo(turn, chosen_column, side, gS, path_all_games):
    # rewrite <path_current_game_state>
    temp = (str)(side) + "\n"
    temp += (str)(turn) + "\n"
    temp += (str)(gS) + "\n"
    f = open(path_current_game_state,'w')
    f.write(temp)

    # add to <path_all_games>
    content_path_all_games = ""
    if turn == 1:
        content_path_all_games += "<<<<<<<<<<<<<<< GAME STARTS >>>>>>>>>>>>>>\n"
        content_path_all_games += "\n"
    content_path_all_games += "==========================================\n"
    if side == 1:
        content_path_all_games += "=================== RED ==================\n"
    elif side == -1:
        content_path_all_games += "================== YELLOW ================\n"
    content_path_all_games += "==========================================\n"
    content_path_all_games += "Turn " + (str)(turn) + ", "
    if side == 1:
        content_path_all_games += "red-side "
    elif side == -1:
        content_path_all_games += "yellow-side "
    content_path_all_games += "player chose column " + (str)(chosen_column + 1) + ".\n"
    content_path_all_games += "\n"
    content_path_all_games += printGS(gS, False)
    content_path_all_games += "\n\n"
    f = open(path_all_games,'a') #读取label.txt文件，没有则创建，‘a’表示再次写入时不覆盖之前的内容
    f.write(content_path_all_games)
