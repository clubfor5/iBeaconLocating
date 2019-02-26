from bluepy.btle import Scanner, DefaultDelegate
import urllib3
import time
import json
import operator
import numpy as np
import json
import ConfigParser
import sys
import os
import thread
#import fp.fpGeneration as fpG
import tcpClient.mtrClient as mtr
#import fp.fingerprint as finp
import positioning.beaconAddress as beaconAdd
import positioning.filters as flts
import positioning.speedDetector as speedDetector
import positioning.position as pos
import positioning.kalman as kalm
import alarm
#myClient = mtr.mtrClient()
#myClient = mtr.mtrClient()
import positioning.RSSITable as RSSITable
import positioning.purePI_ctlersp as purePI
debug = True

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)		
		

### devices: scanned result; beacons: address table of beacons; mask: num of times the the address not received.

            
    
#=========#=====================#==========#======================#=========
def beaconScanner(myRSSI):
    currentTime = time.time()
    collections = np.zeros(numOfBeacons)
    mask = np.zeros(numOfBeacons)
    start = False
    fPositionX = 0.3
    positionBufferX = [0 for i in range(5)]
    positionBufferY = [0 for i in range(5)]
    timeTagBuffer = [0 for i in range(5)]
    preCounter = 0
    initPosition = 0
    alarmCounter = 0
    while True:
        global scanner
        devices = scanner.scan(0.57)
        # insert a time to timeout inside the squares. this returns a list with ALL bluetooth devices nearby (not only iBeacon).
        myRSSI = RSSITable.getEWMAFilteredRSSI(devices, beaconAddress, mask, myRSSI)
        if preCounter < 5:
            positionBufferX[preCounter],positionBufferY[preCounter], timeTagBuffer[preCounter] =  pos.proximity(startTime, myRSSI, beaconInfos)
            preCounter = preCounter + 1
            print ("log1")
            continue
        elif preCounter == 5:
            fPositionX = float (sum(positionBufferX) / len(positionBufferX))
            #print(fPositionX)
            PID = purePI.purePI_Ctler(fPositionX)
            initPosition = fPositionX
            preCounter = preCounter + 1
            #continue
        data = [{
        'Type': 'Raw',
        'mac': 'testMac',
        'ts': float(time.time()-currentTime),
        'rssi': myRSSI,
        'remark': 'Mtrtest',
        }]
        preCounter = preCounter + 1
        # myClient.sendData(data)
        if method == "fingerprint":
            print("Original Output: ")
            #className = finp.knnInitial_dimension(sample, fpTable, positionInfo, 3)
        elif method == 'proximity':
            positionX,positionY, timeTag = pos.proximity(startTime, myRSSI, beaconInfos)
            [positionX, speed] = PID.posiFlter(positionX, timeTag)
            [positionX, speed] = PID.posiFlter(positionX, timeTag)
            #speed = speedDetector.speedCalculate()
            print('current speed: ',speed)
            if preCounter >= 5:
                rawDataLog = str(myRSSI) + '\n'
                positionLog = str(timeTag) + ","+str(positionX) + ','
                speedLog = str(speed) + '\n'
            #myFile.writelines(rawDataLog)
                myFile.writelines(positionLog)
                myFile.writelines(speedLog)
           # myFile.writelines('\n')
                print(positionLog + speedLog)
            if speed >= 2.0:
                alarmCounter = alarmCounter + 1
            else:
                alarmCounter = 0
            if  alarmCounter >= 5:
                thread.start_new_thread(alarm.alarm, ("alarm", 17))
                
            
if __name__ == '__main__':
    #### load program information from db.cfg 
    #time.sleep(20)
    cp = ConfigParser.ConfigParser()
    cp.read("config/db.cfg")
    method = cp.get('iBeacon_config', "locatingMethod")
    beta = cp.get('iBeacon_config','EWMA_Beta')
    myFile = open("log/dataLog " + time.asctime(time.localtime(time.time())) + ".txt", 'w')
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
    
    speedDetector = speedDetector.SpeedDetector(5)
    beaconScanner(myRSSI)
