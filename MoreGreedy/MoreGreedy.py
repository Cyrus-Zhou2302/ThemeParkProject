import math
import random
import os
import glob
from os import listdir
from os.path import isfile, join



def GreedySolve(N,Attractions):
    XLast = 200
    YLast = 200
    
    
    timenow = 0
    
    for i in
    for attraction in Attractions:
        XCurrent = attraction[0]
        YCurrent = attraction[1]
        OCurrent = attraction[2]
        CCurrent = attraction[3]
        UCurrent = attraction[4]
        TCurrent = attraction[5]
        
        dist = math.ceil(math.dist([XCurrent,YCurrent],[XLast,YLast]))
        totaltime = dist
    
    




def read_input():
    input_split = input().split("\n")
    N = int(input_split[0])
    latter_split = input_split[1:]
    attraction = []

    for i in range(N):
        this_attraction = latter_split[i]
        attraction.append([int(val) for val in this_attraction.split()])

    return N, attraction
    
def main():
    N, Attraction = read_input()
    num, sequence = GreedySolve(N,Attraction)
    
    print(num)
    print(sequence)
