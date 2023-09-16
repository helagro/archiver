import os 
import time
import math
import sys
import re

from settings.__main__ import Settings


argument = "" if len(sys.argv) < 2 else sys.argv[1]
settings = Settings()


def main():

    print("= Archiver start =")
    if argument != "do":
        print("Add argument \"do\" to actually archive files")


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
            if argument == "do":
                archiveItem(itemPath)
            else:
                print("Would have archived:", itemPath)


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
    for exception in settings["exclude"]:
        if re.match(exception, itemPath):
            return True

    return False


def getFirstMatchingRule(rulesForFolder, itemPath):
    rules = rulesForFolder + settings["defaultRules"]
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




main()