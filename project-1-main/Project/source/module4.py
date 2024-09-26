from PIL import ImageFilter
from tkinter import filedialog
import module3, module2, time
from module2 import logger

#Blurs the image
def blur(img, currentBlur):
        if currentBlur == 1:
            logger.debug("blur attempting to aquire data lock")
            with module2.data_lock:
                logger.debug("blur aquired data lock")
                module3.write_data("userCheck", True)
            logger.debug("blur released data lock")
            return img
        blurred_img = img.filter(ImageFilter.BoxBlur(currentBlur))
        blurFactor = currentBlur - module2.get_config("blurIncrement")
        logger.debug("blur attempting to aquire data lock")
        with module2.data_lock:
            logger.debug("blur aquired data lock")
            module3.write_data("blurFactor", blurFactor)
        logger.debug("blur released data lock")   
        return blurred_img

#Select Images to use during runtime
def getImage():
    filenames = filedialog.askopenfilenames(initialdir = module2.get_config("initialDir"),
            title = "Select a File",#https://www.geeksforgeeks.org/file-explorer-in-python-using-tkinter/
            filetypes = (("Image files",
                        "*.jpg *.jpeg *.png"),))
    logger.debug("getImage attempting to aquire data lock")
    with module2.data_lock:
        logger.debug("getImage aquired data lock")
        module3.write_data("imageList", list(filenames))
        module3.write_data("currentImage", module2.resource_path(module3.get_data("imageList")[0]))
    logger.debug("getImage released data lock")

#Set the initial file directory of pictures
def getInitialDir():
    folderName = filedialog.askdirectory(title= "Select an initial Image Directory")
    if folderName != None:
        with module2.data_lock:
            module2.write_config("initialDir", module2.resource_path(folderName))

def getDefaultImg():
    imgName = filedialog.askopenfilename(title= "Select a default image")
    if imgName != None:
        with module2.data_lock:
            module2.write_config("defaultImg", module2.resource_path(imgName))

#Reading data sent by the arduino and then processing the data
def process_arduino_data():
    while True:
        if module3.get_data("sensorData") != 0:
            arduinoData = module3.get_data("sensorData")
            hole, stickVal = arduinoData.split(":")
            stickVal = int(stickVal)
            stick = None
            if stickVal >= 505 and stickVal <= 515:
                stick = "Red"
            if stickVal >= 320 and stickVal <= 335:
                stick = "Green"
            if stickVal >= 700 and stickVal <= 715:
                stick = "Blue"
            if stickVal >= 405 and stickVal <= 415:
                stick = "Yellow"
            logger.debug("process_arduino_data attempting to aquire data lock")
            with module2.data_lock:
                logger.debug("process_arduino_data aquired data lock")
                if stick == module3.get_data("stick") and hole == module3.get_data("hole"):
                    module3.write_data("correctUserAction", True)
                else:
                    module3.write_data("correctUserAction", False)
                module3.write_data("sensorData", 0)
            logger.debug("process_arduino_data released data lock")
        time.sleep(0.1)