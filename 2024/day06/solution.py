def part_one(inputData: str) -> int:
    charMatrix = [list(row.strip()) for row in inputData.split('\n')]
    direction = [-1, 0]
    rowNum, colNum = findCharInMatrix('^', charMatrix)
    uniqueCellCount = 1
    while (rowNum + direction[0] >= 0 and rowNum + direction[0] < len(charMatrix)
           and colNum + direction[1] >= 0 and colNum + direction[1] < len(charMatrix[0])):
        if charMatrix[rowNum + direction[0]][colNum + direction[1]] == '#':
            direction[0], direction[1] = direction[1], - direction[0]
        else:
            if charMatrix[rowNum][colNum] != 'X':
                uniqueCellCount += 1
                charMatrix[rowNum][colNum] = 'X'
            rowNum += direction[0]
            colNum += direction[1]
    return uniqueCellCount


def findCharInMatrix(char: str, matrix: list[list[str]]) -> tuple[int, int]:
    for rowNum in range(len(matrix)):
        for colNum in range(len(matrix[0])):
            if matrix[rowNum][colNum] == char:
                return rowNum, colNum
        
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
# print("Part 2 test input:", part_two(testInput)) # expect 6

with open("input.txt", 'r') as file:
    fileInput = file.read()
    print("Part 1 file input:", part_one(fileInput))
    # print("Part 2 file input:", part_two(fileInput))