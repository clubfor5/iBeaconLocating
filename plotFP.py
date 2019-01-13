import numpy as np
from scipy.spatial.distance import pdist
import matplotlib.pyplot as plt
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
             RSSI.append(float(signal[0]))
             sth.append(float(signal[1]))
             var.append(float(signal[2]))
        fpTable[fp.index(lines)] = RSSI
        try:
            positionX = int(position[0])
            positionY = int(position[1])
            positionTag = int(position[2])
            direction = position[3]
        except ValueError:
            print ("invalid input")
   # print(fpTable)
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
    #for i in range(0, tableLength):
       # cosDisTable[i] = cosDistance(vec, table[i])
    #print(cosDisTable)    
    return  np.argsort(eucDisTable)

table = getFingerPrint()
shape = table.shape
result = table
print(result)
for x in range(0, shape[0]):
    for y in range(0, shape[1]):
        if table[x,y] == 0:
            result[x, y] = -160

plt.figure(1)
x = np.linspace(0,51,18)
for i in range(0, 10):
    fig = plt.subplot(5, 2,i+1)
    plt.sca(fig)
    plt.plot(x,result[...,i],'r')
plt.show()
        