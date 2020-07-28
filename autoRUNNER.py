import os

filePath = os.getcwd()
andLine = " & "
cdCommandLine = "cd " + filePath
python3Line = "python3 "

firstPart = cdCommandLine + andLine + python3Line

agentNameLst = ["robot0.py ", "robot1.py "]
order = [" 1", " -1"]

for i in range(0, 2):
    resul1 = ""
    result2 = ""
    roomNum = (str)(i)
    for j in range(0, 2):
        result = firstPart + agentNameLst[j] + roomNum +  order[(i + j) % 2]
        print(result)
        os.popen(result, 'w')
