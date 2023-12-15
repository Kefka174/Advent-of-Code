from typing import List, Dict, Tuple
from collections import deque
from math import lcm

def part_one(inputData: str) -> int:
    directions, _, *nodeMaps = inputData.split('\n')
    nodeMaps = nodeStringsToDict(nodeMaps)
    return advanceNodesToEnd("AAA", directions, nodeMaps)

def part_two(inputData: str) -> int:
    directions, _, *nodeMaps = inputData.split('\n')
    nodeMaps = nodeStringsToDict(nodeMaps)
    
    currentNodes = []
    for node in nodeMaps.keys():
        if node[2] == 'A':
            currentNodes.append(node)
    
    return advanceNodesToEnd(currentNodes, directions, nodeMaps)


def nodeStringsToDict(nodeStringList: List[str]) -> Dict[str, Tuple[str, str]]:
    return {node.strip(): tuple(tup.strip('()').split(", ")) 
            for node, tup in (line.split(" = ") for line in nodeStringList)}

# Cycles are guarenteed since that is the only way a node can return to a 
# finished state after leaving one. Although the problem statement doesn't
# guarantee it, all of the cycles in the input are perfect loops (every cycle
# is the same length as the path from its start node to its end node) so its
# finished stepCount must be a multiple of its cycle length.
def advanceNodesToEnd(nodes: str | List[str], directions: str, 
                      nodeMaps: Dict[str, Tuple[str, str]]) -> int:
    if type(nodes) == str:
        nodes = [nodes]
    
    cycleLengths = [0] * len(nodes)
    for i, node in enumerate(nodes):
        directionDeque = deque(directions)
        while node[2] != 'Z':
            if directionDeque[0] == 'L':
                node = nodeMaps[node][0]
            else:
                node = nodeMaps[node][1]
            cycleLengths[i] += 1
            directionDeque.rotate(-1)

    return lcm(*cycleLengths)

################################ TESTING #################################
testInput1 = """RL

                AAA = (BBB, CCC)
                BBB = (DDD, EEE)
                CCC = (ZZZ, GGG)
                DDD = (DDD, DDD)
                EEE = (EEE, EEE)
                GGG = (GGG, GGG)
                ZZZ = (ZZZ, ZZZ)"""

testInput2 = """LLR

                AAA = (BBB, BBB)
                BBB = (AAA, ZZZ)
                ZZZ = (ZZZ, ZZZ)"""

testInput3 = """LR

                11A = (11B, XXX)
                11B = (XXX, 11Z)
                11Z = (11B, XXX)
                22A = (22B, XXX)
                22B = (22C, 22C)
                22C = (22Z, 22Z)
                22Z = (22B, 22B)
                XXX = (XXX, XXX)"""

print("Part 1 first test input:", part_one(testInput1))
print("Part 1 second test input:", part_one(testInput2))
print("Part 2 test input:", part_two(testInput3))

with open("input.txt", 'r') as file:
    fileInput = file.read()
    print("Part 1 file input:", part_one(fileInput))
    print("Part 2 file input:", part_two(fileInput))