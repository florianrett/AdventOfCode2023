import collections
import copy
import itertools
# from HelperClasses import Number
from ProgressBar import ProgressBar

# Day 5
def ConvertNumber(Number:int, Map:dict[tuple[int]]) -> int:

    for destStart, sourceStart, range in Map:
        if Number >= sourceStart and Number < sourceStart + range:
            return destStart + Number - sourceStart

    return Number

def ConvertNumberRangeRec(RangeStart:int, RangeLength:int, Map:dict[tuple[int]]) -> list[tuple[int]]:

    if RangeLength <= 0:
        return []
    OutRanges = []

    for destStart, sourceStart, range in Map:
        offset = destStart - sourceStart
        if RangeStart >= sourceStart and RangeStart < sourceStart + range:
            validMappingRange = min(RangeLength, range - (RangeStart - sourceStart))
            return [(RangeStart + offset, validMappingRange)] + ConvertNumberRangeRec(RangeStart + validMappingRange, RangeLength - validMappingRange, Map)
        
    # no given mapping, return range to next lowest source mapping and continue from there
    distances = [m[1] - RangeStart for m in Map if m[1] > RangeStart and m[1] < RangeStart + RangeLength]
    if len(distances) == 0: # no more mappings
        return [(RangeStart, RangeLength)]
    
    minDistance = min(distances)
    return [(RangeStart, minDistance)] + ConvertNumberRangeRec(RangeStart + minDistance, RangeLength - minDistance, Map)

# Day 12
def CalculatePossibleArrangementsRec(record:str, groups:list[int], groupSize:int, memoCache:dict[str,int]) -> int:

    CacheKey = (record, tuple(groups), groupSize)
    if CacheKey in memoCache:
        # print("Cache hit")
        return memoCache[CacheKey]

    # print(record, groups, groupSize)

    if len(record) == 0:
        if len(groups) == 0:
            return 1
        else:
            if len(groups) == 1 and groupSize == groups[0]:
                return 1
            else:
                return 0
    
    newGroups = copy.copy(groups)
    if record[0] == '?':
        result = CalculatePossibleArrangementsRec("#" + record[1:], newGroups, groupSize, memoCache) + CalculatePossibleArrangementsRec("." + record[1:], newGroups, groupSize, memoCache)
    
    elif record[0] == '#':
        if len(newGroups) == 0:
            result = 0
        else:
            result = CalculatePossibleArrangementsRec(record[1:], newGroups, groupSize + 1, memoCache)
    elif record[0] == '.':
        if groupSize > 0:
            if groupSize == newGroups.pop(0):
                result = CalculatePossibleArrangementsRec(record[1:], newGroups, 0, memoCache)
            else:
                result = 0
        else:
            result = CalculatePossibleArrangementsRec(record[1:], newGroups, 0, memoCache)
    
    
    memoCache[(record, tuple(newGroups), groupSize)] = result
    return result
    
# These 2 functions are an example for using itertools for brute forcing, from: https://www.reddit.com/r/adventofcode/comments/18gqqbh/comment/kd2a3du/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
def match(records: str, nums: list[int]) -> bool:
    return nums == [
        sum(1 for _ in grouper)
        for key, grouper in itertools.groupby(records)
        if key == "#"
    ]

def brute_force(records: str, nums: list[int]) -> int:
    gen = ("#." if letter == "?" else letter for letter in records)
    # print(gen)
    # for g in gen:
    #     print(g)
    # print("prod")
    # for p in itertools.product(*gen):
    #     print(p)
    return sum(match(candidate, nums) for candidate in itertools.product(*gen))

# Day 15
def Hash(input:str) -> int:
    result = 0
    for v in [ord(c) for c in input]:
        result += v
        result *= 17
        result %= 256
    return result

# Day 16
def CalcEnergizedTiles(input:list[str], entry:tuple) -> int:
    
    width:int = len(input[0])
    height = len(input)

    calculatedBeams:set[tuple] = set()
    beams:set[tuple] = set() # third index is direction, 0 up, 1 right, ..
    beams.add(entry)

    while len(beams) > 0:
        beam = beams.pop()
        x = beam[0]
        y = beam[1]
        dir = beam[2]
        if x < 0 or x >= width or y < 0 or y >= height:
            continue
        if beam in calculatedBeams:
            continue
        # print(beam)
        calculatedBeams.add(beam)

        tile = input[y][x]
        if tile == "/":
            if dir == 0:
                dir = 1
            elif dir == 1:
                dir = 0
            elif dir == 2:
                dir = 3
            elif dir == 3:
                dir = 2
        elif tile == "\\":
            if dir == 0:
                dir = 3
            elif dir == 1:
                dir = 2
            elif dir == 2:
                dir = 1
            elif dir == 3:
                dir = 0
        elif tile == "|":
            if dir == 1 or dir == 3:
                beams.add((x, y-1, 0))
                beams.add((x, y+1, 2))   
                continue 
        elif tile == "-":
            if dir == 0 or dir == 2:
                beams.add((x+1, y, 1))
                beams.add((x-1, y, 3))
                continue

        # empty tiles or pointy-end splitters
        if dir == 0:
            beams.add((x, y-1, dir))
        elif dir == 1:
            beams.add((x+1, y, dir))
        elif dir == 2:
            beams.add((x, y+1, dir))
        elif dir == 3:
            beams.add((x-1, y, dir))

    energizedTiles:set[tuple] = set()
    for b in calculatedBeams:
        energizedTiles.add((b[0], b[1]))

    return len(energizedTiles)

# Day 18
def IsInside(x:int, y:int, bounds:set[tuple]) -> bool:
    maxX = max([x[0] for x in bounds])
    numCrosses = 0
    while x <= maxX:
        if (x, y) in bounds:
            numCrosses += 1
            while (x, y) in bounds:
                x += 1
        else:
            x += 1

    return numCrosses % 2 != 0