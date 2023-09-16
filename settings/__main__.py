import json
import os 

__ENV_PATH = "settings" + os.sep + ".env"


def readEnvLine(number):
    with open(__ENV_PATH, 'r') as file:
        for _ in range(number):
            line = file.readline().rstrip("\n")
            if not line:
                return None
            
        return line



class Settings:
    settings = None

    def __init__(self):
        settingsPath = readEnvLine(1)

        file = open(settingsPath)
        self.settings = json.load(file)


    def __getitem__(self, key):
        if key not in self.settings:
            raise KeyError(f"'{key}' does not exist in settings")
        
        return self.settings[key]
    