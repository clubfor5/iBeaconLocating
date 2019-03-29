from bluepy.btle import Scanner, DefaultDelegate
import time
import json
import operator
import numpy as np
import json
import configparser as ConfigParser
import sys
import os
import threading
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


def mtrAlarm():
    global avspAcc, alarmState
    try:
        while True:
            alarmState = alarmCtl.alarm_ctl(avspAcc)
            if alarmState == True :
                alarm.alarmShort("alarm", 17)        
    except Exception as e:
        print(e)    

#=========#====================#==========#======================#=========
def mtr_service(myRSSI):
    global avspAcc,alarmState
    currentTime = time.time()
    mask = np.zeros(numOfBeacons)
    positionBufferX = [0 for i in range(3)]
    positionBufferY = [0 for i in range(3)]
    timeTagBuffer = [0 for i in range(3)]
    preCounter = 0
    alarmCounter = 0
    alarmState = False
    avspAcc = 0
    previouSpeed = 0.3
    while True:
        # try start udp if failed before
        global mtr_server_state,myClient
        if mtr_server_state == False:
            try:
                print("starting network service... ")
                myClient = mtr.mtrClient()
                mtr_server_state = True
            except:
                print("failed to start network service!")
                mtr_server_state = False
        
        # scan iBeacon
        global scanner
        devices = scanner.scan(0.57)

        # get RSSI table
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

        # start proximity
        if method == "proximity":
            positionX,positionY, timeTag = pos.proximity(startTime, myRSSI, beaconInfos)
            # if jump too fast, smooth the position
            if preCounter >= 10:
                if abs(positionX-fPositionX) > 10:   
                    delta = positionX -fPositionX
                    step = delta / abs(delta)
                    print('step,',step)
                    positionX = positionX + step # add only one single step
                    fPositionX = positionX
                    continue
            # PID control to smooth it again
            fPositionX = positionX
            [positionXX, speed] = PID.posiFlter(positionX, timeTag) 
            
            # LMMSE 
            spd.pushLocation(timeTag,positionXX)
            avsp = spd.speedCalculate()
            avsp = abs(avsp)
            if avsp ==  0:
                avspAcc = avsp
            else:
                avspAcc = avspAcc * 0.3 + avsp * 0.7

            # avoid the case that the iBeacon is too far away 
            if rssiBuf.count(-100) >= 3:
                speed = 0
                
            # print the log 
            if preCounter >= 3:
                positionLog = str(timeTag) + ","+str(positionXX) + ','
                orginLog = str(positionX) + ','
                avrsLog = str(avspAcc)+','
                speedLog = str(speed) + '\n'
                myFile.writelines(positionLog+orginLog+avrsLog)
                myFile.writelines(speedLog)
                #print ("time: ", round(timeTag,2)),
                #print("index: ", indexBuf),
                #print("rssi: ", rssiBuf)
                #print ("position: ", round(positionXX,2)),
                #print("oringin:",round(positionX,2)),
                #print("average speed: ", round(avspAcc, 2)),
            
            #send data to server
            data = {
                'type':'1',
                'target': '1005',
                'ts': round(timeTag,2),
                'loc_x': round(positionXX,2),
                'loc_y': round(positionY, 2),
                'val': round(speed, 2),
                'val_avg': round(avspAcc,2),
                'status':int(alarmState)
            }
            if mtr_server_state == True:
                myClient.sendData(data)
            
            

if __name__ == '__main__':
    #---- load program information from db.cfg-----#
    avspAcc = 0
    alarmState = False
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
    print("network service status:", mtr_server_state)
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
    threadAlarmSrv = threading.Thread(target=mtrAlarm)
    threadAlarmSrv.start()
    mtr_service(myRSSI)


