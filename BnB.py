# Implementation of Branch and Bound method for Travelling Salesman Problem (TSP)
# for CSE 6140
# Created by Yi Ji (yji76) 
# Nov 2019


# Import modules
import time
import numpy 


class BnB:
 
    def __init__(self, tsp_file):
        #
        dist_matx, dimension = self.read_data(tsp_file)
        self.dist_matx = dist_matx
        self.dimension = dimension 
    
    def distance(self,u,v):
        #
        return ((u[0] - v[0])**2 + (u[1] - v[1])**2)**0.5

    def read_data(self, tsp_file):
        #
        with open(tsp_file, 'r') as file:
            dimension = 0
            coordinates = []
            dist_matx = []
            is_read = False

            for line in file:
                if "DIMENSION" in line:
                    Dimen, dimen = line.split(': ')
                    dimension = int(dimen)
                elif "NODE_COORD_SECTION" in line:
                    is_read = True
                elif is_read == True:
                    if "EOF" not in line:
                        ind = line.split(' ')[0]
                        x = line.split(' ')[1]
                        y = line.split(' ')[2]
                        x = float(x)
                        y = float(y)
                        coordinate = []
                        coordinate.append(x)
                        coordinate.append(y)
                        coordinates.append(coordinate)
                    else:
                        break
                else:
                    continue

        for v in coordinates:
            distances = []
            for u in coordinates:
                distance = round(self.distance(u,v))
                distances.append(distance)
            dist_matx.append(distances)
        dist_matx = numpy.array(dist_matx, dtype=float)
        
        for i in range(dimension):
            dist_matx[i, i] = float("inf")

        return dist_matx, dimension

    
    def reduce_matrix(self, dist_matx):
        #
        red_matx = numpy.copy(dist_matx)
        row = red_matx.shape[0]
        row_min = numpy.amin(red_matx, axis=1) # find minimum in each row
        row_min[row_min==float("inf")] = 0 
        row_min_trans = row_min.reshape(row, 1)
        red_matx = red_matx - row_min_trans
        col_min = numpy.amin(red_matx, axis=0)
        col_min[col_min==float("inf")] = 0
        red_matx = red_matx - col_min

        row_reduced = numpy.sum(row_min)
        col_reduced = numpy.sum(col_min)
        lower_bound = row_reduced + col_reduced
        return red_matx, lower_bound

    def next_edge(self, reduced_matx):
        ##
        zero_coordinates = numpy.where(reduced_matx == 0)
        row_zero, col_zero = zero_coordinates
        num_of_zero = len(row_zero)
        if num_of_zero == 0:
            return None, None
        else:
            minsum = []
            for i in range(num_of_zero):
                matrix = numpy.copy(reduced_matx)
                row = matrix[row_zero[i],:] 
                col = matrix[:,col_zero[i]] 
                row[col_zero[i]] = float("inf") 
                col[row_zero[i]] = float("inf") 
                
                row_min = numpy.amin(row)
                col_min = numpy.amin(col)
                sum_min = row_min + col_min

                matrix[row_zero[i],:] = float("inf")
                matrix[:,col_zero[i]] = float("inf")
                minsum.append(sum_min)
            
            j = numpy.argmax(minsum)
            x = row_zero[j]
            y = col_zero[j]
            
        return x,y  

    def search(self, cutoff):
        best_path = None
        lowest_cost = float("inf")

        stack = []
        red_matx = self.reduce_matrix(self.dist_matx)[0]
        lower_bound = self.reduce_matrix(self.dist_matx)[1]
        
        node_dict = {"reduced_matrix": red_matx, "lb": lower_bound, "p": []}
        stack.append(node_dict)

        trace = []

        start_time = time.time()
        isContinues = True
        while stack and isContinues:
            isChanged = False

            node_dict = stack.pop()
            # if the lower_bound bound is greater than the best_path length, drop this node_dict
            if node_dict["lb"] > lowest_cost:
                continue

            # check whether the node_dict is a leaf
            if len(node_dict["p"]) == self.dimension:
                # format the tour, and chech whether it is a valid tour
                is_com_tour, tour = self.complete_tour(node_dict["p"])
                if is_com_tour and node_dict["lb"] < lowest_cost:
                    best_path = tour
                    lowest_cost = node_dict["lb"]
                    isChanged = True
            else:
                red_matx = numpy.copy(node_dict["reduced_matrix"])
                u, v = self.next_edge(red_matx)
                if u == None: # if cannot select an edge, drop this node_dict
                    continue
                l_branch, r_branch = self.expand(node_dict, u, v)
                stack.append(r_branch)
                stack.append(l_branch)

            t = time.time() - start_time
            if t > cutoff:
                isContinues = False

            if isChanged:
                trace.append((t, lowest_cost))

        return best_path, lowest_cost, trace


    def expand(self, node_dict, u, v):
        #
        lower_bound = node_dict["lb"]
        left_m = numpy.copy(node_dict["reduced_matrix"])
        left_m[u, :] = float("inf")
        left_m[:, v] = float("inf")
        left_m[v, u] = float("inf")
        left_p = node_dict["p"][:]
        left_p.append((u, v))
        left_r_mat, left_lb = self.reduce_matrix(left_m)
        l_branch = {"reduced_matrix": left_r_mat, "lb": lower_bound + left_lb, "p": left_p}

        right_m = numpy.copy(node_dict["reduced_matrix"])
        right_m[u, v] = float("inf")
        right_p = node_dict["p"][:]
        right_r_mat, right_lb = self.reduce_matrix(right_m)
        r_branch = {"reduced_matrix": right_r_mat, "lb": lower_bound + right_lb, "p": right_p}
        return l_branch, r_branch
    


    def complete_tour(self, path):
        #
            node_dict = dict(path)
            curr_tour = [0]
            l = len(path)
            d = self.dimension
            i = 0
            while i < l:
                next_vertex = node_dict[curr_tour[i]]
                if next_vertex not in curr_tour:
                    curr_tour.append(next_vertex)
                elif i < d - 1:
                        is_com_tour = False
                        return is_com_tour, curr_tour
                else:
                        print ("get leaf node")
                        is_com_tour = True
                        return is_com_tour, curr_tour
                i = i+1


def BnB_run(city,cutoff):
    input_path = "./DATA/" + city + ".tsp"
    ouput_path_tour = "./output/" + city + "_BnB_" + str(cutoff) + ".sol"
    ouput_path_trace = "./output/" + city + "_BnB_" + str(cutoff) + ".trace"
    city_file = BnB(input_path)
    tour, length, trace = city_file.search(cutoff)
    with open(ouput_path_tour, 'a') as tour_file:
        if length == float("inf"):
            tour_file.write("inf")
        else:
            tour_file.write(str(int(length)) + "\n")
        for vertex in tour[0:(len(tour)-1)]:
            tour_file.write(str(int(vertex)) + ",")
        tour_file.write(str(tour[-1]))
    with open(ouput_path_trace, 'a') as trace_file:
        for record in trace:
            trace_file.write(str("%.2f"%record[0]) + ", " + str(int(record[1])) + "\n")