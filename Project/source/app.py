import tkinter as tk
from PIL import Image, ImageTk #https://youtu.be/VnwDPa9biwc?si=TVNhnOiVH9hD5OvG
import functions


class myGUI:

    def __init__(self):

        self.window = tk.Tk()

        self.window.geometry("500x300")
        self.window.title("Test")

        self.start = tk.Button(self.window, text="Start", font=("Arial", 18), width=10 , command=self.run)
        self.start.pack(pady=20)

        self.setting = tk.Button(self.window, text="Settings", font=("Arial", 18), width=10 , command=self.settings)
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

        default_image = Image.open("default.jpg")
        default_image = default_image.resize((400, 300), Image.LANCZOS)
        default_tk = ImageTk.PhotoImage(default_image)
        

        self.image = tk.Label(self.runWindow, image=default_tk)
        self.image.image = default_tk #https://stackoverflow.com/questions/27430648/tkinter-vanishing-photoimage-issue
        self.image.pack()

        self.position = tk.Label(self.runWindow, text=functions.getPosition(), font=("Arial", 18))
        self.position.pack()

        self.close = tk.Button(self.runWindow, text="Close", font=("Arial", 18), width=15, command=self.closeRun)
        self.close.pack(pady=5)

        self.skip = tk.Button(self.runWindow, text="Skip", font=("Arial", 18), width=15)
        self.skip.pack(pady=5)


    def closeRun(self):
        self.runWindow.destroy()


    def settings(self):
        self.stwindow = tk.Toplevel()

        self.stwindow.geometry("300x500")
        self.stwindow.title("Settings")

        self.gridSettings = tk.Button(self.stwindow, text="Grid Settings", font=("Arial", 18), width=15)
        self.gridSettings.pack(pady=5)

        self.image = tk.Button(self.stwindow, text="Choose Images", font=("Arial", 18), width=15)
        self.image.pack(pady=5)

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