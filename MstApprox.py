# Class which implements the MST Approximation algorithm
import numpy as np
import math
import sys
import timeit

class MstApprox:

    def __init__(self,instance,seed,limit=600):
        self.city = instance
        if seed==9999:
            self.random_seed = 0
            self.userinput_exist = False
        else:
            self.random_seed = seed
            self.userinput_exist = True

        self.cutoff_time = limit
        self.inf=float("inf")
        self.path = []
        self.total=0.0

    def mst(self,graph):
        #find the minimum spaning tree, and output the edge path set plus reverse edge path set
        G = np.array(graph)
        E = []
        visited = [0]

        while len(visited) < len(graph):
            (row,col) = np.unravel_index(G[visited].argmin(),G[visited].shape)

            visited.append(col)
            E.append((visited[row],col))
        
            s = [(col,v) for v in visited]
            for (k,v) in s:
                G[k][v] = self.inf
                G[v][k] = self.inf

        #duplicate mst
        E2 = [(y,x) for (x,y) in E]
        E.extend(E2)

        return E

    def generate_path(self, E, parent):
        if parent not in self.path:
            self.path.append(parent)
            child = []
            for item in E:
                if item[0]==parent:
                    child.append(item[1])
            if len(child) > 0 :
                for node in child:
                    self.generate_path(E,node)
            else:
                return

    def walk(self,G):
        Output = []
        for i in range(0,len(self.path)-1):
            dist = G[self.path[i]][self.path[i+1]]
            Output.append((self.path[i],self.path[i+1],dist))
            self.total += dist
        dist = G[self.path[-1]][self.path[0]]
        Output.append((self.path[-1],self.path[0],dist))
        self.total+=dist
        return Output

    def read_data(self):
        L = []
        with open('./DATA/'+self.city+'.tsp') as f:
            next(f)
            next(f)
            next(f)
            next(f)
            next(f)
            for line in f:
                if line == 'EOF\n':
                    break
                l=line[:-1].split(' ')
                #print line
                L.append({'x':float(l[1]),'y':float(l[2])})

            n = len(L)
            G = np.zeros((n,n))

            for i in range(n):
                for j in range(n):
                    if i == j:
                        G[i][j] = self.inf
                    else:
                        G[i][j] = int(round(math.sqrt((L[i]['x'] - L[j]['x']) ** 2 + (L[i]['y'] - L[j]['y']) ** 2)))
        return G


    def write_sol(self,output,total):
        total = (str)((int)(total))
        if self.userinput_exist==True:
            with open('output/' + self.city + "_Approx_" + str(self.cutoff_time) + "_" + str(self.random_seed) + '.sol',
                      'w') as f:
                f.write(total)
                f.write('\n')
                for i in range(len(output) - 1):
                    f.write(str(output[i][0]) + ',')
                f.write(str(output[-1][0]))
        else:
            with open('output/' + self.city + "_Approx_" + str(self.cutoff_time) + '.sol',
                      'w') as f:
                f.write(total)
                f.write('\n')
                for i in range(len(output) - 1):
                    f.write(str(output[i][0]) + ',')
                f.write(str(output[-1][0]))

            

    def write_trace(self,time,total):
        if self.userinput_exist == True:
            with open(
                    'Output/' + self.city + "_Approx_" + str(self.cutoff_time) + "_" + str(self.random_seed) + '.trace',
                    'w') as f:
                f.write('{:.2f},{}\n'.format(time, total))
        else:
            with open(
                    'Output/' + self.city + "_Approx_" + str(self.cutoff_time) + '.trace',
                    'w') as f:
                f.write('{:.2f},{}\n'.format(time, total))



    def generate_tour(self):
        start = timeit.default_timer()
        graph = self.read_data()
        edge = self.mst(graph)
        self.generate_path(edge,self.random_seed)
        output = self.walk(graph)
        stop = timeit.default_timer()
        self.write_trace(stop-start,int(self.total))
        self.write_sol(output,self.total)

