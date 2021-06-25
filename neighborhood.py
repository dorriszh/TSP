import sys
import utils
#import random

def findNearestPoint(points,no_used , src):
    # If no nearest point found, return max.
    
    dest = src
    minDist = sys.float_info.max
    
    for i in range(len(points)):
        if   no_used[i]  and  i!=src:

            
            dist = utils.length(points[src], points[i]) 
            if dist < minDist:
                dest =i
                minDist = dist 
    

    return dest, minDist
     
def solve(points):
    #get an initial tour by NearestPoint method
    tour = [0 for i in range(len(points))]
    no_used = [True for i in range(len(points))]
    totalDist = 0.0
    
#     src =int( random.random()*(len(points)-1))
#     no_used[src] = False
#     tour[0]=src
    src =0
    no_used[0] = False
   
    for i in range(1, len(points)):
        dest, minDist = findNearestPoint(points, no_used, src)  #find Nearest Point
        tour[i] = dest
        no_used[dest] = False  #have been used
        src = dest
        totalDist += minDist
        #plus distance between last point and initial point
    return totalDist + utils.length(points[tour[-1]], points[tour[0]]), tour
