from bisect import bisect_left, insort

def part_one(inputData: str) -> int: # TODO: modify to use part 2's jumpToObstruction()
    charMatrix = [list(row.strip()) for row in inputData.split('\n')]
    direction = [-1, 0]
    rowNum, colNum = findCharInMatrix('^', charMatrix)
    uniqueCellCount = 1
    while (rowNum + direction[0] >= 0 and rowNum + direction[0] < len(charMatrix)
           and colNum + direction[1] >= 0 and colNum + direction[1] < len(charMatrix[0])):
        if charMatrix[rowNum + direction[0]][colNum + direction[1]] == '#':
            direction[0], direction[1] = direction[1], - direction[0]
        else:
            if charMatrix[rowNum][colNum] != 'x':
                uniqueCellCount += 1
                charMatrix[rowNum][colNum] = 'x'
            rowNum += direction[0]
            colNum += direction[1]
    return uniqueCellCount

def part_two(inputData: str) -> int:
    charMatrix = [list(row.strip()) for row in inputData.split('\n')]
    rowObstructions, colObstructions = mapObstructions('#', charMatrix)
    direction = (-1, 0)
    startPosition = findCharInMatrix('^', charMatrix)
    rowNum, colNum = startPosition
    loopObstructions = set()
    while (rowNum + direction[0] >= 0 and rowNum + direction[0] < len(charMatrix)
           and colNum + direction[1] >= 0 and colNum + direction[1] < len(charMatrix[0])):
        if charMatrix[rowNum + direction[0]][colNum + direction[1]] == '#':
            direction = (direction[1], -direction[0])
        else:
            testObstruction = (rowNum + direction[0], colNum + direction[1])
            if (testObstruction not in loopObstructions
                and obstructionHereMakesLoop(testObstruction, rowObstructions, colObstructions, startPosition)):
                loopObstructions.add(testObstruction)
            rowNum += direction[0]
            colNum += direction[1]
    return len(loopObstructions)


def findCharInMatrix(char: str, matrix: list[list[str]]) -> tuple[int, int]:
    for rowNum in range(len(matrix)):
        for colNum in range(len(matrix[0])):
            if matrix[rowNum][colNum] == char:
                return rowNum, colNum

def mapObstructions(obstructionChar: str, matrix: list[list[str]]) -> tuple[list[list[int]], list[list[int]]]:
    rowObstructions = [[] for _ in range(len(matrix))]
    colObstructions = [[] for _ in range(len(matrix[0]))]
    for rowNum in range(len(matrix)):
        for colNum in range(len(matrix[0])):
            if matrix[rowNum][colNum] == obstructionChar:
                rowObstructions[rowNum].append(colNum)
                colObstructions[colNum].append(rowNum)
    return rowObstructions, colObstructions

def obstructionHereMakesLoop(testObstruction: tuple[int], rowObstructions: list[list[int]], 
                             colObstructions: list[list[int]], startPosition: tuple[int]) -> bool:
    insort(rowObstructions[testObstruction[0]], testObstruction[1])
    insort(colObstructions[testObstruction[1]], testObstruction[0])
    rowNum, colNum = startPosition
    direction = (-1, 0)
    visitedObstructions = set()
    madeItBackToStart = False
    while rowNum >= 0 and colNum >= 0:
        rowNum, colNum = jumpToObstruction(rowNum, colNum, direction, rowObstructions, colObstructions)
        if (rowNum, colNum, direction) in visitedObstructions:
            rowNum, colNum = -1, -1
            madeItBackToStart = True
        visitedObstructions.add((rowNum, colNum, direction))
        direction = (direction[1], -direction[0])
    rowObstructions[testObstruction[0]].remove(testObstruction[1])
    colObstructions[testObstruction[1]].remove(testObstruction[0])
    return madeItBackToStart

def jumpToObstruction(rowNum: int, colNum: int, direction: tuple[int], rowObstructions: list[list[int]], 
                      colObstructions: list[list[int]]) -> tuple[int]: # TODO: condense
    obstructionList, listDirection, listIndex = [], 0, 0
    if direction[0] == 0: # look in row
        obstructionList = rowObstructions[rowNum]
        listDirection = direction[1]
        listIndex = bisect_left(obstructionList, colNum)
    else: # look in col
        obstructionList = colObstructions[colNum]
        listDirection = direction[0]
        listIndex = bisect_left(obstructionList, rowNum)

    jumpValue = -1
    if listDirection == 1 and listIndex < len(obstructionList):
        jumpValue = obstructionList[listIndex] - 1
    elif listDirection == -1 and listIndex > 0:
        jumpValue = obstructionList[listIndex - 1] + 1
    return (rowNum, jumpValue) if direction[0] == 0 else (jumpValue, colNum)


################################ TESTING #################################
testInput = """....#.....
               .........#
               ..........
               ..#.......
               .......#..
               ..........
               .#..^.....
               ........#.
               #.........
               ......#..."""

print("Part 1 test input:", part_one(testInput)) # expect 41
print("Part 2 test input:", part_two(testInput)) # expect 6

with open("input.txt", 'r') as file:
    fileInput = file.read()
    print("Part 1 file input:", part_one(fileInput))
    print("Part 2 file input:", part_two(fileInput))