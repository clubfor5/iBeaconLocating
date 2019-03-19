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
import alarm
import he_alarm 
import positioning.RSSITable as RSSITable
import positioning.purePI_ctlersp as purePI
debug = True
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)		
		

### devices: scanned result; beacons: address table of beacons; mask: num of times the the address not received.

        
#=========#====================#==========#======================#=========
def mtr_service(myRSSI):
    currentTime = time.time()
    mask = np.zeros(numOfBeacons)
    positionBufferX = [0 for i in range(3)]
    positionBufferY = [0 for i in range(3)]
    timeTagBuffer = [0 for i in range(3)]
    preCounter = 0
    alarmCounter = 0
    alarmState = False
    previouSpeed = 0.3
    while True:
        global scanner
        devices = scanner.scan(0.57)
        # insert a time to timeout inside the squares. this returns a list with ALL bluetooth devices nearby (not only iBeacon).
        myRSSI = RSSITable.getEWMAFilteredRSSI(devices, beaconAddress, mask, myRSSI)
        # always make sure that device is under the coverage of at least one beacon
        if myRSSI.count(-100) == len(myRSSI):
            print ("no beacon detected, device out of range!")
            continue
      
        rssiBuf = []
        indexBuf = []
        a = myRSSI
        rssi = sorted(a, reverse = True)
        for i in range(5):
            rssiBuf.append(rssi[i])
            indexBuf.append(a.index(rssi[i]))
        

            
        # prepare basic information of iBeacon before take action
        if preCounter < 3:
            positionBufferX[preCounter],positionBufferY[preCounter], timeTagBuffer[preCounter] =  pos.proximity(startTime, myRSSI, beaconInfos)
            preCounter = preCounter + 1
            continue
        elif preCounter == 3:
            fPositionX = float (sum(positionBufferX) / len(positionBufferX))
            PID = purePI.purePI_Ctler(fPositionX)
            preCounter = preCounter + 1
        else:
            preCounter = preCounter + 1
        if method == "proximity":
            positionX,positionY, timeTag = pos.proximity(startTime, myRSSI, beaconInfos)

            if abs(positionX-fPositionX) >= 1:   
                delta = positionX -fPositionX
                positionX = positionX + delta / abs(delta) # add only one single step
                fPositionX = positionX
            else:
                fPositionX = positionX
            
            spd.pushLocation(timeTag,positionXX)
            avsp = spd.speedCalculate()
            
            if rssiBuf.count(-100) >= 2:
                speed = 0
                

            if preCounter >= 3:
                positionLog = str(timeTag) + ","+str(positionXX) + ','
                orginLog = str(positionX) + ','
                avrsLog = str(avsp)+','
                speedLog = str(speed) + '\n'
                
                myFile.writelines(positionLog+orginLog+avrsLog)
                myFile.writelines(speedLog)

                print("index: ", indexBuf),
                print("rssi: ", rssiBuf),
                print ("time: ", round(timeTag,2)),
                print ("position: ", round(positionXX,2)),
                print("oringin:",round(positionX,2)),
                print("speed: ", round(speed, 2)),
                print ('average speed: ', avsp)
            

            if abs(speed) >= 1.5:
                alarmCounter = alarmCounter + 1
                alramState = False
            else:
                alarmCounter = 0

            
            #---------alarm -----------#
            alarmState = alarmCtl.alarm_ctl(speed)
            if alarmState == True :
                thread.start_new_thread(alarm.alarmShort, ("alarm", 17)) 
            
            data = {
                'target': '1001',
                'ts': round(timeTag,2),
                'loc_x': round(positionXX,2),
                'loc_y': round(positionY, 2),
                'val': round(speed, 2),
                'status':int(alarmState)
            }
            if mtr_server_state == True:
                myClient.sendData(data)
               # alarmState = True
            

if __name__ == '__main__':
    #---- load program information from db.cfg-----#
    cp = ConfigParser.ConfigParser()
    cp.read("config/db.cfg")
    method = cp.get('iBeacon_config', "locatingMethod")
    beta = cp.get('iBeacon_config','EWMA_Beta')
    alarmThreshold = int(cp.get('speed_config','alarmThreshold'))
    alarmSpeed = float(cp.get('speed_config','alarmSpeed'))
    alarmCtl = he_alarm.he_alarm()
    #----- log file built -----#
    myFile = open("log/dataLog " + time.asctime(time.localtime(time.time())) + ".txt", 'w')
    print("Starting locating...")
    #----- start UDP ------# 
    mtr_server_state = True
    try:
        print("starting network service... ")
        myClient = mtr.mtrClient()
    except:
        print("failed to start network service!")
        mtr_server_state = False
    
    # all the information of iBeacon information has been restored.
    beaconInfos,numOfBeacons = beaconAdd.getBeaconInfo()
    beaconAddress = []
    for info in beaconInfos:
        beaconAddress.append(info.address)
    
    #----initial the rssi table ----#
    myRSSI = []
    for i in range(numOfBeacons):
        myRSSI.append(-100)
    spd = speedDetector.SpeedDetector(30)    

    #--defining the scan object--#
    scanner = Scanner().withDelegate(ScanDelegate())
    
    #------start service--------
    startTime = time.time()
    mtr_service(myRSSI)


