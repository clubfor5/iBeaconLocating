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
#myClient = mtr.mtrClient()
# myClient = mtr.mtrClient()

class SpeedDetector:
    def __init__(self, size):
        self.time = []
        self.position =[]
        self.size = size
        self.sumT = 0
        self.sumP = 0
        self.sumT2 = 0
        self.sumP2 = 0
        self.sumTP = 0
        
    def pushLocation(self, time, location):
        self.position.append(location)   
        self.time.append(time)
        if len(self.time) == self.size + 1:
            self.position.pop(0)
            self.time.pop(0)
    
    def speedCalculate(self):
        if len(self.time) < self.size:
           # print(self.size)
           # print(len(self.time))
           # print("OK!")
            return 0
            
        self.sumT = 0
        self.sumP = 0
        self.sumT2 = 0
        self.sumP2 = 0
        self.sumTP = 0
        
        for i in range(self.size):
            self.sumT = self.sumT + self.time[i]
            self.sumP = self.sumP + self.position[i]
            self.sumT2 = self.sumT2 + self.time[i] * self.time[i] 
            self.sumP2 =  self.sumP2 + self.position[i] * self.position[i] 
            self.sumTP = self.sumTP + self.time[i] * self.position[i]
        print(self.position)
        speed = (float)(self.size * self.sumTP - self.sumT * self.sumP) / (float)(self.size* self.sumT2 - self.sumT * self.sumT)

        if abs(speed) < 0.01:
            speed = 0
        print(speed)
        return speed
        
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
                if myRSSI[index] == 0:
                    myRSSI[index] = round(dev.rssi, 2)
                else:
                    temp = myRSSI[index] * beta + dev.rssi * (1-beta)
                    myRSSI[index] = round(temp, 2)
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
    #### Load things from the config file
    beaconInfos,numOfBeacons = beaconAdd.getBeaconInfo()
	for i in range(numOfBeacons):
        print("Beacon Num"),
        print(beaconInfos[i].tag),
        print("with address"),
		print(beaconInfos[i].address)
    ### check out the beacon mac addresses
    for i in range(numOfBeacons):
       
    
   
    fpTable, positionInfo = finp.getFingerPrintTable()
    myRSSI = []
    for i in range(0, numOfBeacons):
        myRSSI.append(-100)
        
    #--defining the scan object--#
    startTime = time.time()
    scanner = Scanner().withDelegate(ScanDelegate())
    speedDetector = SpeedDetector(15)
    beaconScanner()
