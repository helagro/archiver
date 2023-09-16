import json
import os 

def get():

    f = open("settings" + os.sep + ".env", "r")
    settingsPath = f.readline()
    f.close

    file = open(settingsPath)
    return json.load(file)