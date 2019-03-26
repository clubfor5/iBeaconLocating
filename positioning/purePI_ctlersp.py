import numpy as np
#import matplotlib.pyplot as plt
#These imports serves for demo
#########################################################
class purePI_Ctler:

    def __init__(self, start_posi, kp=0.12, ki=0.42, skp=0.63 * 0.75, ski=0.42 * 0.75, skpr = 0.0045 * 0.75):
        self.kp = kp
        self.ki = ki
        self.skp = skp
        self.ski = ski
        self.skpr = skpr
        self.__uBuffer = 0       
        self.__time = [0 for i in range(8)]  
        self.output = 0
        self.uk = 0      
        self.speed = 0    
        self.__uspeed = 0 
        self.__uspeed1 = 0
        self.__speedIBuffer = 0    
        self.__outputBuffer = [start_posi for i in range(8)] 
        self.__speedBuffer = [0.3 for i in range(8)]
    
    def posiFlter(self,position,time):
        self.uk = position - self.__outputBuffer[0]
        delOutput = self.kp*(self.uk-self.__uBuffer) + self.ki*self.uk
        self.output = self.__outputBuffer[0] + delOutput
        self.output = (self.output + self.__outputBuffer[0] + self.__outputBuffer[1])/3
        for i in range(len(self.__outputBuffer)-2,-1,-1):
            self.__outputBuffer[i+1] = self.__outputBuffer[i]
            self.__time[i+1] = self.__time[i]
            self.__speedBuffer[i+1] = self.__speedBuffer[i]
        self.__outputBuffer[0] = self.output
        self.__time[0] = time
        self.__uBuffer = self.uk
        self.speed = (self.__outputBuffer[0]-self.__outputBuffer[3])/(self.__time[0]-self.__time[3])
        self.speed = abs(self.speed)
        self.__uspeed = self.speed - self.__speedBuffer[0]
        delSpeed = self.skp*(self.__uspeed-self.__uspeed1)+self.ski*self.__uspeed-self.skpr*(self.__speedBuffer[0]-self.__speedBuffer[7])
        self.__speedBuffer[0] = self.__speedBuffer[0]+delSpeed
        self.__speedBuffer[0] = sum(self.__speedBuffer[0:4])/4
        self.__uspeed1 = self.__uspeed
        self.speed = self.__speedBuffer[0]

        return self.output,self.speed
    


