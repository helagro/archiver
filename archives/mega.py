from archives.archive import Archive
from mega import Mega as Api
from settings.__main__ import readEnvLine
import os


class Mega(Archive):
    
    def __init__(self, archiveSettings):
        email = archiveSettings["email"]
        password = readEnvLine(2)
        self.api = Api().login(email, password)
        pass


    def archive(self, path):
        result = self.api.upload(path)
        os.remove(path)

        print(path, result)
