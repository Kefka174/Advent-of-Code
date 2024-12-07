from typing import List

def part_one(inputData: str) -> int:
    targetWord = "XMAS"
    charMatrix = [list(row.strip()) for row in inputData.split('\n')]
    wordCount = 0
    for rowNum in range(len(charMatrix)):
        for colNum in range(len(charMatrix[0])):
            if charMatrix[rowNum][colNum] == targetWord[0]:
                wordCount += countWordsStartingAt(rowNum, colNum, charMatrix, targetWord)
    return wordCount

def part_two(inputData: str) -> int:
    charMatrix = [list(row.strip()) for row in inputData.split('\n')]
    xCount = 0
    for rowNum in range(len(charMatrix)):
        for colNum in range(len(charMatrix[0])):
            if (charMatrix[rowNum][colNum] == 'A'
                and charsFormXMas(rowNum, colNum, charMatrix)):
                xCount += 1
    return xCount


def countWordsStartingAt(startRowNum: int, startColNum: int, charMatrix: List[List[str]], targetWord: str) -> int:
    directions = [ # row, col
        (1, 0), # up
        (1, 1), # upright
        (0, 1), # right
        (-1, 1), # downright
        (-1, 0), # down
        (-1, -1), # downleft
        (0, -1), # left
        (1, -1) # upleft
    ]
    directionsWithWord = 0
    for rowDir, colDir in directions:
        charIndex = 1
        rowNum, colNum = startRowNum + rowDir, startColNum + colDir
        while (rowNum >= 0 and rowNum <= len(charMatrix) - 1
               and colNum >= 0 and colNum <= len(charMatrix[0]) -1
               and charIndex < len(targetWord)
               and charMatrix[rowNum][colNum] == targetWord[charIndex]):
            charIndex += 1
            rowNum += rowDir
            colNum += colDir
        if charIndex == len(targetWord):
            directionsWithWord += 1
    return directionsWithWord

def charsFormXMas(rowNum: int, colNum: int, charMatrix: List[List[str]]) -> bool:
    directions = [ # row, col
        (1, 1), # upright
        (-1, 1), # downright
    ]
    directionsMakingX = 0
    for rowDir, colDir in directions:
        diagonaIsInBounds = (rowNum > 0 and rowNum < len(charMatrix) - 1
                             and colNum > 0 and colNum < len(charMatrix[0]) - 1)
        if (diagonaIsInBounds):
            isForwards = (charMatrix[rowNum + rowDir][colNum + colDir] == 'M'
                          and charMatrix[rowNum - rowDir][colNum - colDir] == 'S')
            isBackwards = (charMatrix[rowNum - rowDir][colNum - colDir] == 'M'
                          and charMatrix[rowNum + rowDir][colNum + colDir] == 'S')
            if isForwards or isBackwards:
                directionsMakingX += 1
    return directionsMakingX == 2
        
################################ TESTING #################################
testInput = """MMMSXXMASM
               MSAMXMSMSA
               AMXSXMAAMM
               MSAMASMSMX
               XMASAMXAMM
               XXAMMXXAMA
               SMSMSASXSS
               SAXAMASAAA
               MAMMMXMMMM
               MXMXAXMASX"""

print("Part 1 test input:", part_one(testInput)) # expect 18
print("Part 2 test input:", part_two(testInput)) # expect 9

with open("input.txt", 'r') as file:
    fileInput = file.read()
    print("Part 1 file input:", part_one(fileInput))
    print("Part 2 file input:", part_two(fileInput))