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
import position as pos
#myClient = mtr.mtrClient()
#myClient = mtr.mtrClient()
import RSSITable
debug = True

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)		
		

### devices: scanned result; beacons: address table of beacons; mask: num of times the the address not received.

            
    
#=========#=====================#==========#======================#=========
def beaconScanner():
    currentTime = time.time()
    collections = np.zeros(numOfBeacons)
    mask = np.zeros(numOfBeacons)
    while True:
        global scanner
        devices = scanner.scan(0.57)
        # insert a time to timeout inside the squares. this returns a list with ALL bluetooth devices nearby (not only iBeacon).
        RSSITable.getEWMAFilteredRSSI(devices, beaconAddress, mask, myRSSI)
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
        elif method == 'proximity':
            positionX,positionY, timeTag = pos.proximity(startTime, myRSSI, beaconInfos)
            speedDetector.pushLocation(timeTag, positionX)
            speedDetector.speedCalculate()


if __name__ == '__main__':
    #### load program information from db.cfg 
    cp = ConfigParser.ConfigParser()
    cp.read("db.cfg")
    method = cp.get('iBeacon_config', "locatingMethod")
    beta = cp.get('iBeacon_config','EWMA_Beta')
    
    # load beacon informations 
    beaconAddress = []
    beaconInfos,numOfBeacons = beaconAdd.getBeaconInfo()
    
    #### all the information of iBeacon information has been restored.
    for info in beaconInfos:
        beaconAddress.append(info.address)
        print("Beacon Num"),
        print(info.tag),
        print("with address"),
        print(info.address)
    myRSSI = []
    for i in range(numOfBeacons):
        myRSSI.append(-120)
    #--defining the scan object--#
    startTime = time.time()
    scanner = Scanner().withDelegate(ScanDelegate())
    speedDetector = speedDetector.SpeedDetector(15)
    beaconScanner()
