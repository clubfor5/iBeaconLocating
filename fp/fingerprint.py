import numpy as np
# from scipy.spatial.distance import pdist
from numpy import *
import operator
import ConfigParser
position = []
import time
cp = ConfigParser.ConfigParser()
cp.read("config/db.cfg")
fpNum = cp.get('iBeacon_config', "fpNum")
beaconNums = int(cp.get('iBeacon_address', "numOfBeacons"))


def knnInitial_dimension(sample, dataset, labels, knn):
    checkPoint = []
    for i in range(len(sample)):
        if sample[i] == 0:
            checkPoint.append(i)
    print('checkPoint =', checkPoint)
    #finalCheckPoint = checkContinuePoint(checkPoint)
    sample = delete(sample, checkPoint, axis=0)
    newDataSet = delete(dataset, checkPoint, axis=1)
    dataSetSize = newDataSet.shape[0]
    # print(tile(sample, (dataSetSize, 1)))
    diffMat = tile(sample, (dataSetSize, 1)) - newDataSet
    sqDiffMat = diffMat ** 2
    sqDist = sqDiffMat.sum(axis=1)
    dist = sqDist ** 0.5
    sortDist = dist.argsort()
    print(sortDist)
    result = []
    for i in range(knn):
        voteLabel = labels[sortDist[i]]
        data = [{
            'ts': int(time.time()),
            'loc_x': voteLabel,
            'loc_y': 0,
            'dist': dist[sortDist[i]],
        }]
        result.append(data)
    print(result)
    return result



def getFingerPrintTable():
    fpTable = []
    positionInfo = []
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
            positionInfo.append(0)
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
            positionInfo.append(positionX)
        except ValueError:
            print ("invalid finger print file!")
        fpFile.close()
        # print(positionInfo)
    return fpTable, positionInfo

