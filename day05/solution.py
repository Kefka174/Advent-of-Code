from typing import List
from re import split

def part_one(inputData: List[str]) -> int:
    seeds = [int(x) for x in inputData[0].split()[1:]]
    for mapping in inputData[1:]:
        mapRanges = []
        for line in mapping.split('\n')[1:]:
            mapRanges.append(tuple(map(int, line.split())))
        mapRanges.sort(key=lambda x: x[1])
        
        seeds.sort()
        seedIndex = 0
        for destination, source, length in mapRanges:
            while seedIndex < len(seeds) and seeds[seedIndex] < source + length:
                if seeds[seedIndex] >= source:
                    seeds[seedIndex] = destination + (seeds[seedIndex] - source)
                seedIndex += 1
    return min(seeds)


################################ TESTING #################################
testInput = """seeds: 79 14 55 13
               
               seed-to-soil map:
               50 98 2
               52 50 48
               
               soil-to-fertilizer map:
               0 15 37
               37 52 2
               39 0 15
               
               fertilizer-to-water map:
               49 53 8
               0 11 42
               42 0 7
               57 7 4
               
               water-to-light map:
               88 18 7
               18 25 70
               
               light-to-temperature map:
               45 77 23
               81 45 19
               68 64 13
               
               temperature-to-humidity map:
               0 69 1
               1 0 69
               
               humidity-to-location map:
               60 56 37
               56 93 4"""
testInput = split("\n\s*\n", testInput)
print("Part 1 test input:", part_one(testInput))

with open("input.txt", 'r') as file:
    fileInput = split("\n\s*\n", file.read())
    print("Part 1 file input:", part_one(fileInput))