import tkinter as tk
from random import Random
from tkinter import filedialog
from PIL import Image, ImageTk #https://youtu.be/VnwDPa9biwc?si=TVNhnOiVH9hD5OvG
import functions, data, time, threading
import arduino_interface, config
from config import logger
########################CREATE COMMENTS FOR CLARITY################################################


class myGUI:

    def __init__(self):

        self.window = tk.Tk()

        self.window.geometry("500x300")
        self.window.title("Test")

        self.start = tk.Button(self.window, text="Start", font=("Arial", 18), width=10 , command=self.run)
        self.start.pack(pady=20)

        self.setting = tk.Button(self.window, text="Settings", font=("Arial", 18), width=10 , command=self.settingButtons)
        self.setting.pack(pady=20)

        self.exit = tk.Button(self.window, text="Exit", font=("Arial", 18), width=10 , command=self.closeMain)
        self.exit.pack(pady=20)

        self.window.mainloop()

    def closeMain(self):
        self.window.destroy()

    def run(self):

        self.runWindow = tk.Toplevel()

        self.runWindow.geometry("800x500")
        self.runWindow.title("In-Game")
        
        def update_image_threading():
            while True:
                result = data.get_data("correctUserAction")
                next = data.get_data("userCheck")
                if result == True and next == False:
                    update_image(data.get_data("blurFactor"))
                    logger.debug("update_image_threading attempting to aquire data lock")
                    with config.data_lock:
                        logger.debug("update_image_threading aquired data lock")
                        data.write_data("correctUserAction", None)
                    logger.debug("update_image_threading released data lock")
                time.sleep(0.1)
                #######################ADD ELSE TO FUNCTION IF USER PICKS WRONG HOLE OR STICK###############################################

        def rand():
            var = Random()
    
            hole = config.get_config("hole")
            stick = config.get_config("stick")
            randHole = var.choice(hole)
            randStick = var.choice(stick)
            position = "Place the " + randStick + " Stick in Hole " + randHole
            logger.debug("rand attempting to aquire data lock")
            with config.data_lock:
                logger.debug("rand data lock aquired")
                data.write_data("stick", randStick)
                data.write_data("hole", randHole)
            logger.debug("rand data lock released")

            if hasattr(self, "position"):
                self.position.configure(text=position)
            else:
                self.position = tk.Label(self.runWindow, text=position, font=("Arial", 18))
                self.position.pack()

        def update_image(blurFactor):
            if data.get_data("imageList") == None:
                default_image = Image.open(config.get_config("defaultImg"))          
            else:
                default_image = Image.open(data.get_data("currentImage"))

            default_image = default_image.resize((400, 300), Image.LANCZOS)
            blurredImg = functions.blur(default_image, blurFactor)
            blurredImg = ImageTk.PhotoImage(blurredImg)
            
            if hasattr(self, "image_label"):
                self.image_label.configure(image=blurredImg)
                self.image_label.image = blurredImg
            else:
                self.image_label = tk.Label(self.runWindow, image=blurredImg)
                self.image_label.image = blurredImg #https://stackoverflow.com/questions/27430648/tkinter-vanishing-photoimage-issue
                self.image_label.pack()

            rand()
        update_image(data.get_data("blurFactor"))
    
        def nextButton():
            logger.debug("nextButton attempting to aquire data lock")
            with config.data_lock:
                logger.debug("nextButton aquired data lock")
                data.write_data("userCheck", False)
                data.write_data("blurFactor", 9)

                if data.get_data("imageList") is not None:
                    imgNum = data.get_data("imgNum")
                    imgNum += 1
                    imgList = data.get_data("imageList")
                    imgListLen = len(imgList) - 1
                    if imgNum > imgListLen:
                        imgNum = 0
                    data.write_data("imgNum", imgNum)
                    currentImg = imgList[imgNum]
                    data.write_data("currentImage", currentImg)
            logger.debug("nextButton released data lock")

        self.skip = tk.Button(self.runWindow, text="Next", font=("Arial", 18), width=15, command=nextButton)
        self.skip.pack(pady=5)

        self.close = tk.Button(self.runWindow, text="Close", font=("Arial", 18), width=15, command=self.closeRun)
        self.close.pack(pady=5)

        #Creates and starts the Threads       
        arduino_thread = threading.Thread(target=arduino_interface.arduino_connect)
        arduino_thread.daemon = True
        arduino_thread.start()

        update_image_thread = threading.Thread(target=update_image_threading)
        update_image_thread.daemon = True
        update_image_thread.start()

        arduino_data = threading.Thread(target=functions.process_arduino_data)
        arduino_data.daemon = True
        arduino_data.start()

                

    def closeRun(self):
        self.runWindow.destroy()


    def settingButtons(self):
        self.stwindow = tk.Toplevel()

        self.stwindow.geometry("300x500")
        self.stwindow.title("Settings")

        self.image = tk.Button(self.stwindow, text="Choose Images", font=("Arial", 18), width=15, command=functions.getImage)
        self.image.pack(pady=5)

        self.gridSettings = tk.Button(self.stwindow, text="Grid Settings", font=("Arial", 18), width=15)
        self.gridSettings.pack(pady=5)

        self.stickSettings = tk.Button(self.stwindow, text="Stick Settings", font=("Arial", 18), width=15)
        self.stickSettings.pack(pady=5)

        self.timer = tk.Button(self.stwindow, text="Timer", font=("Arial", 18), width=15)
        self.timer.pack(pady=5)

        self.arduinoSettings = tk.Button(self.stwindow, text="Arduino Settings", font=("Arial", 18), width=15)
        self.arduinoSettings.pack(pady=5)

        self.advanced = tk.Button(self.stwindow, text="Advanced", font=("Arial", 18), width=15)
        self.advanced.pack(pady=5)

        self.reset = tk.Button(self.stwindow, text="Reset", font=("Arial", 18), width=15)
        self.reset.pack(pady=5)

        self.exit = tk.Button(self.stwindow, text="Close", font=("Arial", 18), width=15, command=self.closeSettings)
        self.exit.pack(pady=5)

    def closeSettings(self):
        self.stwindow.destroy()

myGUI()