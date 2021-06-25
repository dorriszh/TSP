

import utils
import neighborhood
#import twoopt
import threeopt
import os
#import math
#from utils import length



from collections import namedtuple

Point = namedtuple("Point", ["idx", 'x', 'y'])

def solve_opt(file_location,method,cutoff,seed):
    
    
    seed_exist=True
    if seed == 9999:
        seed_exist = False
   
    #file_location='./DATA/' + file_location + '.tsp'
    input_data_file = open(file_location, 'r')
    
    
    #when  optional --->argparse.FileType
    #input_data_file = file_location
   
 
     
    #First line -- city name
    
    parts = input_data_file.readline().split()
    
    cityname=parts[1]
    
    print("City:",cityname)
    
    
    #skip 1 line
    input_data_file.readline()
    
    #Third line ----DIMENSION
    parts = input_data_file.readline().split()             #get DIMENSION
    nodeCount=int(parts[1])
    #print(nodeCount)
      
    
    if seed_exist==False:
        tracefile=cityname+'_'+str(method)+'_'+str(cutoff)
        #tracefile=os.path.abspath(os.path.join(os.path.dirname(file_location),os.path.pardir)) +'/output/'+ cityname+'_'+str(method)+'_'+str(cutoff)
    else:
        tracefile=cityname+'_'+str(method)+'_'+str(cutoff)+'_'+str(seed)
        #tracefile=os.path.abspath(os.path.join(os.path.dirname(file_location),os.path.pardir)) +'/output/'+ cityname+'_'+str(method)+'_'+str(cutoff)+'_'+str(seed)
        
    print(tracefile)
    solfile=tracefile +".sol"
    tracefile=tracefile+".trace"
    
    
     
    tr_ofile = open(tracefile, "w")
    sol_ofile = open(solfile, "w")
    
    
    #skip 2 lines  
    
    input_data_file.readline()
    input_data_file.readline()
      
  
    points = []
    for i in range(0, nodeCount):
        
        parts = input_data_file.readline().split()
        if int(parts[0])!=i+1:
            #Index error
            print("Instance index %s error"%parts[0])
            exit()
        points.append(Point(i, float(parts[1]), float(parts[2])))
        
    utils.lengthCache = [[0.0 for j in range(nodeCount - (i - 1))] for i in range(nodeCount)]
    
    
    input_data_file.close()
#     tour = [0 for i in range(len(points))]
#     
#     totalDist = 0.0
    
    #generate initial tour
        
    totalDist, tour = neighborhood.solve(points)
    #print(totalDist)
    
    #make 2-opt
    #totalDist, tour = twoopt.solve(points, tour, totalDist,tr_ofile,cutoff)
    
    #make 3-opt
    totalDist, tour = threeopt.solve(points, tour, totalDist,tr_ofile,cutoff)
    utils.verifyDist(points, tour, totalDist)
    
    # prepare the solution in the specified output format
    #output_data = "{:.2f}".format(totalDist) + ' ' + str(opt) + '\n'
    output_data = "{:.0f}".format(totalDist)+ '\n'
    output_data += ','.join(map(str, tour))
    
    
    #output to file
    sol_ofile.write(output_data)
    sol_ofile.flush()
    
    #close file
    tr_ofile.close()
    sol_ofile.close()
    
    
    return output_data



