from typing import List, Dict
from re import split

def part_one(games: List[str], maxValues: Dict[str, int]) -> int:
    sum = 0
    for i, game in enumerate(games):
        gameIsPossible = True
        for round in split("; |: ", game)[1:]:
            for cube in round.split(', '):
                count, color = cube.split()
                if int(count) > maxValues[color]:
                    gameIsPossible = False
        if gameIsPossible:
            sum += i + 1
    return sum


def part_two(games: List[str]) -> int:
    sum = 0
    for i, game in enumerate(games):
        maxValuesSeen = {}
        for round in split("; |: ", game)[1:]:
            for cube in round.split(', '):
                count, color = cube.split()
                if color not in maxValuesSeen or int(count) > maxValuesSeen[color]:
                    maxValuesSeen[color] = int(count)
        
        power = 1
        for colorCount in maxValuesSeen.values():
            power *= colorCount
        sum += power
    return sum


################################ TESTING #################################
maxValues = {"red": 12, "green": 13, "blue": 14}
testInput = ["Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green", 
              "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue", 
              "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red", 
              "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red", 
              "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"]
print("Part 1 test input:", part_one(testInput, maxValues))
print("Part 2 test input:", part_two(testInput))

with open("input.txt", 'r') as file:
    fileInput = file.read().split('\n')
    print("Part 1 file input:", part_one(fileInput, maxValues))
    print("Part 2 file input:", part_two(fileInput))