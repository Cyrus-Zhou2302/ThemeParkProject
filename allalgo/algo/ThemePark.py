import math
import random
import os
import glob
from os import listdir
from os.path import isfile, join



def solve(N, Attraction):
    
    CurrentPath = InitGreedy(Attraction,[])
    BestPath = CurrentPath
    BestUtility = utilityTotal(Attraction,BestPath)
    NumNoImprove = 0
    P = 0.05
    NumIteration = 100000
    MaxNoImprove = 10
    UtilityWeight = random.uniform(2,10)
    TimeonRoadWeight = random.uniform(3,6)
    DurationWeight = random.uniform(2,5)

    for iteration in range(NumIteration):
        OldPath = CurrentPath
        CurrentPath = randomSwap(CurrentPath)
        while (not (isFeasible(Attraction,CurrentPath)) or (random.random()<P)):
            if CurrentPath != []:
                CurrentPath.pop()
        NeighborPath = greedyInsert(Attraction,CurrentPath,UtilityWeight,TimeonRoadWeight,DurationWeight)
        UtilChange = utilityTotal(Attraction,NeighborPath)-utilityTotal(Attraction,OldPath)

        if (UtilChange > 0):
           CurrentPath = NeighborPath
        else:
            CurrentPath = OldPath

        if (utilityTotal(Attraction, NeighborPath) > BestUtility):
            BestPath = NeighborPath
            BestUtility = utilityTotal(Attraction,CurrentPath)
        else:
            NumNoImprove += 1
            if NumNoImprove > MaxNoImprove:
                UtilityWeight = random.uniform(2,10)
                TimeonRoadWeight = random.uniform(3,6)
                DurationWeight = random.uniform(2,5)
                NumNoImprove = 0
    if not (isFeasible(Attraction,BestPath)):
        print("best path not feasible")
    return utilityTotal(Attraction,BestPath),BestPath


def minCompleteTime(Attraction,Path):
    TimeNow = 0
    LastX = 200
    LastY = 200
    CurrentX = LastX
    CurrentY = LastY

    #Looping to see the current minimum time for finishing
    #the given Path
    for index in Path:
        CurrentAttraction = Attraction[index-1]
        CurrentX = CurrentAttraction[0]
        CurrentY = CurrentAttraction[1]
        CurrentOpen = CurrentAttraction[2]
        CurrentClose = CurrentAttraction[3]
        Dist = math.ceil(math.dist([LastX,LastY],[CurrentX,CurrentY]))
        if (TimeNow+Dist) > CurrentClose:
            return math.inf,CurrentX,CurrentY
        TimeNow = max(CurrentOpen,(TimeNow+Dist))
    
    return TimeNow,CurrentX,CurrentY



def greedyInsert(Attraction,Path,UtilityWeight,TimeonRoadWeight,DurationWeight):
    TimeNow,LastX,LastY = minCompleteTime(Attraction,Path)

    while (True):
        MaxIndex = -1
        MaxKey = -math.inf
        MaxTimeTotal = 0
        HaveChoice = False
        for i in range(len(Attraction)):
            if not (i+1) in Path:
                attraction = Attraction[i]
                XCoord = attraction[0]
                YCoord = attraction[1]
                OpenTime = attraction[2]
                CloseTime = attraction[3]
                Utility = attraction[4]
                Duration = attraction[5]
                Dist = math.ceil(math.dist([XCoord,YCoord],[LastX,LastY]))
                DistToSource = math.ceil(math.dist([XCoord,YCoord],[200,200]))
                TimeWaste = max(OpenTime-TimeNow, Dist)
                TimeTotal = TimeWaste+Duration
                if Dist + TimeNow > CloseTime:
                    Key = -math.inf
                else:
                    if TimeNow + TimeTotal + DistToSource<= 1440:
                        Key = -math.inf
                    else:
                        HaveChoice = True
                        Key = Utility*UtilityWeight - TimeWaste*TimeonRoadWeight - Duration*DurationWeight
                if Key > MaxKey:
                    MaxKey = Key
                    MaxIndex = i + 1
                    MaxTimeTotal = TimeTotal
        if HaveChoice:
            TimeNow += MaxTimeTotal
            Path.append(MaxIndex)
        else:
            break
    
    return Path


def InitGreedy(Attraction,Path):
    TimeNow,LastX,LastY = minCompleteTime(Attraction,Path)

    #Now we have calculated for the original path
    #We want to take more nodes in
    while (math.dist([200,200],[LastX,LastY])+TimeNow)<=1440:
        #Initialze local variables for maximum memory
        MaxIndex = -1
        MaxUnitUtil = 0
        MaxTimeTotal = 0
        for i in range(len(Attraction)):
            if not (i+1) in Path:
                attraction = Attraction[i]
                XCoord = attraction[0]
                YCoord = attraction[1]
                OpenTime = attraction[2]
                CloseTime = attraction[3]
                Utility = attraction[4]
                Duration = attraction[5]
                Dist = math.ceil(math.dist([XCoord,YCoord],[LastX,LastY]))
                DistToSource = math.ceil(math.dist([XCoord,YCoord],[200,200]))
                if Dist + TimeNow > CloseTime:
                    UnitUtil = -1
                else: 
                    TimeWaste = max(OpenTime-TimeNow, Dist)
                    TimeTotal = TimeWaste+Duration
                    if (TimeTotal == 0):
                        Path.append(i+1)
                        UnitUtil = -1
                    else:
                        if (TimeTotal + TimeNow + DistToSource) <= 1440:
                            UnitUtil = Utility/TimeTotal
                        else:
                            UnitUtil = -1
                if UnitUtil > MaxUnitUtil:
                    MaxUnitUtil = UnitUtil
                    MaxIndex = i + 1
                    MaxTimeTotal = TimeTotal

        if MaxUnitUtil > 0:
            TimeNow += MaxTimeTotal
            Path.append(MaxIndex)
        else:
            break
    return Path
    

def isFeasible(Attraction,Path):
    TimeFinish,LastX,LastY = minCompleteTime(Attraction,Path)
    DistToSource = math.ceil(math.dist([LastX,LastY],[200,200]))
    TimeFinish += DistToSource
    if TimeFinish > 1440:
        return False
    return True


def randomSwap(Path):
    if Path == []:
        return Path
    if len(Path) == 1:
        return Path
    i = random.randint(0,len(Path)-1)
    j = random.randint(0,len(Path)-1)
    Temp = Path[j]
    Path[j] = Path[i]
    Path[i] = Temp
    return Path 

def utilityTotal(Attraction,Path):
    acc = 0
    if Path == None:
        return 0
    for i in range(len(Path)):
        acc += Attraction[i][4]
    return acc

def read_input(input_text):
    input_split = input_text.split("\n")
    N = int(input_split[0])
    latter_split = input_split[1:]
    attraction = []

    for i in range(N):
        this_attraction = latter_split[i]
        attraction.append([int(val) for val in this_attraction.split()])

    return N, attraction


def main():

    output_dir = "all_outputs/"
    output_suffix = '.out'

    for filename in glob.glob('all_inputs/*.in'):
        input_name = (filename.split("/"))[1]
        team_name = (input_name.split("."))[0]
        output_name = output_dir + team_name + output_suffix
        print("Now working on " + filename)
        
        with open(os.path.join(os.getcwd(), filename), 'r') as input:
            input_text = input.read()
            N, attraction = read_input(input_text)
            a, l = solve(N, attraction)

            with open(os.path.join(os.getcwd(),output_name),'w') as output:
                print(a,file=output)
                separator = " "
                print(separator.join(map(str,l)),file=output)

        input.close()
        output.close()

if __name__ == '__main__':
    main()