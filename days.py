import HelperFunctions as hf
import HelperClasses as hc
from ProgressBar import ProgressBar
import typing
import collections
import copy
import numpy as np
import time
import ast
import math
from itertools import combinations, permutations
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
        
        Locations.append(hf.ConvertNumber(hf.ConvertNumber(hf.ConvertNumber(hf.ConvertNumber(hf.ConvertNumber(hf.ConvertNumber(hf.ConvertNumber(s, SeedToSoil), SoilToFertilizer), FertilizerToWater), WaterToLight), LightToTemperature), TemperatureToHumidity), HumidityToLocation))

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
        SoilRanges += hf.ConvertNumberRangeRec(r[0], r[1], SeedToSoil)
    for r in SoilRanges:
        FertRanges += hf.ConvertNumberRangeRec(r[0], r[1], SoilToFertilizer)
    for r in FertRanges:
        WaterRanges += hf.ConvertNumberRangeRec(r[0], r[1], FertilizerToWater)
    for r in WaterRanges:
        LightRanges += hf.ConvertNumberRangeRec(r[0], r[1], WaterToLight)
    for r in LightRanges:
        TempRanges += hf.ConvertNumberRangeRec(r[0], r[1], LightToTemperature)
    for r in TempRanges:
        HumidRanges += hf.ConvertNumberRangeRec(r[0], r[1], TemperatureToHumidity)
    for r in HumidRanges:
        LocationRanges += hf.ConvertNumberRangeRec(r[0], r[1], HumidityToLocation)

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
    
    Pbar.StartPuzzle1(len(input))
    Pbar.IncrementProgress()
    Pbar.StartPuzzle2(0)
    Pbar.FinishPuzzle2()

    return -1, -1

def day8(input:list[str], Pbar: ProgressBar):
    
    Pbar.StartPuzzle1(len(input))
    Pbar.IncrementProgress()
    Pbar.StartPuzzle2(0)
    Pbar.FinishPuzzle2()

    return -1, -1

def day9(input:list[str], Pbar: ProgressBar):
    
    Pbar.StartPuzzle1(len(input))
    Pbar.IncrementProgress()
    Pbar.StartPuzzle2(0)
    Pbar.FinishPuzzle2()

    return -1, -1

def day10(input:list[str], Pbar: ProgressBar):
    
    Pbar.StartPuzzle1(len(input))
    Pbar.IncrementProgress()
    Pbar.StartPuzzle2(0)
    Pbar.FinishPuzzle2()

    return -1, -1

def day11(input:list[str], Pbar: ProgressBar):
    
    Pbar.StartPuzzle1(len(input))
    Pbar.IncrementProgress()
    Pbar.StartPuzzle2(0)
    Pbar.FinishPuzzle2()

    return -1, -1

def day12(input:list[str], Pbar: ProgressBar):
    
    Pbar.StartPuzzle1(len(input))
    Pbar.IncrementProgress()
    Pbar.StartPuzzle2(0)
    Pbar.FinishPuzzle2()

    return -1, -1

def day13(input:list[str], Pbar: ProgressBar):
    
    Pbar.StartPuzzle1(len(input))
    Pbar.IncrementProgress()
    Pbar.StartPuzzle2(0)
    Pbar.FinishPuzzle2()

    return -1, -1

def day14(input:list[str], Pbar: ProgressBar):
    
    Pbar.StartPuzzle1(len(input))
    Pbar.IncrementProgress()
    Pbar.StartPuzzle2(0)
    Pbar.FinishPuzzle2()

    return -1, -1

def day15(input:list[str], Pbar: ProgressBar):
    
    Pbar.StartPuzzle1(len(input))
    Pbar.IncrementProgress()
    Pbar.StartPuzzle2(0)
    Pbar.FinishPuzzle2()

    return -1, -1

def day16(input:list[str], Pbar: ProgressBar):
    
    Pbar.StartPuzzle1(len(input))
    Pbar.IncrementProgress()
    Pbar.StartPuzzle2(0)
    Pbar.FinishPuzzle2()

    return -1, -1

def day17(input:list[str], Pbar: ProgressBar):
    
    Pbar.StartPuzzle1(len(input))
    Pbar.IncrementProgress()
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