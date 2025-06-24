from PIL import ImageFilter
from tkinter import filedialog
import data_store, module2, time
from module2 import logger

#Blurs the image
def blur(img, currentBlur):
        if currentBlur == 1:
            logger.debug("blur attempting to aquire data lock")
            with module2.data_lock:
                logger.debug("blur aquired data lock")
                data_store.write_data("userCheck", True)
            logger.debug("blur released data lock")
            return img
        blurred_img = img.filter(ImageFilter.BoxBlur(currentBlur))
        blurFactor = currentBlur - module2.get_config("blurIncrement")
        logger.debug("blur attempting to aquire data lock")
        with module2.data_lock:
            logger.debug("blur aquired data lock")
            data_store.write_data("blurFactor", blurFactor)
        logger.debug("blur released data lock")   
        return blurred_img

#Select Images to use during runtime
def getImage():
    filenames = filedialog.askopenfilenames(initialdir = module2.get_config("initialDir"),
            title = "Select a File",#https://www.geeksforgeeks.org/file-explorer-in-python-using-tkinter/
            filetypes = (("Image files",
                        "*.jpg *.jpeg *.png"),))
    logger.debug("getImage attempting to aquire data lock")
    logger.debug(filenames)
    if filenames != '':
        with module2.data_lock:
            logger.debug("getImage aquired data lock")
            data_store.write_data("imageList", list(filenames))
            data_store.write_data("currentImage", module2.resource_path(data_store.get_data("imageList")[0]))
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
    prevArduinoData = -1
    while True:
        arduinoData = data_store.get_data("sensorData")
        if (arduinoData == prevArduinoData or arduinoData == "None"):
            with module2.data_lock:
                data_store.write_data("correctUserAction", None)
            continue
        prevArduinoData = arduinoData
        splitData = arduinoData.split(',')
        for res in splitData:
            if (res == ''): 
                continue
            hole, stickVal = res.split(":")
            stickVal = int(stickVal)
            stick = None
            if stickVal >= 80 and stickVal <= 100:
                stick = "Red"
            if stickVal >= 400 and stickVal <= 430:
                stick = "Green"
            if stickVal >= 80 and stickVal <= 715:
                stick = "Blue"
            if stickVal >= 80 and stickVal <= 415:
                stick = "Yellow"
            logger.debug(f"process_arduino_data received data: hole={hole}, stick={stick}")
            logger.debug("process_arduino_data attempting to aquire data lock")
            with module2.data_lock:
                logger.debug("process_arduino_data aquired data lock")
                #if stick == data_store.get_data("stick") and hole == transalteHole(data_store.get_data("hole")):
                if hole == translate_hole(data_store.get_data("hole")):
                    data_store.write_data("correctUserAction", True)
                    data_store.write_data("sensorData", "None")
                    break
                else:
                    data_store.write_data("correctUserAction", False)
                    data_store.write_data("sensorData", "None")
            logger.debug("process_arduino_data released data lock")
        time.sleep(0.1)

def translate_hole(inputHole):
    if inputHole == "A1":
        return "A0"
    elif inputHole == "A2":
        return "A1"
    elif inputHole == "A3":
        return "A2"
    elif inputHole == "A4":
        return "A3"
    elif inputHole == "B1":
        return "A4"
    elif inputHole == "B2":
        return "A5"
    elif inputHole == "B3":
        return "A6"
    elif inputHole == "B4":
        return "A7"
    elif inputHole == "C1":
        return "A8"
    elif inputHole == "C2":
        return "A9"
    elif inputHole == "C3":
        return "A10"
    elif inputHole == "C4":
        return "A11"
    elif inputHole == "D1":
        return "A12"
    elif inputHole == "D2":
        return "A13"
    elif inputHole == "D3":
        return "A14"
    elif inputHole == "D4":
        return "A15"