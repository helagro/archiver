import time
import math
import re
import os

class ShouldArchive:

    def __init__(self, excluded, defaultRules):
        self.excluded = excluded
        self.defaultRules = defaultRules


    def getFirstMatchingRule(self, rulesForFolder, itemPath):
        rules = rulesForFolder + self.defaultRules
        for rule in rules:
            ruleMatches = self.__doesRuleMatch(rule["pattern"], itemPath)
            if ruleMatches:
                return rule


    def eval(self, path, rule):
        if rule is None: return False
        if self.__isItemExcepted(path): return False
        if not os.path.exists(path): return False

        minAge = rule["archiveAfterDays"]
        ignoreAccess = "ignoreAccess" in rule and rule["ignoreAccess"]
        return self.__oldEnough(path, minAge, ignoreAccess)


    def __isItemExcepted(self, itemPath):
        for exception in self.excluded:
            if re.match(exception, itemPath):
                return True

        return False


    def __doesRuleMatch(self, rulePattern, itemPath):
        if rulePattern == "<folder>":
            return os.path.isdir(itemPath)
        if re.match(rulePattern, itemPath):
            return True
        return False
    

    def __oldEnough(self, path, minAge, ignoreAccess):
        try:
            timeStamps = [
                os.path.getmtime(path), #modified
                os.path.getctime(path) #changed
            ]

            if not ignoreAccess:
                timeStamps.append(os.path.getatime(path))
            
            ageInSeconds = time.time() - max(timeStamps)
            ageInDays = math.floor(ageInSeconds / 3600 / 24)

            if(ageInDays >= minAge):
                if(os.path.isdir(path)):
                    return self.__folderOldEnough(path, minAge)
                else:
                    return True
            else:
                return False
        except:
            return False


    def __folderOldEnough(self, path, minAge):
        for itemName in os.listdir(path):
            itemPath = path + os.sep + itemName
            oldEnough = self.__oldEnough(itemPath, minAge)
            if not oldEnough: return False

        return True
