import HelperFunctions as hf
import HelperClasses as hc
from ProgressBar import ProgressBar
from HelperClasses import Number
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
    Pbar.IncrementProgress()
    Pbar.StartPuzzle2(0)
    Pbar.FinishPuzzle2()

    return -1, -1

def day2(input, Pbar: ProgressBar):
    
    Pbar.StartPuzzle1(len(input))
    Pbar.IncrementProgress()
    Pbar.StartPuzzle2(0)
    Pbar.FinishPuzzle2()

    return -1, -1

def day3(input, Pbar: ProgressBar):
    
    Pbar.StartPuzzle1(len(input))
    Pbar.IncrementProgress()
    Pbar.StartPuzzle2(0)
    Pbar.FinishPuzzle2()

    return -1, -1

def day4(input, Pbar: ProgressBar):
    
    Pbar.StartPuzzle1(len(input))
    Pbar.IncrementProgress()
    Pbar.StartPuzzle2(0)
    Pbar.FinishPuzzle2()

    return -1, -1

def day5(input, Pbar: ProgressBar):
    
    Pbar.StartPuzzle1(len(input))
    Pbar.IncrementProgress()
    Pbar.StartPuzzle2(0)
    Pbar.FinishPuzzle2()

    return -1, -1

def day6(input, Pbar: ProgressBar):
    
    Pbar.StartPuzzle1(len(input))
    Pbar.IncrementProgress()
    Pbar.StartPuzzle2(0)
    Pbar.FinishPuzzle2()

    return -1, -1

def day7(input, Pbar: ProgressBar):
    
    Pbar.StartPuzzle1(len(input))
    Pbar.IncrementProgress()
    Pbar.StartPuzzle2(0)
    Pbar.FinishPuzzle2()

    return -1, -1

def day8(input, Pbar: ProgressBar):
    
    Pbar.StartPuzzle1(len(input))
    Pbar.IncrementProgress()
    Pbar.StartPuzzle2(0)
    Pbar.FinishPuzzle2()

    return -1, -1

def day9(input, Pbar: ProgressBar):
    
    Pbar.StartPuzzle1(len(input))
    Pbar.IncrementProgress()
    Pbar.StartPuzzle2(0)
    Pbar.FinishPuzzle2()

    return -1, -1

def day10(input, Pbar: ProgressBar):
    
    Pbar.StartPuzzle1(len(input))
    Pbar.IncrementProgress()
    Pbar.StartPuzzle2(0)
    Pbar.FinishPuzzle2()

    return -1, -1

def day11(input, Pbar: ProgressBar):
    
    Pbar.StartPuzzle1(len(input))
    Pbar.IncrementProgress()
    Pbar.StartPuzzle2(0)
    Pbar.FinishPuzzle2()

    return -1, -1

def day12(input, Pbar: ProgressBar):
    
    Pbar.StartPuzzle1(len(input))
    Pbar.IncrementProgress()
    Pbar.StartPuzzle2(0)
    Pbar.FinishPuzzle2()

    return -1, -1

def day13(input, Pbar: ProgressBar):
    
    Pbar.StartPuzzle1(len(input))
    Pbar.IncrementProgress()
    Pbar.StartPuzzle2(0)
    Pbar.FinishPuzzle2()

    return -1, -1

def day14(input, Pbar: ProgressBar):
    
    Pbar.StartPuzzle1(len(input))
    Pbar.IncrementProgress()
    Pbar.StartPuzzle2(0)
    Pbar.FinishPuzzle2()

    return -1, -1

def day15(input, Pbar: ProgressBar):
    
    Pbar.StartPuzzle1(len(input))
    Pbar.IncrementProgress()
    Pbar.StartPuzzle2(0)
    Pbar.FinishPuzzle2()

    return -1, -1

def day16(input, Pbar: ProgressBar):
    
    Pbar.StartPuzzle1(len(input))
    Pbar.IncrementProgress()
    Pbar.StartPuzzle2(0)
    Pbar.FinishPuzzle2()

    return -1, -1

def day17(input, Pbar: ProgressBar):
    
    Pbar.StartPuzzle1(len(input))
    Pbar.IncrementProgress()
    Pbar.StartPuzzle2(0)
    Pbar.FinishPuzzle2()

    return -1, -1

def day18(input, Pbar: ProgressBar):
    
    Pbar.StartPuzzle1(len(input))
    Pbar.IncrementProgress()
    Pbar.StartPuzzle2(0)
    Pbar.FinishPuzzle2()

    return -1, -1

def day19(input, Pbar: ProgressBar):
    
    Pbar.StartPuzzle1(len(input))
    Pbar.IncrementProgress()
    Pbar.StartPuzzle2(0)
    Pbar.FinishPuzzle2()

    return -1, -1

def day20(input, Pbar: ProgressBar):
    
    Pbar.StartPuzzle1(len(input))
    Pbar.IncrementProgress()
    Pbar.StartPuzzle2(0)
    Pbar.FinishPuzzle2()

    return -1, -1

def day21(input, Pbar: ProgressBar):
    
    Pbar.StartPuzzle1(len(input))
    Pbar.IncrementProgress()
    Pbar.StartPuzzle2(0)
    Pbar.FinishPuzzle2()

    return -1, -1

def day22(input, Pbar: ProgressBar):
    
    Pbar.StartPuzzle1(len(input))
    Pbar.IncrementProgress()
    Pbar.StartPuzzle2(0)
    Pbar.FinishPuzzle2()

    return -1, -1

def day23(input, Pbar: ProgressBar):
    
    Pbar.StartPuzzle1(len(input))
    Pbar.IncrementProgress()
    Pbar.StartPuzzle2(0)
    Pbar.FinishPuzzle2()

    return -1, -1

def day24(input, Pbar: ProgressBar):
    
    Pbar.StartPuzzle1(len(input))
    Pbar.IncrementProgress()
    Pbar.StartPuzzle2(0)
    Pbar.FinishPuzzle2()

    return -1, -1

def day25(input, Pbar: ProgressBar):
    
    Pbar.StartPuzzle1(len(input))
    Pbar.IncrementProgress()
    Pbar.StartPuzzle2(0)
    Pbar.FinishPuzzle2()


    return -1, "Merry Christmas!"