import threading

configuration = {
    "portVar" : "COM4",
    "hole" : ["A1"],#, "A2", "A3", "A4", "B1", "B2", "B3", "B4", "C1", "C2", "C3", "C4", "D1", "D2", "D3", "D4"],
    "stick" : ["Red"]#, "Green", "Blue", "Yellow"]
}

data_lock = threading.Lock()

def get_config(key):
    return configuration.get(key)

def write_config(key, value):
    configuration[key] = value