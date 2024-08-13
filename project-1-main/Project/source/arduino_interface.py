import serial.tools.list_ports
import data, config, time
from config import logger


def portConfig():
    ports = serial.tools.list_ports.comports() #https://youtu.be/AHr94RtMj1A?si=uIVSIY6_S2sPDFUR

    portList = []

    for onePort in ports:
        portList.append(str(onePort))
        print(str(onePort))

    comPort = input("select com port: ")

    for x in range(0, len(portList)):
        if portList[x].startswith("COM" + str(comPort)):
            portVar = "COM" + str(comPort)
            config.write_config("portVar", portVar)

def arduino_connect():
    serialInst = serial.Serial()  
    serialInst.baudrate = 9600
    serialInst.port = config.get_config("portVar")
    serialInst.open()

    while True:
        if serialInst.in_waiting:
            packet = serialInst.readline().decode("utf").rstrip("\r\n")
            if packet != 0:
                logger.debug("arduino_connect attempting to aquire data lock")
                with config.data_lock:
                    logger.debug("arduino_connect aquired data lock")
                    data.write_data("sensorData", packet)
                logger.debug("arduino_connect released data lock")
                packet = 0
            time.sleep(0.1)

