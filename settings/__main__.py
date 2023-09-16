import json
import os
from dotenv import load_dotenv





class Settings:
    __settings = None
    _instance = None


    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
        return cls._instance


    def __init__(self):
        envPath = "settings" + os.sep + ".env"
        load_dotenv(dotenv_path=envPath)
        self.__megaPassword = os.getenv("MEGA_PASSWORD")

        file = open(os.getenv("SETTINGS_FILE"))
        self.__settings = json.load(file)



    def __getitem__(self, key):
        if key not in self.__settings:
            raise KeyError(f"'{key}' does not exist in settings")
        
        return self.__settings[key]
    

    def getMegaPassword(self):
        return self.__megaPassword
    