import math

def solve(N,Attraction):


def distanceBetween(start,finish,Attraction):
    startX = Attraction[start][0]
    startY = Attraction[start][1]
    finishX = Attraction[finish][0]
    finishY = Attraction[finish][1]

    return math.ceil(math.dist([startX,startY],[finishX,finishY]))



def dynamicProgram(N,Attraction):
    #Subproblem: Finishing at Attraction K, Max Utility by time T
    #Initializes N by 1440 matrix for Utility Tracking
    #First get a 1440 1d array
    Line = [0 for i in range(1441)]
    #Then get a 2-d array that is composed of (N+1) such lines
    #The first line is for source
    UtilMatrix = Line*(N+1)

    #Initializes another 2d array to track previously visited node
    #-1 Denotes none
    PrevMatrix = [-1 for i in range(1441)]*(N+1)
    #The element of any list in the TrackMatrix should be a tuple specifying time and node



    for timeFinish in range(1441):
        for attraction_index in range(N+1):
            
            #Getting all values from the attraction
            CurrentAttraction = Attraction[attraction_index]
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
                MaxBefore = 0
                MaxPrev = -1
                for t in range(timeFinish):
                    UtilCurrent = UtilMatrix[attraction_index][t]
                    PrevCurrent = PrevMatrix[attraction_index][t]
                    if UtilCurrent > MaxBefore:
                        MaxBefore = UtilCurrent
                        MaxPrev = 



            MaxUtil = 0
            Maxprev = -1

            for loop_column in reversed(range(timeFinish)):

                for potential_previous in range(N):
                    if 






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