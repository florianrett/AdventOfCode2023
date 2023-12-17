import collections
import copy
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
