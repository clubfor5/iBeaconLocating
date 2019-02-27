import ConfigParser
import sys
import filters as flts
import time
import json
cp = ConfigParser.ConfigParser()
cp.read("/home/pi/iBeaconLocating/config/db.cfg")
debug = cp.get('iBeacon_config', "rssiInfo")
beta = float(cp.get('iBeacon_config', 'EWMA_Beta'))
rawDataFile = open("/home/pi/iBeaconLocating/log/RawDataLog " + time.asctime(time.localtime(time.time())) + ".txt", 'w')
def getEWMAFilteredRSSI(devices, beaconAddress, mask, rssiTable):
        for i in range(len(mask)):
            mask[i] = mask[i] + 1
        buffer = rssiTable
        for dev in devices:
            # first of all check if the device at this position is or not one of ours beacons. if not, we just continue the loop, passing to next interaction.
            if not beaconAddress.__contains__(dev.addr):
                continue
            elif beaconAddress.__contains__(dev.addr):
                index = beaconAddress.index(dev.addr)
                mask[index]  = 0 
                temp = flts.ewma(rssiTable[index], dev.rssi, beta)
                rssiTable[index] = round(temp,2)
                buffer[index] = dev.rssi
            data = [{
                'Type': 'Raw',
                'mac': 'testMac',
                'ts': int(time.time()),
                'rssi': buffer,
                'remark': 'Mtrtest',
            }]
            rawDataFile.writelines(json.dumps(data) + '\n')
        for i in range(len(mask)):
            if mask[i] > 8:
                rssiTable[i] = -100
        
        if debug == '1':
            print("Filtered Raw Data:", rssiTable)
        
        return rssiTable


def getKalmanFilteredRSSI():
    return 0 
   
    
def getRawData(devices, beaconAddress, mask):
    numOfBeacons = len(beaconAddress)
    
    rssiTable = []
    for i in range(numOfBeacons):
        rssiTable.append(-100)
        
    for dev in devices:
        if not beaconAddress.__contains__(dev.addr):
            continue
        elif beaconAddress.__contains__(dev.addr):
            index = beaconAddress.index(dev.addr)
            rssiTable[index] = dev.rssi
            
    if debug == '1':
        print("Raw Data: ", rssiTable)
        
    return rssiTable
