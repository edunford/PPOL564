# Example Algorithm 1
# Locate Students Near By. 

import math
from matplotlib import pyplot as plt

# %% -----------------------------------------

locations = {"Eric":(0,1),
             "Sean":(2,2),
             "Laila":(0,2),
             "Drew": (3,3),
             "Max":(4,8),
             "Xi":(5,1),
             "Samantha":(3,7),
             "Roxanne":(8,2)}


# %% Locations -----------------------------------------

x_axis = [val[0] for val in locations.values()]
y_axis = [val[1] for val in locations.values()]
plt.figure(figsize=(15,7))
plt.scatter(x_axis,y_axis,c="blue",s=100)


# %% -----------------------------------------


def distance(loc1,loc2):
    '''Calculate the Euclidean Distance'''
    return math.sqrt((loc1[0]-loc2[0])**2 + (loc1[1]-loc2[1])**2)

distance((1,1),(8,8))



locations


def close(locations,dist):
    '''
    Isolate which students are close within some threshold from one another.
    '''

    close_students = []
    for student_1, loc_1 in locations.items():
        for student_2, loc_2 in locations.items():
            if student_1 != student_2:
                if distance(loc_1,loc_2) <= float(dist):
                    close_students.append([student_1,student_2])

    print("Here are the students that are",dist,"away:")
    for pairs in close_students:
        print(pairs[0],"->",pairs[1])


close(locations,dist=1)
