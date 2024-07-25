from random import Random
from PIL import ImageFilter, Image, ImageTk
from tkinter import filedialog
import data

def getPosition():
    var = Random()

    hole = var.choice(["A1", "A2", "A3", "A4", "B1", "B2", "B3", "B4", "C1", "C2", "C3", "C4", "D1", "D2", "D3", "D4"])
    stick = var.choice(["Blue", "Green", "Red", "Yellow"])
    position = "Place the " + stick + " Stick in Hole " + hole
    data.write_data("stick", stick)
    data.write_data("hole", hole)
    return position

def blur(img, currentBlur):
    if currentBlur == 1:
        return img
    blurFactor = currentBlur - 2
    data.write_data("blurFactor", blurFactor)
    return img.filter(ImageFilter.BoxBlur(blurFactor))

def getImage():
    filenames = filedialog.askopenfilenames(initialdir = r"C:\Users\micha.DESKTOP-IHJJH3S\Desktop\Final Project Git\project-1\project-1-main\Project",
            title = "Select a File",#https://www.geeksforgeeks.org/file-explorer-in-python-using-tkinter/
            filetypes = (("Image files",
                        "*.jpg *.jpeg *.png"),))
    data.write_data("imageList", list(filenames))
    data.write_data("currentImage", data.get_data("imageList")[0])

def process_arduino_data():
    while True:
        arduinoData = data.get_data("sensorData")
        hole, stickVal = arduinoData.split(":")
        
        if stickVal >= 950 and stickVal <= 1000:
            stick = "Red"

        if stick == data.get_data("stick") and hole == data.get_data("hole"):
            return True
        return False