import numpy as np
import urllib3
import ConfigParser
cp = ConfigParser.ConfigParser()
cp.read("db.cfg")
beta = cp.getfloat('iBeacon_config', "EWMA_Beta")
beacons =  cp.get('iBeacon_address', "beacons").split(',')
print(beacons)

def validVar():
        validVar = np.zeros(10, np.float)
        validSequences = np.zeros(10)
        for i in range(0, 10):
            table = a[...,i]
             #remove 0s
            E2X = 0
            EX = 0.0
            SUM = 0.0
            EX2 = 0.0
            Counter = 0
            for j in range(0, a.shape[0]):
                if(table[j] != 0):
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
        return validVar

def mean():
    mean = np.zeros(10, np.float)
    validSequences = np.zeros(10)
    for i in range(0, 10):
        table = a[...,i]
             #remove 0s
        E2X = 0
        EX = 0.0
        SUM = 0.0
        EX2 = 0.0
        Counter = 0
        for j in range(0, a.shape[0]):
            if(table[j] != 0):
                Counter = Counter + 1
                SUM = SUM + table[j]
        if Counter != 0:
            mean[i] = SUM / Counter
        else:
            mean[i] = 0
    return mean

def num():
    num = np.zeros(10, np.float)
    for i in range(0, 10):
        table = a[...,i]
        for j in range(0, a.shape[0]):
            if(table[j] != 0):
                num[i] = num[i] + 1
        num[i] = num[i] / a.shape[0]
    return num
"""for i in range(10,18):
    with open(str(i) +".txt", 'r') as myFile:
        output = open("0"+ str(i) +".txt",'w')
        data = myFile.readlines()
    
        for line in data:
            myLine = line.replace("[","")
            myLine = myLine.replace("]","")
            output.write(myLine+"\n")
        output.close()"""
meanV = np.zeros((18,10), np.float)
var = np.zeros((18,10), np.float)
for i in range(0,7):
    a = np.loadtxt("Data/0" + str(i) + ".txt")
    #print(a)
    var = validVar()
    #print("the var of " + str(i *3) + "m is "),
    #print( var )
    meanV[i] = mean()
    #print("the mean of " + str(i *3) + "m is "),
    #print( meanV[i] )
    #print("rate of receiving: "),
    numV = num()
    #print(numV)
    #print("\n")
    
for i in range(10,18):
    a = np.loadtxt("Data/0" + str(i) + ".txt")
    #print(a)
    var = validVar()
    #print("the var of " + str(i *3) + "m is "),
    #print( var )
    meanV[i] = mean()
    #print("the mean of " + str(i *3) + "m is "),
    #print( meanV[i] )
    #print("rate of receiving: "),
    numV = num()
   # print(numV)
   # print("\n")
