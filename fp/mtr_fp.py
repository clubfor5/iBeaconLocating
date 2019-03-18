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
import fingerprint as fp
cp = ConfigParser.ConfigParser()
cp.read("db.cfg")
myTable = rssiTable.RssiTable(10, 5)
beta = cp.getfloat('iBeacon_config', "EWMA_Beta")
#print(beta * 99)
beacons =  cp.get('iBeacon_address', "beacons").split(',')

out = np.loadtxt("Data/066.txt")
#print(beacons)
myRSSI = []
for i in range(0,10):
    myRSSI.append(0)
    
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
    myFile = open("Data/RD " + time.asctime(time.localtime(time.time())) + ".txt", 'w')
    myFile1 = open("Data/RS " + time.asctime(time.localtime(time.time())) + ".txt", 'w')
    while True:
        currentTime = time.time()
        myDevice = False
        global lastSended, scanner,locked   
        devices = scanner.scan(0.58) #insert a time to timeout inside the squares. this returns a list with ALL bluetooth devices nearby (not only BLE).
       # print(time.time() - currentTime)
        rssiTable = np.zeros(10)
        for dev in devices:
            if not beacons.__contains__(dev.addr): #first of all check if the device at this position is or not one of ours beacons. if not, we just continue the loop, passing to next interaction.
                continue

            elif beacons.__contains__(dev.addr):
                myDevice = True
                index = beacons.index(dev.addr)
                rssiTable[index] = dev.rssi
        
        tick = tick + 1
        #myTable.addRawData(rssiTable)
        myTable.addRawData(out[tick])
        #print(myTable.table)
        myRSSI = myTable.mean()
        #print(myRSSI)
        #(time.time() - currentTime)      
        #print(myTable.table)
        #print("Var:")
        var = myTable.validVar()
        position(myRSSI)
       # print(var)
       # print(myRSSI)
       # myFile1.writelines(json.dumps({"tick": tick, "RSSI": rssiTable.tolist(), "Var": var.tolist()  }, sort_keys = True, indent = 4, separators=(',', ':')) + "\n")
       # myFile.writelines(str(rssiTable) + '\n')   
def position(rssi):
    #rssiVec = myRSSI
    #print(myRSSI)
    fpTable = fp.getFingerPrint()
    #rssiVec = fpTable[1]
    tableLength = len(fpTable)
    result = fp.determination(rssi,fpTable,tableLength)*3
    print("positions order: ")
    print(result)
    print


thread.start_new_thread(beaconScanner())
