from typing import Dict, List, Set
import re

def part_one(inputData: str) -> int:
    ruleDict = makeRuleDict(inputData)
    middleValTotal = 0
    for line in re.findall("\s*(.*,.*)", inputData):
        manual = line.split(',')
        if manualIsOrdered(manual, ruleDict):
            middleValTotal += int(manual[len(manual) // 2])
    return middleValTotal

def part_two(inputData: str) -> int:
    ruleDict = makeRuleDict(inputData)
    middleValTotal = 0
    for line in re.findall("\s*(.*,.*)", inputData):
        manual = line.split(',')
        if not manualIsOrdered(manual, ruleDict):
            orderedManual = orderManual(manual, ruleDict)
            middleValTotal += int(orderedManual[len(orderedManual) // 2])
    return middleValTotal


def makeRuleDict(inputData: str) -> dict[str, set[str]]:
    ruleDict = {}
    for key, val in re.findall("(\d+)\|(\d+)", inputData):
        if not key in ruleDict:
            ruleDict[key] = set()
        ruleDict[key].add(val)
    return ruleDict

def manualIsOrdered(manual: list[str], ruleDict: dict[str, set[str]]) -> bool:
    pageDict = {number: index for index, number in enumerate(manual)}
    for page in manual:
        if page in ruleDict:
            for laterPage in ruleDict[page]:
                if (laterPage in pageDict 
                    and pageDict[laterPage] < pageDict[page]):
                    return False
    return True

def orderManual(manual: list[str], ruleDict: dict[str, set[str]]) -> list[str]:
    orderedManual = []
    for page in manual:
        if page not in ruleDict:
            orderedManual.append(page)
        else:
            i = 0
            while i < len(orderedManual) and orderedManual[i] not in ruleDict[page]:
                i += 1
            orderedManual.insert(i, page)
    return orderedManual
        
################################ TESTING #################################
testInput = """47|53
               97|13
               97|61
               97|47
               75|29
               61|13
               75|53
               29|13
               97|29
               53|29
               61|53
               97|53
               61|29
               47|13
               75|47
               97|75
               47|61
               75|61
               47|29
               75|13
               53|13
               
               75,47,61,53,29
               97,61,53,29,13
               75,29,13
               75,97,47,61,53
               61,13,29
               97,13,75,29,47"""

print("Part 1 test input:", part_one(testInput)) # expect 143
print("Part 2 test input:", part_two(testInput)) # expect 123

with open("input.txt", 'r') as file:
    fileInput = file.read()
    print("Part 1 file input:", part_one(fileInput))
    print("Part 2 file input:", part_two(fileInput))