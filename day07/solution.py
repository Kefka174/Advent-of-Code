from typing import Tuple
from collections import Counter

def part_one(inputData: str) -> int:
    return sumHandStringBidsTimesRanks(inputData)

def part_two(inputData: str) -> int:
    return sumHandStringBidsTimesRanks(inputData, True)

def sumHandStringBidsTimesRanks(inputData: str, treatJAsJoker: bool = False) -> int:
    hands = [(hand, int(bid)) for hand, bid in 
             (line.split() for line in inputData.split('\n'))]
    hands.sort(key=lambda hand : (handStrength(hand[0], treatJAsJoker), 
                                  cardStrengthsTuple(hand[0], treatJAsJoker)))

    sum = 0
    for i, (_, bid) in enumerate(hands):
        sum += (i + 1) * bid
    return sum

def handStrength(cards: str, treatJAsJoker: bool = False) -> int:
    cardFrequencies = Counter(cards)
    maxFrequency = 0
    if treatJAsJoker:
        maxFrequency += cardFrequencies.pop('J', 0)
    maxFrequency += max(cardFrequencies.values(), default=0)

    match maxFrequency:
        case 5: # 5 of a kind
            return 7
        case 4: # 4 of a kind
            return 6
        case 3: # Full house or 3 of a kind
            if len(cardFrequencies) == 2:
                return 5 # 7 - len
            return 4
        case 2: # Two or one pairs
            if len(cardFrequencies) == 3:
                return 3
            return 2
        case 1: # High card
            return 1

def cardStrengthsTuple(cards: str, treatJAsJoker: bool = False) -> Tuple[int]:
    return tuple(getCardValue(card, treatJAsJoker) for card in cards)

def getCardValue(card: str, treatJAsJoker: bool = False) -> int:
    faceValues = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10}
    if treatJAsJoker:
        faceValues['J'] = 1
        
    if card in faceValues:
        return faceValues[card]
    return int(card)

################################ TESTING #################################
testInput = """32T3K 765
               T55J5 684
               KK677 28
               KTJJT 220
               QQQJA 483"""
print("Part 1 test input:", part_one(testInput))
print("Part 2 test input:", part_two(testInput))

with open("input.txt", 'r') as file:
    fileInput = file.read()
    print("Part 1 file input:", part_one(fileInput))
    print("Part 2 file input:", part_two(fileInput))