#!/usr/local/bin/python3
from collections import defaultdict
import ast
import itertools
import ahpy
import random
import scipy.stats as stats
from itertools import islice

'''
There are in general 3 major steps: A) Produce all valid paths with their three
factors being stored; B) Generate comparison matrix; and C) Use AHP to find best path
where each major step can be divided into several sub-steps.

A-1: create a graph with every edge being recorded
store them into allPaths, a dictionary
find all valid paths that contain information about traffic and distance
'''

allPaths = {}
path_count = 1


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
        return len(self.Edge[u, v])

    def getTrafficBT2nodes(self, u, v):
        return self.Traffic[u, v]

    def getEdgesBT2nodes(self, u, v):
        return self.Edge[u, v]

    # remove the first element of the edge set after it's used
    # def setEdge(self, u, v):
    #     self.Edge[u, v].pop(0)

        # function to add an edge to graph
    def addEdge(self, u, v, distance, traffic):
        self.Graph[u].append(v)

        # in case there are more than one edge between two vertices
        self.Edge[u, v].append(distance)

        self.Traffic[u, v].append(traffic)

    def printAllPathsUntill(self, u, d, visited, path):

        # Mark the current node as visited and store in path
        visited[u] = True
        path.append(u)

        # If current vertex is same as destination, then print current path[]
        if u == d:
            global path_count
            global allPaths
            path_count = path_count + 1
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
        visited = [False] * (self.V)

        # create an array to store paths
        path = []

        # call the recursive function to print all paths
        self.printAllPathsUntill(s, d, visited, path)

    def printAllEdges(self, s, e):
        list1 = self.Edge[s, e]
        return list1


'''
A-Step 2: Create class Bin to store each site's height and time

'''


class Bin:

    def __init__(self, number):

        # number of bin sites
        self.number = number

        # default dictionary to store bins
        self.Bins = defaultdict(list)

    # calculate the Urgency degree of a particular trashcan
    def calUrgency(self, site_num):

        # Urgency = 0.4 * time + 0.6 * height
        t = self.getTime(site_num)
        h = self.getTime(site_num)
        value = 0.4 * t + 0.6 * h
        self.Bins[site_num].append(value)

    def updateBin(self, site_num, time, height):
        # site_num = site_num
        # time = time
        # height = height
        # input current status of the bin
        self.Bins[site_num].append(time)
        self.Bins[site_num].append(height)

    def getTime(self, site_num):
        return self.Bins[site_num][0]

    def getHeight(self, site_num):
        return self.Bins[site_num][1]

    def getUrgency(self, site_num):
        return self.Bins[site_num][2]


b = Bin(5)
b.updateBin(0, 1, 80)
b.updateBin(1, 2, 21)
b.updateBin(2, 3, 32)
b.updateBin(3, 4, 34)
b.updateBin(4, 1, 75)

for i in range(0, b.number):
    b.calUrgency(i)

print("There are %d bins in this graph: " % b.number)
for i in range(0, b.number):
    print("This is Bin %d, and its information is as follows: " % i)
    print("Time the trash remains inside: %d" % b.getTime(i))
    print("Height the trash piles up: %d" % b.getHeight(i))
    print("Urgency degree of this bin: %d" % b.getUrgency(i))
    print("\n")

print('\n')
print("------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")


'''
A-2: Create two functions that can generate traffic and distances
'''
# function to generate a random, or multiple values for distance


def assignDistanceAndTraffic(node_i, node_j):
    # stores all distances between two nodes
    list_Distance = []

    # stores all traffics between two nodes, in compliance with the distance list
    list_Traffic = []

    # for each node pair, there will be no more than 3 edges
    num = random.randrange(1, 3, 1)

    # function to generate a random number either 7 or 3 for traffic
    def assignTraffic(times):
        listx = []
        for i in range(times):
            if random.randrange(1, 11, 1) <= 5:
                listx.append(3)
            else:
                listx.append(7)
        return listx

    list_Traffic = assignTraffic(num)

    for i in range(0, num):
        a, b = 1, 15
        mu, sigma = 5, 3
        dist = stats.truncnorm(
            (a - mu) / sigma, (b - mu) / sigma, loc=mu, scale=sigma)

        value = dist.rvs(1)
        result = 0
        result = round(value[0])

        global g
        g.addEdge(node_i, node_j, result, list_Traffic[i])
        # list_Distance.append(result)


# Create a graph given in the above diagram
g = Graph(5)
for i in range(g.V):
    for j in range(g.V):
        if i != j:
            assignDistanceAndTraffic(i, j)


for i in range(g.V):
    for j in range(g.V):
        if i != j:
            length_i_j = len(allPaths)
            g.printAllPaths(i, j)
            length_i_j = len(allPaths) - length_i_j
            print("There are in total of %d paths from %d to %d" %
                  (length_i_j, i, j))


print("The total count of paths, starting from any point to any end, is: %d" %
      (path_count - 1))
print("Length of allPaths: %d" % len(allPaths))
print("Test case: allPaths['path1000']: ", allPaths['path20'])


print("------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")


'''
A-Step 3: Process all possible paths--leave only VALID path--and ultimately store them into [paths]
        Use VALID paths in [paths] to generate permutation of them and assign them corresponding factors:
        Satisfaction, distance, and traffic

'''
# convert string representation of path list back to list type
for key, value in allPaths.items():
    allPaths[key] = ast.literal_eval(allPaths[key])

paths = {}
for key, value in allPaths.items():
    if len(value) == 5:
        paths[key] = value

# remove paths with same order to only one so that every path now remaining
# is unique and valid
d2 = {tuple(v): k for k, v in paths.items()}  # exchange keys, values
paths = {v: list(k) for k, v in d2.items()}
print("Prototype paths below (stored by paths), in total of %d: " % len(paths))
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
            num = num * g.calEdgeNumber(one_path[i], one_path[i + 1])

        global path_permutation
        path_permutation[key] = num


generateAllPaths(paths)
path_permutation = sorted(path_permutation.items())
print('Below are number of permutations for each prototype (stored by path_permutation), in total of %d: ' %
      len(path_permutation))
print(path_permutation)
print("------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")


def produceAllPath(paths):

    # Step 2 & 3 function
    def makeList(list, length):
        list = list
        list_edge_path = []
        list_traffic_path = []
        for i in range(0, length - 1):
            global g
            list_edge_path.append(g.getEdgesBT2nodes(list[i], list[i + 1]))
            list_traffic_path.append(
                g.getTrafficBT2nodes(list[i], list[i + 1]))
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

    def calSatisfaction(path_name, current_path):
        global b
        maximum = 100
        for i in range(0, len(current_path) - 1):
            for j in range(i + 1, len(current_path)):

                # if the former bin's urgency is smaller than latter one's, it means
                # it's not right
                if b.getUrgency(i) < b.getUrgency(j):
                    maximum = maximum - 1
        return maximum

    # Step 5 function -- return final path dictionary
    def produce(permutation_sum_Distance, permutation_sum_Traffic, length, path_name, current_path):
        permutation_sum_Distance = permutation_sum_Distance
        permutation_sum_Traffic = permutation_sum_Traffic
        length = length
        count = 1

        maximum = calSatisfaction(path_name, current_path)

        while count <= length:
            name = 'path' + str(count)
            global AllPath
            AllPath[name] = {'Satisfaction': maximum,
                             'Distance': permutation_sum_Distance[count - 1],
                             'Traffic':  permutation_sum_Traffic[count - 1]}
            count = count + 1

    # iterate through paths
    for key, value in paths.items():
        length = len(value)
        list_edge_path, list_traffic_path = makeList(value, length)

        # Step 3
        permutation_distance = list(itertools.product(*list_edge_path))
        permutation_traffic = list(itertools.product(*list_traffic_path))

        # Step 4 -- Calculate sum
        permutation_sum_Distance, permutation_sum_Traffic = calSum(
            permutation_distance, permutation_traffic)

        # Step 5 -- prodocue dictionary
        produce(permutation_sum_Distance, permutation_sum_Traffic,
                len(permutation_sum_Distance), key, value)


AllPath = {}
produceAllPath(paths)
print("Below are ULTIMATE VALID PATHS, in a total number of %d (stored in AllPath): " % len(AllPath))
print(AllPath)
print("\n")
print("------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")


'''
C:


'''


def chunks(data, SIZE=10000):
    it = iter(data)
    for i in range(0, len(data), SIZE):
        yield {k: data[k] for k in islice(it, SIZE)}

# function used to generate comparison matrix


def make_cmp(list, cmp_obj):

    traffic_comparisons = {}
    distance_comparisons = {}
    satisfaction_comparisons = {}

    for path in list:
        for anopath in list:
            if path[0] >= anopath[0]:
                continue

            if path[1] > anopath[1]:
                dif = (path[1] - anopath[1]) / (path[1] + anopath[1]) * 10
                dif = round(dif)
                if dif < 1:
                    dif = 1
                if dif > 3:
                    dif = 3

                if cmp_obj == 'traffic':
                    traffic_comparisons[path[0], anopath[0]] = dif

                if cmp_obj == 'distance':
                    distance_comparisons[path[0], anopath[0]] = dif

                if cmp_obj == 'satisfaction':
                    satisfaction_comparisons[path[0], anopath[0]] = dif

            else:
                dif = (anopath[1] - path[1]) / (path[1] + anopath[1]) * 10
                dif = round(dif)
                if dif == 0:
                    dif = 1
                if dif > 3:
                    dif = 3
                dif = 1 / dif

                if cmp_obj == 'traffic':
                    traffic_comparisons[path[0], anopath[0]] = dif

                if cmp_obj == 'distance':
                    distance_comparisons[path[0], anopath[0]] = dif

                if cmp_obj == 'satisfaction':
                    satisfaction_comparisons[path[0], anopath[0]] = dif

    if cmp_obj == 'satisfaction':
        return satisfaction_comparisons

    if cmp_obj == 'distance':
        return distance_comparisons

    if cmp_obj == 'traffic':
        return traffic_comparisons


def storeAllSatisfaction(AllPath):
    all_satisfaction = {}
    for key, value in AllPath.items():
        for key2, value2 in value.items():
            if key2 == 'Satisfaction':
                all_satisfaction[key] = value2
                break
    all_satisfaction = sorted(all_satisfaction.items())
    print('The ordered path series with each corresponding to their satisfaction: ')
    print(all_satisfaction)
    return all_satisfaction


def storeAllDistance(AllPath):
    all_distance = {}
    for key, value in AllPath.items():
        for key2, value2 in value.items():
            if key2 == 'Distance':
                all_distance[key] = value2
                break
    all_distance = sorted(all_distance.items())
    print('The ordered path series with each corresponding to their Distance: ')
    print(all_distance)
    return all_distance


def storeAllTraffic(AllPath):
    all_traffic = {}
    for key, value in AllPath.items():
        for key2, value2 in value.items():
            if key2 == 'Traffic':
                all_traffic[key] = value2
                break
    all_traffic = sorted(all_traffic.items())
    print('The ordered path series with each corresponding to their Traffic: ')
    print(all_traffic)
    return all_traffic


def getBestPath(d):

    count = 1
    for item in chunks(d, 5):
        one_group = {}
        one_group = item
        if len(one_group) <= 1:
            return
        print("Below is the process of generating comparison matrix for this path division %d: \n" % count)
        print("For this round, the paths to be processed are as follows: ")
        print(one_group)

        count = count + 1

        all_satisfaction = storeAllSatisfaction(one_group)
        all_distance = storeAllDistance(one_group)
        all_traffic = storeAllTraffic(one_group)

        satisfaction_comparisons = {}
        distance_comparisons = {}
        traffic_comparisons = {}

        satisfaction_comparisons = make_cmp(all_satisfaction, 'satisfaction')
        distance_comparisons = make_cmp(all_distance, 'distance')
        traffic_comparisons = make_cmp(all_traffic, 'traffic')

        print('comparison matrix for satisfaction: ')
        print(satisfaction_comparisons)
        print('comparison matrix for distance: ')
        print(distance_comparisons)
        print('comparison matrix for traffic: ')
        print(traffic_comparisons)
        print('\n')

        criteria_comparisons = {('distance', 'satisfaction'): 7,
                                ('distance', 'traffic'): 4, ('traffic', 'satisfaction'): 4}
        print('comparison matrix for criteria: ')
        print(criteria_comparisons)

        print("The resulting optimal path in this round: ")
        satisfaction = ahpy.Compare(
            'satisfaction', satisfaction_comparisons, precision=3, random_index='dd')
        distance = ahpy.Compare(
            'distance', distance_comparisons, precision=3, random_index='dd')
        traffic = ahpy.Compare(
            'traffic', traffic_comparisons, precision=3, random_index='dd')
        criteria = ahpy.Compare(
            'Criteria', criteria_comparisons, precision=3, random_index='dd')
        criteria.add_children([satisfaction, traffic, distance])

        print(criteria.target_weights)
        report = criteria.report(show=True)
        print(report)
        print("\n")
        print("------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")


getBestPath(AllPath)


'''
3: Take the comparison in every path division into AHP and get the optimal one
   And then take all optimal paths into the AHP again to get global optimum

'''

local_optimum_path_name = []
local_optimum_path_name.append('path1')
local_optimum_path_name.append('path10')
local_optimum_path_name.append('path14')


local_optimum_path = {}

# find local optimum through original path storage and store them into a new
# dictionary called local_optimum_path
for key, value in AllPath.items():
    for name in local_optimum_path_name:
        if name == key:
            local_optimum_path[key] = value
print("All local optimums: ")
print(local_optimum_path)

print("Take all local optimums into AHP again to find the ultimat path...")
print("The ultimate global optimum is as follows")

getBestPath(local_optimum_path)
