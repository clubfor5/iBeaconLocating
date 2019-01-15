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
import ConfigParser
import sys
import os
import fpGeneration as fpG

arg = sys.argv
length = len(sys.argv)
node = 0

def exit():
    try:
        print("invalid input argument.")
        os._exit(0)
    except:
        print("unknown error")

if length == 2:
    try:
        node = int(arg[1])
        print("collecting fingerprint No."),
        print(node)
    except:
       print(length)
       exit()
else:
    exit()

#myClient = mtr.mtrClient()
cp = ConfigParser.ConfigParser()
cp.read("db.cfg")

beta = cp.getfloat('iBeacon_config', "EWMA_Beta")
scanInterval = cp.getint('iBeacon_config', 'scanInt')
beacons =  cp.get('iBeacon_address', "beacons").split(',')
numOfBeacons = len(beacons)
myRSSI = []
for i in range(0,numOfBeacons):
    myRSSI.append(-100)

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)		
		
#--defining the scan object--#
scanner = Scanner().withDelegate(ScanDelegate())
#=========#=====================#==========#======================#=========
def beaconScanner():
    rawDataFileName = "fpRawData/" + str(node) + ".txt"
    fpFileName = "fp/" + str(node) + ".txt"
    rawDataFile = open(rawDataFileName, 'w')
    currentTime = time.time()
    collections = np.zeros(numOfBeacons)
    while time.time() - currentTime <= scanInterval:
        global lastSended, scanner,locked   
        devices = scanner.scan(0.57) #insert a time to timeout inside the squares. this returns a list with ALL bluetooth devices nearby (not only BLE).
        #get the existing RSSI table
        for i in range(0,numOfBeacons):
            myRSSI[i] = -100
        for dev in devices:
            if not beacons.__contains__(dev.addr): #first of all check if the device at this position is or not one of ours beacons. if not, we just continue the loop, passing to next interaction.
                continue
            elif beacons.__contains__(dev.addr):
                index = beacons.index(dev.addr)
                myRSSI[index] = dev.rssi
                collections[i] = collections[i] + 1
        for rssi in myRSSI:
            print(rssi),
            rawDataFile.write(str(rssi) + " ")
        print
        rawDataFile.write("\n")
    rawDataFile.close()
    fpG.fingerPrint(rawDataFileName, fpFileName)
    rawData = np.loadtxt(rawDataFileName)
    mean = fpG.getMean(rawData)
    print("finish collection of node No." + str(node))
    print("received packets: ")
    print(collections)
    print("RSSI Mean: ")
    print(mean)


beaconScanner()
