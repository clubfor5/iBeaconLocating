import sys
import os
import matplotlib.pyplot as plt
import numpy as np
import purePI_ctlersp as purePI
Qk = 1
P0 = -72
Hk = 1
Rk = 1000
v = 0
fposition = -72
P = []
newPosition = []
def kalman_filter(position, fPosition, time, Pk_):
	### prediction 
	xk = fPosition + time * v 
	Pk = Pk_ + Qk
	#print ("Pk: ", Pk)
	### update 1
	ek = position - xk
	Sk = Pk  + Rk
	#print ("SK: ", Sk)
	Kk = 0.02
	#print ("Kk: ", Kk)
	#### update 2
	xkk = xk + Kk * ek
	Pk = (1 - Kk)*Pk   
	return xkk, Pk

def speedCalculator(position,fPosition,timeLag):
	return (position - fPosition) / timeLag


if __name__ == '__main__':
	myfile = open('2.txt')
	line = myfile.readlines()
	for i  in range (len(line)):
		line[i] = line[i].rstrip('\n')
		#print line[i]
	time = []
	time.append(0)
	position = []
	position. append(P0)
	speed = []
	for i in range(len(line)):
		buff = line[i].split(',')
		time.append(float(buff[0]))
		position.append (float(buff[1]))
		#speed.append(float(buff[2]))	
	P.append(1.22)
	speed.append(0)
	newPosition.append(-72)
	for i in range(1, len(position)):
		filtered_position,Pk = kalman_filter(position[i], fposition, time[i] - time[i-1], P[i-1]) 
		fposition = filtered_position
		P.append(Pk)
		newPosition.append(filtered_position)
	print newPosition
	#print position
	#print P
	for i in range(5, len(newPosition)):
		sp = speedCalculator(newPosition[i] , newPosition[i-5] , (time[i] - time[i-5] ))
		speed.append(sp)
	for i in range(4):
		speed.append(0)

	print speed
	x = np.array(time)
	y = np.array(newPosition)
	s = np.array(speed)
	ok = np.array(position)
	#plt.plot(x, ok)
	#plt.show()
	#plt.plot(x, y)
	#plt.show()
	#plt.plot(x, s)
	#plt.show()
	################### 
	fig = plt.subplot(1,3,1)
	plt.sca(fig)
	plt.grid()
	plt.plot(x, ok,'r')
	fig = plt.subplot(1,3,2)
	plt.sca(fig)
	plt.grid()
	plt.plot(x, y,'r')
	fig = plt.subplot(1,3,3)
	plt.sca(fig)
	plt.grid()
	plt.plot(x, s,'r')
	plt.show()
        
