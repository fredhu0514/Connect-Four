import playGround
import time
import sys

TXTpaths = [playGround.path_current_game_state, playGround.path_all_games, playGround.txt_file]

def ifMyTurn(mySide):
    f = open(TXTpaths[0], 'r')
    line = f.readline()
    temp = eval(line)
    if temp == -mySide:
        return True
    return False

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

def chooseSide(side=0):
    if side == 0:
        temp = 0
        while not (temp == 1 or temp == -1):
            str = input("If RED, enter 1; else if YELLOW, enter 2: ")
            if str != "":
                side = eval(str)
            if side == 1:
                temp = 1
            elif side == 2:
                temp = -1
        return temp
    else:
        return side

def chooseColumn(side, gS):
    tempGS = None
    col = None
    while not tempGS:
        if side == 1:
            col = chooseNumberFrom1TO7()
            tempGS = playGround.putRed(gS, col)
        elif side == -1:
            col = chooseNumberFrom1TO7()
            tempGS = playGround.putYel(gS, col)
    return col, tempGS

def chooseNumberFrom1TO7():
    # but return 0 to 6
    a = 0
    while a < 1 or a > 7:
        a = input("Please input a integer from 1 to 7: ")
        if a != "":
            a = eval(a)
        else:
            a = 0
    a -= 1
    return a

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
