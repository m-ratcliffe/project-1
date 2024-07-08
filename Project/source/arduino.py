import serial.tools.list_ports


ports = serial.tools.list_ports.comports() #https://youtu.be/AHr94RtMj1A?si=uIVSIY6_S2sPDFUR
serialInst = serial.Serial()

portList = []

for onePort in ports:
    portList.append(str(onePort))
    print(str(onePort))

comPort = input("select com port: ")

for x in range(0, len(portList)):
    if portList[x].startswith("COM" + str(comPort)):
        portVar = "COM" + str(comPort)
        print(portVar)

serialInst.baudrate = 9600
serialInst.port = portVar
serialInst.open()

while True:
    if serialInst.in_waiting:
        packet = serialInst.readline().decode("utf")
        print(packet, end="")