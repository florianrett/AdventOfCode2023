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
    
    Pbar.StartPuzzle2(0)
    Pbar.FinishPuzzle2()

    return -1, -1

def day18(input:list[str], Pbar: ProgressBar):
    
    Pbar.StartPuzzle1(len(input))
    Pbar.IncrementProgress()
    Pbar.StartPuzzle2(0)
    Pbar.FinishPuzzle2()

    return -1, -1

def day19(input:list[str], Pbar: ProgressBar):
    
    Pbar.StartPuzzle1(len(input))
    Pbar.IncrementProgress()
    Pbar.StartPuzzle2(0)
    Pbar.FinishPuzzle2()

    return -1, -1

def day20(input:list[str], Pbar: ProgressBar):
    
    Pbar.StartPuzzle1(len(input))
    Pbar.IncrementProgress()
    Pbar.StartPuzzle2(0)
    Pbar.FinishPuzzle2()

    return -1, -1

def day21(input:list[str], Pbar: ProgressBar):
    
    Pbar.StartPuzzle1(len(input))
    Pbar.IncrementProgress()
    Pbar.StartPuzzle2(0)
    Pbar.FinishPuzzle2()

    return -1, -1

def day22(input:list[str], Pbar: ProgressBar):
    
    Pbar.StartPuzzle1(len(input))
    Pbar.IncrementProgress()
    Pbar.StartPuzzle2(0)
    Pbar.FinishPuzzle2()

    return -1, -1

def day23(input:list[str], Pbar: ProgressBar):
    
    Pbar.StartPuzzle1(len(input))
    Pbar.IncrementProgress()
    Pbar.StartPuzzle2(0)
    Pbar.FinishPuzzle2()

    return -1, -1

def day24(input:list[str], Pbar: ProgressBar):
    
    Pbar.StartPuzzle1(len(input))
    Pbar.IncrementProgress()
    Pbar.StartPuzzle2(0)
    Pbar.FinishPuzzle2()

    return -1, -1

def day25(input:list[str], Pbar: ProgressBar):
    
    Pbar.StartPuzzle1(len(input))
    Pbar.IncrementProgress()
    Pbar.StartPuzzle2(0)
    Pbar.FinishPuzzle2()


    return -1, "Merry Christmas!"