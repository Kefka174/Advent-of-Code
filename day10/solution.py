from typing import List, Tuple

def part_one(inputData: str) -> int:
    pipeMap = [[*line.strip()] for line in inputData.split('\n')]
    start = [(rowNum, row.index('S')) for rowNum, row in enumerate(pipeMap) 
             if 'S' in row][0]
    
    nextDirection = findConnectedPipe(start, pipeMap)
    currentPipe = directionToCoords(start, nextDirection)
    stepCount = 1
    while currentPipe != start:
        nextDirection = getNextDirection(pipeMap[currentPipe[0]][currentPipe[1]], nextDirection)
        currentPipe = directionToCoords(currentPipe, nextDirection)
        stepCount += 1
    return stepCount // 2


def findConnectedPipe(startPoint: Tuple[int, int], pipeMap: List[List[str]]) -> str:
    direction, dirIndex = ["right", "down", "left", "up"], 0
    relativeCoords = (0, 1)
    for _ in range(4):
        neighbor = (startPoint[0] + relativeCoords[0], startPoint[1] + relativeCoords[1])
        neighborIsInBounds = (neighbor[0] >= 0 and neighbor[0] < len(pipeMap) 
                              and neighbor[1] >= 0 and neighbor[1] < len(pipeMap[0]))
        nextDirection = getNextDirection(pipeMap[neighbor[0]][neighbor[1]], direction[dirIndex])
        
        if neighborIsInBounds and nextDirection is not None:
            return direction[dirIndex]

        relativeCoords = (relativeCoords[1], -relativeCoords[0])
        dirIndex += 1

def getNextDirection(pipe: str, directionTraveledIn: str) -> str:
    pipeDirections = {'|': ("up", "down"), '-': ("left", "right"), 
                      'L': ("up", "right"), 'J': ("up", "left"), 
                      '7': ("left", "down"), 'F': ("right", "down")}
    if pipe not in pipeDirections: return None
    invertDirection = {"right": "left", "left": "right", "up": "down", "down": "up"}
    directionApproachedFrom = invertDirection[directionTraveledIn]

    if pipeDirections[pipe][0] == directionApproachedFrom:
        return pipeDirections[pipe][1]
    else:
        return pipeDirections[pipe][0]
    
def directionToCoords(startCoords: Tuple[int, int], direction: str) -> Tuple[int, int]:
    match direction:
        case "up":
            return (startCoords[0] - 1, startCoords[1])
        case "down":
            return (startCoords[0] + 1, startCoords[1])
        case "right":
            return (startCoords[0], startCoords[1] + 1)
        case "left":
            return (startCoords[0], startCoords[1] - 1)


################################ TESTING #################################
testInput1 = """-L|F7
                7S-7|
                L|7||
                -L-J|
                L|-JF"""
testInput2 = """7-F7-
                .FJ|7
                SJLL7
                |F--J
                LJ.LJ"""

print("Part 1 first test input:", part_one(testInput1))
print("Part 1 second test input:", part_one(testInput2))

with open("input.txt", 'r') as file:
    fileInput = file.read()
    print("Part 1 file input:", part_one(fileInput))