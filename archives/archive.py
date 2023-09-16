from abc import ABC, abstractmethod


def getArchive(archive, archiveSettings):
    if archive == "harddrive":
        from archives.harddrive import Harddrive
        return Harddrive(archiveSettings)
    elif archive == "mega":
        from archives.mega import Mega
        return Mega(archiveSettings)
    else:
        raise Exception(f"Archive \"{archive}\" not found")


class Archive(ABC):

    @abstractmethod
    def __init__(self, archiveSettings):
        pass
    
    @abstractmethod
    def archive(self, path):
        pass