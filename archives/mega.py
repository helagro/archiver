from archives.archive import Archive
from mega import Mega as Api
from settings.__main__ import readEnvLine
import os
import zipfile
import delete


class Mega(Archive):
    
    def __init__(self, archiveSettings):
        email = archiveSettings["email"]
        password = readEnvLine(2)
        self.api = Api().login(email, password)
        pass


    def archive(self, path):
        if os.path.isdir(path):
            path = self.__zip(path)

        if not path: return

        self.api.upload(path)

        delete.any(path)
        print(path)


    def __zip(self, path):
        newPath = path + ".zip"

        try:
            with zipfile.ZipFile(newPath, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, _, files in os.walk(path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zipf.write(file_path, os.path.relpath(file_path, path))
            
            delete.any(path)
        except Exception as e:
            print(e)
            return
        return newPath
