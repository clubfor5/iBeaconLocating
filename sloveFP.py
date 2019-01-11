import numpy as np
position = []

def getFingerPrint():
    fpFile = open("fp.txt",'r')
    fp = fpFile.readlines()
    fpNum = len(fp)
    numBeacons = len(fp[0].split(" "))-2
    fpTable = np.zeros((fpNum, numBeacons),np.float)
    for lines in fp:
        sublines = lines.split(" ")
        position = sublines[0].split(",")
        addr  = []
        RSSI  = []
        var = []
        sth = []
        for i in range(1, len(sublines)-1):
             addRSSI = sublines[i].split(":")
             addr.append(addRSSI[0])
             signal = addRSSI[1].split(",")
             RSSI.append(signal[0])
             sth.append(signal[1])
             var.append(signal[2])
        fpTable[fp.index(lines)] = RSSI
        try:
            positionX = int(position[0])
            positionY = int(position[1])
            positionTag = int(position[2])
            direction = position[3]
        except ValueError:
            print ("invalid input")
    print(fpTable)
    fpFile.close()
    return fpTable

getFingerPrint()
        
        