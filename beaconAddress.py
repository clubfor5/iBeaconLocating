import ConfigParser
class BeaconPoll:
	def __init__(self, address, positionX, positionY, tag):
		self.address = address
		self.positionX = positionX
		self.positionY = positionY
		self.tag = tag

def getBeaconInfo():
	beaconInfos = []
	cp = ConfigParser.ConfigParser()
	cp.read("addressTable.cfg")
	beaconAdd = cp.get('iBeacon_address', "beacons").split(';\n')
	numOfBeacons = len(beaconAdd)
	for beacon in beaconAdd:
		#print(beacon)
		beaconOperator = beacon.split(',')
		addressBuffer = beaconOperator[0]
		try: 
			positionXBuffer = (float)(beaconOperator[1])
			positionYBuffer = (float)(beaconOperator[2])
			tagBuffer = (int)(beaconOperator[3])
		except:
			print("failed of construction of beacon addressTable, error with addressTable.cfg")			
			break	
					
		beacon = BeaconPoll(addressBuffer, positionXBuffer, positionYBuffer, tagBuffer)
		beaconInfos.append(beacon)
	return beaconInfos,numOfBeacons

if __name__ == '__main__':
    #### Load things from the config file
	beaconInfos,numOfBeacons = getBeaconInfo()
	for i in range(numOfBeacons):
		print(beaconInfos[i].address)

