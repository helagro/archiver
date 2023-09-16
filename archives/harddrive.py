import os
import shutil
import time


def archiveItem(path):
    newPath = getNewPath(path)

    try:
        shutil.move(path, newPath)
        os.utime(newPath, (time.time(), time.time()))

        print("Archived:", path)
    except OSError:
        print("Could not archive", path)


def getNewPath(path):
    basePath = archivePath + os.sep + os.path.basename(path)
    path = basePath
    num = 1

    while os.path.exists(path):
        path = basePath + f" ({num})"
        num += 1

    return path