shared_data = {
    "sensorData" : 0,
    "stick" : None,
    "hole" : None,
    "imageList" : None,
    "currentImage": None,
    "blurFactor" : 9,
    "imgNum" : 0,
    "correctUserAction": None,
    "userCheck" : False
}

def get_data(key):
    return shared_data.get(key)

def write_data(key, value):
    shared_data[key] = value 