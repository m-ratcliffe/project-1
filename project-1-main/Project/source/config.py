import threading

configuration = {
    "portVar" : "COM4"
}

data_lock = threading.Lock()

def get_config(key):
    return configuration.get(key)

def write_config(key, value):
    configuration[key] = value