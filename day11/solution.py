from typing import List, Tuple, Set
from itertools import combinations

def part_one(inputData: str) -> int:
    spaceMap = [list(line.strip()) for line in inputData.split('\n')]
    expandedSpaceMap = expandSpace(spaceMap)
    
    distancesSum = 0
    for galA, galB in combinations(findGalaxies(expandedSpaceMap), 2):
        distancesSum += distanceBetweenCoords(galA, galB)
    return distancesSum


def expandSpace(spaceMap: List[List[str]]) -> List[List[str]]:
    galaxyCoords = findGalaxies(spaceMap)
    rowsToExpand = set(range(len(spaceMap))).difference({row for row, _ in galaxyCoords})
    colsToExpand = set(range(len(spaceMap[0]))).difference({col for _, col in galaxyCoords})
    expandedSpaceMap = [['.'] * (len(spaceMap[0]) + len(colsToExpand)) 
                        for _ in range(len(spaceMap) + len(rowsToExpand))]
    
    rowsExpanded = set()
    for row in range(len(expandedSpaceMap)):
        colsExpanded = set()
        if row - len(rowsExpanded) in rowsToExpand:
            rowsExpanded.add(row - len(rowsExpanded))
        else:
            for col in range(len(expandedSpaceMap[0])):
                if col - len(colsExpanded) in colsToExpand:
                    colsExpanded.add(col - len(colsExpanded))
                elif (row - len(rowsExpanded), col - len(colsExpanded)) in galaxyCoords:
                    expandedSpaceMap[row][col] = '#'
    return expandedSpaceMap

def findGalaxies(spaceMap: List[List[str]]) -> Set[Tuple[int, int]]:
    galaxyCoords = set()
    for row in range(len(spaceMap)):
        for col in range(len(spaceMap[0])):
            if spaceMap[row][col] == '#':
                galaxyCoords.add((row, col))
    return galaxyCoords

def distanceBetweenCoords(coordsA: Tuple[int, int], coordsB: Tuple[int, int]) -> int:
    rowDistance = abs(coordsA[0] - coordsB[0])
    colDistance = abs(coordsA[1] - coordsB[1])
    return rowDistance + colDistance


################################ TESTING #################################
testInput = """...#......
               .......#..
               #.........
               ..........
               ......#...
               .#........
               .........#
               ..........
               .......#..
               #...#....."""

print("Part 1 first test input:", part_one(testInput)) # expect 374

with open("input.txt", 'r') as file:
    fileInput = file.read()
    print("Part 1 file input:", part_one(fileInput))