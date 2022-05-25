import math

def solve(N,Attraction):





def dynamicProgram(N,Attraction):
    #Subproblem: Finishing at Attraction K, Max Utility by time T
    #Initializes N by 1440 matrix for Utility Tracking
    #First get a 1440 1d array
    Line = [0 for i in range(1441)]
    #Then get a 2-d array that is composed of N such lines
    UtilMatrix = Line*N

    #Initializes another 2d array to track previously visited node
    #-1 Denotes none
    TrackMatrix = []*N
    #The element of any list in the TrackMatrix should be a tuple specifying time and node



    for timeFinish in range(1441):
        for attraction_index in range(N):
            





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