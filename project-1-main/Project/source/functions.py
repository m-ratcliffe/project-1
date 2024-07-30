from random import Random
from PIL import ImageFilter, Image, ImageTk
from tkinter import filedialog
import data, config


def getPosition():
    var = Random()

    hole = var.choice(["A1"])#, "A2", "A3", "A4", "B1", "B2", "B3", "B4", "C1", "C2", "C3", "C4", "D1", "D2", "D3", "D4"])
    stick = var.choice(["Red"])#, "Green", "Blue", "Yellow"])
    position = "Place the " + stick + " Stick in Hole " + hole
    with config.data_lock:
        data.write_data("stick", stick)
        data.write_data("hole", hole)
    return position

def blur(img, currentBlur):
    if currentBlur == 1:
        print("success")
        imgNum = data.get_data("imgNum")
        imgNum += 1
        print(imgNum)
        with config.data_lock:
            data.write_data("imgNum", imgNum)
            #data.write_data("blurFactor", 1)
        return img
    blurFactor = currentBlur - 2
    with config.data_lock:
        data.write_data("blurFactor", blurFactor)
    blurred_img = img.filter(ImageFilter.BoxBlur(currentBlur))
    return blurred_img


def getImage():
    filenames = filedialog.askopenfilenames(initialdir = r"C:\Users\micha.DESKTOP-IHJJH3S\Desktop\Final Project Git\project-1\project-1-main\Project",
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
                if stickVal >= 505 and stickVal <= 515:
                    stick = "Red"

                if stick == data.get_data("stick") and hole == data.get_data("hole"):
                    #print("condition met")
                    with config.data_lock:
                        data.write_data("correctUserAction", True)
                with config.data_lock:
                    data.write_data("sensorData", 0)
