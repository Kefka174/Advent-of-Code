from typing import List, Tuple
from collections import Counter

def part_one(inputData: str) -> int:
    firstList, secondList = parseLists(inputData)
    firstList.sort()
    secondList.sort()

    distance = 0
    for i in range(len(firstList)):
        distance += abs(firstList[i] - secondList[i])
    return distance

# Could reduce by n operations by forming secondListFreqMap in original parsing
# instead of parsing to list and converting to counter
def part_two(inputData: str) -> int:
    firstList, secondList = parseLists(inputData)
    secondListFreqMap = Counter(secondList)

    similarityScore = 0
    for val in firstList:
        similarityScore += val * secondListFreqMap[val]
    return similarityScore


def parseLists(inputData: str) -> Tuple[List[int]]:
    firstList, secondList = [], []
    for line in inputData.split('\n'):
        firstValue, secondValue = map(int, line.split())
        firstList.append(firstValue)
        secondList.append(secondValue)
    return firstList, secondList


################################ TESTING #################################
testInput = """3   4
               4   3
               2   5
               1   3
               3   9
               3   3"""

print("Part 1 test input:", part_one(testInput)) # expect 11
print("Part 2 test input:", part_two(testInput)) # expect 31

with open("input.txt", 'r') as file:
    fileInput = file.read()
    print("Part 1 file input:", part_one(fileInput))
    print("Part 2 file input:", part_two(fileInput))