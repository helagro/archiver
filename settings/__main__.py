import json
import os 


class Settings:
    settings = None

    def __init__(self):
        # load path of settings file to use from .env
        f = open("settings" + os.sep + ".env", "r")
        settingsPath = f.readline()
        f.close

        file = open(settingsPath)
        self.settings = json.load(file)


    def __getitem__(self, key):
        if key not in self.settings:
            raise KeyError(f"'{key}' does not exist in settings")
        
        return self.settings[key]