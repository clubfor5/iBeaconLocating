from bluepy.btle import Scanner, DefaultDelegate
import urllib3
import time
#from requests_futures.sessions import FuturesSession as FS


locked = False
beacons = ['12:3b:6a:1b:90:a2','f9:70:db:a9:7c:7a','DB:D5:1D:C1:F3:49','db:d5:1d:c1:f3:49', 'FF:D8:B1:6B:5E:9D','ff:d8:b1:6b:5e:9d','DF:67:4F:0F:DA:8D','df:67:4f:0f:da:8d']


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
    loss = 0
    while True:
        count = count + 1
        myDevice = False
        global lastSended, scanner,locked
        devices = scanner.scan(0.5) #insert a time to timeout inside the squares. this returns a list with ALL bluetooth devices nearby (not only BLE).
        for dev in devices:
            if not beacons.__contains__(dev.addr): #first of all check if the device at this position is or not one of ours beacons. if not, we just continue the loop, passing to next interaction.
                continue

            elif beacons.__contains__(dev.addr):
                myDevice = True
                print(dev.addr)
                print(dev.rssi)
        if myDevice == False:
            loss = loss + 1
            print("packet loss: "),
            print(loss),
            print("/"),
            print(count)
beaconScanner()
