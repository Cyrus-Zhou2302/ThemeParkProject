import numpy as np
import math
import random

class Node:
    def distance(self,Node):
        # return math.ceil(math.sqrt(pow(Node.x - self.x, 2) + pow(Node.y - self.y, 2)))
        return ((self.x - Node.x)**2 + (self.y - Node.y)**2)**0.5
    def __init__(self, i, x, y, o, c, u, t, d_to_s):
        self.i = i
        self.x = x
        self.y = y
        self.o = o
        self.c = c
        self.u = u
        self.t = t
        self.d_to_s = d_to_s
        
    def __repr__(self):
        return "Node " + repr(self.i)
        

              

def read_input():
    
    nodes_array = []
    
    N = int(input())
    
    for j in range(N):
        x, y, o, c, u, t = [int(i) for i in input().split()]
        d_to_s = math.ceil(math.sqrt(pow(x - 200, 2) + pow(y - 200, 2)))
        curr = Node(j, x, y, o, c, u, t, d_to_s)
        nodes_array.append(curr)
    
    
    # for i in range(N):
    #     x = random.randint(0, 400)
    #     y = random.randint(0, 400)
    #     o = random.randint(0, 1440)
    #     c = random.randint(o, 1440)
    #     u = random.randint(0, 27200)
    #     t = random.randint(0, 1000)
    #     d_to_s = math.ceil(math.sqrt(pow(x - 200, 2) + pow(y - 200, 2)))
    #     curr = Node(x, y, o, c, u, t, d_to_s)
    #     nodes_array.append(curr)
    
    # print(nodes_array)
    
    return N, nodes_array


a = Node(1,200,200,12,32,43,54,0)
b = Node(2,200,300,53,6,3,31,100)

# print(a.distance(b))
res = []

def find_path(nodes_array):
    track = []
    backtrack(nodes_array, track, 0)
       
    # print(res)
    max_utility = 0
    max_utility_track = []
    for track in res:

        total_utility = 0
        for node in track:
            total_utility += node.u
        if total_utility > max_utility:
            max_utility = total_utility
            max_utility_track = track
    
    return max_utility, max_utility_track


def backtrack(nodes_array, track, current_time):
    time_left = 1440 - current_time
    # print(track)
    count = 0
    for node in nodes_array:
        if node in track:
            count += 1
            continue
    
        if len(track) != 0:
            if track[-1].distance(node) + node.t + node.d_to_s > time_left:
                count += 1
                continue
            
            if current_time + track[-1].distance(node) < node.o or current_time + track[-1].distance(node) > node.c:
                count += 1
                continue
    
    # print(count)
    
    if count == len(nodes_array):
        # print("+1")
        # print(len(track))
        # print(type(track))
        # print("executed")
        
        res.append(track[:])
        return
        
    for node in nodes_array:
        # if already in track
        if node in track:
            continue
        
        # if don't have enough time to go to next node, play, and go back
        if len(track) != 0:
            if track[-1].distance(node) + node.t + node.d_to_s > time_left:
                continue
            
            # print(current_time)
            # if arrive before opening time or after closing time
            if current_time + track[-1].distance(node) < node.o or current_time + track[-1].distance(node) > node.c:
                continue
        
        # add node to the track
        
        time_distance = 0
        
        if(len(track) != 0):
            time_distance = math.ceil(track[-1].distance(node))
            # print("distance" + str(track[-1].distance(node)))
        
        time = node.t + time_distance
        
        # print("before append" + str(track))
        track.append(node)
        # print("after append" + str(track))
        
        # for node in track:
        #     print("new node")
        #     print(node.x)
        #     print(node.y)
            
        
        # increase the current_time
    
        # print(track[-1])
        # print(node)
        
        
        
        current_time = current_time + time
        
        # decrease the time_left
        
        
        # backtrack the rest of the node
        backtrack(nodes_array, track, current_time)
        
        # reverse all operations
        current_time = current_time - time
        
        
        track.remove(node)
        # print("after remove" + str(track))

# print(find_path(read_input(10)))

def main():
    N, nodes_array = read_input()
    util, util_track = find_path(nodes_array)
    print(util)
    print(util_track)
    
    time_sum = 0
    last = 0


if __name__ == '__main__':
    main()
       
        
    