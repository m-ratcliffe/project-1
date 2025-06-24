import threading
import logging
import pickle
import os, sys

configuration = {
    "portVar" : "COM3",
    "blurIncrement": 2,
    "initialDir" : "assets",
    "defaultImg" : "assets/default.jpg",
    "hole" : ["A1", "A2", "A3", "A4"],#, "B1", "B2", "B3", "B4", "C1", "C2", "C3", "C4", "D1", "D2", "D3", "D4"],
    "stick" : ["Red"]#, "Green", "Blue", "Yellow"]
}

def resource_path(relative_path):#Got this from ChatGpt
    try:
        # If the app is run as an executable, PyInstaller sets this attribute
        base_path = sys._MEIPASS
    except AttributeError:
        # When running the script directly, use the current directory
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    # Join the base path with the relative resource path
    return os.path.join(base_path, relative_path)

#Basic logging for debug
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(threadName)s - %(message)s', filename=resource_path("assets/basic.log"))
logger = logging.getLogger("app_logger")

#Threading locks so data isn't corrupted or overwritten
data_lock = threading.Lock()

config_file_path = resource_path("assets/config.pkl")

def load_config():
    global configuration
    if os.path.exists(config_file_path):
        with open(config_file_path, "rb") as file:
            configuration = pickle.load(file)
    else:
        logger.warning("Configuration file not found, using default settings.")

def save_config():
    with open(config_file_path, "wb") as file:
        pickle.dump(configuration, file)
        
def get_config(key):
    if (key == "hole" or key == "stick"):
        return configuration.get(key, [])
    else:
        return configuration.get(key)

def write_config(key, value):
    configuration[key] = value
    save_config()