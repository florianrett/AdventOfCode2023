import collections
import itertools
# from HelperClasses import Number
from ProgressBar import ProgressBar
from copy import copy

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
    
    newGroups = copy(groups)
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

# Day 19 
def CalculateAcceptanceRangesRec(xRange:range, mRange:range, aRange:range, sRange:range, currentWorkflow:str, workflows:dict[str,list[tuple]], results:list[tuple], flow:list[str] = []) -> None:

    if currentWorkflow == "R":
        return
    
    if currentWorkflow == "A":
        results.append((xRange, mRange, aRange, sRange, flow))
        return

    if len(xRange) == 0 or len(mRange) == 0 or len(aRange) == 0 or len(sRange) == 0:
        return
    
    NewFlow = copy(flow)
    NewFlow.append(currentWorkflow)
        
    RemainingRangeX = copy(xRange)
    RemainingRangeM = copy(mRange)
    RemainingRangeA = copy(aRange)
    RemainingRangeS = copy(sRange)

    workflow = workflows[currentWorkflow]
    for rule in workflow:
        compValue:int = rule[2]
        nextWorkflow:str = rule[3]
        if rule[1]: # greater
            if rule[0] == 0:
                NewRange = range(max(RemainingRangeX.start, compValue + 1), RemainingRangeX.stop) # need to ensure range start is not set to 0 when comparing to the specialized "x>0" condition I used to encode the final fallback rule
                RemainingRangeX = range(RemainingRangeX.start, compValue + 1)
                CalculateAcceptanceRangesRec(NewRange, RemainingRangeM, RemainingRangeA, RemainingRangeS, nextWorkflow, workflows, results, NewFlow)
            elif rule[0] == 1:
                NewRange = range(compValue + 1, RemainingRangeM.stop)
                RemainingRangeM = range(RemainingRangeM.start, compValue + 1)
                CalculateAcceptanceRangesRec(RemainingRangeX, NewRange, RemainingRangeA, RemainingRangeS, nextWorkflow, workflows, results, NewFlow)
            elif rule[0] == 2:
                NewRange = range(compValue + 1, RemainingRangeA.stop)
                RemainingRangeA = range(RemainingRangeA.start, compValue + 1)
                CalculateAcceptanceRangesRec(RemainingRangeX, RemainingRangeM, NewRange, RemainingRangeS, nextWorkflow, workflows, results, NewFlow)
            else:
                NewRange = range(compValue + 1, RemainingRangeS.stop)
                RemainingRangeS = range(RemainingRangeS.start, compValue + 1)
                CalculateAcceptanceRangesRec(RemainingRangeX, RemainingRangeM, RemainingRangeA, NewRange, nextWorkflow, workflows, results, NewFlow)
        else: # smaller
            if rule[0] == 0:
                NewRange = range(RemainingRangeX.start, compValue)
                RemainingRangeX = range(compValue, RemainingRangeX.stop)
                CalculateAcceptanceRangesRec(NewRange, RemainingRangeM, RemainingRangeA, RemainingRangeS, nextWorkflow, workflows, results, NewFlow)
            elif rule[0] == 1:
                NewRange = range(RemainingRangeM.start, compValue)
                RemainingRangeM = range(compValue, RemainingRangeM.stop)
                CalculateAcceptanceRangesRec(RemainingRangeX, NewRange, RemainingRangeA, RemainingRangeS, nextWorkflow, workflows, results, NewFlow)
            elif rule[0] == 2:
                NewRange = range(RemainingRangeA.start, compValue)
                RemainingRangeA = range(compValue, RemainingRangeA.stop)
                CalculateAcceptanceRangesRec(RemainingRangeX, RemainingRangeM, NewRange, RemainingRangeS, nextWorkflow, workflows, results, NewFlow)
            else:
                NewRange = range(RemainingRangeS.start, compValue)
                RemainingRangeS = range(compValue, RemainingRangeS.stop)
                CalculateAcceptanceRangesRec(RemainingRangeX, RemainingRangeM, RemainingRangeA, NewRange, nextWorkflow, workflows, results, NewFlow)

    # for p in parts:
    #     # print("part", p)
    #     workflowName = "in"
    #     while workflowName not in ["A", "R"]:
    #         # print("workflow", workflowName)
    #         workflow = workflows[workflowName]
    #         for rule in workflow:
    #             # print("rule", rule)
    #             if rule[1] and p[rule[0]] > rule[2]:
    #                 workflowName = rule[3]
    #                 break
    #             elif not rule[1] and p[rule[0]] < rule[2]:
    #                 workflowName = rule[3]
    #                 break
    #     if workflowName == "A":
    #         AcceptanceRating += sum(p)
    pass

# Day 21
def SolveThirdDegreePolynomialCoefficients(results:list[int]) -> list[int]:
    
    # f(x) = ax^2 + bx + c

    # u = a + b + c
    # v = 4a + 2b + c
    # w = 9a + 3b + c

    # a = u - b - c

    # v = 4*(u-b-c) + 2b + c
    # v = 4u-4b-4c + 2b + c
    # v = 4u - 2b - 3c
    # 2b = 4u - 3c - v
    # b = 2u - 1.5c - 0.5v

    # w = 9a + 3b + c
    # w = 9*(u - b - c) + 3b + c
    # w = 9*(u - (2u - 1.5c - 0.5v) - c) + 3*(2u - 1.5c - 0.5v) + c
    # w = 9*(u - 2u + 1.5c + 0.5v - c) + 6u - 4.5c - 1.5v + c
    # w = 9u - 18u + 13.5c + 4.5v - 9c + 6u - 4.5c - 1.5v + c
    # w = 9u - 18u + 6u + 13.5c - 9c - 4.5c + c + 4.5v - 1.5v
    # w = - 3u + c + 3v
    # c = w + 3u - 3v

    # b = 2u - 1.5*(w + 3u - 3v) - 0.5v
    # b = 2u - 1.5w - 4.5u + 4.5v - 0.5v
    # b = -2.5u - 1.5w + 4v

    # a = u - b - c
    # a = u - (-2.5u - 1.5w + 4v) - (w + 3u - 3v)
    # a = u + 2.5u + 1.5w - 4v - w - 3u + 3v
    # a = 0.5u + 0.5w - 1v

    u = results[0]
    v = results[1]
    w = results[2]

    coefficients = []
    coefficients.append(0.5 * u + 0.5 * w - v)
    coefficients.append(-2.5 * u - 1.5 * w + 4 * v)
    coefficients.append(w + 3 * u - 3 * v)

    return coefficients

# Day 23
def FindLongestHikeTrailRec(map:list[str], currentX:int, currentY:int, Visited:set[tuple], bIgnoreSlopes:bool, last = (0, 0)) -> int:
    
    mapTile = map[currentY][currentX]
    if mapTile == "#":
        return -1
    
    if currentY == len(map) - 1:
        return 0

    CurrentPos = (currentX, currentY)
    if CurrentPos in Visited:
        return -1
                
    NewVisited = copy(Visited)
    NewVisited.add(CurrentPos)
    
    if mapTile == "." or bIgnoreSlopes:
        PossibleSteps = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    elif mapTile == "^":
        PossibleSteps = [(0, -1)]
    elif mapTile == ">":
        PossibleSteps = [(1, 0)]
    elif mapTile == "v":
        PossibleSteps = [(0, 1)]
    elif mapTile == "<":
        PossibleSteps = [(-1, 0)]

    options = []
    for step in PossibleSteps:
        x = currentX + step[0]
        y = currentY + step[1]
        options.append(1 + FindLongestHikeTrailRec(map, x, y, NewVisited, bIgnoreSlopes, CurrentPos))
    
    # if len([x for x in options if x > 0]) > 1:
    #     print(currentX, currentY, options)
        
    result = max(options)
    if result > 0:
        return result
    else:
        return -1