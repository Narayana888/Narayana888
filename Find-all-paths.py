#!/usr/local/bin/python3
from collections import defaultdict
import ast
import itertools

'''
Step 1: create a graph with every edge being recorded; output all possible routes;
store them into allPaths, a dictionary
find all valid paths that contain information about traffic and distance
'''
# Used by DFS function
path_count = 0
count = 0
allPaths = {}



# This class represents a directed graph
# using adjacency list representaion
class Graph:

    def __init__(self, vertices):
        # number of vertices
        self.V = vertices

        # default dictionary to store graph
        self.Graph = defaultdict(list)

        # default edge length between two vertices
        self.Edge = defaultdict(list)

        # defualt traffic between two vertices
        self.Traffic = defaultdict(list)

    def calEdgeNumber(self, u, v):
        return len(self.Edge[u,v])

    def getEdge(self):
        list = self.Edge
        return list

    def getTrafficBT2nodes(self, u, v):
        return self.Traffic[u,v]

    def getEdgesBT2nodes(self, u, v):
        return self.Edge[u,v]

    # remove the first element of the edge set after it's used
    def setEdge(self, u, v):
        self.Edge[u, v].pop(0)

        # function to add an edge to graph
    def addEdge(self, u, v, distance, traffic):
        self.Graph[u].append(v)

        # in case there are more than one edge between two vertices
        self.Edge[u,v].append(distance)

        self.Traffic[u,v].append(traffic)



    def printAllPathsUntill(self, u, d, visited, path):

        # Mark the current node as visited and store in path
        visited[u] = True
        path.append(u)


        #If current vertex is same as destination, then print current path[]
        if u == d:
            global path_count
            global allPaths
            path_count = path_count + 1
            print(path)
            name = 'path' + str(path_count)
            allPaths[name] = str(path)

        else:
            # If current vertex is not destination,
            # recur for all vertices adjecent to this vertex
            for i in self.Graph[u]:
                if visited[i] == False:
                    self.printAllPathsUntill(i, d, visited, path)

        # remove current vertex from path[] and mark it as unvisited
        path.pop()
        visited[u] = False



    # prints all paths from 's' to 'd'
    def printAllPaths(self, s, d):

        # mark all the vertices as not visited
        visited = [False]*(self.V)

        # create an array to store paths
        path = []

        # call the recursive function to print all paths
        self.printAllPathsUntill(s, d, visited, path)


    def printAllEdges(self, s, e):
        list = self.Edge[s,e]
        return list


# create a graph given in the above diagram
# NOTE: traffic has three string values: "1"--red, "2"--Yello
# "3"--green, denoting degree of traffic stagnancy

g = Graph(6)
g.addEdge(0, 1, 8, 1)
g.addEdge(0, 1, 13, 2)

g.addEdge(0, 2, 8, 3)
g.addEdge(0, 2, 4, 1)

g.addEdge(0, 3, 120, 3)

g.addEdge(0, 4, 12, 1)


g.addEdge(1, 0, 15, 2)

g.addEdge(1, 2, 68, 3)
g.addEdge(1, 2, 21, 3)

g.addEdge(1, 4, 20, 1)
g.addEdge(2, 1, 53, 1)
g.addEdge(2, 3, 12, 2)
g.addEdge(2, 3, 14, 2)
g.addEdge(2, 3, 3, 2)

g.addEdge(2, 4, 32, 1)
g.addEdge(2, 4, 2, 2)

g.addEdge(3, 0, 135, 3)
g.addEdge(3, 2, 12, 3)

g.addEdge(3, 4, 12, 1)
g.addEdge(4, 0, 10, 1)
g.addEdge(4, 1, 7, 2)
g.addEdge(4, 2, 4, 3)
g.addEdge(4, 3, 18, 2)
g.addEdge(4, 5, 89, 1)
g.addEdge(4, 5, 20, 1)
g.addEdge(4, 5, 115, 3)

g.addEdge(5, 4, 15, 1)
g.addEdge(3, 5, 15, 1)
g.addEdge(3, 5, 12, 3)
g.addEdge(5, 3, 6, 1)
g.addEdge(5, 3, 89, 1)

s = 0
d = 5

# prints all paths from any given source to any given destination
for i in range(0,5):
    for j in range(0,5):
        if i != j:
            print("Followings are different paths from %d to %d :" %(i, j))
            g.printAllPaths(i, j)
            print('There are paths in total of: ' + str(path_count))
            path_count = 0
print('\n')
# prints all edges between every two vertices
for i in range(0,5):
    for j in range(0,5):
        if i != j:
            print("Followings are different edges between %d to %d :" %(i, j))
            print(g.printAllEdges(i, j))

    print('\n')


# for key, value in allPaths.items():
#     print(type(allPaths[key])
#
# for key, value in allPaths.items():
#     if len(value) != 5:
#         del allPaths[key]

# convert string representation of path list back to list type
for key, value in allPaths.items():
    allPaths[key] = ast.literal_eval(allPaths[key])

paths = {}
for key, value in allPaths.items():
    if len(value) == 5:
        paths[key] = value

#remove paths with same order to only one so that every path now remaining
#is unique and valid
d2 = {tuple(v): k for k, v in paths.items()}  # exchange keys, values
paths = {v: list(k) for k, v in d2.items()}
print("valid prototype paths below (stored by paths): ")
print(paths)

print('\n')


# permutation of valid paths concerning traffic and distance -- Using trees
# path_permutation stores permutation number for each valid path
path_permutation = {}
def generateAllPaths(proto_paths):

    # for each valid path, find permutation of it
    # calculate number of permutation
    global g
    for key, value in proto_paths.items():
        one_path = value
        num = 1
        for i in range(0, len(one_path) - 1):
            global g
            num = num * g.calEdgeNumber(one_path[i], one_path[i+1])

        global path_permutation
        path_permutation[key] = num



generateAllPaths(paths)
path_permutation = sorted(path_permutation.items())
print('Below is permutation of the prototype of valid paths (stored by path_permutation): ')
print(path_permutation)
print("\n")


'''
Until now, paths stores prototype paths, and path_permutation stores permutation
of each prototype path.
Next step is to calculate every permutation's total distance and total traffic.
By total traffic, we mean the sum of each node pair's traffic
'''


def produceAllPath(paths):

    # Step 2 & 3 function
    def makeList(list, length):
        list = list
        list_edge_path = []
        list_traffic_path = []
        for i in range(0, length-1):
            global g
            list_edge_path.append(g.getEdgesBT2nodes(list[i], list[i+1]))
            list_traffic_path.append(g.getTrafficBT2nodes(list[i], list[i+1]))
        return list_edge_path, list_traffic_path

    # Step 4 function
    def calSum(permutation_distance, permutation_traffic):
        permutation_distance = permutation_distance
        permutation_traffic = permutation_traffic
        permutation_sum_Distance = []
        permutation_sum_Traffic = []
        for list in permutation_distance:
            permutation_sum_Distance.append(sum(list))

        for list in permutation_traffic:
            permutation_sum_Traffic.append(sum(list))

        return permutation_sum_Distance, permutation_sum_Traffic

    # Step 5 function -- return final path dictionary
    def produce(permutation_sum_Distance, permutation_sum_Traffic, length):
        permutation_sum_Distance = permutation_sum_Distance
        permutation_sum_Traffic = permutation_sum_Traffic
        length = length
        count = 1

        while count <= length:
            name = 'path' + str(count)
            global AllPath
            AllPath[name] = {'Satisfaction' : 0,
                             'Distance' : permutation_sum_Distance[count-1],
                             'Traffic' :  permutation_sum_Traffic[count-1]}
            count = count + 1

    # iterate through paths
    for key, value in paths.items():
        length = len(value)
        list_edge_path, list_traffic_path = makeList(value, length)

        # Step 3
        permutation_distance = list(itertools.product(*list_edge_path))
        permutation_traffic = list(itertools.product(*list_traffic_path))

        # Step 4 -- Calculate sum
        permutation_sum_Distance, permutation_sum_Traffic = calSum(permutation_distance, permutation_traffic)

        # Step 5 -- prodocue dictionary
        produce(permutation_sum_Distance, permutation_sum_Traffic, len(permutation_sum_Distance))

AllPath = {}
produceAllPath(paths)
print("Below are Ulatimate ALL PATHS, in total of %d paths: "%len(AllPath))
print(AllPath)



# '''
# Step 2: process every path first by checking 1) if they miss any important bin
# 2) calculate their Urgency value for late use in AHP
#
# # NOTE: all paths are stored in allPaths, this dictionary
# # NOTE: Step 2 is independent of step 1
#
# '''
#
# # input each transhcan site's time and height
#
# class Bins:
#
#     def __init__(self, number):
#
#         # number of bin sites
#         self.N = number
#
#         # default dictionary to store bins
#         self.Bins = defaultdict(list)
#
#
#     def updateBin(self, site_num, time, height):
#
#         # input current status of the bin
#         self.Bins[site_num] = {'height' : height,
#                                'time' : time}
#
#     # calculate the Urgency degree of a particular trashcan
#     def calUrgency(self, site_num):
#
#         # Urgency = 0.4 * time + 0.6 * height
#         t = self.getTime(site_num)
#         h = self.getTime(site_num)
#         value = 0.4 * t + 0.6 * h
#         self.Bins[site_num] = {'urgency' : value }
#
#     def getTime(self, site_num):
#         return self.Bins[site_num]['time']
#
#     def getHeight(self, site_num):
#         return self.Bins[site_num]['height']
#
# # update Bins
# b = Bins(5)
# b.updateBin(1, 10, 3)
# b.updateBin(2, 2, 2)
# b.updateBin(3, 15, 9)
# b.updateBin(4, 1, 7)
# b.updateBin(5, 20, 10)
#
# # calculate each transhcan's Urgency
# for i in range(1, b.N + 1):
#     b.calUrgency(i)
# for i in range(1, b.N + 1):
#     print("trash site %d has an urgency of %.4f" %(i, b.Bins[i]['urgency']))
#
#
#
#
# '''
# Step 3: Use AHP to find the optimal route
# sub-step: 1) auto-generate comparison matrix
#           2) use matrix generated to start AHP
#
# '''
#
# urgency_comparisons = {}
# fuel_comparisons = {}
