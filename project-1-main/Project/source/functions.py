from PIL import ImageFilter
from tkinter import filedialog
import data, config, time
from config import logger

#Blurs the image
def blur(img, currentBlur):
        if currentBlur == 1:
            logger.debug("blur attempting to aquire data lock")
            with config.data_lock:
                logger.debug("blur aquired data lock")
                data.write_data("userCheck", True)
            logger.debug("blur released data lock")
            return img
        blurred_img = img.filter(ImageFilter.BoxBlur(currentBlur))
        blurFactor = currentBlur - config.get_config("blurIncrement")
        logger.debug("blur attempting to aquire data lock")
        with config.data_lock:
            logger.debug("blur aquired data lock")
            data.write_data("blurFactor", blurFactor)
        logger.debug("blur released data lock")   
        return blurred_img

#Select Images to use during runtime
def getImage():
    filenames = filedialog.askopenfilenames(initialdir = config.get_config("initialDir"),
            title = "Select a File",#https://www.geeksforgeeks.org/file-explorer-in-python-using-tkinter/
            filetypes = (("Image files",
                        "*.jpg *.jpeg *.png"),))
    logger.debug("getImage attempting to aquire data lock")
    with config.data_lock:
        logger.debug("getImage aquired data lock")
        data.write_data("imageList", list(filenames))
        data.write_data("currentImage", data.get_data("imageList")[0])
    logger.debug("getImage released data lock")

#Set the initial file directory of pictures
def getInitialDir():
    folderName = filedialog.askdirectory(title= "Select an initial Image Directory")

#Reading data sent by the arduino and then processing the data
def process_arduino_data():
    while True:
        if data.get_data("sensorData") != 0:
            arduinoData = data.get_data("sensorData")
            hole, stickVal = arduinoData.split(":")
            stickVal = int(stickVal)
            stick = None
            if stickVal >= 505 and stickVal <= 515:
                stick = "Red"
            if stickVal >= 600 and stickVal <= 700:
                stick = "Green"
            if stickVal >= 705 and stickVal <= 800:
                stick = "Blue"
            if stickVal >= 805 and stickVal <= 900:
                stick = "Yellow"
            logger.debug("process_arduino_data attempting to aquire data lock")
            with config.data_lock:
                logger.debug("process_arduino_data aquired data lock")
                if stick == data.get_data("stick") and hole == data.get_data("hole"):
                    data.write_data("correctUserAction", True)
                else:
                    data.write_data("correctUserAction", False)
                data.write_data("sensorData", 0)
            logger.debug("process_arduino_data released data lock")
        time.sleep(0.1)

#Overwriting the config file with a default file
def reset():
    with open("defaultConfig.py", "r") as source_file:
        content = source_file.read()
    
    with open("config.py", "w") as destination_file:
        destination_file.write(content)