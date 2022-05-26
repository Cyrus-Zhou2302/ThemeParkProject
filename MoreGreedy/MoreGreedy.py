import math
import random
import os
import glob
from os import listdir
from os.path import isfile, join



def GreedySolve(N,Attractions):
    XLast = 200
    YLast = 200
    
    Sequence = []

    timenow = 0
    
    while(timenow <= 1440):
        MaxUnitUtil = 0
        MaxIndex = -1
        MaxX = 200
        MaxY = 200
        MaxTimeIncrease = 0
        for i in range(N):
            #We skip this node if it is already visited
            if (i+1) in Sequence:
                continue

            #Getting data from the attraction input
            attraction = Attractions[i]
            XCurrent = attraction[0]
            YCurrent = attraction[1]
            OCurrent = attraction[2]
            CCurrent = attraction[3]
            UCurrent = attraction[4]
            TCurrent = attraction[5]
            
            #Calculate the distance from current position to this node
            dist = math.ceil(math.dist([XCurrent,YCurrent],[XLast,YLast]))

            #If we can't make it before it is closed, forget about it
            if timenow + dist > CCurrent:
                continue

            #The earliest time TAs can get to play is the maximum between
            #the opening time of the attraction and the time at which they
            #reach the attraction
            timePlayEarliest = max(OCurrent,timenow+dist)

            #Then the total time cost for visiting this attraction is
            #the time on road plus the time for waiting plus the time
            #the attraction would take
            totalToSpend = timePlayEarliest - timenow + TCurrent

            #We use unit utility (with total time cost calculated as said)
            #as a key to decide 
            UnitUtil = UCurrent/totalToSpend

            #If the unit utility for this attraction is greater than the
            #current best, then we store the information of this 
            if UnitUtil > MaxUnitUtil:
                MaxUnitUtil = UnitUtil
                MaxIndex = i + 1
                MaxX = XCurrent
                MaxY = YCurrent
                MaxTimeIncrease = totalToSpend
        
        Sequence.append(MaxIndex)
        XLast = MaxX
        YLast = MaxY
        timenow += MaxTimeIncrease

    Sequence.pop()
    
    return len(Sequence),Sequence


def utilityTotal(Attraction,Path):
    acc = 0
    if Path == None:
        return 0
    for i in range(len(Path)):
        acc += Attraction[i][4]
    return acc

def read_input():
    N = int(input())
    attraction = [[int(i) for i in input().split()] for _ in range(N)]
    return N, attraction


def main():
    N, attraction = read_input()
    a, l = GreedySolve(N, attraction)
    print(a)
    print(l)
    print(utilityTotal(attraction,l))

if __name__ == '__main__':
    main()