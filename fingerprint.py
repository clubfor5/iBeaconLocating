import numpy as np
from scipy.spatial.distance import pdist
import ConfigParser
cp = ConfigParser.ConfigParser()
cp.read("db.cfg")
fpNum = cp.get('iBeacon_config', "fpNum")
beaconNums = int(cp.get('iBeacon_address', "numOfBeacons"))
def getFingerPrintTable():
    fpTable = []
    for i in range(0, int(fpNum)):
        fileName = "fp/" + str(i) + ".txt"
        try:
            fpFile = open(fileName, 'r')
        except:
            print("the file " + fileName + " is not valid, please repeat to collect finger print")
            buff = []
            for i in range (0,beaconNums):
                buff.append(0)
            fpTable.append(buff)
            continue
        fp = fpFile.readlines()
        numBeacons = len(fp[0].split(" ")) - 2
        sublines = fp[0].split(" ")
        position = sublines[0].split(",")
        addr  = []
        RSSI  = []
        var = []
        sth = []
        for i in range(1, len(sublines)-1):
             addRSSI = sublines[i].split(":")
             addr.append(addRSSI[0])
             signal = addRSSI[1].split(",")
             RSSI.append(float(signal[0]))
             sth.append(float(signal[1]))
             var.append(float(signal[2]))
        fpTable.append(RSSI)
        try:
            positionX = int(position[0])
            positionY = int(position[1])
            positionTag = int(position[2])
            direction = position[3]
        except ValueError:
            print ("invalid finger print file!")
        fpFile.close()
    return fpTable

#getFingerPrint()
def eucDistance(vec1, vec2):
    return np.linalg.norm(vec1-vec2)

def cosDistance(vec1, vec2):
    if np.linalg.norm(vec1)!= 0 and np.linalg.norm(vec2)!= 0:
        return pdist(np.vstack([vec1, vec2]),'cosine')
    else:
        return 0
    
def determination(vec, table, tableLength):
    eucDisTable = np.zeros(tableLength)
    cosDisTable = np.zeros(tableLength)
    for i in range(0, tableLength):
        eucDisTable[i] = eucDistance(vec, table[i])
    print(eucDisTable)
    return  np.argsort(eucDisTable)

table = getFingerPrintTable()
for line in table:
    print(line)

        