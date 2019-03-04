from bluepy.btle import Scanner, DefaultDelegate
import time
import json
import operator
import numpy as np
import json
import ConfigParser
import sys
import os
import thread
import tcpClient.mtrClient as mtr
import positioning.beaconAddress as beaconAdd
import positioning.filters as flts
import positioning.speedDetector as speedDetector
import positioning.position as pos
#import positioning.kalman as kalm
import alarm

#myClient = mtr.mtrClient()
import positioning.RSSITable as RSSITable
import positioning.purePI_ctlersp as purePI
debug = True

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)		
		

### devices: scanned result; beacons: address table of beacons; mask: num of times the the address not received.

def mtr_alarm(speed):
    if abs(speed) >= alarmSpeed:
        alarmCounter = alarmCounter + 1
    else:
        alarmCounter = 0
        
    if  alarmCounter >= alarmThreshold:
        thread.start_new_thread(alarm.alarm, ("alarm", 17))  
        
#=========#=====================#==========#======================#=========
def mtr_service(myRSSI):
    currentTime = time.time()
    mask = np.zeros(numOfBeacons)
    positionBufferX = [0 for i in range(3)]
    positionBufferY = [0 for i in range(3)]
    timeTagBuffer = [0 for i in range(3)]
    preCounter = 0
    alarmCounter = 0
    while True:
        global scanner
        devices = scanner.scan(0.57)
        # insert a time to timeout inside the squares. this returns a list with ALL bluetooth devices nearby (not only iBeacon).
        myRSSI = RSSITable.getEWMAFilteredRSSI(devices, beaconAddress, mask, myRSSI)
        if preCounter < 3:
            positionBufferX[preCounter],positionBufferY[preCounter], timeTagBuffer[preCounter] =  pos.proximity(startTime, myRSSI, beaconInfos)
            preCounter = preCounter + 1
            continue
        elif preCounter == 3:
            fPositionX = float (sum(positionBufferX) / len(positionBufferX))
            PID = purePI.purePI_Ctler(fPositionX)
            preCounter = preCounter + 1

        if method == "proximity":
            positionX,positionY, timeTag = pos.proximity(startTime, myRSSI, beaconInfos)
            [positionX, speed] = PID.posiFlter(positionX, timeTag)
            if preCounter >= 3:
                positionLog = str(timeTag) + ","+str(positionX) + ','
                speedLog = str(speed) + '\n'
                myFile.writelines(positionLog)
                myFile.writelines(speedLog)
                print ("time: ", round(timeTag,2)),
                print ("position: ", round(positionX,2)),
                print("speed: ", round(speed, 2))
                
                data = {
                'target': 'A',
                'ts': round(timeTag,2),
                'loc_x': round(positionX,2),
                'loc_y': round(positionY, 2),
                'val': round(speed, 2)
            }
            
            if mtr_server_state == True:
                myClient.send(data)
            
            mtr_alarm(speed)
            
        ###################### alarm #########################
           
                
            
if __name__ == '__main__':
    #### load program information from db.cfg
    cp = ConfigParser.ConfigParser()
    cp.read("config/db.cfg")
    method = cp.get('iBeacon_config', "locatingMethod")
    beta = cp.get('iBeacon_config','EWMA_Beta')
    alarmThreshold = int(cp.get('speed_config','alarmThreshold'))
    alarmSpeed = float(cp.get('speed_config','alarmSpeed'))
    myFile = open("log/dataLog " + time.asctime(time.localtime(time.time())) + ".txt", 'w')
    # load beacon informations 
    beaconAddress = []
    beaconInfos,numOfBeacons = beaconAdd.getBeaconInfo()
    mtr_server_state = True
    try:
        print("Connecting to mtr Server... ")
        myClient = mtr.mtrClient()
    except:
        print("failed to connect the server!")
        mtr_server_state = False
    #### all the information of iBeacon information has been restored.
    for info in beaconInfos:
        beaconAddress.append(info.address)
        
    myRSSI = []
    for i in range(numOfBeacons):
        myRSSI.append(-120)
    #--defining the scan object--#
    startTime = time.time()
    scanner = Scanner().withDelegate(ScanDelegate())
    
    speedDetector = speedDetector.SpeedDetector(5)
    mtr_service(myRSSI)
