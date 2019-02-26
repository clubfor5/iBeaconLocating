import numpy as np
import matplotlib.pyplot as plt
#These imports serves for demo
#########################################################
class purePI_Ctler:

    def __init__(self, start_posi, kp=0.12, ki=0.42):
        self.kp = kp
        self.ki = ki
        self.__uBuffer = 0       
        self.__time = [0 for i in range(10)]
        self.output = 0
        self.uk = 0      
        self.__delOutput = 0   
        self.speed = 0   
        self.__uspeed = 0 
        self.__delSpeed = 0
        self.__formerSpeed = 0   
        self.__speedIBuffer = 0    
        self.__outputBuffer = [start_posi for i in range(10)]
        self.__speedBuffer = [0 for i in range(10)]
    
    def posiFlter(self,position,time):
        self.uk = position - self.__outputBuffer[0]
        self.__delOutput = self.kp*(self.uk-self.__uBuffer) + self.ki*self.uk
        self.output = self.__outputBuffer[0] + self.__delOutput
        self.output = (self.output + self.__outputBuffer[0] + self.__outputBuffer[1])/3
        for i in range(len(self.__outputBuffer)-2,-1,-1):
            self.__outputBuffer[i+1] = self.__outputBuffer[i]
            self.__time[i+1] = self.__time[i]
            self.__speedBuffer[i+1] = self.__speedBuffer[i]
        self.__outputBuffer[0] = self.output
        self.__time[0] = time
        self.__uBuffer = self.uk
        self.speed = (self.__outputBuffer[0]-self.__outputBuffer[9])/(self.__time[0]-self.__time[9])
        self.__speedBuffer[0] = self.speed
        self.speed = sum(self.__speedBuffer)/len(self.__speedBuffer)
        self.__uspeed = self.speed - self.__formerSpeed
        self.__delSpeed = (self.kp - 0.08)*(self.__uspeed-self.__speedIBuffer) + (0)*self.__uspeed
        self.speed = self.__delSpeed + self.__formerSpeed
        self.__formerSpeed = self.speed

        return self.output,self.speed
    

#####################################
#demo
if __name__ == '__main__':
        f = np.loadtxt("/Users/siriushe/Documents/MATLAB/sampledata.txt",delimiter = ',')
        ctler = purePI_Ctler(f[0][1]) 
        output = [0 for i in range(len(f[:][:]))] 
        speed = [0 for i in range(len(output))] 
        output[0] = f[0][1]         
        speed[0] = 0            
        for i in range(len(output)-1):   
                [output[i+1],speed[i+1]] = ctler.posiFlter(f[i+1][1],f[i+1][0])
                x = [i for i in range(len(output))] 
        plt.figure
        plt.plot(x,speed)
        plt.savefig('/Users/siriushe/Desktop/abcd.png')


