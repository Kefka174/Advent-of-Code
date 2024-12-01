from typing import List, Tuple
from re import split
from collections import deque

def part_one(inputData: List[str]) -> int:
    seeds = [int(x) for x in inputData[0].split()[1:]]
    for mapping in inputData[1:]:
        mapRanges = mapRangesFromMappingString(mapping)
        
        seeds.sort()
        seedIndex = 0
        for mapDestination, mapRangeStart, mapRangeLength in mapRanges:
            while seedIndex < len(seeds) and seeds[seedIndex] < mapRangeStart + mapRangeLength:
                if seeds[seedIndex] >= mapRangeStart:
                    seeds[seedIndex] = mapDestination + (seeds[seedIndex] - mapRangeStart)
                seedIndex += 1
    return min(seeds)

def part_two(inputData: List[str]) -> int:
    seeds = [(int(start), int(length)) for start, length 
             in zip(*[iter(inputData[0].split()[1:])] * 2)]

    for mapping in inputData[1:]:
        mapRanges = mapRangesFromMappingString(mapping)

        seedDeque = deque(sorted(seeds))
        mappedSeeds = []
        for mapDestination, mapRangeStart, mapRangeLength in mapRanges:
            while seedDeque and seedDeque[0][0]  < mapRangeStart + mapRangeLength:
                seedRangeStart, seedRangeLength = seedDeque.popleft()
                if seedRangeStart + seedRangeLength > mapRangeStart + mapRangeLength:
                    seedLengthAboveMap = ((seedRangeStart + seedRangeLength) 
                                          - (mapRangeStart + mapRangeLength))
                    seedDeque.appendleft((mapRangeStart + mapRangeLength, seedLengthAboveMap))
                    seedRangeLength -= seedLengthAboveMap
                
                if seedRangeStart + seedRangeLength > mapRangeStart:
                    seedLengthInMap = ((seedRangeStart + seedRangeLength) 
                                       - max(seedRangeStart, mapRangeStart))
                    mappedSeeds.append((mapDestination + (max(seedRangeStart, mapRangeStart) 
                                                          - mapRangeStart), seedLengthInMap))
                    seedRangeLength -= seedLengthInMap
                
                if seedRangeLength and seedRangeStart + seedRangeLength <= mapRangeStart:
                    mappedSeeds.append((seedRangeStart, seedRangeLength))

        while seedDeque:
            mappedSeeds.append(seedDeque.popleft())
        seeds = mappedSeeds
    return min(seeds)[0]

def mapRangesFromMappingString(string: str) -> List[Tuple[int, int, int]]:
    mapRanges = []
    for line in string.split('\n')[1:]:
        mapRanges.append(tuple(map(int, line.split())))
    mapRanges.sort(key=lambda x: x[1])
    return mapRanges


################################ TESTING #################################
testInput = split("\n\s*\n", """seeds: 79 14 55 13

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
                                56 93 4""")
print("Part 1 test input:", part_one(testInput))
print("Part 2 test input:", part_two(testInput))

with open("input.txt", 'r') as file:
    fileInput = split("\n\s*\n", file.read())
    print("Part 1 file input:", part_one(fileInput))
    print("Part 2 file input:", part_two(fileInput))