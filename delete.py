import shutil
import os

def any(path):
    if not os.path.exists(path): 
        print(f"Tried to delete '{path}' but it does not exist")
        return

    if os.path.isdir(path):
        folder(path)
    else:
        file(path)


def file(path):
    os.remove(path)

def folder(path):
    shutil.rmtree(path)