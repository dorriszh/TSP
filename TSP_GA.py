# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 19:54:24 2019

@author: Zhengyang Chen
"""

import numpy as np
import random
import sys
import time

class TSP_GA_main():
    
    def __init__(self,filepath,cutoff,seed):
        self.cutoff=cutoff
        self.filepath=filepath
        self.node_num=0; #number of nodes
        self.G=None #Graph
        self.cities=None #list of cities
        self.pop_size=50
        self.pool=None
        self.curdist=0
        self.bestdist=0
        self.curfit=None
        self.c_rate=0.7
        self.m_rate=0.05
        self.fitness=None
        self.maxiter=100000
        self.bestgene=None
        self.timetrace=None
        self.valtrace=None
        self.seed=seed
        
    
    def console(self,flag):
        #if flag==1 begin run
        if flag:
            random.seed(self.seed)
            self.load_data(self.filepath)
            self.pool=self.pop_gen()
            self.fitness=[0 for i in range(self.pop_size)]
            self.timetrace=[]
            self.valtrace=[]
            self.evolution()
    
    #PRINT THE RESULT
    def log(self):
        print(self.bestgene)
        
        if len(self.timetrace)!=len(self.valtrace):
            print('error in tracing')
        
        for i in range(len(self.timetrace)):
            print(self.timetrace[i],',',self.valtrace[i])
    
    def writefile(self):
        
        filepath=self.filepath
        splited=filepath.split('\\' )
        splited=splited[-1]
        splited=splited.split('/')
        splited=splited[-1]
        city=splited.split('.')[0]
        
        print(city)
        if (self.seed==9999):
            Sol_filename='./output/'+city+'_LS2'+'_'+str(self.cutoff)+'.sol'
            Trace_filename='./output/'+city+'_LS2'+'_'+str(self.cutoff)+'.trace'
        else:
            Sol_filename='./output/'+city+'_LS2'+'_'+str(self.cutoff)+'_'+str(self.seed)+'.sol'
            Trace_filename='./output/'+city+'_LS2'+'_'+str(self.cutoff)+'_'+str(self.seed)+'.trace'
        #print(filename)
        sol_file=open(Sol_filename,'w')
        
        strbestgene=''
        for i in range(len(self.bestgene)):
            strbestgene+=str(self.bestgene[i])
            if i<len(self.bestgene)-1:
                strbestgene+=','
                
        #print(strbestgene)
        sol_file.writelines(str(self.bestdist)+'\n')
        sol_file.writelines(strbestgene+'\n')
        sol_file.close()
        
        trace_file=open(Trace_filename,'w')
        
        for i in range(len(self.timetrace)):
            trace_file.writelines(str(round(self.timetrace[i],2))+','+str(self.valtrace[i])+'\n')
        trace_file.close()
        
    
    
    #LOAD DATA FROM TSP FILES
    def load_data(self,filepath):
        print(filepath)
        file=open(filepath,'r')
        
        for i in range(5):
            line=file.readline()
            if i==2:
                self.node_num=int(line.strip().split(' ')[-1])
                
        #create graph
        self.G=[[0 for i in range(self.node_num)] for j in range(self.node_num)]
        self.cities=[0 for i in range(self.node_num)]
        
        for line in file.readlines()[:self.node_num]:
            node_id,node_x,node_y=line.strip().split(' ')
            node_id =int(node_id)-1
            node_x=float(node_x)
            node_y=float(node_y)
            self.cities[node_id]=[node_x,node_y]
        
        #print(self.cities)
    
    #CALCULATE DISTANCE BETWEEN TWO CITIES
    def calc_dist(self,city_1,city_2):
        return int(np.sqrt((city_1[0]-city_2[0])**2+(city_1[1]-city_2[1])**2))
    
    
    def calc_dist_no_round(self,city_1,city_2):
        return np.sqrt((city_1[0]-city_2[0])**2+(city_1[1]-city_2[1])**2)
    
    #CALCULATE TOTAL DISTANCE OF ONE SOLUTION
    def total_dist(self,gene):
        sumDIST=0
        #distance of path from start point to the end point
        for i in range(len(self.cities)-1):
            index1=gene[i]
            index2=gene[i+1]
            dist=self.calc_dist_no_round(self.cities[index1],self.cities[index2])
            sumDIST+=dist
        #add the distance from end point to the start point
        end_start_dist=self.calc_dist_no_round(self.cities[gene[0]],self.cities[gene[-1]])
        sumDIST+=end_start_dist
        sumDIST=int(sumDIST+0.5)
        self.curdist=sumDIST
        #print(gene)
        #print(sumDIST)
        return sumDIST
        
    #generate gene pool
    def pop_gen(self):
        popsize=self.pop_size
        pool=[0 for i in range(popsize)]
        for i in range(popsize):
            gene=[i for i in range(len(self.cities))]
            random.shuffle(gene)
            pool[i]=(gene)
        self.pool=pool
        return pool
    
    #calculate the fitness of current gene pool
    def calc_fitness(self):
        fitness=[]
        for gene in self.pool:
            self.total_dist(gene) #calculate the total distance of current gene
            fit=float(self.bestdist)/float(self.curdist) #calculate fitness
            fitness.append(fit)
        return fitness
    
    #POLICY #1: fitness below average should be replaced
    def select_Darwin(self,pool):
        fitness_np=np.array(self.fitness)
        best_fitness_index=np.argmax(fitness_np)
        avg=np.median(fitness_np,axis=0)
        for i in range(len(self.pool)):
            if i!=best_fitness_index and self.fitness[i]<avg:
                adv_gene=self.cross_OX(pool[best_fitness_index],pool[i])
                adv_gene=self.mutate(adv_gene)
                pool[i]=adv_gene
        
        return pool
    
    #policy #2: low fitness have high probability of being replaced
    def select_RR(self):
        pass
    
    #exchange a gene slice, use Order Crossover
    #reference: https://blog.csdn.net/u012750702/article/details/54563515/
    def cross_OX(self,gene1,gene2):
        #25% not doing cross
        if random.random()>self.c_rate: return gene1
        G_indices=[i for i in range(len(gene1))]
        sample_indices=random.sample(G_indices,2)
        gene_piece=gene2[min(sample_indices):max(sample_indices)]
        
        offspring=[]
        counter=0
               
        for i in range(len(gene1)):
            if counter==min(sample_indices):
                offspring.extend(gene_piece)
                counter=-9999999999 #once gene piece pasted, disable the counter
            if gene1[i] not in gene_piece:
                offspring.append(gene1[i])
                counter+=1
        
        #ERROR HANDELING
        if len(offspring)!=len(gene1):
            print ('cross_OX error')
            regene=[i for i in range(len(gene1))]
            random.shuffle(regene)
            return regene
        
        return offspring
        
        
        
    def mutate(self,gene):
        #small mutation rate
        rv=random.random()
        #print(rv)
        if rv>self.m_rate:return gene
        
        G_indices=[i for i in range(len(gene))]
        sample_indices=random.sample(G_indices,2)
        low=min(sample_indices)
        high=max(sample_indices)
        gene_piece=gene[low:high]
        
        mutate_gene=self.mutate_reverse(gene,low,high)
        #mutate_gene=self.mutate_shuffle(gene,low,high)
        
        if len(mutate_gene)!=len(gene):
            print ('fail to mutate')
            regene=gene
            return regene
        
        return mutate_gene
        
        
    #METHOD1: SHUFFLE THE GENE PIECE    
    def mutate_shuffle(self,gene,low, high):
        if high<low:
            print('mutate_shuffle error')
            return gene
        
        gene_piece=gene[low:high]
        random.shuffle(gene_piece)
        
        newgene=[]
        for i in range(len(gene)):
            if i>low and i<high:
                continue
            if i==low:
                newgene.extend(gene_piece)
                continue
            newgene.append(gene[i])
        return newgene
    
    #METHOD2: REVERSE THE GENE PIECE
    def mutate_reverse(self,gene,low,high):
        if high<low:
            print('mutate_reverse error')
            return gene
        #gene_piece=gene[low:high]
        rev_gene=gene
        rev_gene[low:high]=reversed(rev_gene[low:high])
        #print (rev_gene)
        return rev_gene
    
    #main function
    def evolution(self):
        start_time=time.time()
        for i in range(self.maxiter):
            curtime=time.time()
            if curtime>start_time+self.cutoff:
                break
            fitness_np=np.array(self.fitness)
            best_fitness_index=np.argmax(fitness_np)
            local_best_gene=self.pool[best_fitness_index]
            local_best_dist=self.total_dist(local_best_gene)
            
            worst_fitness_index=np.argmin(fitness_np)
            
            if i==0:
                self.bestgene=local_best_gene
                self.bestdist=local_best_dist
            
            if local_best_dist<self.bestdist:
                temp_timestamp=time.time()
                time_step=temp_timestamp-start_time
                self.timetrace.append(time_step)
                self.bestdist=local_best_dist
                self.valtrace.append(local_best_dist)
            
            else:
                self.pool[worst_fitness_index]=self.bestgene
            
            #SELECT LOW FIT POPS AND EVOLUTION
            self.pool=self.select_Darwin(self.pool)
            self.fitness=self.calc_fitness()
            
            for j in range(self.pop_size):
                k=random.randint(0,self.pop_size-1)
                if j==k: 
                    continue
                self.pool[j]=self.cross_OX(self.pool[j],self.pool[k])
                self.pool[j]=self.mutate(self.pool[j])
            
            #self.bestdist=self.gen_distance(self.bestgene)
        return 0
                
                
            
            
            
        


if __name__=='__main__':
    filepath='DATA/Berlin.tsp'
    myTSP=TSP_GA_main(filepath,10,3)
    myTSP.console(1)
    myTSP.log()
    myTSP.writefile()
    #myTSP.total_dist(myTSP.pool[6])
    #TESTDIST=myTSP.calc_dist(myTSP.cities[1],myTSP.cities[8])
    #print(TESTDIST)
    #TESTPOOL=myTSP.pop_gen(myTSP.pop_size) 
    #print(TESTPOOL)      
        
        

        