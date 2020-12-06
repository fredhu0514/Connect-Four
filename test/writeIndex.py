RED_FILE = "RED.txt"
YEL_FILE = "YEL.txt"
RED_AIM = "AIM_RED.txt"
YEL_AIM = "AIM_YEL.txt"

def isIn(gS, path):
    file = open(path, 'r')
    line = file.readline()
    while line:
        temp = eval(line)
        if temp[0] == gS:
            return True
        line = file.readline()
    return False

def writeIndex():
    rf = open(RED_FILE, 'r')
    line = rf.readline()
    while line:
        temp = eval(line)
        if not isIn(temp[0], RED_AIM):
            wrf = open(RED_AIM, 'a')
            wrf.write(line)
        line = rf.readline()

    yf = open(YEL_FILE, 'r')
    line = yf.readline()
    while line:
        temp = eval(line)
        if not isIn(temp[0], YEL_AIM):
            wyf = open(YEL_AIM, 'a')
            wyf.write(line)
        line = yf.readline()

open(RED_AIM, 'a')
open(YEL_AIM, 'a')

writeIndex()
