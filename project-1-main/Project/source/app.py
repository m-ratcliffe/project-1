import tkinter as tk
from random import Random
from tkinter import filedialog
from PIL import Image, ImageTk #https://youtu.be/VnwDPa9biwc?si=TVNhnOiVH9hD5OvG
import functions, data, time, threading
import arduino_interface, config
import serial.tools.list_ports
from config import logger
from tkinter import messagebox

config.load_config()

class myGUI:
    #Main menu window
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

    #Main runtime window
    def run(self):
        if data.get_data("windowOpen") == True and data.get_data("arduinoConnect") == True:
            self.runWindow.deiconify()
        else:
            with config.data_lock:
                data.write_data("windowOpen", True)

        if data.get_data("imageList") == None and config.get_config("defaultImg") == None:
            messagebox.showerror("Error", "Please select one or more images, or set a default image.")
            self.runWindow.withdraw()

        self.runWindow = tk.Toplevel()

        self.runWindow.geometry("800x500")
        self.runWindow.title("In-Game")

        #This thread is constantly looking for certain criteria to be met and then calls the blur function
        def update_image_threading():
            while True:
                result = data.get_data("correctUserAction")
                next = data.get_data("userCheck")
                if result == True and next == False:
                    self.userAction("green")
                    update_image(data.get_data("blurFactor"))
                    logger.debug("update_image_threading attempting to aquire data lock")
                    with config.data_lock:
                        logger.debug("update_image_threading aquired data lock")
                        data.write_data("correctUserAction", None)
                    logger.debug("update_image_threading released data lock")
                elif result == False:
                    self.userAction("red")
                    logger.debug("update_image_threading(incorrect user action) attempting to aquire data lock")
                    with config.data_lock:
                        logger.debug("update_image_threading(incorrect user action) aquired data lock")
                        data.write_data("correctUserAction", None)
                    logger.debug("update_image_threading(incorrect user action) released data lock")
                time.sleep(0.1)

        #Choosing a random location on the board for the user to interact with
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
        
        #Updates the GUI and calls the blur function
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

        #Requires the user to click a button before the next image is selected(can also be done preemptively if another image is desired)
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
        try:
        # Attempt to open the serial port
            port_name = config.get_config("portVar")
            ser = serial.Serial(port_name, 9600, timeout=1)
            ser.close()  # Close the port if it's successfully opened
            arduino_thread = threading.Thread(target=arduino_interface.arduino_connect)
            arduino_thread.daemon = True
            arduino_thread.start()

            update_image_thread = threading.Thread(target=update_image_threading)
            update_image_thread.daemon = True
            update_image_thread.start()

            arduino_data = threading.Thread(target=functions.process_arduino_data)
            arduino_data.daemon = True
            arduino_data.start()
            with config.data_lock:
                data.write_data("arduinoConnect", True)
        except serial.SerialException:
            self.runWindow.withdraw()
            messagebox.showerror("Error", "Could not connect to Arduino. Please make sure it is plugged in and the correct Port is selected.")     

    #Indicates to the user if their action was correct
    def userAction(self, color):
        if color == "red":
            colors = ['red', 'white']
        elif color == "green":
            colors = ['green', 'white']
        def update_color(index):
            self.runWindow.config(bg=colors[index])
            next_index = (index + 1) % len(colors)
            self.runWindow.after(500, update_color, next_index)
        update_color(0)

                

    def closeRun(self):
        self.runWindow.withdraw()

    #Settings window
    def settingButtons(self):
        self.stwindow = tk.Toplevel()

        self.stwindow.geometry("300x360")
        self.stwindow.title("Settings")

        self.image = tk.Button(self.stwindow, text="Choose Images", font=("Arial", 18), width=15, command=functions.getImage)
        self.image.pack(pady=5)

        self.arduinoSettings = tk.Button(self.stwindow, text="Arduino Settings", font=("Arial", 18), width=15, command=self.portWindow)
        self.arduinoSettings.pack(pady=5)

        self.advanced = tk.Button(self.stwindow, text="Advanced", font=("Arial", 18), width=15, command=self.advancedSettings)
        self.advanced.pack(pady=5)

        self.reset = tk.Button(self.stwindow, text="Reset", font=("Arial", 18), width=15, command=functions.reset)
        self.reset.pack(pady=5)#Add a gui that asks if user is sure

        self.exit = tk.Button(self.stwindow, text="Close", font=("Arial", 18), width=15, command=self.closeSettings)
        self.exit.pack(pady=5)

    #Arduino settings window
    def portWindow(self):
        self.portWndw = tk.Toplevel()

        self.portWndw.geometry("500x200")
        self.portWndw.title("Arduino Settings")

        tempStr=self.portConfig()

        selected_option = tk.StringVar()
        selected_option.set(tempStr[0])

        self.availablePorts = tk.OptionMenu(self.portWndw, selected_option, *tempStr)
        self.availablePorts.pack(pady=5)

        self.save = tk.Button(self.portWndw, text="Save", font=("Arial", 17), command=lambda: self.saveArduinoSettings(selected_option.get()))
        self.save.pack(pady=5)

    #Advanced settings window
    def advancedSettings(self):
        self.advWnd = tk.Toplevel()

        self.advWnd.geometry("500x300")
        self.advWnd.title("Advanced Settings")

        currentValue = config.get_config("blurIncrement")

        blur_increment = tk.IntVar()

        def updateBlurIncrement(value):
            self.blurInc.config(text=f"Blur Increment: {value}")
        
        slider = tk.Scale(self.advWnd, from_= 1, to= 10, orient=tk.HORIZONTAL, variable=blur_increment, command=updateBlurIncrement)
        slider.pack(pady=5)

        self.blurInc = tk.Label(self.advWnd, text=f"Current Blur Increment: {currentValue}")
        self.blurInc.pack(pady=5)

        self.initalDir = tk.Button(self.advWnd, text="Set initial Image Directory", command=functions.getInitialDir)
        self.initalDir.pack(pady=5)

        self.defaultImg = tk.Button(self.advWnd, text="Set default image", command=functions.getDefaultImg)
        self.defaultImg.pack(pady=5)

        self.saveBlurIncrement = tk.Button(self.advWnd, text="Save", command=lambda: config.write_config("blurIncrement", blur_increment.get()))
        self.saveBlurIncrement.pack(pady=5)

        self.closeAdvanced = tk.Button(self.advWnd, text="Close", command=lambda: self.advWnd.destroy())
        self.closeAdvanced.pack(pady=5)

    #Identifies ports in use
    def portConfig(self):
        ports = serial.tools.list_ports.comports() #https://youtu.be/AHr94RtMj1A?si=uIVSIY6_S2sPDFUR
        port_info = [f"{port.device} - {port.description}" for port in ports]
        return port_info
    
    def saveArduinoSettings(self, portVar):
        newPort = str(portVar)[:4]
        with config.data_lock:
            config.write_config("portVar", newPort)

    def closeSettings(self):
        self.stwindow.destroy()

myGUI()