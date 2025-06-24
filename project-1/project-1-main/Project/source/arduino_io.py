import serial.tools.list_ports
import data_store, module2, time
from module2 import logger

#Pulls data from the arduino
def arduino_connect():
    serialInst = serial.Serial()  
    serialInst.baudrate = 9600
    serialInst.port = module2.get_config("portVar")
    serialInst.open()

    try:
        while True:
            if serialInst.in_waiting:
                packet = serialInst.readline().decode("utf").rstrip("\r\n")
                if packet != "None":
                    logger.debug("arduino_connect attempting to aquire data lock")
                    with module2.data_lock:
                        logger.debug("arduino_connect aquired data lock")
                        data_store.write_data("sensorData", packet)
                    logger.debug("arduino_connect released data lock")
                    
                #time.sleep(0.1)
    except serial.SerialException as e:
        logger.error(f"Error connecting to Arduino: {e}")
