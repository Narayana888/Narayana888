#!/usr/local/bin/python3
'''
Step 2 - Auto-generate comparison matrix where it takes urgency degree and
distance as criteria

The rule to calculate Saaty value is by subtracting the smaller value
from larger one and then dividing it up by their sum and multiply the result
by 10. Finally we round the result to get the integer in Saaty Scale.
'''
allPaths = {'path1': {'Satisfaction': 1, 'Distance': 99, 'Traffic': 8}, 'path2': {'Satisfaction': 1, 'Distance': 101, 'Traffic': 8}, 'path3': {'Satisfaction': 1, 'Distance': 90, 'Traffic': 8}, 'path4': {'Satisfaction': 1, 'Distance': 52, 'Traffic': 8}, 'path5': {'Satisfaction': 1, 'Distance': 54, 'Traffic': 8}, 'path6': {'Satisfaction': 1, 'Distance': 43, 'Traffic': 8}, 'path7': {'Satisfaction': 1, 'Distance': 105, 'Traffic': 7}, 'path8': {'Satisfaction': 1, 'Distance': 188, 'Traffic': 7}, 'path9': {'Satisfaction': 1, 'Distance': 36, 'Traffic': 7}, 'path10': {'Satisfaction': 1, 'Distance': 119, 'Traffic': 7}, 'path11': {'Satisfaction': 1, 'Distance': 131, 'Traffic': 9}, 'path12': {'Satisfaction': 1, 'Distance': 214, 'Traffic': 9}, 'path13': {'Satisfaction': 1, 'Distance': 131, 'Traffic': 4}, 'path14': {'Satisfaction': 1, 'Distance': 214, 'Traffic': 4}, 'path15': {'Satisfaction': 1, 'Distance': 62, 'Traffic': 4}, 'path16': {'Satisfaction': 1, 'Distance': 145, 'Traffic': 4}, 'path17': {'Satisfaction': 1, 'Distance': 157, 'Traffic': 6}, 'path18': {'Satisfaction': 1, 'Distance': 240, 'Traffic': 6}, 'path19': {'Satisfaction': 1, 'Distance': 101, 'Traffic': 5}, 'path20': {'Satisfaction': 1, 'Distance': 184, 'Traffic': 5}, 'path21': {'Satisfaction': 1, 'Distance': 32, 'Traffic': 5}, 'path22': {'Satisfaction': 1, 'Distance': 115, 'Traffic': 5}, 'path23': {'Satisfaction': 1, 'Distance': 127, 'Traffic': 7}, 'path24': {'Satisfaction': 1, 'Distance': 210, 'Traffic': 7}}


traffic_comparisons = {}
distance_comparisons = {}
satisfaction_comparisons = {}

# function used to generate comparison matrix

def make_cmp(list, cmp_obj):
    for path in list:
        for anopath in list:
            if path[0] >= anopath[0]:
                continue

            global traffic_comparisons
            global distance_comparisons
            global satisfaction_comparisons

            if path[1] > anopath[1]:
                dif = (path[1] - anopath[1]) / (path[1] + anopath[1]) * 10
                dif = round(dif)
                if dif < 1:
                    dif = 1
                if dif > 9:
                    dif = 9

                if(cmp_obj == 'traffic'):
                    traffic_comparisons[path[0], anopath[0]] = dif

                if(cmp_obj == 'distance'):
                    distance_comparisons[path[0], anopath[0]] = dif

                if(cmp_obj == 'satisfaction'):
                    satisfaction_comparisons[path[0], anopath[0]] = dif


            else:
                dif = (anopath[1] - path[1]) / (path[1] + anopath[1]) * 10
                dif = round(dif)
                if dif == 0:
                    dif = 1
                if dif > 9:
                    dif = 9
                dif = 1/dif

                if(cmp_obj == 'traffic'):
                    traffic_comparisons[path[0], anopath[0]] = dif

                if(cmp_obj == 'distance'):
                    distance_comparisons[path[0], anopath[0]] = dif

                if(cmp_obj == 'satisfaction'):
                    satisfaction_comparisons[path[0], anopath[0]] = dif




all_traffic = {}
all_distance = {}
all_satisfaction = {}

# store all paths' satisfaction
for key, value in allPaths.items():
    for key2, value2 in value.items():
        if key2 == 'Satisfaction':
            all_satisfaction[key] = value2
            break

# store all paths' distance
for key, value in allPaths.items():
    for key2, value2 in value.items():
        if key2 == 'Distance':
            all_distance[key] = value2
            break


# store all paths' traffic
for key, value in allPaths.items():
    for key2, value2 in value.items():
        if key2 == 'Traffic':
            all_traffic[key] = value2
            break

# print('Distance for each path: ' )
# print(all_distance)
# print('\n')

all_satisfaction = sorted(all_satisfaction.items())
all_distance = sorted(all_distance.items())
all_traffic = sorted(all_traffic.items())
print('The ordered path series with each corresponding to their satisfaction: ')
print(all_satisfaction)
print('The ordered path series with each corresponding to their distance: ')
print(all_distance)
print('\n')
print('The ordered path series with each corresponding to their traffic: ')
print(all_traffic)
print('\n')

# make comparisons for two criteria
make_cmp(all_satisfaction, 'satisfaction')
make_cmp(all_distance, 'distance')
make_cmp(all_traffic, 'traffic')

# print out comparison matrix
print('comparison matrix for satisfaction: ')
print(satisfaction_comparisons)
print('comparison matrix for distance: ')
print(distance_comparisons)
print('comparison matrix for traffic: ')
print(traffic_comparisons)
print('\n')

# print comparison matrix with criteria vs. goal
criteria_comparisons = {('distance', 'satisfaction'): 7, ('distance', 'traffic'): 4, ('traffic', 'satisfaction'): 4  }
print('comparison matrix for criteria: ')
print(criteria_comparisons)
