import math
import random
import os
import glob
from os import listdir
from os.path import isfile, join

import signal

def signal_handler(signum, frame):
    raise Exception("Timed out! Try dp")

def solve(N,Attraction):

    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(60)   # 60 seconds
    try:
        return btsolve()
    except Exception, msg:
        print "Timed out! Now Trying Dynamic Programming"
    return dpsolve(N,Attraction)

"""
Following is dynamic programming Solver:
"""

# dynamic progamming solver
def solve(N,Attraction):
    attWithSource = [[200,200,0,1440,0,0]]+Attraction
    UtilMatrix, PrevMatrix = dynamicProgram(N,attWithSource)
    print(UtilMatrix)
    print("UtilMatrx[0][0] is "+str(UtilMatrix[0][0]))
    Sequence = PrevMatrix[0][1440]
    Sequence.pop(0)

    return len(Sequence),Sequence

def dynamicProgram(N,Attractions):
    #Initialization, Utility Tracker Matrix:
    UtilLine = [-1 for i in range(1441)]
    UtilMatrix = [UtilLine for i in range(N+1)]
    UtilMatrix[0][0] = 0

    #Initialization, Previous Path Tracker Matrix:
    PrevLine = [[] for i in range(1441)]
    PrevMatrix = [PrevLine for i in range(N+1)]
    PrevMatrix[0][0] = []

    #Moving through the two tables column by column
    for timeFinish in range(1441):
        #Go index by index in each column iteration
        for indexFinish in range(N+1):
            
            print("Now working on index "+str(indexFinish)+"/"+str(N)+" at time "+str(timeFinish)+"/1440")

            attractionFinish = Attractions[indexFinish]
            XFinish = attractionFinish[0]
            YFinish = attractionFinish[1]
            OFinish = attractionFinish[2]
            CFinish = attractionFinish[3]
            UFinish = attractionFinish[4]
            Duration = attractionFinish[5]

            ##################################################################################################################
            ##################################################################################################################
            #Case 1: go to an vertex that has not yet been open
            if timeFinish - Duration < OFinish:
                #Initializes local variables to store information at maximum
                maxPathPrev = []
                maxUtilPrev = 0
                #We loop through all possible previous vertices
                for indexPrev in range(N+1):
                    attractionPrev = Attractions[indexPrev]
                    XPrev = attractionPrev[0]
                    YPrev = attractionPrev[1]
                    Dist = math.ceil(math.dist([XPrev,YPrev],[XFinish,YFinish]))
                    #We only need to care about the marginal case at the latest leaving
                    #time from the previous attraction
                    timePrev = timeFinish - Dist
                    #If the required time is less than zero than we know this is impossible
                    if timePrev < 0:
                        continue
                    #If there is no valid path to the previous attraction at the required
                    #time, then we know that no path is feasible
                    pathPrev = PrevMatrix[indexPrev][timePrev]
                    #If the attraction at the finish time is already in the path
                    #We may not visit it again
                    if indexPrev in pathPrev:
                        continue
                    #If there is a valid path to the previous attraction at required time
                    #then we get the utility at that time
                    utilPrev = UtilMatrix[indexPrev][timePrev]

                    if utilPrev < 0:
                        continue
                    #If we found this utility to be greater than the original maximum value
                    #then we replace it and store the path to the current previous at the 
                    #current required time in the maxUtilPrev variable
                    if utilPrev >= maxUtilPrev:
                        maxUtilPrev = utilPrev
                        maxPathPrev = pathPrev
                #It is also possible for TAs to wait at the attraction
                #in this case we may just inherit information from the last minute
                #We check to see if this is a better choice
                utilJustInherit = UtilMatrix[indexFinish][timeFinish-1]
                if utilJustInherit >= maxUtilPrev:
                    maxUtilPrev = utilJustInherit
                    maxPathPrev = PrevMatrix[indexFinish][timeFinish-1]

                #After we have found information for the maximum,
                #We set the corresponding values in matrices
                UtilMatrix[indexFinish][timeFinish]=maxUtilPrev
                PrevMatrix[indexFinish][timeFinish]=maxPathPrev

                print("Got Utility "+str(maxUtilPrev)+" with Path "+str(maxPathPrev))
            
            #Case 2: go to an vertex that is closed
            elif timeFinish - Duration > CFinish:
                UtilMatrix[indexFinish][timeFinish]=UtilMatrix[indexFinish][timeFinish-1]
                PrevMatrix[indexFinish][timeFinish]=PrevMatrix[indexFinish][timeFinish-1]
                print("The attraction is closed")

            ##################################################################################################################
            ##################################################################################################################
            #Case 3: go to an vertex that is open
            else:
                #Initializes local variables to store information at maximum
                maxPathPrev = [0]
                maxUtilPrev = 0
                #We loop through all possible previous vertices
                for indexPrev in range(N+1):
                    attractionPrev = Attractions[indexPrev]
                    XPrev = attractionPrev[0]
                    YPrev = attractionPrev[1]
                    Dist = math.ceil(math.dist([XPrev,YPrev],[XFinish,YFinish]))
                    #We only need to care about the marginal case at the latest leaving
                    #time from the previous attraction
                    timePrev = timeFinish - Dist - Duration
                    #If the required time is less than zero than we know this is impossible
                    if timePrev < 0:
                        continue
                    #If there is no valid path to the previous attraction at the required
                    #time, then we know that no path is feasible
                    pathPrev = PrevMatrix[indexPrev][timePrev]
                    #If the attraction at the finish time is already in the path
                    #We may not visit it again
                    if indexPrev in pathPrev:
                        continue
                    #If there is a valid path to the previous attraction at required time
                    #then we get the utility at that time plus the utility from this attraction
                    utilPrev = UtilMatrix[indexPrev][timePrev]
                    if utilPrev < 0:
                        continue
                    utilPrev += UFinish
                    #If we found this utility to be greater than the original maximum value
                    #then we replace it and store the path to the current previous at the 
                    #current required time in the maxUtilPrev variable
                    if utilPrev >= maxUtilPrev:
                        maxUtilPrev = utilPrev
                        maxPathPrev = pathPrev + [indexPrev]
                #It is also possible for TAs to wait at the attraction
                #in this case we may just inherit information from the last minute
                #We check to see if this is a better choice
                utilJustInherit = UtilMatrix[indexFinish][timeFinish-1]
                if utilJustInherit >= maxUtilPrev:
                    maxUtilPrev = utilJustInherit
                    maxPathPrev = PrevMatrix[indexFinish][timeFinish-1]

                #After we have found information for the maximum,
                #We set the corresponding values in matrices
                UtilMatrix[indexFinish][timeFinish]=maxUtilPrev
                PrevMatrix[indexFinish][timeFinish]=maxPathPrev
                print("Got Utility "+str(maxUtilPrev)+"with Path "+str(maxPathPrev))
            
            ##################################################################################################################
            ##################################################################################################################
            

    return UtilMatrix,PrevMatrix



"""
End of Dynamic Programming Solver
"""


"""
Following is Backtracking Solver:
"""

def minCompleteTime(Attractions,Sequence):
    TimeNow = 0
    LastX = 200
    LastY = 200
    CurrentX = LastX
    CurrentY = LastY

    #Looping to see the current minimum time for finishing
    #the given Path
    for index in Sequence:
        CurrentAttraction = Attraction[index-1]
        CurrentX = CurrentAttraction[0]
        CurrentY = CurrentAttraction[1]
        CurrentOpen = CurrentAttraction[2]
        CurrentClose = CurrentAttraction[3]
        Duration = CurrentAttraction[5]
        Dist = math.ceil(math.dist([LastX,LastY],[CurrentX,CurrentY]))
        if (TimeNow+Dist) > CurrentClose:
            return math.inf,CurrentX,CurrentY
        TimeNow = max(CurrentOpen,(TimeNow+Dist))+Duration
    
    return TimeNow,CurrentX,CurrentY

def isFeasible(Attractions,Sequence):
    TimeFinish,LastX,LastY = minCompleteTime(Attraction,Path)
    DistToSource = math.ceil(math.dist([LastX,LastY],[200,200]))
    TimeFinish += DistToSource
    if TimeFinish > 1440:
        return False
    return True

def backTrack(N,Attractions):
    Sequence = []
    i = 1
    while len(Sequence) > 0:
        if isFeasible(Attractions,Sequence):
            Sequence + []

"""
Endof Backtracking Solver:
"""

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
