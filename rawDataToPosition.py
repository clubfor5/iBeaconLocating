import numpy as np
import json
import positioning.beaconAddress as beaconAdd
import positioning.position as pos
import time
if __name__ == '__main__':
	myFile = open("log/feb261540.txt")
	lines = myFile.readlines()
	beaconAddress = []
	beaconInfos,numOfBeacons = beaconAdd.getBeaconInfo()
	lines[0] = lines[0].lstrip('[')
	lines[0] = lines[0].rstrip(']\n')
	buff = json.loads(lines[0])
	startTime = time.time()
	timeTag = 0
	for i in range(1,len(lines)):
		#lines[i].replace('{','')
		#lines[i].replace('{','')
		lines[i] = lines[i].lstrip('[')
		lines[i] = lines[i].rstrip(']\n')
		data = json.loads(lines[i])
		RSSI = data['rssi']
		#print(data['rssi'],timeTag)
		positionX,positionY, timeT = pos.proximity(startTime, RSSI, beaconInfos)
		timeTag = timeTag + 0.6
		print(timeTag,positionX)
	
