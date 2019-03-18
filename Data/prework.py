
with open("77.txt", 'r') as myFile:
    output = open("077.txt",'w')
    data = myFile.readlines()
    
    for line in data:
        myLine = line.replace("[","")
        myLine = myLine.replace("]","")
        output.write(myLine+"\n")
    output.close()