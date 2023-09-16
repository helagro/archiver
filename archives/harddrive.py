import os
import shutil
import time
from archives.archive import Archive

class Harddrive(Archive):

    def __init__(self, archiveSettings):
        self.archivePath = archiveSettings["path"]


    def archive(self, path):
        newPath = self.__getNewPath(path)

        try:
            shutil.move(path, newPath)
            os.utime(newPath, (time.time(), time.time()))

            print("Archived:", path)
        except OSError:
            print("Could not archive", path)


    def __getNewPath(self, path):
        basePath = self.archivePath + os.sep + os.path.basename(path)
        path = basePath
        num = 1

        while os.path.exists(path):
            path = basePath + f" ({num})"
            num += 1

        return path