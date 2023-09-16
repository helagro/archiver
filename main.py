import os 
import time
import math
import sys
import re
import shutil

from settings.__main__ import get as getSettings

argument = "" if len(sys.argv) < 2 else sys.argv[1]
defaultRules = None
exclude = None
archivePath = None

def main():
    global defaultRules
    global exclude
    global archivePath

    print("= Archiver start =")
    if argument != "do":
        print("Add argument \"do\" to actually archive files")

    settings = getSettings()
    exclude = settings["exclude"]
    archivePath = settings["archivePath"]
    defaultRules = settings["defaultRules"]

    for folderItem in settings["folders"]:
        archiveOldFiles(folderItem)



def archiveOldFiles(folderItem):
    for itemName in os.listdir(folderItem["path"]):

        itemPath = folderItem["path"] + os.sep + itemName
        if isItemExcepted(itemPath): continue

        rule = getFirstMatchingRule(folderItem["rules"], itemPath)
        if rule is None: continue

        itemAge = getItemAge(itemPath)
        if itemAge >= rule["archiveAfterDays"]:
            archiveItem(itemPath)


def getItemAge(path):
    timeStamps = [
        os.path.getmtime(path), #modified
        os.path.getatime(path), #accessed
        os.path.getctime(path) #changed
    ]
    
    ageInSeconds = time.time() - max(timeStamps)
    ageInDays = ageInSeconds / 3600 / 24
    return math.floor(ageInDays)


def isItemExcepted(itemPath):
    for exception in exclude:
        if re.match(exception, itemPath):
            return True

    return False


def getFirstMatchingRule(rulesForFolder, itemPath):
    rules = rulesForFolder + defaultRules
    for rule in rules:
        ruleMatches = doesRuleMatch(rule["pattern"], itemPath)
        if ruleMatches:
            return rule


def doesRuleMatch(rulePattern, itemPath):
    if rulePattern == "<folder>":
        return os.path.isdir(itemPath)
    if re.match(rulePattern, itemPath):
        return True
    return False


def archiveItem(path):
    newPath = getNewPath(path)

    if argument == "do":
        try:
            shutil.move(path, newPath)
            os.utime(newPath, (time.time(), time.time()))

            print("Archived:", path)
        except OSError:
            print("Could not archive", path)
    else:
        print("Would have archived:", path)


def getNewPath(path):
    basePath = archivePath + os.sep + os.path.basename(path)
    path = basePath
    num = 1

    while os.path.exists(path):
        path = basePath + f" ({num})"
        num += 1

    return path

main()