from bluepy.btle import Scanner, DefaultDelegate
import urllib3
import time
#from requests_futures.sessions import FuturesSession as FS


locked = False
beacons = ['12:3b:6a:1b:90:8d','f9:70:db:a9:7c:7a','DB:D5:1D:C1:F3:49','db:d5:1d:c1:f3:49', 'FF:D8:B1:6B:5E:9D','ff:d8:b1:6b:5e:9d','DF:67:4F:0F:DA:8D','df:67:4f:0f:da:8d']


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
    while True:
        global lastSended, scanner,locked
        devices = scanner.scan(1) #insert a time to timeout inside the squares. this returns a list with ALL bluetooth devices nearby (not only BLE).
        for dev in devices:
            if not beacons.__contains__(dev.addr): #first of all check if the device at this position is or not one of ours beacons. if not, we just continue the loop, passing to next interaction.
                print(dev.addr)
                continue

            elif beacons.__contains__(dev.addr):
                if dev.addr.upper() == '12:3B:6A:1B:90:8D':  # 1 
                    print('A found')
                    print(dev.rssi)
                    locked = True #Change the state of the locked variable, forcing to enter in the "if" bellow.
                    if locked:
                        verifyBeacon('F9:70:DB:A9:7C:7A') #we will be inside this function while beacon stills present.
						#when it finishes, we continue to the next interaction. Repeat it for each beacon.
						#You can add other functionalities to your code here, like sending the beacon state(far/close).
                        continue

                elif dev.addr.upper() == 'DB:D5:1D:C1:F3:49':  # 1
                    print('B found')
                    locked = True
                    if locked:
                        verifyBeacon('DB:D5:1D:C1:F3:49')
                        continue

                elif dev.addr.upper() == 'FF:D8:B1:6B:5E:9D':  # 1
                    print('C found')
                    locked = True
                    if locked:
                        verifyBeacon('FF:D8:B1:6B:5E:9D')
                        continue

                elif dev.addr.upper() == 'DF:67:4F:0F:DA:8D':  # 1
                    print('D found')
                    locked = True
                    if locked:
                        verifyBeacon('DF:67:4F:0F:DA:8D')
                        continue


beaconScanner()
