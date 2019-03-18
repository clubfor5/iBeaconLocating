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


myClient = mtr.mtrClient()

#from requests_futures.sessions import FuturesSession as FS
import ConfigParser
cp = ConfigParser.ConfigParser()
cp.read("db.cfg")

beta = cp.getfloat('iBeacon_config', "EWMA_Beta")
beacons =  cp.get('iBeacon_address', "beacons").split(',')
#print(beacons)
myRSSI = []
for i in range(0,10):
    myRSSI.append(-150)
    
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)		
		
#--defining the scan object--#
scanner = Scanner().withDelegate(ScanDelegate())
#=========#=====================#==========#======================#=========
def beaconScanner():
    count = 0
    tick = 0
    loss = 0
    total = 0
    myFile = open("iBeaconRawData " + time.asctime(time.localtime(time.time())) + ".txt", 'w')
    while True:
        currentTime = time.time()
        myDevice = False
        global lastSended, scanner,locked   
        devices = scanner.scan(0.57) #insert a time to timeout inside the squares. this returns a list with ALL bluetooth devices nearby (not only BLE).
        print(time.time() - currentTime)
        for dev in devices:
            if not beacons.__contains__(dev.addr): #first of all check if the device at this position is or not one of ours beacons. if not, we just continue the loop, passing to next interaction.
                continue

            elif beacons.__contains__(dev.addr):
                myDevice = True
                index = beacons.index(dev.addr)
                if myRSSI[index] == -150:
                    myRSSI[index] = dev.rssi
                else:
                    myRSSI[index] = int(myRSSI[index] * beta + dev.rssi * (1-beta))
                myFile.writelines(json.dumps({"addr": dev.addr, "RSSI": dev.rssi, "time": currentTime}, sort_keys = True, indent = 4, separators=(',', ':')) + "\n")
                count = count + 1
        tick = tick + 1
        #(time.time() - currentTime)
        if myDevice == True:
            print("Received "),
            print(count),
            print(" packets in time"),
            print(currentTime)
            total = total + count
            print("Total: "),
            print(total),
            print(" Tick: "),
            print(tick),
            print(" Average: "),
            print(total / tick)
            count = 0
        else:
            loss = loss + 1
            print("packet loss"),
            print(loss),
            print("int time"),
            print(currentTime)
            count = 0
        position()
        print("")
        
def position():
    a = myRSSI
    c = np.argsort(a)
    MAX = myRSSI[c[9]]
    SMAX = myRSSI[c[8]]
    print(c)
    if MAX - SMAX >= 8:
        position = c[9] * 6
    elif MAX - SMAX >= 4:
        position = (c[9] * 0.75 + c[8]* 0.25) * 6
    else:
        position = (c[9] * 0.5 + c[8] * 0.5) * 6
    print(position)
    data = [{
    'mac': 'testMac',
    'ts': int(time.time()),
    'loc_x': '0',
    'loc_y': position,
    'remark': 'Mtrtest',
    }]
    
    myClient.sendData(data)
    
    
    
thread.start_new_thread(beaconScanner())
