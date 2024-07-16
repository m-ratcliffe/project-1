from random import Random
from PIL import ImageFilter, Image, ImageTk
from tkinter import filedialog

def getPosition():
    var = Random()

    hole = var.choice(["A1", "A2", "A3", "A4", "B1", "B2", "B3", "B4", "C1", "C2", "C3", "C4", "D1", "D2", "D3", "D4"])
    stick = var.choice(["Blue", "Green", "Red", "Yellow"])
    position = "Place the " + stick + " Stick in Hole " + hole

    return position

def blur(img, currentBlur):
    if currentBlur == 1:
        return img
    blurFactor = currentBlur - 2
    return img.filter(ImageFilter.BoxBlur(blurFactor))

def getImage(settings_update):
    filenames = filedialog.askopenfilenames(initialdir = "/home/kali/Downloads/project-1-main/Project",#Change to Windows pictures folder
            title = "Select a File",#https://www.geeksforgeeks.org/file-explorer-in-python-using-tkinter/
            filetypes = (("Image files",
                        "*.jpg *.jpeg *.png"),))
    settings_update("image", list(filenames))