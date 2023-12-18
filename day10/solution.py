from typing import List, Tuple, Set

def part_one(inputData: str) -> int:
    pipeMap = [[*line.strip()] for line in inputData.split('\n')]
    start, connectedPipeDirections = findAndReplaceStart(pipeMap)
    return len(getConnectedPipes(start, connectedPipeDirections, pipeMap)) // 2


DIRECTIONS = ["right", "down", "left", "up"]
DIRECTION_INVERSES = {"right": "left", "down": "up", "left": "right", "up": "down"}
PIPE_DIRECTIONS = {'|': ("up", "down"), '-': ("left", "right"), 'L': ("up", "right"), 
                  'J': ("up", "left"), '7': ("left", "down"), 'F': ("right", "down")}

# Finds the start 'S' in a pipeMap and replaces it with the appropriate pipe
# Returns the starting coordinates and the directions of its connected pipes
def findAndReplaceStart(pipeMap: List[List[str]]) -> Tuple[int, int]:
    startCoords = [(rowNum, row.index('S')) for rowNum, row in enumerate(pipeMap) 
                   if 'S' in row][0]
    connectedPipeDirections = set()
    relativeCoords, directionIndex = (0, 1), 0
    for _ in range(4): # coupled to directions order [right, down, left, up]
        neighbor = (startCoords[0] + relativeCoords[0], startCoords[1] + relativeCoords[1])
        neighborIsInBounds = (neighbor[0] >= 0 and neighbor[0] < len(pipeMap) 
                              and neighbor[1] >= 0 and neighbor[1] < len(pipeMap[0]))
        nextDirection = getNextDirection(pipeMap[neighbor[0]][neighbor[1]], 
                                         DIRECTIONS[directionIndex])

        if neighborIsInBounds and nextDirection is not None:
            connectedPipeDirections.add(DIRECTIONS[directionIndex])

        relativeCoords = (relativeCoords[1], -relativeCoords[0])
        directionIndex += 1

    for pipe in PIPE_DIRECTIONS.items():
        if set(pipe[1]) == connectedPipeDirections:
            pipeMap[startCoords[0]][startCoords[1]] = pipe[0]
    
    return startCoords, list(connectedPipeDirections)

# Returns a list of the pipes in a pipe loop
def getConnectedPipes(start: Tuple[int, int], connectedPipeDirections: List[str], 
                      pipeMap: List[List[str]]) -> List[Tuple[int, int]]:
    pipesInLoop = [start]
    nextDirection = connectedPipeDirections[0]
    currentPipe = getCoordsFromDirection(start, nextDirection)
    while currentPipe != start:
        pipesInLoop.append(currentPipe)
        nextDirection = getNextDirection(pipeMap[currentPipe[0]][currentPipe[1]], nextDirection)
        currentPipe = getCoordsFromDirection(currentPipe, nextDirection)
    return pipesInLoop

# Returns the Direction a pipe leads given the direction used to travel to that pipe
def getNextDirection(pipe: str, directionTraveledIn: str) -> str:
    if pipe in PIPE_DIRECTIONS:
        directionApproachedFrom = DIRECTION_INVERSES[directionTraveledIn]

        if PIPE_DIRECTIONS[pipe][0] == directionApproachedFrom:
            return PIPE_DIRECTIONS[pipe][1]
        elif PIPE_DIRECTIONS[pipe][1] == directionApproachedFrom:
            return PIPE_DIRECTIONS[pipe][0]
    return None
    
def getCoordsFromDirection(startCoords: Tuple[int, int], direction: str) -> Tuple[int, int]:
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

print("Part 1 first test input:", part_one(testInput1)) # expect 4
print("Part 1 second test input:", part_one(testInput2)) # expect 8

with open("input.txt", 'r') as file:
    fileInput = file.read()
    print("Part 1 file input:", part_one(fileInput))