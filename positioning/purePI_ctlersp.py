import numpy as np
import matplotlib.pyplot as plt
#These imports serves for demo
#########################################################
class purePI_Ctler:

    def __init__(self, start_posi, kp=0.12, ki=0.42, skp=0.63, ski=0.42, skpr = 0.0045):
        self.kp = kp
        self.ki = ki
        self.skp = skp
        self.ski = ski
        self.skpr = skpr
        self.__uBuffer = 0       #上一时刻的控制器输入
        self.__time = [0 for i in range(8)]  #用于平滑
        self.output = 0
        self.uk = 0      #现在时刻的controller输入
        self.speed = 0    #当前输出速度
        self.__uspeed = 0 #当前速度输入量
        self.__uspeed1 = 0
        self.__speedIBuffer = 0    #上一时刻速度输入量
        self.__outputBuffer = [start_posi for i in range(8)] 
        self.__speedBuffer = [0 for i in range(8)]
    
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
        self.__uspeed = self.speed - self.__speedBuffer[0]
        delSpeed = self.skp*(self.__uspeed-self.__uspeed1)+self.ski*self.__uspeed-self.skpr*(self.__speedBuffer[0]-self.__speedBuffer[7])
        self.__speedBuffer[0] = self.__speedBuffer[0]+delSpeed
        self.__speedBuffer[0] = sum(self.__speedBuffer[0:4])/4
        self.__uspeed1 = self.__uspeed
        self.speed = self.__speedBuffer[0]

        return self.output,self.speed
    

#####################################
#demo
'''
f = np.loadtxt("/Users/siriushe/Documents/MATLAB/newdata2.txt",delimiter = ',')
ctler = purePI_Ctler(f[0][1]) #初始化时输入位置信息
output = [0 for i in range(len(f[:][:]))] #为方便输出图像用的list nevermind
speed = [0 for i in range(len(output))]  #同上
output[0] = f[0][1]          #初始信息
speed[0] = 0            #同上
for i in range(len(output)-1):   #每次把位置&时间输入进去
    [output[i+1],speed[i+1]] = ctler.posiFlter(f[i+1][1],f[i+1][0])
plt.figure
#plt.plot(f[:,0],f[:,2])
#plt.plot(f[:,0],speed)
plt.plot(f[:,0],output)
plt.savefig('/Users/siriushe/Desktop/abcdd.png')
'''

