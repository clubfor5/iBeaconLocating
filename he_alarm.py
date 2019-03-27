import time
import numpy as np
#import matplotlib.pyplot as plt


### use as in the demo ################
### You only need to feed the current speed to it!!!####
### Very convenient!!!#######
###-.-#####

class he_alarm:

    def __init__(self, sp=1.4, almc1=1.3, alm_step=0.12, almc2=1.4):
        self.sp = sp
        self.almc1 = almc1
        self.alm_step = alm_step
        self.almc2 = almc2
        self.__speedBuffer = [0.3 for i in range(6)]
        self.status = 0
        self.time = time.time()
        self.thre1 = self.almc1 * self.sp
        self.thre2 = self.almc2 * self.sp
        self.threk = self.alm_step * self.sp

    def alarm_ctl(self, x):  # return alm_signal
        x = abs(x)
        for i in range(len(self.__speedBuffer) - 2, -1, -1):
            self.__speedBuffer[i + 1] = self.__speedBuffer[i]
        self.__speedBuffer[0] = x
        k = (sum(self.__speedBuffer[0:3]) - sum(self.__speedBuffer[3:6])) / 3
        t = time.time()
        # 1
        if ((self.status == 0)) and (x <= self.sp):
            self.status = 0
            return False
        # 2
        if (self.status == 0) and (x > self.sp):
            self.status = 1
            return False
        # 3
        if (self.status == 1) and (x <= self.sp):
            self.status = 0
            return False
        # 4
        if (self.status == 1) and (x > self.thre1) and (x <= self.thre2) and (k <= (self.threk)):
            self.status = 1
            return False
        # 5
        if (self.status == 1) and ((k > self.threk) and (x > self.thre1)) or (x > self.thre2):
            self.status = 2
            self.time = time.time()
            return True
        # 6
        if (self.status == 2) and ((t - self.time) > 3) and (x <= self.thre2) and (x > self.thre1):
            self.status = 1
            return False
        # 7
        if (self.status == 2) and (t - self.time <= 3):
            self.status = 2
            return True
        # 8
        if (self.status == 2) and (t - self.time > 3) and (x > self.thre2):
            self.status = 2
            self.time = time.time()
            return True
        # 9
        if (self.status == 2) and (t - self.time > 3) and (x <= self.thre1):
            self.status = 0
            return False
        self.status = 0
        return False


if __name__ == '__main__':
    f = np.loadtxt("/Users/siriushe/Documents/MATLAB/34data.txt")
    alarmCtl = he_alarm()  # here to create an object
    plt.figure
    plt.plot(f[:, 0], f[:, 4])
    alarm = [0 for i in range(len(f[:, 4]))]
    for i in range(len(f[:, 4])):
        alarm[i] = alarmCtl.alarm_ctl(f[i, 4])  # feed the current speed to it!!!
        time.sleep(0.6)

    plt.plot(f[:, 0], alarm)
    plt.savefig('/Users/siriushe/Desktop/abcdd.png')
