import serial.tools.list_ports
import data, config, time
from config import logger

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

