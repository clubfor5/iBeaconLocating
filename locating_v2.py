from bluepy.btle import Scanner, DefaultDelegate
import urllib3
import time
import json
#import mythread
import thread
import operator
import numpy as np
import mtrClient as mtr
import json
import ConfigParser
import sys
import os
import fpGeneration as fpG
import mtrClient as mtr
import fingerprint as finp
import beaconAddress as beaconAdd
import filters as flts
import speedDetector
#myClient = mtr.mtrClient()
#myClient = mtr.mtrClient()

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)		
		



#=========#=====================#==========#======================#=========
def beaconScanner():
    currentTime = time.time()
    collections = np.zeros(numOfBeacons)
    while True:
        global lastSended, scanner,locked
        # insert a time to timeout inside the squares. this returns a list with ALL bluetooth devices nearby (not only BLE).
        devices = scanner.scan(0.57)
        #get the existing RSSI table
        #for i in range(0,numOfBeacons):
            #myRSSI[i] = 0
        for dev in devices:
            # first of all check if the device at this position is or not one of ours beacons. if not, we just continue the loop, passing to next interaction.
            if not beacons.__contains__(dev.addr):
                continue
            elif beacons.__contains__(dev.addr):
                index = beacons.index(dev.addr)
                temp = flts.ewma(myRSSI[index], dev.rssi, beta)
                myRSSI[index] = round(myRSSI[index],2)
    
        ####
        #print("Raw Data:", myRSSI)
        sample = []
        for rssi in myRSSI:
            sample.append(rssi)
        maxIndex = myRSSI.index(max(myRSSI))
        #print(maxIndex)
        if maxIndex == 0:
            for i in range(3,10):
                sample[i] = 0
        elif maxIndex == 9:
            for i in range(0, 7):
                sample[i] = 0
        else:
            for i in range(0,maxIndex-1):
                sample[i] = 0
            for i in range(maxIndex+2,10):
                sample[i] = 0
        data = [{
        'Type': 'Raw',
        'mac': 'testMac',
        'ts': float(time.time()-currentTime),
        'rssi': myRSSI,
        'remark': 'Mtrtest',
        }]
        # myClient.sendData(data)
        if method == "fingerprint":
            print("Original Output: ")
            className = finp.knnInitial_dimension(sample, fpTable, positionInfo, 3)
            print
            print("Modified Output: ")
            calssName = finp.knnInitial_dimension(myRSSI, fpTable, positionInfo, 3)
           #print
           #print("proximity result: ")
           #position()
        elif method == 'proximity':
            position()


def position():
    ### Sort the strength of signals 
    a = myRSSI
    c = np.argsort(a)
    MAX = myRSSI[c[numOfBeacons - 1]]
    SMAX = myRSSI[c[numOfBeacons - 2]]
    
    ### Check out the difference of signal strength 
    if MAX - SMAX >= 8:
        position = c[numOfBeacons - 1] * 6
    elif MAX - SMAX >= 4:
        position = (c[numOfBeacons -1] * 0.75 + c[numOfBeacons - 2] * 0.25) * 6
    else:
        position = (c[numOfBeacons - 1] * 0.5 + c[numOfBeacons - 2] * 0.5) * 6
    
    ### in case that max and smax is not neighbor 
    if abs(c[numOfBeacons -1] -c[numOfBeacons - 2] ) >= 2:
        position = c[numOfBeacons - 1] * 6
    
    timeTag = round(time.time() - startTime, 2)
    speedDetector.pushLocation(timeTag, position)
    speedDetector.speedCalculate()
    print('loc:', position, timeTag)
    #print()
    

if __name__ == '__main__':
    #print("hello!")
    cp = ConfigParser.ConfigParser()
    cp.read("db.cfg")
    method = cp.get('iBeacon_config', "locatingMethod")
    beta = cp.get('iBeacon_config','EWMA_Beta')
    beacons = []
    #### Load things from the config file
    beaconInfos,numOfBeacons = beaconAdd.getBeaconInfo()
    myRSSI = []
    for i in range(numOfBeacons):
        myRSSI.append(0)
    for info in beaconInfos:
        beacons.append(info.address)
        print("Beacon Num"),
        print(info.tag),
        print("with address"),
        print(info.address)
    #--defining the scan object--#
    startTime = time.time()
    scanner = Scanner().withDelegate(ScanDelegate())
    speedDetector = speedDetector.SpeedDetector(15)
    beaconScanner()
