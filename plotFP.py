import numpy as np
from scipy.spatial.distance import pdist
import matplotlib.pyplot as plt
import fingerprint as fp
position =[]
table = []
table, positionInfo = fp.getFingerPrintTable()
for i in range(1, len(positionInfo)):
    positionInfo[i] = positionInfo[i] + 3
result = np.array(table)
shape = result.shape
print(result)
for x in range(0, shape[0]):
    for y in range(0, shape[1]):
        if table[x][y] == 0:
            if(x !=0):
                result[x][y] = result[x-1][y]
            else:
                result[x][y] = -90

plt.figure(1)
x = np.linspace(0,51,18)
for i in range(0, 10):
    fig = plt.subplot(5, 2,i+1)
    #fig.set_size_inches(3,2)
    plt.sca(fig)
    plt.xlim((0,51))
    plt.ylim((-100,-50))
    plt.xlabel('distance',fontsize=11)
    plt.ylabel('RSSI', fontsize=11)
    plt.title("No."+str(i))
    plt.xticks(np.linspace(0,51,18))
    plt.yticks(np.linspace(-100,-50,11))
    plt.axvspan(0,51,-100,-50)
    plt.grid()
    plt.plot(positionInfo,result[...,i],'r')
plt.show()
        