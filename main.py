import os 
import sys

from settings.__main__ import Settings
from shouldArchive import ShouldArchive
from archives.archive import Archive, getArchive


argument = "" if len(sys.argv) < 2 else sys.argv[1]

settings = Settings()
shouldArchive = ShouldArchive(
    settings["exclude"], 
    settings["defaultRules"]
)
archive: Archive = getArchive(
    settings["archiveType"],
    settings["archiveSettings"]
)


def main():
    print("= Archiver start =")
    if argument != "do":
        print("Add argument \"do\" to actually archive files")

    for folderItem in settings["folders"]:
        archiveOldFiles(folderItem)



def archiveOldFiles(folderItem):
    for itemName in os.listdir(folderItem["path"]):

        # should archive file?
        itemPath = folderItem["path"] + os.sep + itemName
        rules = folderItem["rules"]
        doArchive = shouldArchive.eval(itemPath, rules)

        # archive file
        if doArchive:
            if argument == "do":
                archive.archive(itemPath)
            else:
                print("Would have archived:", itemPath)



main()