import threading
import logging
import pickle
import os

configuration = {
    "portVar" : "COM4",
    "blurIncrement": 2,
    "initialDir" : r"C:\Users\micha.DESKTOP-IHJJH3S\Desktop\Final Project Git\project-1\project-1-main\Project",
    "defaultImg" : r"C:\Users\micha.DESKTOP-IHJJH3S\Desktop\Final Project Git\project-1\project-1-main\Project\default.jpg",
    "hole" : ["A1"],#, "A2", "A3", "A4", "B1", "B2", "B3", "B4", "C1", "C2", "C3", "C4", "D1", "D2", "D3", "D4"],
    "stick" : ["Red"]#, "Green", "Blue", "Yellow"]
}

#Basic logging for debug
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(threadName)s - %(message)s', filename="basic.log")
logger = logging.getLogger("app_logger")

#Threading locks so data isn't corrupted or overwritten
data_lock = threading.Lock()

config_file_path = "config.pkl"

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
    return configuration.get(key)

def write_config(key, value):
    configuration[key] = value
    save_config()