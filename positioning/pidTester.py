import purePI_ctlersp as purePI
import matplotlib.pyplot as plt
import time
if __name__ == '__main__':
	myFile = open("dataLog " + time.asctime(time.localtime(time.time())) + ".txt", 'w')
	myfile = open('4.txt')
	line = myfile.readlines()
	PID = purePI.purePI_Ctler(-72)
	for i  in range (len(line)):
		line[i] = line[i].rstrip('\n')
		#print line[i]
	time = []
	position = []
	speed = []
	for i in range(len(line)):
		buff = line[i].split(',')
		time.append(float(buff[0]))
		position.append (float(buff[1]))
		speed.append(float(buff[2]))
		
	for i in range(len(position)-1):
		[position[i], speed[i]] = PID.posiFlter(position[i], time[i])
		print position[i],speed[i]
		positionLog = str(time[i]) + "," + str(position[i]) + ','
		speedLog = str(speed[i]) + '\n'
		# myFile.writelines(rawDataLog)
		myFile.writelines(positionLog)
		myFile.writelines(speedLog)

