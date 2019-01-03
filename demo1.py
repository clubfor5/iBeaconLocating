from bluepy.btle import Scanner, DefaultDelegate
import urllib3
import time
import json
#import mythread
import thread
import operator
import numpy as np
import rssiTable
#from requests_futures.sessions import FuturesSession as FS
import ConfigParser
cp = ConfigParser.ConfigParser()
cp.read("db.cfg")
myTable = rssiTable.RssiTable(10, 10)
beta = cp.getfloat('iBeacon_config', "EWMA_Beta")
print(beta * 99)
beacons =  cp.get('iBeacon_address', "beacons").split(',')
print(beacons)
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
        devices = scanner.scan(1) #insert a time to timeout inside the squares. this returns a list with ALL bluetooth devices nearby (not only BLE).
        print(time.time() - currentTime)
        rssiTable = np.zeros(10)
        for dev in devices:
            if not beacons.__contains__(dev.addr): #first of all check if the device at this position is or not one of ours beacons. if not, we just continue the loop, passing to next interaction.
                continue

            elif beacons.__contains__(dev.addr):
                myDevice = True
                index = beacons.index(dev.addr)
                rssiTable[index] = dev.rssi
        
        tick = tick + 1
        myTable.addRawData(rssiTable)
        #(time.time() - currentTime)
        print(myTable.table)
        print("Var:")
        print(myTable.validVar())
        
        
def position():
    a = myRSSI
    c = np.argsort(a)
    print(a)
    print(c)
    
    


thread.start_new_thread(beaconScanner())
