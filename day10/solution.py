from typing import List, Tuple, Set, Callable
from itertools import count

def part_one(inputData: str) -> int:
    pipeMap = [[*line.strip()] for line in inputData.split('\n')]
    start = findAndReplaceStart(pipeMap)
    loopLengthCount = count(1)
    traversePipeLoop(start, pipeMap, lambda _: next(loopLengthCount))
    return next(loopLengthCount) // 2

def part_two(inputData: str) -> int:
    pipeMap = [[*line.strip()] for line in inputData.split('\n')]
    start = findAndReplaceStart(pipeMap)

    loopPipes = [start]
    traversePipeLoop(start, pipeMap, lambda x: loopPipes.append(x))

    tilesOutsideLoop = floodFillFromBorder(pipeMap, set(loopPipes))
    return (len(pipeMap) * len(pipeMap[1])) - (tilesOutsideLoop + len(loopPipes))


DIRECTIONS = ["right", "down", "left", "up"]
DIRECTION_INVERSES = {"right": "left", "down": "up", "left": "right", "up": "down"}
PIPE_DIRECTIONS = {'|': ("up", "down"), '-': ("left", "right"), 'L': ("up", "right"), 
                  'J': ("up", "left"), '7': ("left", "down"), 'F': ("right", "down")}
SQUEEZE_DIRECTIONS = {'L': ("left", "down"), 'J': ("down", "right"), 
                      '7': ("up", "right"), 'F': ("up", "left")}

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
    
    return startCoords

# Calls the given function on each pipe of a pipe loop
def traversePipeLoop(start: Tuple[int, int], pipeMap: List[List[str]], 
                     func: Callable[..., None]) -> None:
    # TODO: better mimic of do-while
    nextDirection = PIPE_DIRECTIONS[pipeMap[start[0]][start[1]]][0]
    currentPipe = getCoordsFromDirection(start, nextDirection)
    while currentPipe != start:
        func(currentPipe)
        nextDirection = getNextDirection(pipeMap[currentPipe[0]][currentPipe[1]], nextDirection)
        currentPipe = getCoordsFromDirection(currentPipe, nextDirection)
    func(start)

# Returns the Direction a pipe leads given the direction used to travel to that pipe
# or the next side of the pipe after squeezing around it
def getNextDirection(pipe: str, directionTraveledIn: str, squeezingAroundPipe: bool = False) -> str:
    nextDirection = None
    if pipe in PIPE_DIRECTIONS:
        directionApproachedFrom = directionTraveledIn
        if not squeezingAroundPipe:
            directionApproachedFrom = DIRECTION_INVERSES[directionTraveledIn]

        # TODO: simplify
        if PIPE_DIRECTIONS[pipe][0] == directionApproachedFrom:
            nextDirection = PIPE_DIRECTIONS[pipe][1]
        elif PIPE_DIRECTIONS[pipe][1] == directionApproachedFrom:
            nextDirection = PIPE_DIRECTIONS[pipe][0]
        elif squeezingAroundPipe:
            if PIPE_DIRECTIONS[pipe][0] == DIRECTION_INVERSES[directionApproachedFrom]:
                nextDirection = DIRECTION_INVERSES[PIPE_DIRECTIONS[pipe][1]]
            elif PIPE_DIRECTIONS[pipe][1] == DIRECTION_INVERSES[directionApproachedFrom]:
                nextDirection = DIRECTION_INVERSES[PIPE_DIRECTIONS[pipe][0]]
    return nextDirection
    
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
        
# Floodfills a matrix with 'X' from the borders and returns the number of tiles filled
# Will squeeze and fill through adjacent pipe gaps
def floodFillFromBorder(pipeMap: List[List[str]], tilesToIgnore: Set[Tuple[int, int]]) -> int:
    # counter = 0
    # for border tiles
        # if not 'X' add to queue

        # while queue:
            # currentPipe = queue.pop
            # for neighbor
                # if neighbor not 'X'
                    # if neighbor in tilesToIgnore:
                        # squeezeAroundLoop
                    # else:
                        # add to queue
                        # increment counter
    tilesTouchingLoop = squeezeAroundLoop((1,1), pipeMap, tilesToIgnore) #------------------------
    return 0
    
# Returns a set of tiles that border one side of a pipe loop
def squeezeAroundLoop(startCoords: Tuple[int, int], pipeMap: List[List[str]], 
                      tilesToIgnore: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
    sideOfPipe = [startingSide(startCoords, pipeMap)] # TODO: wrap in mutable object
    tilesTouchingLoop = set()
    def addSqueezedNeighborsToSet(pipeCoords):
        pipeShape = pipeMap[pipeCoords[0]][pipeCoords[1]]
        nextSide = getNextDirection(pipeShape, sideOfPipe[0], True)
        if nextSide:
            sideOfPipe[0] = nextSide
        
        directionsToCheck = ()
        if pipeShape in SQUEEZE_DIRECTIONS:
            if sideOfPipe[0] in SQUEEZE_DIRECTIONS[pipeShape]:
                directionsToCheck = SQUEEZE_DIRECTIONS[pipeShape]
        else:
            directionsToCheck = tuple(sideOfPipe)
        
        for direction in directionsToCheck:
            neighbor = getCoordsFromDirection(pipeCoords, direction)
            # TODO: make neighborIsInBounds a function
            neighborIsInBounds = (neighbor[0] >= 0 and neighbor[0] < len(pipeMap) 
                              and neighbor[1] >= 0 and neighbor[1] < len(pipeMap[0]))
            if neighborIsInBounds and neighbor not in tilesToIgnore:
                tilesTouchingLoop.add(neighbor)

    traversePipeLoop(startCoords, pipeMap, lambda coords: addSqueezedNeighborsToSet(coords))
    return tilesTouchingLoop

###############################TODO: Merge neighbor checking with findAndReplaceStart and floodFill
def startingSide(startCoords: Tuple[int, int], pipeMap: List[List[str]]) -> Tuple[str, str]:
    relativeCoords, diagIndex = (0, 1), 0
    for _ in range(4):
        neighbor = (startCoords[0] + relativeCoords[0], startCoords[1] + relativeCoords[1])
        neighborIsInBounds = (neighbor[0] >= 0 and neighbor[0] < len(pipeMap) 
                              and neighbor[1] >= 0 and neighbor[1] < len(pipeMap[0]))
        if neighborIsInBounds and pipeMap[neighbor[0]][neighbor[1]] == 'X':
            return DIRECTIONS[diagIndex]

        relativeCoords = (relativeCoords[1], -relativeCoords[0])
        diagIndex += 1
    return DIRECTIONS[-1]


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

testInput3 = """...........
                .S-------7.
                .|F-----7|.
                .||.....||.
                .||.....||.
                .|L-7.F-J|.
                .|..|.|..|.
                .L--J.L--J.
                ..........."""
testInput4 = """..........
                .S------7.
                .|F----7|.
                .||....||.
                .||....||.
                .|L-7F-J|.
                .|..||..|.
                .L--JL--J.
                .........."""
testInput5 = """.F----7F7F7F7F-7....
                .|F--7||||||||FJ....
                .||.FJ||||||||L7....
                FJL7L7LJLJ||LJ.L-7..
                L--J.L7...LJS7F-7L7.
                ....F-J..F7FJ|L7L7L7
                ....L7.F7||L7|.L7L7|
                .....|FJLJ|FJ|F7|.LJ
                ....FJL-7.||.||||...
                ....L---J.LJ.LJLJ..."""
testInput6 = """FF7FSF7F7F7F7F7F---7
                L|LJ||||||||||||F--J
                FL-7LJLJ||||||LJL-77
                F--JF--7||LJLJ7F7FJ-
                L---JF-JLJ.||-FJLJJ7
                |F|F-JF---7F7-L7L|7|
                |FFJF7L7F-JF7|JL---7
                7-L-JL7||F7|L7F-7F7|
                L.L7LFJ|||||FJL7||LJ
                L7JLJL-JLJLJL--JLJ.L"""

print("Part 2 first test input:", part_two(testInput3)) # expect 4

with open("input.txt", 'r') as file:
    fileInput = file.read()
    # print("Part 1 file input:", part_one(fileInput))