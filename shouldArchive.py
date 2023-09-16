import time
import math
import re
import os

class ShouldArchive:

    def __init__(self, excluded, defaultRules):
        self.excluded = excluded
        self.defaultRules = defaultRules


    def eval(self, path, rules):
        if self.__isItemExcepted(path): return False

        rule = self.__getFirstMatchingRule(rules, path)
        if rule is None: return False

        age = self.__getItemAge(path)
        return age >= rule["archiveAfterDays"]


    def __isItemExcepted(self, itemPath):
        for exception in self.excluded:
            if re.match(exception, itemPath):
                return True

        return False


    def __getFirstMatchingRule(self, rulesForFolder, itemPath):
        rules = rulesForFolder + self.defaultRules
        for rule in rules:
            ruleMatches = self.__doesRuleMatch(rule["pattern"], itemPath)
            if ruleMatches:
                return rule


    def __doesRuleMatch(self, rulePattern, itemPath):
        if rulePattern == "<folder>":
            return os.path.isdir(itemPath)
        if re.match(rulePattern, itemPath):
            return True
        return False
    

    def __getItemAge(self, path):
        timeStamps = [
            os.path.getmtime(path), #modified
            os.path.getatime(path), #accessed
            os.path.getctime(path) #changed
        ]
        
        ageInSeconds = time.time() - max(timeStamps)
        ageInDays = ageInSeconds / 3600 / 24
        return math.floor(ageInDays)