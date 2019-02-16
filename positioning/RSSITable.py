import ConfigParser

cp = ConfigParser.ConfigParser()
cp.read("config/db.cfg")
debug = cp.get('iBeacon_config', "rssiInfo")

def getEWMAFilteredRSSI(devices, beaconAddress, mask, rssiTable):
        for i in range(len(mask)):
            mask[i] = mask[i] + 1
            
        for dev in devices:
            # first of all check if the device at this position is or not one of ours beacons. if not, we just continue the loop, passing to next interaction.
            if not beaconAddress.__contains__(dev.addr):
                continue
            elif beaconAddress.__contains__(dev.addr):
                index = beaconAddress.index(dev.addr)
                mask[index]  = 0 
                temp = flts.ewma(rssiTable[index], dev.rssi, beta)
                rssiTable[index] = round(rssiTable[index],2)
                
        for i in range(len(mask)):
            if mask[i] > 5:
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
