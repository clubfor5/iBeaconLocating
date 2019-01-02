import ConfigParser


cp = ConfigParser.ConfigParser()
cp.read("db.cfg")

beta = cp.getfloat('iBeacon_config', "EWMA_Beta")
print(beta * 99)
beacons =  cp.get('iBeacon_address', "beacons").split(',')
print(beacons)