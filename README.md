Author          : Ruixuan Zhang
Created         : Dec 3, 2019
Last Modified   : Dec 3, 2019

Affiliation          : Georgia Institute of Technology


Description
-------------

This program is to solve the Travelling Salesman problem using 4 different algorithms (Branch-and-Bound as exact algorithm, Mst-Approx as Construction Heuristcs, LS1 (Neighborhood 3-opt exchange) and LS2 (Genetic Algorithm) as Local Search).


The input file has the following form:

NAME: Atlanta 
COMMENT: 20 locations in Atlanta
DIMENSION: 20 
EDGE_WEIGHT_TYPE: EUC_2D 
NODE_COORD_SECTION 
1 33665568.000000 -84411070.000000 
2 33764940.000000 -84371819.000000 
.......
Where the first five lines represent the name of the city, simple comment, dimension (number of cities), edge weight type (distance) and NODE_COORD_SECTION.
From the sixth line, the first column indicates the ID (int) of locations, while the second indicates the x coordinates and the third indicates the y coordinates (both are float). Columns are separated by spaces.


We have two output files. One is .sol and the other one is .trace.

The solution file has the following format:
File name: <instance>_<method>_<cutoff>[_<random_seed>].sol, e.g. Atlanta_BnB_600.sol. 

	line 1: QUALITY_OF_THE_BEST_SOLUTION_FOUND
	line 2: list of vertex IDs of the TSP tour (comma-separated and without spaces)

The solution trace file has the following format:
File name: <instance>_<method>_<cutoff>[_<random_seed>].trace, e.g. Atlanta_BnB_600.trace. 

	TIMESTAMP,SOL_AT_THAT_TIME

There are two columns. The first column is a timestamp in CPU seconds (to two decimal places), after comma followed by quality of the best found solution at that point in time (integer), that is, the record when every time a new improved solution is found. 



Execution
-----------

There are 9 Python files in our code package.
BnB.py is for performance of BnB, MstApprox.py is for Mst-approx heuristics, TSP_GA.py for Genetic Algorithm(LS2),LS1Solver.py,neighborhood.py,threeopt.py,Tour_opt.py, utils.py for 3-opt(LS1)

The executable is named tsp_main.py, to run the code, simply use

    tsp_main[.py] -inst <filename> -alg [BnB | Approx | LS1 | LS2] -time <cutoff_in_seconds> [-seed <random_seed>]

Specifically, the filename should be the filepath of a simple input instance, the four choice of -alg are BnB, Approx, LS1, LS2. The random_seed is optional for deterministic algorithms (BnB and LS1 in our program).

    


