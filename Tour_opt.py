import utils

#global lenth
class InitTour:
    def __init__(self, points, tour, dist):
        self.points = points
        self.tour = tour
        self.endDist = dist
        
    def mapIndex(self, i):
        return i
    
    def getEndDist(self):
        return self.endDist
    
    def swap(self):
        return self.tour
        
class TwoOpt(InitTour):
    
    def __init__(self, parent, start, end):
        self.parent = parent
        self.points = parent.points
        self.tour = parent.tour
        self.start = start
        self.end = end
        self.endDist = self.calcEndDist()
        
    def mapIndex(self, i):
        i = self.parent.mapIndex(i)
        if self.start <= i and i <= self.end:
            #i between start and end, there are an exchange
            return  self.start+(self.end -i)
        else:
            return i
        
    def getEndDist(self):
        return self.endDist
    
    def calcEndDist(self):
        
        # Return the new tour distance if 2-exchange is performed at start, end.
        # In the new tour, the previous point will connect to the end and the start will
        # connect to the next point.
        # (AB) (CD) ---->(AC) (BD)
        #start=B,end=C
        
        
        
        #get distance before exchange
        endDist = self.parent.getEndDist()
        
        
        
        A_index=self.points[self.tour[self.parent.mapIndex(self.start - 1)]]
        B_index=self.points[self.tour[self.parent.mapIndex(self.start)]]
        C_index=self.points[self.tour[self.parent.mapIndex(self.end)]]
        D_index=self.points[self.tour[self.parent.mapIndex((self.end + 1) % len(self.tour))]]
       
        #length AB
        oldStartEdgeLen = utils.length(A_index,B_index )
        #length CD
        oldEndEdgeLen = utils.length(C_index,D_index )
        #length AC 
        newStartEdgeLen = utils.length(A_index, C_index)
        #length BD
        newEndEdgeLen = utils.length(B_index, D_index)
         
         
        
        
        # return distance after exchange
        # new distance=old distance-AB-CD+AC+BD
        return endDist + (newStartEdgeLen - oldStartEdgeLen) + (newEndEdgeLen - oldEndEdgeLen)

    def swap(self):
        self.tour = self.parent.swap()
        # Perform the 2-opt  swap at start, end.
        si, ei = self.start, self.end
        while si < ei:
            self.tour[si], self.tour[ei] = self.tour[ei], self.tour[si]
            si += 1
            ei -= 1
        return self.tour
        