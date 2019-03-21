import numpy as np
import time
import ConfigParser



def proximity(startTime, rssiTable, beaconInfos):
    ### Sort the strength of signals 

    cp = ConfigParser.ConfigParser()
    cp.read("/home/pi/iBeaconLocating/config/db.cfg")
    debug = cp.get('iBeacon_config', "positionInfo")
    numOfBeacons = len(rssiTable)
    buff = rssiTable
    sortList = np.argsort(buff)
    
    maxIndex = sortList[numOfBeacons - 1]
    smaxIndex = sortList[numOfBeacons - 2]

    maxRSSI = rssiTable[maxIndex]
    smaxRSSI = rssiTable[smaxIndex]
    maxTag = beaconInfos[maxIndex].tag
    smaxTag = beaconInfos[smaxIndex].tag 
    maxPositionX = (beaconInfos[maxIndex]).positionX
    maxPositionY = (beaconInfos[maxIndex]).positionY
    smaxPositionX = (beaconInfos[smaxIndex]).positionX
    smaxPositionY = (beaconInfos[smaxIndex]).positionY
	

	
    ### Check out the difference of signal strength 
    if maxRSSI - smaxRSSI  >= 6:
        positionX = maxPositionX
        positionY = maxPositionY
        
    elif maxRSSI - smaxRSSI  >= 3:
        positionX = maxPositionX * 0.75 + smaxPositionX * 0.25
        positionY = maxPositionY * 0.75 + smaxPositionY * 0.25
   
    else:
	      positionX = maxPositionX * 0.5 + smaxPositionX * 0.5
	      positionY = maxPositionY * 0.5 + smaxPositionY * 0.5 
	
    
    ### in case that max and smax is not neighbor 
    if abs(maxPositionX - smaxPositionX) >= 11:
        positionX = maxPositionX
	positionY = maxPositionY
    
    timeTag = round(time.time() - startTime, 2)
    if debug == '2':
		print('max and smax tag: ', maxTag, smaxTag)
		print('max and smax position: ', maxPositionX, maxPositionY, smaxPositionX, smaxPositionY)
		print('loc:', positionX, positionY,timeTag)
    elif debug == '1':
		print('loc:', positionX, positionY,timeTag)
        
    return positionX,positionY,timeTag
