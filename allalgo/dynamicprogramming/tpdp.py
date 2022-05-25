import math
import random
import os
import glob
from os import listdir
from os.path import isfile, join

def solve(N,Attraction):

    UtilMatrix, PrevMatrix = dynamicProgram(N,Attraction)
    Sequence = PrevMatrix(0,1440)
    return len(Sequence),Sequence

def distanceBetween(start,finish,Attraction):
    startX = Attraction[start-1][0]
    startY = Attraction[start-1][1]
    finishX = Attraction[finish-1][0]
    finishY = Attraction[finish-1][1]

    return math.ceil(math.dist([startX,startY],[finishX,finishY]))

def getSequenceDP(N,Attraction,PrevMatrix,Index,Time):
    res = []
    t = Time
    i = Index

    while (i != 0):
        res.append(i)
        PrevNow = PrevMatrix[i][t]

        while(PrevMatrix[i][t]==PrevNow):
            if t > 0:
                t -= 1
            else:
                return res

        t += 1

        t -= (distanceBetween(i,PrevNow,Attraction)+Attraction[i-1][5])
        i = PrevNow

    return reversed(res)


def dynamicProgram(N,Attraction):
    #Subproblem: Finishing at Attraction K, Max Utility by time T
    #Initializes N by 1440 matrix for Utility Tracking
    #First get a 1440 1d array
    Line = [0 for i in range(1441)]
    #Then get a 2-d array that is composed of (N+1) such lines
    #The first line is for source
    UtilMatrix = [Line for i in range(N+1)]

    #Initializes another 2d array to track previously visited node
    #-1 Denotes none
    Track = [[] for i in range(1441)]
    PrevMatrix = [Track for i in range(N+1)]
    #The element of any list in the TrackMatrix should be a tuple specifying time and node



    for timeFinish in range(1441):
        for attraction_index in range(N+1):
            print("Now on "+str(attraction_index) + " , " + str(timeFinish))
            #Getting all values from the attraction
            #For source node, we hard code the values
            if attraction_index == 0:
                CurrentX = 200
                CurrentY = 200
                OpenTime = 0
                CloseTime = 1440
                Utility = 0
                Duration = 0

            #For other nodes, we get the values from the parameter matrix
            else:
                CurrentAttraction = Attraction[attraction_index-1]
                CurrentX = CurrentAttraction[0]
                CurrentY = CurrentAttraction[1]
                OpenTime = CurrentAttraction[2]
                CloseTime = CurrentAttraction[3]
                Utility = CurrentAttraction[4]
                Duration = CurrentAttraction[5]

            #If there is no way for this attraction to be finished at this moment
            #Set the max utility as the max among anytime before
            TimeShouldStart = timeFinish - Duration
            if not TimeShouldStart in range(OpenTime,CloseTime+1):
                MaxUtil = UtilMatrix[attraction_index][timeFinish-1]
                MaxPrev = PrevMatrix[attraction_index][timeFinish-1]
                UtilMatrix[attraction_index][timeFinish]=MaxUtil
                PrevMatrix[attraction_index][timeFinish]=MaxPrev
                continue


            #Storing data at Maximum
            MaxUtil = 0
            MaxPrev = -1


            #If there is a corresponding start time that would end right
            #at this moment, then we find the maximum utility from potential
            #previous attractions
            for PrevTime in (range(TimeShouldStart)):
                for PrevIndex in range(N+1):
                    #print("PrevTime is"+ str(PrevTime))
                    #print("PrevIndex is"+ str(PrevIndex))
                    #If already visited in the sequence of the previous attraction, then ignore
                    PrevListofPrev = PrevMatrix[PrevIndex][PrevTime]
                    if not attraction_index in PrevListofPrev:
                        if PrevIndex == 0:
                            PrevX = 200
                            PrevY = 200
                        else:
                            PrevAttraction = Attraction[PrevIndex-1]
                            PrevX = PrevAttraction[0]
                            PrevY = PrevAttraction[1]
                        Dist = math.ceil(math.dist([PrevX,PrevY],[CurrentX,CurrentY]))
                        if PrevTime+Dist <= TimeShouldStart:
                            UtilThisWay = UtilMatrix[PrevIndex][PrevTime]+Utility
                            if UtilThisWay > MaxUtil:
                                MaxUtil = UtilThisWay
                                MaxPrev = PrevListofPrev + [PrevIndex]
            
            UtilMatrix[attraction_index][timeFinish] = MaxUtil
            PrevMatrix[attraction_index][timeFinish] = MaxPrev

    return UtilMatrix,PrevMatrix





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
        print("Now working on" + filename)
        
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

    #print(a)
    #separator = " "
    #print(separator.join(map(str,l)))
    
if __name__ == '__main__':
    main()