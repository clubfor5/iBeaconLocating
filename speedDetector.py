class SpeedDetector:
    def __init__(self, size):
        self.time = []
        self.position =[]
        self.size = size
        self.sumT = 0
        self.sumP = 0
        self.sumT2 = 0
        self.sumP2 = 0
        self.sumTP = 0
        
    def pushLocation(self, time, location):
        self.position.append(location)   
        self.time.append(time)
        if len(self.time) == self.size + 1:
            self.position.pop(0)
            self.time.pop(0)
    
    def speedCalculate(self):
        if len(self.time) < self.size:
           # print(self.size)
           # print(len(self.time))
           # print("OK!")
            return 0
            
        self.sumT = 0
        self.sumP = 0
        self.sumT2 = 0
        self.sumP2 = 0
        self.sumTP = 0
        
        for i in range(self.size):
            self.sumT = self.sumT + self.time[i]
            self.sumP = self.sumP + self.position[i]
            self.sumT2 = self.sumT2 + self.time[i] * self.time[i] 
            self.sumP2 =  self.sumP2 + self.position[i] * self.position[i] 
            self.sumTP = self.sumTP + self.time[i] * self.position[i]
        print(self.position)
        speed = (float)(self.size * self.sumTP - self.sumT * self.sumP) / (float)(self.size* self.sumT2 - self.sumT * self.sumT)

        if abs(speed) < 0.01:
            speed = 0
        print(speed)
        return speed
        
