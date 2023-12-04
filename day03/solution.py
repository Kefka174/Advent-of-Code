from typing import List, Tuple, Callable

def part_one(schematic: List[str]) -> int:
    schematic = [list(string) for string in schematic]
    sum = 0
    for row in range(len(schematic)):
        for col in range(len(schematic[row])):
            if (not schematic[row][col].isalnum() 
                and not schematic[row][col] == '.'):
                numericNeighbors = checkNeighbors(row, col, str.isdigit, schematic)
                for neighbor in numericNeighbors:
                    if schematic[neighbor[0]][neighbor[1]] != '.':
                        sum += removeNumberFromList(schematic[neighbor[0]], neighbor[1])
    return sum

def checkNeighbors(row: int, col: int, isValidNeighbor: Callable[[str], bool], 
                   matrix: List[List[str]]) -> List[Tuple[int, int]]:
    validNeighbors = []
    nextDirection = (-1, 0)
    for _ in range(2): # checks cardinal neighbors then diagonal neighbors
        for _ in range(4):
            neighborRow = row + nextDirection[0]
            neighborCol = col + nextDirection[1]
            if (coordsInBounds(neighborRow, neighborCol, matrix) 
                and isValidNeighbor(matrix[neighborRow][neighborCol])):
                validNeighbors.append((neighborRow, neighborCol))

            nextDirection = (nextDirection[1], -nextDirection[0])
        nextDirection = (-1, 1)
    return validNeighbors

def coordsInBounds(row: int, col: int, matrix: List[List[str]]) -> bool:
    return (row >= 0 and row < len(matrix) 
            and col >= 0 and col < len(matrix[0]))

def removeNumberFromList(list: List[str], startIndex: int) -> int:
    endIndex = startIndex
    while startIndex - 1 >= 0 and list[startIndex - 1].isdigit():
        startIndex -= 1
    while endIndex < len(list) and list[endIndex].isdigit():
        endIndex += 1
    
    val = int(''.join(list[startIndex : endIndex]))
    list[startIndex : endIndex] = ['.'] * (endIndex - startIndex)
    return val


################################ TESTING #################################
testInput = ["467..114..", 
             "...*......", 
             "..35..633.", 
             "......#...", 
             "617*......", 
             ".....+.58.", 
             "..592.....", 
             "......755.", 
             "...$.*....", 
             ".664.598.."]
print("Part 1 test input:", part_one(testInput))

with open("input.txt", 'r') as file:
    fileInput = file.read().split('\n')
    print("Part 1 file input:", part_one(fileInput))