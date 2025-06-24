import tkinter as tk
from random import Random
from tkinter import filedialog
from PIL import Image, ImageTk #https://youtu.be/VnwDPa9biwc?si=TVNhnOiVH9hD5OvG
import module4, data_store, time, threading, os
import arduino_io, module2
import serial.tools.list_ports
from module2 import logger
from tkinter import messagebox

module2.load_config()

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

    #Main runtime window
    def run(self):
        self.window.withdraw() #Hides the main window

        if hasattr(self, "stwindow") and self.stwindow.winfo_exists():
            self.stwindow.withdraw()
         # Check if runWindow exists and is still a valid window
        if hasattr(self, "runWindow") and self.runWindow.winfo_exists():
            self.runWindow.deiconify()
            self.update_image(9)
            return  # Do not create a new instance

        # Checks if the user has selected images or set a default image
        if data_store.get_data("imageList") == None and module2.get_config("defaultImg") == None:
            messagebox.showerror("Error", "Please select one or more images, or set a default image.")
            self.runWindow.withdraw()

        self.runWindow = tk.Toplevel()
        self.runWindow.geometry("800x500")
        self.runWindow.title("In-Game")
        self.runWindow.protocol("WM_DELETE_WINDOW", self.closeRun)

        self.update_image(data_store.get_data("blurFactor"))

        self.skip = tk.Button(self.runWindow, text="Next", font=("Arial", 18), width=15, command=self.nextButton)
        self.skip.pack(pady=5)

        self.close = tk.Button(self.runWindow, text="Close", font=("Arial", 18), width=15, command=self.closeRun)
        self.close.pack(pady=5)

        #DRR
        #self.position = tk.Label(self.runWindow, text="Place...", font=("Arial", 18))
        #self.position.pack()
        
        #Creates and starts the Threads
        if data_store.get_data("arduinoConnect") == False:
            try:
            # Attempt to open the serial port
                port_name = module2.get_config("portVar")
                ser= serial.Serial(port_name, 9600, timeout=1)
                ser.close()
                    #self.runWindow.withdraw()
                arduino_thread = threading.Thread(target=arduino_io.arduino_connect)
                arduino_thread.daemon = True
                arduino_thread.start()

                update_image_thread = threading.Thread(target=self.update_image_threading)
                update_image_thread.daemon = True
                update_image_thread.start()

                arduino_data = threading.Thread(target=module4.process_arduino_data)
                arduino_data.daemon = True
                arduino_data.start()
                with module2.data_lock:
                    data_store.write_data("arduinoConnect", True)
            except serial.SerialException:
                self.runWindow.withdraw()
                messagebox.showerror("Error", "Could not connect to Arduino. Please make sure it is plugged in and the correct Port is selected.")  
                self.window.deiconify()   
    

    #Requires the user to click a button before the next image is selected(can also be done preemptively if another image is desired)
    def nextButton(self):
        logger.debug("nextButton attempting to aquire data lock")
        
        with module2.data_lock:
            logger.debug("nextButton aquired data lock")
            data_store.write_data("blurFactor", 9)

        if data_store.get_data("imageList") is not None:
            imgNum = data_store.get_data("imgNum")
            imgNum += 1
            imgList = data_store.get_data("imageList")
            imgListLen = len(imgList) - 1
            if imgNum > imgListLen:
                imgNum = 0
            data_store.write_data("imgNum", imgNum)
            currentImg = imgList[imgNum]
            data_store.write_data("currentImage", currentImg)
            self.update_image(9)

        logger.debug("nextButton released data lock")
        
    #This thread is constantly looking for certain criteria to be met and then calls the blur function
    def update_image_threading(self):
        while True:
            result = data_store.get_data("correctUserAction")
            if result == True:
                # Correct
                self.userAction("green")
                self.update_image(data_store.get_data("blurFactor"))
                logger.debug("update_image_threading attempting to aquire data lock")
                with module2.data_lock:
                    logger.debug("update_image_threading aquired data lock")
                    data_store.write_data("correctUserAction", None)
                logger.debug("update_image_threading released data lock")
            elif result == False:
                # Incorrect
                self.userAction("red")
                logger.debug("update_image_threading(incorrect user action) attempting to aquire data lock")
                with module2.data_lock:
                    logger.debug("update_image_threading(incorrect user action) aquired data lock")
                    data_store.write_data("correctUserAction", None)
                logger.debug("update_image_threading(incorrect user action) released data lock")
            
            time.sleep(0.1)
    
    #Choosing a random location on the board for the user to interact with
    def rand(self):
        ran = Random()
        hole = module2.get_config("hole")
        stick = module2.get_config("stick")
        randHole = ran.choice(hole)
        randStick = ran.choice(stick)
        position = "Place the " + randStick + " Stick in Hole " + randHole
        logger.debug(f"rand attempting to aquire data lock: {position}")

        with module2.data_lock:
            logger.debug("rand data lock aquired")
            data_store.write_data("stick", randStick)
            data_store.write_data("hole", randHole)
        logger.debug("rand data lock released")

        if hasattr(self, "position"):
            self.position.configure(text=position)
        else:
            self.position = tk.Label(self.runWindow, text=position, font=("Arial", 18))
            self.position.pack()

    #Updates the GUI and calls the blur function
    def update_image(self, blurFactor):
        logger.debug("update_image called")
        if data_store.get_data("imageList") == None:
            default_image = Image.open(module2.resource_path(module2.get_config("defaultImg")))          
        else:
            default_image = Image.open(module2.resource_path(data_store.get_data("currentImage")))

        default_image = default_image.resize((400, 300), Image.LANCZOS)
        blurredImg = module4.blur(default_image, blurFactor)
        blurredImg = ImageTk.PhotoImage(blurredImg)
        
        if hasattr(self, "image_label"):
            self.image_label.configure(image=blurredImg)
            self.image_label.image = blurredImg
        else:
            self.image_label = tk.Label(self.runWindow, image=blurredImg)
            self.image_label.image = blurredImg #https://stackoverflow.com/questions/27430648/tkinter-vanishing-photoimage-issue
            self.image_label.pack()

        self.rand()
        logger.debug("update_image completed")

    def settingButtons(self):
        if hasattr(self, "stwindow") and self.stwindow.winfo_exists():
            self.stwindow.deiconify()
            return

        self.stwindow = tk.Toplevel()

        self.stwindow.geometry("300x360")
        self.stwindow.title("Settings")

        self.image = tk.Button(self.stwindow, text="Choose Images", font=("Arial", 18), width=15, command=module4.getImage)
        self.image.pack(pady=5)

        self.arduinoSettings = tk.Button(self.stwindow, text="Arduino Settings", font=("Arial", 18), width=15, command=self.portWindow)
        self.arduinoSettings.pack(pady=5)

        self.advanced = tk.Button(self.stwindow, text="Advanced", font=("Arial", 18), width=15, command=self.advancedSettings)
        self.advanced.pack(pady=5)

        self.reset_button = tk.Button(self.stwindow, text="Reset", font=("Arial", 18), width=15, command=self.reset)
        self.reset_button.pack(pady=5)

        self.exit = tk.Button(self.stwindow, text="Close", font=("Arial", 18), width=15, command=self.closeSettings)
        self.exit.pack(pady=5)
    def closeMain(self):
        self.window.destroy()

    #Indicates to the user if their action was correct
    def userAction(self, color):
        if color == "red":
            colors = ['red', 'white']
        elif color == "green":
            colors = ['green', 'white']
        def update_color(index, count):
                if count > 4:
                    self.runWindow.config(bg="white")
                    return
                self.runWindow.config(bg=colors[index])
                next_index = (index + 1) % len(colors)
                self.runWindow.after(500, update_color, next_index, count + 1)

        update_color(0,0)              

    def closeRun(self):
        self.runWindow.withdraw()
        self.window.deiconify() #Shows the main window again

    #Arduino settings window
    def portWindow(self):
        self.portWndw = tk.Toplevel()

        self.portWndw.geometry("500x100")
        self.portWndw.title("Arduino Settings")

        tempStr=self.portConfig()

        selected_option = tk.StringVar()
        selected_option.set(tempStr[0])

        self.availablePorts = tk.OptionMenu(self.portWndw, selected_option, *tempStr)
        self.availablePorts.pack(pady=5)

        self.save = tk.Button(self.portWndw, text="Save", font=("Arial", 13), command=lambda: self.saveArduinoSettings(selected_option.get()))
        self.save.pack(pady=5)

    #Advanced settings window
    def advancedSettings(self):
        self.advWnd = tk.Toplevel()

        self.advWnd.geometry("500x300")
        self.advWnd.title("Advanced Settings")

        currentValue = module2.get_config("blurIncrement")

        blur_increment = tk.IntVar()

        def updateBlurIncrement(value):
            self.blurInc.config(text=f"Blur Increment: {value}")
        
        slider = tk.Scale(self.advWnd, from_= 1, to= 10, orient=tk.HORIZONTAL, variable=blur_increment, length=170, command=updateBlurIncrement)
        slider.pack(pady=5)

        self.blurInc = tk.Label(self.advWnd, text=f"Current Blur Increment: {currentValue}", font=("Arial", 13))
        self.blurInc.pack(pady=5)

        self.initalDir = tk.Button(self.advWnd, text="Set initial Image Directory", font=("Arial", 13), width=23, command=module4.getInitialDir)
        self.initalDir.pack(pady=5)

        self.defaultImg = tk.Button(self.advWnd, text="Set default image", font=("Arial", 13), width=23, command=module4.getDefaultImg)
        self.defaultImg.pack(pady=5)

        self.saveBlurIncrement = tk.Button(self.advWnd, text="Save", font=("Arial", 13), width=23, command=lambda: module2.write_config("blurIncrement", blur_increment.get()))
        self.saveBlurIncrement.pack(pady=5)

        self.closeAdvanced = tk.Button(self.advWnd, text="Close", font=("Arial", 13), width=23, command=lambda: self.advWnd.destroy())
        self.closeAdvanced.pack(pady=5)

    #Identifies ports in use
    def portConfig(self):
        ports = serial.tools.list_ports.comports() #https://youtu.be/AHr94RtMj1A?si=uIVSIY6_S2sPDFUR
        port_info = [f"{port.device} - {port.description}" for port in ports]
        return port_info
    
    def saveArduinoSettings(self, portVar):
        newPort = str(portVar)[:4]
        with module2.data_lock:
            module2.write_config("portVar", newPort)

    def closeSettings(self):
        self.stwindow.destroy()

    def reset(self):
            confirmation = messagebox.askyesno("Reset Settings", "Are you sure you want to reset the settings?", parent=self.stwindow)
            if confirmation == True:
                os.remove("assets/config.pkl")

myGUI()