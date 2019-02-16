import numpy as np
import ConfigParser
cp = ConfigParser.ConfigParser()
cp.read("config/db.cfg")
MAC =  cp.get('iBeacon_address', "beacons").split(',')
for num in MAC:
    MAC[MAC.index(num)] = num.replace(":","")
numMAC = len(MAC)
def validVar(rssiRawData):
        validVar = np.zeros(numMAC, np.float)
        validSequences = np.zeros(numMAC, np.int)
        for i in range(0, numMAC):
            table = rssiRawData[...,i]
            E2X = 0
            EX = 0.0
            SUM = 0.0
            EX2 = 0.0
            Counter = 0
            for j in range(0, rssiRawData.shape[0]):
                if(table[j] != -100):
                    Counter = Counter + 1
                    SUM = SUM + table[j]
                    EX2 = EX2 + table[j] * table[j]
            if Counter != 0:
                EX2 = EX2 / Counter
                EX = SUM / Counter
                E2X = EX * EX
                validSequences[i] = Counter
                validVar[i] = EX2 - E2X
            else:
                validVar[i] = 0
            validVar[i] = round(validVar[i], 6)
        return validVar

def getMean(rssiRawData):
    mean = np.zeros(numMAC, np.float)
    validSequences = np.zeros(numMAC)
    for i in range(0, 10):
        table = rssiRawData[...,i]
             #remove 0s
        E2X = 0
        EX = 0.0
        SUM = 0.0
        EX2 = 0.0
        Counter = 0
        for j in range(0, rssiRawData.shape[0]):
            if(table[j] != -100):
                Counter = Counter + 1
                SUM = SUM + table[j]
        if Counter != 0:
            mean[i] = SUM / Counter
        else:
            mean[i] = 0
    return mean

def num():
    num = np.zeros(numMAC, np.float)
    for i in range(0, numMAC):
        table = a[...,i]
        for j in range(0, rssiRawData.shape[0]):
            if(table[j] != 0):
                num[i] = num[i] + 1
        num[i] = num[i] / rssiRawData.shape[0]
    return num


def fingerPrint(inputFileName, outputFileName):
    rawData = np.loadtxt(inputFileName)
    try:
        inputFileName = inputFileName.split('/')[1]
        node = int(inputFileName.split('.')[0])
    except:
        print("invalid input file formatter transfer to finger print")
        return
    meanV = getMean(rawData)
    var = validVar(rawData)
    positionX = str(node * 3)
    positionY = "0"
    positionNum = str(node)
    direction = 'D'
    rssiTable = ""
    for j in range(0,10):
        addr = MAC[j]
        mean = "%.1f" % float(meanV[j])
        var1  = "%.1f" % float(var[j])
        myTable = addr + ":" + mean + "," + "0.0," + var1 + " "
        rssiTable = rssiTable + myTable
    buffer = positionX + "," + positionY + "," + positionNum + "," + direction + " " + rssiTable
    outputFile = open(outputFileName,'w')
    outputFile.write(buffer)
    outputFile.close()

#fingerPrint("fpRawData/3.txt", "fp/3.txt")
