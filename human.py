import playGround
import time

def ifMyTurn(mySide):
    f = open(playGround.path_current_game_state, 'r')
    line = f.readline()
    temp = eval(line)
    if temp == -mySide:
        return True
    return False

def chooseSide():
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
            print(sideSTR + "Turn " + (str)(curTurn) + ".\n")
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

    print("<<<<<<<<<<<<<<<< GAME OVER >>>>>>>>>>>>>>>\n\n\n\n\n")

if __name__ == "__main__":
    args = chooseSide()
    play(args)
