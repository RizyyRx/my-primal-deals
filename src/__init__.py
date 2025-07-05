import json

def check():
    print("working good....")

def get_config(key):
    config_file = "/home/rizwankendo/myPrimalDealsConfig.json"
    file = open(config_file,"r")
    config = json.load(file) # json load converts json data to python dictionary
    file.close() # close file after reading

    if key in config:
        return config[key]
    else:
        raise Exception("The key {} is not found in config.json",format(key))
