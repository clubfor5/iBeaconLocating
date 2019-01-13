import numpy as np
import time
class RssiTable:
    def __init__(self, beaconNum = 3, sequenceNum = 3):
        self.table = np.zeros([sequenceNum, beaconNum], dtype = np.int16)
        self.beaconNum = beaconNum
        self.sequenceNum = sequenceNum
        self.validSequences = np.zeros(self.beaconNum)
     # Notice that the rssiRaw should be array of size sequenceNum
    def addRawData(self, rssiRaw):
         for i in range(0, self.sequenceNum-1):
             self.table[i] = self.table[i+1]
         self.table[i+1] = rssiRaw
     
     # the RSSI at certain timing
    def selectTiming(self, time):
         return self.table[time,...]
     
     # RSSI of certain beacon in different timing
    def selectBeacon(self, beacon):
         return self.table[...,beacon]
    
    # ugly code calculating the var and valid num, I want C!!!!
    def validVar(self):
         validVar = np.zeros(self.beaconNum, np.float)
         self.validSequences = np.zeros(self.beaconNum)
         for i in range(0, self.beaconNum):
             table = self.table[...,i]
             #remove 0s
             E2X = 0
             EX = 0.0
             SUM = 0.0
             EX2 = 0.0
             Counter = 0
             for j in range(0, self.sequenceNum):
                if(table[j] != 0):
                   Counter = Counter + 1
                   SUM = SUM + table[j]
                   EX2 = EX2 + table[j] * table[j]
             if Counter != 0:
                 
                 EX2 = EX2 / Counter
                 EX = SUM / Counter
                 E2X = EX * EX
                 self.validSequences[i] = Counter
                 validVar[i] = EX2 - E2X
             else:
                 validVar[i] = 0
         return validVar
    

    def mean(self):
        mean = np.zeros(10, np.float)
        self.validSequences = np.zeros(10)
        for i in range(0, 10):
            table = self.table[...,i]
             #remove 0s
            E2X = 0
            EX = 0.0
            SUM = 0.0
            EX2 = 0.0
            Counter = 0
            for j in range(0, self.sequenceNum):
                if(table[j] != 0):
                    Counter = Counter + 1
                    SUM = SUM + table[j]
            if Counter != 0:
                mean[i] = SUM / Counter
            else:
                mean[i] = 0
        return mean