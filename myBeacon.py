from bluepy.btle import Scanner, DefaultDelegate
import urllib3
import time
import json
#from requests_futures.sessions import FuturesSession as FS


locked = False
beacons = ['12:3b:6a:1b:90:98','12:3b:6a:1b:94:2d','12:3b:6a:1b:8e:08','12:3b:6a:1b:8e:06','12:3b:6a:1b:97:f5', '12:3b:6a:1b:8f:64','12:3b:6a:1b:93:52','12:3b:6a:1b:8e:96','12:3b:6a:1b:87:ce', '12:3b:6a:1b:90:9f']


class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)		
		

def verifyBeacon(macBeacon): #function responsible for verify if we still in the beacon presence.
    global locked,scanner
    found = False
    print('Looking for beacon')
    while locked:
        devices = scanner.scan(3)
        for item in devices:
            if macBeacon == item.addr.upper():
                print('Beacon stills')
                found = item.addr.upper()
        if macBeacon == found:
            found = False;
            print('#----------#----------#---------#---------------#--------------#')
            continue
        else:
            print('Beacon perdido')
            locked = False
            if macBeacon == 'F9:70:DB:A9:7C:7A':
                pass
            elif macBeacon == 'DB:D5:1D:C1:F3:49':
                pass
            elif macBeacon == 'FF:D8:B1:6B:5E:9D':
                pass
            elif macBeacon == 'DF:67:4F:0F:DA:8D':
                pass
            return

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
        devices = scanner.scan(0.47) #insert a time to timeout inside the squares. this returns a list with ALL bluetooth devices nearby (not only BLE).
        for dev in devices:
            if not beacons.__contains__(dev.addr): #first of all check if the device at this position is or not one of ours beacons. if not, we just continue the loop, passing to next interaction.
                continue

            elif beacons.__contains__(dev.addr):
                myDevice = True
                myFile.writelines(json.dumps({"addr": dev.addr, "RSSI": dev.rssi, "time": currentTime}, sort_keys = True, indent = 4, separators=(',', ':')) + "\n")
                
                count = count + 1
        tick = tick + 1
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
        print("")
beaconScanner()
