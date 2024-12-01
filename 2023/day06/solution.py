from typing import List, Callable

def part_one(inputData: str) -> int:
    splitData = inputData.split()
    races = [(int(time), int(distance)) for time, distance in 
             zip(splitData[1:len(splitData)//2], splitData[(len(splitData)//2)+1:])]
    
    product = 1
    for time, distance in races:
        product *= countWaysToWinRace(time, distance)
    return product

def part_two(inputData: str) -> int:
    time, distance = (int("".join(line.split()[1:])) for line in inputData.split('\n'))
    return countWaysToWinRace(time, distance)


def countWaysToWinRace(time: int, distance: int) -> int:
    firstWin = binarySearchRange(0, time, lambda x : prepTimeWinsRace(x, time, distance))
    lastWin = binarySearchRange(firstWin, time, lambda x : not prepTimeWinsRace(x, time, distance))
    return lastWin - firstWin

def prepTimeWinsRace(prepTime: int, time: int, distance: int) -> bool:
    distanceTraveled = prepTime * (time - prepTime)
    return distanceTraveled > distance

def binarySearchRange(bottomIndex: int, topIndex: int, 
                      func: Callable[[int], bool]) -> int:
    while bottomIndex < topIndex:
        middleIndex = (topIndex + bottomIndex) // 2
        if func(middleIndex):
            topIndex = middleIndex
        else:
            bottomIndex = middleIndex + 1
    return topIndex


################################ TESTING #################################
testInput = """Time:      7  15   30
               Distance:  9  40  200"""
print("Part 1 test input:", part_one(testInput))
print("Part 2 test input:", part_two(testInput))

fileInput = """Time:        60     80     86     76
               Distance:   601   1163   1559   1300"""
print("Part 1 file input:", part_one(fileInput))
print("Part 2 file input:", part_two(fileInput))