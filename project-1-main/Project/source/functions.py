from random import Random
from PIL import ImageFilter, Image, ImageTk
from tkinter import filedialog
import data, config


def getPosition():
    var = Random()
    
    hole = config.get_config("hole")
    stick = config.get_config("stick")
    randHole = var.choice(hole)
    randStick = var.choice(stick)
    position = "Place the " + randStick + " Stick in Hole " + randHole
    with config.data_lock:
        data.write_data("stick", randStick)
        data.write_data("hole", randHole)
    return position

def blur(img, currentBlur):
    if currentBlur == 1:
        with config.data_lock:
            data.write_data("blurFactor", 9)
        return img
    blurred_img = img.filter(ImageFilter.BoxBlur(currentBlur))
    blurFactor = currentBlur - config.get_config("blurIncrement")
    with config.data_lock:
        data.write_data("blurFactor", blurFactor)
    return blurred_img


def getImage():
    filenames = filedialog.askopenfilenames(initialdir = config.get_config("initialDir"),
            title = "Select a File",#https://www.geeksforgeeks.org/file-explorer-in-python-using-tkinter/
            filetypes = (("Image files",
                        "*.jpg *.jpeg *.png"),))
    with config.data_lock:
        data.write_data("imageList", list(filenames))
        data.write_data("currentImage", data.get_data("imageList")[0])

def process_arduino_data():
        while True:
            if data.get_data("sensorData") != 0:
                arduinoData = data.get_data("sensorData")
                hole, stickVal = arduinoData.split(":")
                stickVal = int(stickVal)
                stick = None
                if stickVal >= 505 and stickVal <= 515:
                    stick = "Red"

                if stick == data.get_data("stick") and hole == data.get_data("hole"):
                    with config.data_lock:
                        data.write_data("correctUserAction", True)
                with config.data_lock:
                    data.write_data("sensorData", 0)
