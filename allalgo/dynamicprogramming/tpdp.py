import math
import random
import os
import glob
from os import listdir
from os.path import isfile, join

import signal

def signal_handler(signum, frame):
    raise Exception("Timed out! Try dp")
"""
def solve(N,Attraction):

    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(60)   # 60 seconds
    try:
        return btsolve()
    except Exception, msg:
        print "Timed out!"
    return dpsolve(N,Attraction)
"""
# dynamic progamming solver
def solve(N,Attraction):
    UtilMatrix, PrevMatrix = dynamicProgram(N,Attraction)
    Sequence = PrevMatrix[0][1440]
    return len(Sequence),Sequence

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


    PrevMatrix[0][0]=[0]


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

            MaxUtil = 0
            MaxPrev = []
            timeShouldStart = timeFinish-Duration
            if timeShouldStart < 0:
                continue

            for PrevTime in (range(timeShouldStart+1)):
                for PrevIndex in range(N+1):
                    if PrevMatrix[PrevIndex][PrevTime] == []:
                        continue
                    UtilThisWay = 0
                    if PrevIndex == attraction_index:
                        UtilThisWay = UtilMatrix[PrevIndex][PrevTime]
                    else:
                        if PrevIndex == 0:
                            PrevX = 200
                            PrevY = 200
                        else:
                            prevAttraction = Attraction[PrevIndex-1]
                            PrevX = prevAttraction[0]
                            PrevY = prevAttraction[1]
                        Dist = math.ceil(math.dist([PrevX,PrevY],[CurrentX,CurrentY]))
                        if not (attraction_index in PrevMatrix[PrevIndex][PrevTime]):
                            if (PrevTime+Dist <= CloseTime):
                                if (PrevTime+Dist+Duration <= timeFinish):
                                    UtilThisWay = UtilMatrix[PrevIndex][PrevTime]+Utility
                    if UtilThisWay > MaxUtil:
                        MaxUtil = UtilThisWay
                        MaxPrev = PrevMatrix[PrevIndex][PrevTime]
            UtilMatrix[attraction_index][timeFinish]=MaxUtil
            PrevMatrix[attraction_index][timeFinish]=MaxPrev+[attraction_index]
                            

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