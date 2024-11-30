from ProgressBar import ProgressBar
import collections
import copy
import numpy as np
import time
import ast
import math
from itertools import combinations, permutations, repeat, groupby
import operator
import re

def day1(input, Pbar: ProgressBar):
    
    Pbar.StartPuzzle1(len(input))

    calibrationValues: list[int] = []
    pattern = r'[a-z]'
    line: str
    for line in input:
        digits = re.sub(pattern, '', line)
        calibrationValues.append(int(digits[0]+digits[-1]))
        Pbar.IncrementProgress()
        
    Pbar.StartPuzzle2(len(input))
    calibrationValues2: list[int] = []
    parser:dict = {'one':1, 'two':2, 'three':3,'four':4, 'five':5,'six':6,'seven':7,'eight':8,'nine':9}
    
    for line in input:
        digits = re.findall(r'(?=(one|two|three|four|five|six|seven|eight|nine|[1-9]))', line)
        first:str = digits[0]
        last:str = digits[-1]
        if not first.isnumeric():
            first = parser[first]
        if not last.isnumeric():
            last = parser[last]
        
        calibrationValues2.append(10 * int(first) + int(last))
        # print(line, first, last, calibrationValues2[-1])
        Pbar.IncrementProgress()

    Pbar.FinishPuzzle2()

    return sum(calibrationValues), sum(calibrationValues2)

def day2(input, Pbar: ProgressBar):
    
    sumIDs = 0
    sumPowers = 0
    for line in input:
        bIsPossible = True
        minRed = 0
        minGreen = 0
        minBlue = 0
        ID = int(re.findall('(\d+):', line)[0])

        pulls = line.split(';')
        for pull in pulls:
            NumBlue = re.findall('(\d+) blue', pull)
            NumBlue = int(NumBlue[0]) if NumBlue else 0
            NumRed = re.findall('(\d+) red', pull)
            NumRed = int(NumRed[0]) if NumRed else 0
            NumGreen = re.findall('(\d+) green', pull)
            NumGreen = int(NumGreen[0]) if NumGreen else 0
            
            if NumRed > 12 or NumGreen > 13 or NumBlue > 14:
                bIsPossible = False

            #puzzle 2
            minRed = max(minRed,NumRed)
            minGreen = max(minGreen,NumGreen)
            minBlue = max(minBlue,NumBlue)
        
        if bIsPossible:
            sumIDs += ID

        sumPowers += minRed * minGreen * minBlue
    
    
    Pbar.StartPuzzle1(0)
    Pbar.StartPuzzle2(0)
    Pbar.FinishPuzzle2()

    return sumIDs, sumPowers

def day3(input, Pbar: ProgressBar):
    Pbar.StartPuzzle1(len(input))

    PartNumberSum = 0
    Gears:dict[tuple,list] = {}
    for i in range(len(input)):
        
        for match in re.finditer('\d+', input[i]):
            #symbol search ranges
            minX = max(0, match.start() - 1)
            maxX = match.end()
            minY = max(0, i - 1)
            maxY = min(len(input) - 1, i + 1)
            PartNumber = int(match.group())
            bFoundSymbol = False
            for y in range(minY, maxY + 1):
                searchstr:str = input[y][minX:maxX + 1]
                # print(searchstr)
                if not re.fullmatch('[\d.]*', searchstr):
                    bFoundSymbol = True
                    # print('Found symbol in',searchstr)
                    for gear in re.finditer('\*', searchstr):
                        gearIdx = (minX + gear.start(), y)
                        if gearIdx in Gears:
                            Gears[gearIdx].append(PartNumber)
                        else:
                            Gears[gearIdx] = [PartNumber]

            if bFoundSymbol:
                PartNumberSum += PartNumber

    Pbar.StartPuzzle2(len(input))

    GearRatioSum = 0
    for g in Gears.values():
        if len(g) == 2:
            GearRatioSum += g[0] * g[1]

    # s = "1234a"
    # print(re.fullmatch('[\d.]*', s))
    Pbar.FinishPuzzle2()

    return PartNumberSum, GearRatioSum

def day4(input, Pbar: ProgressBar):
    
    Pbar.StartPuzzle1(len(input))
    TotalWorth = 0
    WonCards:dict[int,int] = {}
    TotalCardCount = 0
    for line in input:
        CardNumber = int(re.search('(\d+):', line).group(1))
        CardCount = WonCards.get(CardNumber, 0) + 1 # Total count I have won of this card
        TotalCardCount += CardCount
        line = line.split(':')[1]
        winningNumbers = {int(m.group()) for m in re.finditer('\d+', line.split('|')[0])}
        numbers = {int(m.group()) for m in re.finditer('\d+', line.split('|')[1])}
        NumMatches = len(winningNumbers.intersection(numbers))
        if NumMatches > 0:
            TotalWorth += pow(2, NumMatches - 1)
        #puzzle 2

        for i in range(1, NumMatches + 1):
            if CardNumber + i in WonCards:
                WonCards[CardNumber+i] += CardCount
            else:
                WonCards[CardNumber+i] = CardCount

    Pbar.StartPuzzle2(0)
    Pbar.FinishPuzzle2()

    return TotalWorth, TotalCardCount

def day5(input:list[str], Pbar: ProgressBar):
    from HelperFunctions import ConvertNumber,ConvertNumberRangeRec
    
    seeds:list = [int(x) for x in re.findall('\d+', input[0])]    
    emptyLines:list = [i for i in range(len(input)) if len(input[i]) == 0]

    SeedToSoil:list[tuple[int]] = [[int(x) for x in re.findall('\d+', line)] for line in input[emptyLines[0] + 2 : emptyLines[1]]]
    SoilToFertilizer:list[tuple[int]] = [[int(x) for x in re.findall('\d+', line)] for line in input[emptyLines[1] + 2 : emptyLines[2]]]
    FertilizerToWater:list[tuple[int]] = [[int(x) for x in re.findall('\d+', line)] for line in input[emptyLines[2] + 2 : emptyLines[3]]]
    WaterToLight:list[tuple[int]] = [[int(x) for x in re.findall('\d+', line)] for line in input[emptyLines[3] + 2 : emptyLines[4]]]
    LightToTemperature:list[tuple[int]] = [[int(x) for x in re.findall('\d+', line)] for line in input[emptyLines[4] + 2 : emptyLines[5]]]
    TemperatureToHumidity:list[tuple[int]] = [[int(x) for x in re.findall('\d+', line)] for line in input[emptyLines[5] + 2 : emptyLines[6]]]
    HumidityToLocation:list[tuple[int]] = [[int(x) for x in re.findall('\d+', line)] for line in input[emptyLines[6] + 2 :]]

    Pbar.StartPuzzle1(len(seeds))

    Locations:list[int] = []
    for s in seeds:
        
        Locations.append(ConvertNumber(ConvertNumber(ConvertNumber(ConvertNumber(ConvertNumber(ConvertNumber(ConvertNumber(s, SeedToSoil), SoilToFertilizer), FertilizerToWater), WaterToLight), LightToTemperature), TemperatureToHumidity), HumidityToLocation))

        Pbar.IncrementProgress()
    
    Pbar.StartPuzzle2(7)

    SeedRanges = [(seeds[i], seeds[i+1]) for i in range(0, len(seeds), 2)]
    SoilRanges:list[tuple] = []
    FertRanges:list[tuple] = []
    WaterRanges:list[tuple] = []
    LightRanges:list[tuple] = []
    TempRanges:list[tuple] = []
    HumidRanges:list[tuple] = []
    LocationRanges:list[tuple] = []
    for r in SeedRanges:
        SoilRanges += ConvertNumberRangeRec(r[0], r[1], SeedToSoil)
    for r in SoilRanges:
        FertRanges += ConvertNumberRangeRec(r[0], r[1], SoilToFertilizer)
    for r in FertRanges:
        WaterRanges += ConvertNumberRangeRec(r[0], r[1], FertilizerToWater)
    for r in WaterRanges:
        LightRanges += ConvertNumberRangeRec(r[0], r[1], WaterToLight)
    for r in LightRanges:
        TempRanges += ConvertNumberRangeRec(r[0], r[1], LightToTemperature)
    for r in TempRanges:
        HumidRanges += ConvertNumberRangeRec(r[0], r[1], TemperatureToHumidity)
    for r in HumidRanges:
        LocationRanges += ConvertNumberRangeRec(r[0], r[1], HumidityToLocation)

    Pbar.FinishPuzzle2()

    return min(Locations), min([x[0] for x in LocationRanges])

def day6(input:list[str], Pbar: ProgressBar):

    Times:list[int] = [int(x) for x in re.findall('\d+', input[0])]
    Records:list[int] = [int(x) for x in re.findall('\d+', input[1])]
    
    Pbar.StartPuzzle1(sum(Times))

    WinningScenarios:list[int] = [0] * len(Times)
    for race in range(len(Times)):
        time = Times[race]
        record = Records[race]
        for i in range(time):
            distance = i * (time - i)
            if distance > record:
                WinningScenarios[race] += 1

    Pbar.StartPuzzle2(0)
    time = int(re.search('\d+', input[0].replace(' ', '')).group())
    record = int(re.search('\d+', input[1].replace(' ', '')).group())
    
    FirstWin:int = -1
    LastWin:int = -1
    for i in range(0, time, int(time / 100)):
        distance = i * (time - i)
        if distance > record:
            if FirstWin < 0:
                FirstWin = i
            else:
                LastWin = i
    while True:
        i = FirstWin - 1
        distance = i * (time - i)
        if distance > record:
            FirstWin = i
        else:
            break
    while True:
        i = LastWin + 1
        distance = i * (time - i)
        if distance > record:
            LastWin = i
        else:
            break
            
    WinningScenarios2:int = LastWin - FirstWin + 1

    Pbar.FinishPuzzle2()

    return np.prod(WinningScenarios), WinningScenarios2

def day7(input:list[str], Pbar: ProgressBar):
    from HelperClasses import CamelCardHand
    
    Pbar.StartPuzzle1(len(input))

    OrderedHands:list[CamelCardHand] = []
    for line in input:
        Hand:CamelCardHand = CamelCardHand(line, False)
        bInserted = False
        for i in range(len(OrderedHands)):
            if OrderedHands[i].IsHigher(Hand):
                OrderedHands.insert(i, copy.copy(Hand))
                bInserted = True
                break
        if not bInserted:
            OrderedHands.append(copy.copy(Hand))

        Pbar.IncrementProgress()
    
    TotalWinnings = 0
    for i in range(len(OrderedHands)):
        TotalWinnings += (i + 1) * OrderedHands[i].Bid

    Pbar.StartPuzzle2(len(input))
    OrderedHands.clear()
    for line in input:
        Hand:CamelCardHand = CamelCardHand(line, True)
        bInserted = False
        for i in range(len(OrderedHands)):
            if OrderedHands[i].IsHigher(Hand):
                OrderedHands.insert(i, copy.copy(Hand))
                bInserted = True
                break
        if not bInserted:
            OrderedHands.append(copy.copy(Hand))

        Pbar.IncrementProgress()

    TotalWinningsJokers = 0
    for i in range(len(OrderedHands)):
        TotalWinningsJokers += (i + 1) * OrderedHands[i].Bid

    Pbar.FinishPuzzle2()

    return TotalWinnings, TotalWinningsJokers

def day8(input:list[str], Pbar: ProgressBar):
    from HelperClasses import NodeSolver
    Pbar.StartPuzzle1(0)
    
    Instructions:list[bool] = [x == 'R' for x in input[0]]
    NumInstructions:int = len(Instructions)
    for i in range(2, len(input)):
        nodes = re.findall('[A-Z12]+', input[i])
        NodeSolver.Network[nodes[0]] = (nodes[1], nodes[2])

    NumSteps:int = 0
    Solver:NodeSolver = NodeSolver('AAA')
    while not Solver.IsSolved():
        CurrentInstruction = Instructions[NumSteps % NumInstructions]
        Solver.Step(CurrentInstruction)
        NumSteps += 1
    
    Pbar.StartPuzzle2(0)

    Solvers:list[NodeSolver] = []
    for node in NodeSolver.Network:
        if re.match('..A$', node):
            Solvers.append(NodeSolver(node))

    LoopLengths:list[np.int64] = []
    RemainingSolvers:list[int] = [x for x in range(len(Solvers))]
    NumSteps2:int = 0
    while len(RemainingSolvers) > 0:
        InstructionIndex = NumSteps2 % NumInstructions
        CurrentInstruction = Instructions[InstructionIndex]
        NumSteps2 += 1
        ToBeRemoved = []
        for i in RemainingSolvers:
            Solvers[i].Step(CurrentInstruction)
            if Solvers[i].IsSolved2():
                ToBeRemoved.append(i)
                LoopLengths.append(NumSteps2)
        for i in ToBeRemoved:            
            RemainingSolvers.remove(i)

    Solution2:np.int64 = np.lcm.reduce(LoopLengths, dtype=object)

    Pbar.FinishPuzzle2()

    return NumSteps, Solution2

def day9(input:list[str], Pbar: ProgressBar):
    
    Pbar.StartPuzzle1(len(input))

    TotalExtrapolatedValues = 0
    TotalHistoryValues = 0 # puzzle 2
    for line in input:
        sequences:list[list[int]] = []
        sequences.append([int(x) for x in re.findall('-?\d+', line)])

        while True:
            lastSequence = sequences[-1]
            sequences.append([])
            bOnlyZeros:bool = True
            for i in range(len(lastSequence) - 1):
                diff = lastSequence[i+1] - lastSequence[i]
                sequences[-1].append(diff)
                if diff:
                    bOnlyZeros = False
            if bOnlyZeros:
                break

        nextValue = 0
        historyValue = 0 # puzzle 2
        for i in reversed(range(len(sequences) - 1)):
            nextValue += sequences[i][-1]
            historyValue = sequences[i][0] - historyValue
        TotalExtrapolatedValues += nextValue
        TotalHistoryValues += historyValue


    Pbar.IncrementProgress()
    Pbar.StartPuzzle2(0)
    Pbar.FinishPuzzle2()

    return TotalExtrapolatedValues, TotalHistoryValues

def day10(input:list[str], Pbar: ProgressBar):
    
    Pbar.StartPuzzle1(0)

    StartPos:tuple = (-1, -1)
    for y in range(len(input)):
        x = input[y].find('S')
        if x >= 0:
            StartPos = (x, y)
            break
    
    pos = StartPos
    Loop:list[tuple] = [pos]
    dir = 0 #direction current position was entered; 0 up, 1 right, 2 down, 3 left
    # determine first loop tile
    StartConnections = []
    nPos = (StartPos[0], StartPos[1] - 1)
    neighbor = input[nPos[1]][nPos[0]]
    if neighbor == '|' or neighbor == 'F' or neighbor == '7':
        StartConnections.append(0)
        pos = nPos
        dir = 0
    nPos = (StartPos[0] + 1, StartPos[1])
    neighbor = input[nPos[1]][nPos[0]]
    if neighbor == '-' or neighbor == '7' or neighbor == 'J':
        StartConnections.append(1)
        pos = nPos
        dir = 1
    nPos = (StartPos[0], StartPos[1] + 1)
    neighbor = input[nPos[1]][nPos[0]]
    if neighbor == '|' or neighbor == 'J' or neighbor == 'L':
        StartConnections.append(2)
        pos = nPos
        dir = 2
    nPos = (StartPos[0] - 1, StartPos[1])
    neighbor = input[nPos[1]][nPos[0]]
    if neighbor == '-' or neighbor == 'F' or neighbor == 'L':
        StartConnections.append(3)
        pos = nPos
        dir = 3

    StartTile = ''
    if 0 in StartConnections and 1 in StartConnections:
        StartTile = 'L'
    elif 0 in StartConnections and 2 in StartConnections:
        StartTile = '|'
    elif 0 in StartConnections and 3 in StartConnections:
        StartTile = 'J'
    elif 1 in StartConnections and 2 in StartConnections:
        StartTile = 'F'
    elif 1 in StartConnections and 3 in StartConnections:
        StartTile = '-'
    elif 2 in StartConnections and 3 in StartConnections:
        StartTile = '7'
    else:
        print("Invalid start tile detected!")

    while True:
        Loop.append(pos)
        CurrentTile = input[pos[1]][pos[0]]
        if CurrentTile == '-':
            if dir == 1:
                pos = (pos[0] + 1, pos[1])
            else:
                pos = (pos[0] - 1, pos[1])
            pass
        elif CurrentTile == '|':
            if dir == 0:
                pos = (pos[0], pos[1] - 1)
            else:
                pos = (pos[0], pos[1] + 1)
            pass
        elif CurrentTile == '7':
            if dir == 1:
                dir = 2
                pos = (pos[0], pos[1] + 1)
            else:
                dir = 3
                pos = (pos[0] - 1, pos[1])
            pass
        elif CurrentTile == 'J':
            if dir == 1:
                dir = 0
                pos = (pos[0], pos[1] - 1)
            else:
                dir = 3
                pos = (pos[0] - 1, pos[1])
            pass
        elif CurrentTile == 'L':
            if dir == 2:
                dir = 1
                pos = (pos[0] + 1, pos[1])
            else:
                dir = 0
                pos = (pos[0], pos[1] - 1)
            pass
        elif CurrentTile == 'F':
            if dir == 0:
                dir = 1
                pos = (pos[0] + 1, pos[1])
            else:
                dir = 2
                pos = (pos[0], pos[1] + 1)
            pass
        if pos == StartPos:
            break
        
    FarthestDistance = len(Loop) // 2

    SizeX = len(input[0])
    SizeY = len(input)

    Pbar.StartPuzzle2(SizeX * SizeY)

    LoopSet:set = set(Loop)
    # find all tiles outside the loop
    OutsideTiles:set[tuple] = set()
    HandledLoopTiles:set[tuple] = set()
    Candidates:set[tuple] = set() # 3rd tuple index indicates which direction is outide the loop: 0 up, 1 right, 2 down, 3 left

    for x in range(SizeX):
        Candidates.add((x, 0, 0))
        Candidates.add((x, SizeY - 1, 2))
    for y in range(SizeY):
        Candidates.add((0, y, 3))
        Candidates.add((SizeX - 1, y, 1))

    while not len(Candidates) == 0:
        NewCandidates:set[tuple] = set()
        for c in Candidates:
            x = c[0]
            y = c[1]
            dir = c[2]
            if (x, y) in OutsideTiles or (x, y) in HandledLoopTiles:
                continue
            if (x, y) in LoopSet:
                tile = input[y][x]
                if tile == 'S':
                    tile = StartTile
                if tile == 'F':
                    if dir == 0 or dir == 3:
                        NewCandidates.add((x, y-1, 2, x, y))
                        NewCandidates.add((x-1, y, 1, x, y))
                        NewCandidates.add((x+1, y, 0, x, y))
                        NewCandidates.add((x, y+1, 3, x, y))
                    elif dir == 1 or dir == 2:
                        NewCandidates.add((x+1, y, 2, x, y))
                        NewCandidates.add((x, y+1, 1, x, y))
                elif tile == 'J':
                    if dir == 0 or dir == 3:
                        NewCandidates.add((x, y-1, 3, x, y))
                        NewCandidates.add((x-1, y, 0, x, y))
                    elif dir == 1 or dir == 2:
                        NewCandidates.add((x+1, y, 3, x, y))
                        NewCandidates.add((x, y+1, 0, x, y))
                        NewCandidates.add((x, y-1, 1, x, y))
                        NewCandidates.add((x-1, y, 2, x, y))
                elif tile == 'L':
                    if dir == 0 or dir == 1:
                        NewCandidates.add((x, y-1, 1, x, y))
                        NewCandidates.add((x+1, y, 0, x, y))
                    elif dir == 2 or dir == 3:
                        NewCandidates.add((x, y+1, 0, x, y))
                        NewCandidates.add((x-1, y, 1, x, y))
                        NewCandidates.add((x, y-1, 3, x, y))
                        NewCandidates.add((x+1, y, 2, x, y))
                elif tile == '7':
                    if dir == 0 or dir == 1:
                        NewCandidates.add((x, y-1, 2, x, y))
                        NewCandidates.add((x+1, y, 3, x, y))
                        NewCandidates.add((x-1, y, 0, x, y))
                        NewCandidates.add((x, y+1, 1, x, y))
                    elif dir == 2 or dir == 3:
                        NewCandidates.add((x, y+1, 3, x, y))
                        NewCandidates.add((x-1, y, 2, x, y))
                elif tile == '|':
                    if dir == 1:
                        NewCandidates.add((x, y-1, 1, x, y))
                        NewCandidates.add((x, y+1, 1, x, y))
                    elif dir == 3:
                        NewCandidates.add((x, y-1, 3, x, y))
                        NewCandidates.add((x, y+1, 3, x, y))
                    else:
                        print("Invalid Candidate:", x, y, dir)
                elif tile == '-':
                    if dir == 0:
                        NewCandidates.add((x-1, y, 0, x, y))
                        NewCandidates.add((x+1, y, 0, x, y))
                    elif dir == 2:
                        NewCandidates.add((x-1, y, 2, x, y))
                        NewCandidates.add((x+1, y, 2, x, y))
                    else:
                        print("Invalid Candidate:", x, y, dir)                            

                HandledLoopTiles.add((x, y))
                continue
            
            OutsideTiles.add((x, y))
            NewCandidates.add((x - 1, y, 1))
            NewCandidates.add((x + 1, y, 3))
            NewCandidates.add((x, y - 1, 2))
            NewCandidates.add((x, y + 1, 0))

        Candidates.clear()
        for n in NewCandidates:
            if n[0] > 0 and n[0] < SizeX and n[1] > 0 and n[1] < SizeY:
                Candidates.add(n)

    # for y in range(SizeY):
    #     OutputString:str = ""
    #     for x in range(SizeX):
    #         pos = (x, y)
    #         if pos in OutsideTiles:
    #             OutputString += "O"
    #         elif pos in LoopSet:
    #             OutputString += input[y][x]
    #         else:
    #             OutputString += "I"
    #     print(OutputString)

    NumEnclosedTiles = SizeX * SizeY - len(LoopSet) - len(OutsideTiles)

    Pbar.FinishPuzzle2()

    return FarthestDistance, NumEnclosedTiles

def day11(input:list[str], Pbar: ProgressBar):
    
    Pbar.StartPuzzle1(0)

    emptyRows:set[int] = set()
    emptyColumns:set[int] = set()

    for row in range(len(input)):
        line = input[row]
        if re.fullmatch('\.*', line):
            emptyRows.add(row)
    for column in range(len(input[0])):
        bIsEmpty = True
        for row in input:
            if row[column] != '.':
                bIsEmpty = False
                break
        if bIsEmpty:
            emptyColumns.add(column)
    
    galaxies:list[tuple] = []
    for y in range(len(input)):
        for x in range(len(input[y])):
            if input[y][x] == '#':
                galaxies.append((x, y))

    shortestPathsSum = 0
    shortestPaths2 = 0
    for pair in combinations(galaxies, 2):
        x1 = pair[0][0]
        x2 = pair[1][0]
        y1 = pair[0][1]
        y2 = pair[1][1]
        crossedColumns = set(range(min(x1, x2), max(x1, x2)))
        crossedRows = set(range(min(y1, y2), max(y1, y2)))
        expansionX = len(crossedColumns.intersection(emptyColumns))
        expansionY = len(crossedRows.intersection(emptyRows))
        distanceX = abs(x1 - x2)
        distanceY = abs(y1 - y2)

        # print(pair, distanceX, distanceY, expansionX, expansionY)

        shortestPathsSum += distanceX + distanceY + expansionX + expansionY
        shortestPaths2 += distanceX + distanceY + (expansionX + expansionY) * 999999

    Pbar.StartPuzzle2(0)
    Pbar.FinishPuzzle2()

    return shortestPathsSum, shortestPaths2

def day12(input:list[str], Pbar: ProgressBar):
    from HelperFunctions import CalculatePossibleArrangementsRec
    
    Pbar.StartPuzzle1(len(input))

    PossibleArrangements = 0
    for line in input:
        record = re.match('[\?#\.]*', line).group()
        groups = [int(x) for x in line.split(' ')[1].split(',')]
        MemoCache:dict[str,int] = {}
        PossibleArrangements += CalculatePossibleArrangementsRec(record, groups, 0, MemoCache)
        Pbar.IncrementProgress()

    Pbar.StartPuzzle2(len(input))

    PossibleArrangements2 = 0
    for line in input:
        record = re.match('[\?#\.]*', line).group()
        groups = [int(x) for x in line.split(' ')[1].split(',')]
        record += 4* ("?" + record)
        groups *= 5

        MemoCache:dict[str,int] = {}
        PossibleArrangements2 += CalculatePossibleArrangementsRec(record, groups, 0, MemoCache)
        Pbar.IncrementProgress()

    Pbar.FinishPuzzle2()

    return PossibleArrangements, PossibleArrangements2

def day13(input:list[str], Pbar: ProgressBar):
    

    blocks = [block for block in [list(group) for k, group in groupby(input, lambda x: x == '')] if len(block) > 1]
    Pbar.StartPuzzle1(len(blocks))

    Sum = 0
    b = 0
    for rows in blocks:
        # find horizontal reflection lines
        for i in range(0, len(rows) - 1):
            reflects = True
            for j in range(min(i + 1, len(rows) - i - 1)):
                # print(i, j)
                if rows[i-j] != rows[i+j+1]:
                    reflects = False
                    break
            if reflects:
                # print("reflection row found at index", i)
                Sum += 100 * (i + 1)

        # find vertical reflection lines
        columns = [''.join([row[c] for row in rows]) for c in range(len(rows[0]))]
        for i in range(0, len(columns) - 1):
            reflects = True
            for j in range(min(i + 1, len(columns) - i - 1)):
                if columns[i-j] != columns[i+j+1]:
                    reflects = False
                    break
            if reflects:
                # print("reflection column found at index", i)
                Sum += i + 1
        
        Pbar.IncrementProgress()

    Pbar.StartPuzzle2(len(blocks))
    Sum2 = 0
    for rows in blocks:
        # find horizontal reflection lines
        rowlength =  len(rows[0])
        for i in range(0, len(rows) - 1):
            smudges = 0
            for j in range(min(i + 1, len(rows) - i - 1)):
                # print(i, j)
                smudges += sum([1 for x in range(rowlength) if rows[i-j][x] != rows[i+j+1][x]])
                if smudges > 1:
                    break
            if smudges == 1:
                # print("reflection row found at index", i)
                Sum2 += 100 * (i + 1)

        # find vertical reflection lines
        columns = [''.join([row[c] for row in rows]) for c in range(len(rows[0]))]
        columnlength = len(columns[0])
        for i in range(0, len(columns) - 1):
            smudges = 0
            for j in range(min(i + 1, len(columns) - i - 1)):
                smudges += sum([1 for x in range(columnlength) if columns[i-j][x] != columns[i+j+1][x]])
                if smudges > 1:
                    break
            if smudges == 1:
                # print("reflection column found at index", i)
                Sum2 += i + 1
        
        Pbar.IncrementProgress()

    Pbar.FinishPuzzle2()

    return Sum, Sum2

def day14(input:list[str], Pbar: ProgressBar):
    from itertools import product
    
    platform:dict[tuple,str] = {}
    stones:set[tuple] = set()
    rocks:set[tuple] = set()
    for x, y in product(range(len(input[0])), range(len(input))):
        if input[y][x] == "O":
            stones.add((x, y))
        elif input[y][x] == "#":
            rocks.add((x, y))

    Pbar.StartPuzzle1(0)
    load = 0
    numrows = len(input)
    numColumns = len(input[0])

    oldStones = copy.copy(stones)
    for (x, y) in oldStones:
        testRow, newRow = y, y
        while testRow > 0:
            coords = (x, testRow - 1)
            if coords in rocks:
                break
            elif coords in stones:
                testRow -= 1
            else:
                testRow -= 1
                newRow = testRow
        stones.remove((x, y))
        stones.add((x, newRow))
        load += numrows - newRow

    NumIterations = 1000000000
    Pbar.StartPuzzle2(NumIterations)
    coords = list(product(range(numColumns), range(numrows)))
    knownStoneConfigs:dict[frozenset, int] = {} 
    for i in range(NumIterations):
        # north
        oldStones = copy.copy(stones)
        for (x, y) in oldStones:
            testRow, newRow = y, y
            while testRow > 0:
                coords = (x, testRow - 1)
                if coords in rocks:
                    break
                elif coords in stones:
                    testRow -= 1
                else:
                    testRow -= 1
                    newRow = testRow
            stones.remove((x, y))
            stones.add((x, newRow))
        # west
        oldStones = copy.copy(stones)
        for (x, y) in oldStones:
            testCol, newCol = x, x
            while testCol > 0:
                coords = (testCol - 1, y)
                if coords in rocks:
                    break
                elif coords in stones:
                    testCol -= 1
                else:
                    testCol -= 1
                    newCol = testCol
            stones.remove((x, y))
            stones.add((newCol, y))
        # south
        oldStones = copy.copy(stones)
        for (x, y) in oldStones:
            testRow, newRow = y, y
            while testRow + 1 < numrows:
                coords = (x, testRow + 1)
                if coords in rocks:
                    break
                elif coords in stones:
                    testRow += 1
                else:
                    testRow += 1
                    newRow = testRow
            stones.remove((x, y))
            stones.add((x, newRow))
        # east
        oldStones = copy.copy(stones)
        for (x, y) in oldStones:
            testCol, newCol = x, x
            while testCol + 1 < numColumns:
                coords = (testCol + 1, y)
                if coords in rocks:
                    break
                elif coords in stones:
                    testCol += 1
                else:
                    testCol += 1
                    newCol = testCol
            stones.remove((x, y))
            stones.add((newCol, y))

        # Pbar.IncrementProgress()
        
        stoneConfig = frozenset(stones)
        if stoneConfig in knownStoneConfigs:
            cycleLength = i - knownStoneConfigs[stoneConfig]
            if (NumIterations - 1 - i) % cycleLength == 0:
                break
        knownStoneConfigs[stoneConfig] = i

    load2 = sum([numrows - y for (x, y) in stones])
    Pbar.FinishPuzzle2()

    return load, load2

def day15(input:list[str], Pbar: ProgressBar):
    from HelperFunctions import Hash
    
    sequence:list[str] = input[0].split(',')
    Pbar.StartPuzzle1(len(sequence))
    verificationNumber = 0
    for s in sequence:
        verificationNumber += Hash(s)

    Pbar.StartPuzzle2(len(sequence))

    boxes:list[dict[str,tuple]] = [{} for i in range(256)]

    for s in sequence:
        label = re.match("[a-z]+", s).group()
        box:dict[str,tuple] = boxes[Hash(label)]
        operation = s[len(label)]
        if operation == '-':
            if label in box:
                removedLens = box.pop(label)
                for k,v in box.items():
                    if v[0] > removedLens[0]:
                        box[k] = (v[0] - 1, v[1])
        else:
            focal = int(s[len(label)+1:])
            if label in box:
                box[label] = (box[label][0], focal)
            else:
                box[label] = (len(box), focal)
            pass
    
    power = 0
    for i in range(256):
        box = boxes[i]
        for k,v in box.items():
            power += (i + 1) * (v[0] + 1) * v[1]

    Pbar.FinishPuzzle2()

    return verificationNumber, power

def day16(input:list[str], Pbar: ProgressBar):
    from HelperFunctions import CalcEnergizedTiles
    
    Pbar.StartPuzzle1(0)
    tiles = CalcEnergizedTiles(input, (0, 0, 1))

    width = len(input[0])
    height = len(input)
    Pbar.StartPuzzle2(width + height)

    maxTiles = 0
    for x in range(width):
        maxTiles = max(maxTiles, CalcEnergizedTiles(input, (x, 0, 2)), CalcEnergizedTiles(input, (x, height - 1, 0)))
        Pbar.IncrementProgress()
    for y in range(height):
        maxTiles = max(maxTiles, CalcEnergizedTiles(input, (0, y, 1)), CalcEnergizedTiles(input, (width - 1, y, 3)))
        Pbar.IncrementProgress()

    Pbar.FinishPuzzle2()

    return tiles, maxTiles

def day17(input:list[str], Pbar: ProgressBar):
    
    Pbar.StartPuzzle1(0)

    width = len(input[0])
    height = len(input)
    startHeat = -int(input[0][0])
    Candidates:dict[int,tuple] = {}
    Candidates[startHeat] = [(0, 0, 1, 0)]
    Visited:set[tuple] = set()

    currentHeatLoss = startHeat
    while True:
        while currentHeatLoss not in Candidates:
            currentHeatLoss += 1
        CurrentCandidates = Candidates.pop(currentHeatLoss)
        for c in CurrentCandidates:
            x = c[0]
            y = c[1]
            dir = c[2]
            streak = c[3]
            NewHeatloss = currentHeatLoss + int(input[y][x])

            key:tuple = (x, y, dir, streak)
            if key in Visited:
                continue
            Visited.add(key)

            if x == width - 1 and y == height - 1:
                leastPossibleHeatloss = NewHeatloss
                break
            
            # print(x, y, heatloss)

            for i in [0, -1, 1] if streak < 3 else [-1, 1]:
                NewDir = (dir + i + 4) % 4
                if NewDir == 0:
                    NewX = x
                    NewY = y - 1
                elif NewDir == 1:
                    NewX = x + 1
                    NewY = y
                elif NewDir == 2:
                    NewX = x
                    NewY = y + 1
                elif NewDir == 3:
                    NewX = x - 1
                    NewY = y
                NewStreak = streak + 1 if i == 0 else 1
                

                if NewX < 0 or NewX >= width or NewY < 0 or NewY >= height:
                    continue
                if (NewX, NewY, NewDir, NewStreak) in Visited:
                    continue

                NewCandidate = (NewX, NewY, NewDir, NewStreak)
                if NewHeatloss in Candidates:
                    Candidates[NewHeatloss].append(NewCandidate)
                else:
                    Candidates[NewHeatloss] = [NewCandidate]
        else:
            continue
        break

    Pbar.StartPuzzle2(0)

    Candidates:dict[int,tuple] = {}
    Candidates[startHeat] = [(0, 0, 1, 0)]
    Visited:set[tuple] = set()

    currentHeatLoss = startHeat
    while True:
        while currentHeatLoss not in Candidates:
            currentHeatLoss += 1
        CurrentCandidates = Candidates.pop(currentHeatLoss)
        for c in CurrentCandidates:
            x = c[0]
            y = c[1]
            dir = c[2]
            streak = c[3]
            NewHeatloss = currentHeatLoss + int(input[y][x])

            key:tuple = (x, y, dir, streak)
            if key in Visited:
                continue
            Visited.add(key)

            if x == width - 1 and y == height - 1 and streak >= 4:
                solution2 = NewHeatloss
                break
            
            # print(x, y, heatloss)

            DirectionChanges = [-1, 0 , 1]
            if streak < 4:
                DirectionChanges = [0]
            elif streak == 10:
                DirectionChanges = [-1, 1]
            for i in DirectionChanges:
                NewDir = (dir + i + 4) % 4
                if NewDir == 0:
                    NewX = x
                    NewY = y - 1
                elif NewDir == 1:
                    NewX = x + 1
                    NewY = y
                elif NewDir == 2:
                    NewX = x
                    NewY = y + 1
                elif NewDir == 3:
                    NewX = x - 1
                    NewY = y
                NewStreak = streak + 1 if i == 0 else 1
                

                if NewX < 0 or NewX >= width or NewY < 0 or NewY >= height:
                    continue
                if (NewX, NewY, NewDir, NewStreak) in Visited:
                    continue

                NewCandidate = (NewX, NewY, NewDir, NewStreak)
                if NewHeatloss in Candidates:
                    Candidates[NewHeatloss].append(NewCandidate)
                else:
                    Candidates[NewHeatloss] = [NewCandidate]
        else:
            continue
        break


    Pbar.FinishPuzzle2()

    return leastPossibleHeatloss, solution2

def day18(input:list[str], Pbar: ProgressBar):
    from HelperFunctions import IsInside
    from itertools import product
    
    Pbar.StartPuzzle1(0)
    vertices:list[tuple] = []
    x = 0
    y = 0
    trenchlength = 0
    for line in input:
        s = line.split(" ")
        dir = s[0]
        num = int(s[1])
        color = s[2].strip("()#")
        # print(dir, num, color)

        vertices.append((x, y))
        if dir == "U":
            y += num
        elif dir == "D":
            y -= num
        elif dir == "R":
            x += num
        elif dir == "L":
            x -= num
        trenchlength += num

    TotalArea = 0
    for i in range(len(vertices)):
        v0 = (0, 0)
        v1 = vertices[i]
        v2 = vertices[i-1]
        area = 0.5 * (v1[0] * v2[1] - v1[1] * v2[0])
        TotalArea += area
        
    # in the 2D geometri projection every vertex lies in the center of a 1m cube
    # for straight edges exactly half a meter lies outisde of this boundary
    # for outer corners this increases to 0.75, for inner corners it is reduced to 0.25
    # a polygon always has 4 outer corners more than it has inner corners, the remaining corners average out to 0.5
    solution1 = int(TotalArea + trenchlength / 2 + 1)

    Pbar.StartPuzzle2(0)
    vertices:list[tuple] = []
    x = 0
    y = 0
    trenchlength = 0
    for line in input:
        ins = line.split(" ")[2].strip("()#")
        dir = ins[-1]
        num = int(ins[:-1], 16)

        vertices.append((x, y))
        if dir == "0":
            x += num
        elif dir == "1":
            y -= num
        elif dir == "2":
            x -= num
        elif dir == "3":
            y += num
        trenchlength += num

    TotalArea = 0
    for i in range(len(vertices)):
        v0 = (0, 0)
        v1 = vertices[i]
        v2 = vertices[i-1]
        area = 0.5 * (v1[0] * v2[1] - v1[1] * v2[0])
        TotalArea += area

    # same calculation as for part 1
    solution2 = int(TotalArea + trenchlength / 2 + 1)
    
    Pbar.FinishPuzzle2()

    return solution1, solution2

def day19(input:list[str], Pbar: ProgressBar):
    from HelperFunctions import CalculateAcceptanceRangesRec

    workflows:dict[str,list[tuple]] = {}
    parts:list[tuple] = []
    
    for line in input:
        if len(line) == 0:
            continue
        if line[0] == "{":
            parts.append([int(x) for x in re.findall('\d+', line)])
        else:
            rules = re.search('{(.*)}', line)
            name = line[:rules.start()]
            rulelist:list[tuple] = []
            for rule in rules.group(1).split(","):
                # print(rule)
                if not ":" in rule:
                    rulelist.append((0, True, 0, rule))
                else:
                    dataIndex = 0 if rule[0] == "x" else 1 if rule[0] == "m" else 2 if rule[0] == "a" else 3
                    compareGreater = rule[1] == ">"
                    value = int(re.search('\d+', rule).group())
                    target = rule.split(":")[1]
                    rulelist.append((dataIndex, compareGreater, value, target))
                    # print(dataIndex, compareGreater, value, target)
            workflows[name] = copy.copy(rulelist)
 
    AcceptanceRating = 0
    Pbar.StartPuzzle1(len(parts))
    for p in parts:
        # print("part", p)
        workflowName = "in"
        while workflowName not in ["A", "R"]:
            # print("workflow", workflowName)
            workflow = workflows[workflowName]
            for rule in workflow:
                # print("rule", rule)
                if rule[1] and p[rule[0]] > rule[2]:
                    workflowName = rule[3]
                    break
                elif not rule[1] and p[rule[0]] < rule[2]:
                    workflowName = rule[3]
                    break
        if workflowName == "A":
            AcceptanceRating += sum(p)

        Pbar.IncrementProgress()

    Pbar.StartPuzzle2(0)

    AcceptedRanges:list[tuple] = []
    CalculateAcceptanceRangesRec(range(1, 4001), range(1, 4001), range(1, 4001), range(1, 4001), "in", workflows, AcceptedRanges)
    # print(AcceptedRanges)

    RangeSets:list[list] = []
    for a in AcceptedRanges:
        RangeSets.append([])
        for r in a:
            RangeSets[-1].append(set([x for x in r]))

    TotalCombinations = 0
    for r in AcceptedRanges:
        combinations = 1
        for i in range(4):
            combinations *= len(r[i])
        # print(r, combinations)

        TotalCombinations += combinations

    Pbar.FinishPuzzle2()

    return AcceptanceRating, TotalCombinations

def day20(input:list[str], Pbar: ProgressBar):
    from HelperClasses import Module

    Pbar.StartPuzzle1(0)

    Modules:dict[str,Module] = {}

    for line in input:
        mod = Module(line)
        Modules[mod.name] = mod

    Modules["output"] = Module("output")
    Modules["rx"] = Module("rx")

    for m in Modules.values():
        for d in m.destinations:
            if d in Modules:
                Modules[d].InitConnection(m.name)

    NumLowPulses = 0
    NumHighPulses = 0
    for i in range(1000):
        pulses = [("button", "broadcaster", False)]
        while len(pulses) > 0:
            pulse = pulses.pop(0)
            # print("pulse", pulse[0], "high" if pulse[2] else "low", "->", pulse[1])
            if pulse[2]:
                NumHighPulses += 1
            else:
                NumLowPulses += 1
            
            pulses += Modules[pulse[1]].Pulse(pulse[2], pulse[0])
    result1 = NumLowPulses * NumHighPulses

    Pbar.StartPuzzle2(0)

    for m in Modules.values():
        m.Reset()
    NumPresses = 0
    CycleLengths = {}
    RxSource = Modules["rx"].source
    while True:
        NumPresses += 1
        pulses = [("button", "broadcaster", False)]
        while len(pulses) > 0:
            pulse = pulses.pop(0)         
            if pulse[2]:
                NumHighPulses += 1
            else:
                NumLowPulses += 1
            
            pulses += Modules[pulse[1]].Pulse(pulse[2], pulse[0])

            # rx will be pulsed when &lv sends a low pulse, meaning all of [st, tn, hh, dt] need to be high
            if pulse[1] == RxSource and pulse[2]:
                if pulse[0] not in CycleLengths:
                    CycleLengths[pulse[0]] = NumPresses

                    if len(CycleLengths) == len(Modules[RxSource].memory):
                        break
        else:
            continue
        break
    
    result2 = np.lcm.reduce([x for x in CycleLengths.values()], dtype=np.int64)

    Pbar.FinishPuzzle2()

    return result1, result2

def day21(input:list[str], Pbar: ProgressBar):
    from itertools import product
    from copy import copy
    from HelperFunctions import SolveThirdDegreePolynomialCoefficients
    
    Pbar.StartPuzzle1(64)
    width = len(input[0])
    height = len(input)

    Plots:set[tuple] = set()
    for x, y in product(range(width), range(height)):
        if input[y][x] == "S":
            StartPosition = (x, y)
    Plots.add(StartPosition)
    
    for i in range(64):
        NewPlots:set[tuple] = set()
        for p in Plots:
            x, y = p
            for x1, y1 in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                NewX = x + x1
                NewY = y + y1
                if NewX < 0 or NewY < 0 or NewX >= width or NewY >= height:
                    continue
                if input[NewY][NewX] == "#":
                    continue
                NewPlots.add((NewX, NewY))
            pass
        Plots = NewPlots

        Pbar.IncrementProgress()
    result1 = len(Plots)

    NumSteps = 131 * 2 + 66
    # NumSteps = 1000
    Pbar.StartPuzzle2(NumSteps)

    Neighbors:dict[tuple,list] = {}
    for x, y in product(range(width), range(height)):
        n = []
        for x1, y1 in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            newx = x  + x1
            newy = y + y1
            if input[newy % height][newx % width] != '#':
                n.append((x1, y1))
        Neighbors[(x, y)] = n

    Plots.clear()
    Plots.add(StartPosition)
    KnownOddPlots :set[tuple] = set()
    KnownEvenPlots:set[tuple] = set()
    Sequence:list[int] = []
    for i in range(NumSteps):
        NewPlots:set[tuple] = set()
        bIsEven = i % 2 == 0 # whether the currently reachable plots are after an even number of steps

        if (i - 65) % 131 == 0:
            num = len(Plots) + len(KnownEvenPlots if i % 2 == 0 else KnownOddPlots)
            Sequence.append(num)
            # print(i, (i - 65) // 131, num)

        for p in Plots:
            x, y = p
            # if (x%width, y%height) == StartPosition:
            #     print("reached mirrored start at", x, y, "at step", i)
            (KnownEvenPlots if bIsEven else KnownOddPlots).add((x, y))
            for x1, y1 in Neighbors[(x%width, y%height)]:
                NewX = x + x1
                NewY = y + y1
                if input[NewY % height][NewX % width] == "#":
                    continue
                if (NewX, NewY) in (KnownOddPlots if bIsEven else KnownEvenPlots):
                    continue

                NewPlots.add((NewX, NewY))
        Plots = NewPlots

        Pbar.IncrementProgress()

    # the plot field has a perfectly empty cross in its middle, thereby reaching a new mirrored sparting spot every 131 steps
    # since the total number of steps is 202300 * 131 + 65 this should be mappable to a function
    # f(x) -> reachable fields after x*131 + 65 steps
    # therefore puzzle solution would be f(202300)
    # Number of map squares explored: g(1) = 1; g(2) = 5; g(3) = 13; g(4) = 25
    # --> f(x) should be polynomial of 3rd degree i.e. f(x) = ax^2 + bx + c and can be solved with first 3 entries of sequence (u,v,w)
    coeffs = SolveThirdDegreePolynomialCoefficients(Sequence)
    a = int(coeffs[0])
    b = int(coeffs[1])
    c = int(coeffs[2])
    x = 202301 # needs +1 since measurements are taken for 131*0 + 65, 131*1 + 65 etc. but mapped to f(1), f(2), f(3)
    result2 = int(a * x * x + b * x + c)
    Pbar.FinishPuzzle2()

    return result1, result2

def day22(input:list[str], Pbar: ProgressBar):
    from itertools import product
    
    Pbar.StartPuzzle1(len(input))

    NumBricks = len(input)

    BlockCoords:list[list] = []
    for line in input:
        c:list[int] = [int(x) for x in re.findall('\d+', line)]
        # print(coords)
        BlockCoords.append(c)
    BlockCoords.sort(key=lambda x:x[2])
        
    FallenBricks:dict[tuple,int] = {}
    SupportingBricks:dict[int,set[int]] = {}
    for BrickID in range(NumBricks):
        x1 = BlockCoords[BrickID][0]
        y1 = BlockCoords[BrickID][1]
        z1 = BlockCoords[BrickID][2]
        x2 = BlockCoords[BrickID][3]
        y2 = BlockCoords[BrickID][4]
        z2 = BlockCoords[BrickID][5]
        for offset in range(0, min(z1, z2)):
            Supports:set[int] = set()
            for p in product(range(x1, x2+1), range(y1, y2+1), range(z1 - offset, z2+1 - offset)):
                if p in FallenBricks:
                    Supports.add(FallenBricks[p])
            if len(Supports) > 0:
                offset -= 1
                SupportingBricks[BrickID] = Supports
                break
        for p in product(range(x1, x2+1), range(y1, y2+1), range(z1 - offset, z2+1 - offset)):
            FallenBricks[p] = BrickID

    SingleSupports:set = set()
    for s in SupportingBricks.values():
        if len(s) == 1:
            SingleSupports = SingleSupports.union(s)
    solution1 = NumBricks - len(SingleSupports)

    Pbar.StartPuzzle2(NumBricks)
    SupportedBricks:dict[int,list] = {}
    for BrickID, Supports in SupportingBricks.items():
        for s in Supports:
            if s in SupportedBricks:
                SupportedBricks[s].append(BrickID)
            else:
                SupportedBricks[s] = [BrickID]

    solution2 = 0
    for i in range(NumBricks):
        FallingBricks = set()
        FallingBricks.add(i)

        if i not in SupportedBricks:
            continue

        Candidates:set = SupportedBricks[i]
        while Candidates:
            c = Candidates.pop()
            if SupportingBricks[c].issubset(FallingBricks):
                FallingBricks.add(c)
                if c not in SupportedBricks:
                    continue
                Candidates += SupportedBricks[c]
        
        solution2 += len(FallingBricks) - 1

        Pbar.IncrementProgress()
    Pbar.FinishPuzzle2()

    return solution1, solution2

def day23(input:list[str], Pbar: ProgressBar):
    from HelperFunctions import FindLongestPathRec, ReduceGraph
    from itertools import product
    
    Pbar.StartPuzzle1(0)

    StartNode = (input[0].find("."), 0)
    GoalNode = (input[-1].find("."), len(input) - 1)

    DirectionalGraph:dict[tuple,list[tuple]] = {} #  (x, y) -> (x, y, steps)
    Graph:dict[tuple,list[tuple]] = {}

    for x, y in product(range(len(input[0])), range(len(input))):
        tile = input[y][x]
        if tile == '#':
            continue
        neighbors = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        Graph[(x, y)] = []
        for n in neighbors:
            nx = x + n[0]
            ny = y + n[1]
            if ny < 0 or ny >= len(input):
                continue
            if input[ny][nx] == '#':
                continue
            Graph[(x, y)].append((nx, ny, 1))

        if tile == '>':
            neighbors = [(1, 0)]
        elif tile == '<':
            neighbors = [(-1, 0)]
        elif tile == '^':
            neighbors = [(0, -1)]
        elif tile == 'v':
            neighbors = [(0, 1)]

        DirectionalGraph[(x, y)] = []
        for n in neighbors:
            nx = x + n[0]
            ny = y + n[1]
            if ny < 0 or ny >= len(input):
                continue
            if input[ny][nx] == '#':
                continue
            DirectionalGraph[(x, y)].append((nx, ny, 1))


    MinimalNodes:set[tuple] = set([x for x in Graph if len(Graph[x]) > 2])
    MinimalNodes.add(StartNode)
    MinimalNodes.add(GoalNode)

    DirectionalGraph = ReduceGraph(DirectionalGraph, MinimalNodes)
    solution1 = FindLongestPathRec(DirectionalGraph, GoalNode, StartNode, set())

    Pbar.StartPuzzle2(pow(2, 11))
    
    Graph = ReduceGraph(Graph, MinimalNodes)
    for k,v in Graph.items():
        for node in v:
            if node[:2] == GoalNode:
                Graph[k] = [node]
                break
        else:
            continue
        break
    
    solution2 = FindLongestPathRec(Graph, GoalNode, StartNode, set(), Pbar)

    Pbar.FinishPuzzle2()

    return solution1, solution2

def day24(input:list[str], Pbar: ProgressBar):
    from HelperFunctions import FindIntersection, TestHit
    from itertools import combinations
    from numpy import linalg
    
    Pbar.StartPuzzle1(len(input) * len(input))

    lowerBound = 7
    upperBound = 27
#    lowerBound = 200000000000000
#    upperBound = 400000000000000

    hailstones:list[list] = []
    for line in input:
        hailstones.append([int(x) for x in re.findall("-?\d+", line)])
    
    numIntersections = 0
    for stone1, stone2 in combinations(hailstones, r=2):
        intersection = FindIntersection(stone1, stone2)
        if intersection[0]:
            x = intersection[1]
            y = intersection[2]
            if (lowerBound <= x <= upperBound and lowerBound <= y <= upperBound):
                numIntersections += 1
        Pbar.IncrementProgress()

    Pbar.StartPuzzle2(0)
    
    # transform all hailstones relative to stone0
    relstones = [[stone[i] - hailstones[0][i] for i in range(6)] for stone in hailstones]
    # collisions of stone 1 & 2 need to be on the same line through origin
    # thus c1 = c2 * x
    # collisions can be written based on their initial p and v, with their respective collision times being unknown
    # thus p1 + v1 * t1 = (p2 + v2 * t2) * x
    # breaking this down for all dimensions gives 3 equations to solve for x, t1, t2
    # a + b * t1 = c * x + d * t2 * x
    # by substituting y = t2 * x this gives: a + b * t1 = c * x + d * y
    # --> a = c * x + d * y - b * t1
    # with a = p1, b = v1, c = p2, d = v2

    p1 = relstones[1][:3]
    v1 = relstones[1][3:]
    p2 = relstones[2][:3]
    v2 = relstones[2][3:]
    
    sol = linalg.solve([[p2[0], v2[0], -1*v1[0]], [p2[1], v2[1], -1*v1[1]], [p2[2], v2[2], -1*v1[2]]], p1)
    x = sol[0]
    t1 = sol[2]
    t2 = sol[1] / x

    # knowing the collision times allows to compute c1 and c2 in absolute space
    c1 = [hailstones[1][i] + t1 * hailstones[1][i+3] for i in range(3)]
    c2 = [hailstones[2][i] + t2 * hailstones[2][i+3] for i in range(3)]

    velocity = [(c2[i] - c1[i]) / (t2-t1) for i in range(3)]
    stonepos = [int(c1[i] - velocity[i] * t1) for i in range(3)]

    Pbar.FinishPuzzle2()

    return numIntersections, sum(stonepos)

def day25(input:list[str], Pbar: ProgressBar):
    
    Pbar.StartPuzzle1(len(input))
    Pbar.IncrementProgress()
    Pbar.StartPuzzle2(0)
    Pbar.FinishPuzzle2()


    return -1, "Merry Christmas!"