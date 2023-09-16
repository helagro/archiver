import os 
import sys
from settings.__main__ import Settings
from shouldArchive import ShouldArchive


argument = "" if len(sys.argv) < 2 else sys.argv[1]

settings = Settings()
shouldArchive = ShouldArchive(
    settings["excluded"], 
    settings["defaultRules"]
)


def main():

    print("= Archiver start =")
    if argument != "do":
        print("Add argument \"do\" to actually archive files")


    for folderItem in settings["folders"]:
        archiveOldFiles(folderItem)



def archiveOldFiles(folderItem):
    for itemName in os.listdir(folderItem["path"]):

        itemPath = folderItem["path"] + os.sep + itemName
        rules = folderItem["rules"]

        doArchive = shouldArchive.eval(itemPath, rules)
        if doArchive:
            archiveItem(itemPath)
        else:
            print("Would have archived:", itemPath)



main()