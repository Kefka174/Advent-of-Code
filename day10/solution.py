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

    loopPipes = []
    traversePipeLoop(start, pipeMap, lambda x: loopPipes.append(x))

    numTilesOutsideLoop = floodFillFromBorder(pipeMap, set(loopPipes))
    return (len(pipeMap) * len(pipeMap[0])) - (numTilesOutsideLoop + len(loopPipes))


DIRECTIONS = ["right", "down", "left", "up"]
DIRECTION_INVERSES = {"right": "left", "down": "up", "left": "right", "up": "down"}
PIPE_DIRECTIONS = {'|': ("up", "down"), '-': ("left", "right"), 'L': ("up", "right"), 
                  'J': ("up", "left"), '7': ("left", "down"), 'F': ("right", "down")}
SQUEEZE_DIRECTIONS = {'L': ("left", "down"), 'J': ("down", "right"), 
                      '7': ("up", "right"), 'F': ("up", "left")}

# Finds the start 'S' in a pipeMap and replaces it with the appropriate pipe
# Returns the starting coordinates and the directions of its connected pipes
def findAndReplaceStart(pipeMap: List[List[str]]) -> Tuple[int, int]:
    startCoords = [(rowNum, row.index('S')) for rowNum, row in enumerate(pipeMap) if 'S' in row][0]
    connectedPipeDirections, dirIndex = set(), 0
    def appendConnectedNeighbors(neighbor: Tuple[int, int]) -> None:
        nonlocal dirIndex # coupled to directions order [right, down, left, up]
        if getNextSideOfPipe(pipeMap[neighbor[0]][neighbor[1]], DIRECTIONS[dirIndex]):
            connectedPipeDirections.add(DIRECTIONS[dirIndex])
        dirIndex += 1
    callFuncOnNeighbors(startCoords, pipeMap, appendConnectedNeighbors)

    for pipe in PIPE_DIRECTIONS.items():
        if set(pipe[1]) == connectedPipeDirections:
            pipeMap[startCoords[0]][startCoords[1]] = pipe[0]
    
    return startCoords

# Calls the given function on each pipe of a pipe loop
def traversePipeLoop(start: Tuple[int, int], pipeMap: List[List[str]], 
                     func: Callable[..., None]) -> None:
    nextDirection = PIPE_DIRECTIONS[pipeMap[start[0]][start[1]]][0]
    currentPipe = getCoordsFromDirection(start, nextDirection)
    while currentPipe != start:
        nextDirection = getNextSideOfPipe(pipeMap[currentPipe[0]][currentPipe[1]], nextDirection)
        func(currentPipe)
        currentPipe = getCoordsFromDirection(currentPipe, nextDirection)
    func(start)

# Returns the Direction a pipe leads given the direction used to travel to that pipe
# or the next side of the pipe after squeezing around it
def getNextSideOfPipe(pipeShape: str, directionTraveledIn: str, squeezingAroundPipe: bool = False) -> str:
    nextDirection = None
    if pipeShape in PIPE_DIRECTIONS:
        directionApproachedFrom = directionTraveledIn
        if not squeezingAroundPipe:
            directionApproachedFrom = DIRECTION_INVERSES[directionTraveledIn]

        if PIPE_DIRECTIONS[pipeShape][0] == directionApproachedFrom:
            nextDirection = PIPE_DIRECTIONS[pipeShape][1]
        elif PIPE_DIRECTIONS[pipeShape][1] == directionApproachedFrom:
            nextDirection = PIPE_DIRECTIONS[pipeShape][0]
        elif squeezingAroundPipe: # TODO: simplify
            if PIPE_DIRECTIONS[pipeShape][0] == DIRECTION_INVERSES[directionApproachedFrom]:
                nextDirection = DIRECTION_INVERSES[PIPE_DIRECTIONS[pipeShape][1]]
            elif PIPE_DIRECTIONS[pipeShape][1] == DIRECTION_INVERSES[directionApproachedFrom]:
                nextDirection = DIRECTION_INVERSES[PIPE_DIRECTIONS[pipeShape][0]]
    return nextDirection
    
def getCoordsFromDirection(coords: Tuple[int, int], direction: str) -> Tuple[int, int]:
    match direction:
        case "up":
            return (coords[0] - 1, coords[1])
        case "down":
            return (coords[0] + 1, coords[1])
        case "right":
            return (coords[0], coords[1] + 1)
        case "left":
            return (coords[0], coords[1] - 1)
        
def callFuncOnNeighbors(coords: Tuple[int, int], pipeMap: List[List[str]], 
                   func: Callable[..., None]) -> None:
    relativeCoords = (0, 1)
    for _ in range(4):
        neighbor = (coords[0] + relativeCoords[0], coords[1] + relativeCoords[1])
        neighborIsInBounds = (neighbor[0] >= 0 and neighbor[0] < len(pipeMap) 
                            and neighbor[1] >= 0 and neighbor[1] < len(pipeMap[0]))
        if neighborIsInBounds:
            func(neighbor)

        relativeCoords = (relativeCoords[1], -relativeCoords[0])
        
# Floodfills a matrix with 'X' from the borders and returns the number of tiles filled
# Will squeeze and fill through adjacent pipe gaps
def floodFillFromBorder(pipeMap: List[List[str]], tilesToIgnore: Set[Tuple[int, int]]) -> int:
    numTilesFilled = 0
    for borderTile in ([(0, x) for x in range(len(pipeMap[0]))] + 
                       [(len(pipeMap) - 1, x) for x in range(len(pipeMap[0]))] +
                       [(x, 0) for x in range(1, len(pipeMap) - 1)] + 
                       [(x, len(pipeMap[0]) - 1) for x in range(1, len(pipeMap) - 1)]):
        tilesToFill = set()
        if (pipeMap[borderTile[0]][borderTile[1]] != 'X' and borderTile not in tilesToIgnore):
            tilesToFill.add(borderTile)
        
        def addNeighborToSet(neighbor: Tuple[int, int]) -> None:
            if pipeMap[neighbor[0]][neighbor[1]] != 'X':
                if neighbor in tilesToIgnore:
                    tilesToFill.update(squeezeAroundLoop(neighbor, pipeMap, tilesToIgnore))
                else:
                    tilesToFill.add(neighbor)
        while tilesToFill:
            currentPipe = tilesToFill.pop()
            pipeMap[currentPipe[0]][currentPipe[1]] = 'X'
            numTilesFilled += 1
            callFuncOnNeighbors(currentPipe, pipeMap, addNeighborToSet)
    return numTilesFilled
    
# Returns a set of tiles that border the side of the pipe loop with an 'X'
def squeezeAroundLoop(startCoords: Tuple[int, int], pipeMap: List[List[str]], 
                      tilesToIgnore: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
    sideOfPipe = startingSide(startCoords, pipeMap)
    tilesTouchingLoop = set()
    def addSqueezedNeighborsToSet(pipeCoords):
        nonlocal sideOfPipe
        pipeShape = pipeMap[pipeCoords[0]][pipeCoords[1]]
        pipeMap[pipeCoords[0]][pipeCoords[1]] = 'X'
        nextSide = getNextSideOfPipe(pipeShape, sideOfPipe, True)
        if nextSide:
            sideOfPipe = nextSide
        
        directionsToCheck = ()
        if pipeShape in SQUEEZE_DIRECTIONS:
            if sideOfPipe in SQUEEZE_DIRECTIONS[pipeShape]:
                directionsToCheck = SQUEEZE_DIRECTIONS[pipeShape]
        else:
            directionsToCheck = (sideOfPipe,)
        
        for direction in directionsToCheck:
            neighbor = getCoordsFromDirection(pipeCoords, direction)
            neighborIsInBounds = (neighbor[0] >= 0 and neighbor[0] < len(pipeMap) 
                              and neighbor[1] >= 0 and neighbor[1] < len(pipeMap[0]))
            if (neighborIsInBounds and pipeMap[neighbor[0]][neighbor[1]] != 'X' 
                and neighbor not in tilesToIgnore):
                tilesTouchingLoop.add(neighbor)

    traversePipeLoop(startCoords, pipeMap, addSqueezedNeighborsToSet)
    return tilesTouchingLoop

# Returns the side of the pipe in the pipe loop that the loop was approached from
def startingSide(coords: Tuple[int, int], pipeMap: List[List[str]]) -> Tuple[str, str]:
    side, dirIndex = DIRECTIONS[-1], 0
    def findSideWithX(neighbor: Tuple[int, int]) -> None:
        nonlocal side, dirIndex
        if pipeMap[neighbor[0]][neighbor[1]] == 'X':
            side = DIRECTIONS[dirIndex]
        dirIndex += 1
    callFuncOnNeighbors(coords, pipeMap, findSideWithX)

    pipeShape = pipeMap[coords[0]][coords[1]]
    # coupled to loop traversal's initial direction being PIPE_DIRECTIONS[pipe][0]
    if side == DIRECTION_INVERSES[PIPE_DIRECTIONS[pipeShape][0]]:
        side = getNextSideOfPipe(pipeShape, side, True)
    return side


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
testInput4 = """.........
                S------7.
                |F----7|.
                ||....||.
                ||....||.
                |L-7F-J|.
                |..||..|.
                L--JL--J.
                ........."""
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
print("Part 2 second test input:", part_two(testInput4)) # expect 4
print("Part 2 third test input:", part_two(testInput5)) # expect 8
print("Part 2 fourth test input:", part_two(testInput6)) # expect 10

with open("input.txt", 'r') as file:
    fileInput = file.read()
    print("Part 1 file input:", part_one(fileInput))
    print("Part 2 file input:", part_two(fileInput))