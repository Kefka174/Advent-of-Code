from typing import List, Tuple, Set
from itertools import combinations
from bisect import bisect

def part_one(inputData: str) -> int:
    spaceMap = [list(line.strip()) for line in inputData.split('\n')]
    expandedSpaceMap = expandSpace(spaceMap, 2)
    
    distancesSum = 0
    for galA, galB in combinations(findGalaxies(expandedSpaceMap), 2):
        distancesSum += distanceBetweenCoords(galA, galB)
    return distancesSum

def part_two(inputData: str, spaceMultiplier: int) -> int:
    spaceMap = [list(line.strip()) for line in inputData.split('\n')]
    galaxyCoords = findGalaxies(spaceMap)
    rowsToExpand, colsToExpand = map(lambda x: sorted(list(x)), 
                                     getRowsAndColsToExpand(galaxyCoords, len(spaceMap), len(spaceMap[0])))
    
    distancesSum = 0
    for galA, galB in combinations(galaxyCoords, 2):
        distancesSum += distanceBetweenExpandedCoords(galA, galB, rowsToExpand, colsToExpand, spaceMultiplier)
    return distancesSum


def expandSpace(spaceMap: List[List[str]], spaceMultiplier: int) -> List[List[str]]:
    galaxyCoords = findGalaxies(spaceMap)
    rowsToExpand, colsToExpand = getRowsAndColsToExpand(galaxyCoords, len(spaceMap), len(spaceMap[0]))
    expandedSpaceMap = [['.'] * (len(spaceMap[0]) + (len(colsToExpand) * (spaceMultiplier - 1))) 
                        for _ in range(len(spaceMap) + (len(rowsToExpand) * (spaceMultiplier - 1)))]
    
    numRowsExpanded, rowExpansionsInProgress = 0, 0
    for row in range(len(expandedSpaceMap)):
        if rowExpansionsInProgress:
            numRowsExpanded += 1
            rowExpansionsInProgress -= 1
        else:
            if row - numRowsExpanded in rowsToExpand:
                rowExpansionsInProgress = spaceMultiplier - 1
            else:
                numColsExpanded, colExpansionsInProgress = 0, 0
                for col in range(len(expandedSpaceMap[0])):
                    if colExpansionsInProgress:
                        numColsExpanded += 1
                        colExpansionsInProgress -= 1
                    else:
                        if col - numColsExpanded in colsToExpand:
                            colExpansionsInProgress = spaceMultiplier - 1
                        elif (row - numRowsExpanded, col - numColsExpanded) in galaxyCoords:
                            expandedSpaceMap[row][col] = '#'
    return expandedSpaceMap

def findGalaxies(spaceMap: List[List[str]]) -> Set[Tuple[int, int]]:
    galaxyCoords = set()
    for row in range(len(spaceMap)):
        for col in range(len(spaceMap[0])):
            if spaceMap[row][col] == '#':
                galaxyCoords.add((row, col))
    return galaxyCoords

def getRowsAndColsToExpand(galaxyCoords: Set[Tuple[int, int]], spaceMapHeight: int, 
                           spaceMapWidth: int) -> (Set[int], Set[int]):
    rowsToExpand = set(range(spaceMapHeight)).difference({row for row, _ in galaxyCoords})
    colsToExpand = set(range(spaceMapWidth)).difference({col for _, col in galaxyCoords})
    return rowsToExpand, colsToExpand

def distanceBetweenCoords(coordsA: Tuple[int, int], coordsB: Tuple[int, int]) -> int:
    rowDistance = abs(coordsA[0] - coordsB[0])
    colDistance = abs(coordsA[1] - coordsB[1])
    return rowDistance + colDistance

def distanceBetweenExpandedCoords(coordsA: Tuple[int, int], coordsB: Tuple[int, int], 
                                  rowsToExpand: List[int], colsToExpand: List[int], 
                                  spaceMultiplier: int) -> int:
    expandedRowsToCross = abs(bisect(rowsToExpand, coordsA[0]) - bisect(rowsToExpand, coordsB[0]))
    expandedColsToCross = abs(bisect(colsToExpand, coordsA[1]) - bisect(colsToExpand, coordsB[1]))
    rowDistance = abs(coordsA[0] - coordsB[0]) + (expandedRowsToCross * (spaceMultiplier - 1))
    colDistance = abs(coordsA[1] - coordsB[1]) + (expandedColsToCross * (spaceMultiplier - 1))
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

print("Part 1 test input:", part_one(testInput)) # expect 374
print("Part 2 first test input:", part_two(testInput, 10)) # expect 1030
print("Part 2 second test input:", part_two(testInput, 100)) # expect 8410

with open("input.txt", 'r') as file:
    fileInput = file.read()
    print("Part 1 file input:", part_one(fileInput))
    print("Part 2 file input:", part_two(fileInput, 1000000))