import time
#import utils
import neighborhood
from Tour_opt import InitTour, TwoOpt 

#maxTimeToRun = 30 * 60  #  30 minute





def getBestThreeOpt(points, tour, currentDist, i, j, k):
    
    
    
    
    #####################################################
    #one 2-exchange operation is below:
    #   before:      -->semicycle 0 --->A->B--->semicycle 1--->C->D--->semicycle 0-->
    #   after:       -->semicycle 0 --->A->C--->semicycle 1--->B->D--->semicycle 0-->
    #   in a plane, the half circle Of B--->1 elcycimes--->C flipes 180 degree
    # or reversed the   half circle into C--->1 elcycimes--->B
    #####################################################
    
    # Notes:2-exchange is independent of order
    
    # Find the best 3-Tour_opt sequence out of the 7 possibilities.
    #combinations: C(3,1)+C(3,2)+C(3,3) =7
    # 
    #  i=B  j=C k=E
    #       3 edge  (AB),(CD),(EF)
    #Special case :
    #     if B=C or D=E,3-Opt will degenerate to 2-Opt
    
    
    
    
    ##################################################
    #                                                #
    #                3case one  2-exchange                    #
    #                                                #
    ##################################################
    # case 1: A&F exchange
    #exchange to    (FB),(CD),(EA)
    
    AF_exchg = TwoOpt(InitTour(points, tour, currentDist), i, k)

    bestThreeOptSequence = AF_exchg
    
     
    # case 2: B&C exchange
    #exchange to    (AC),(BD),(EF)
    if i!=j:   
        BC_exchg = TwoOpt(InitTour(points, tour, currentDist), i, j)
        if BC_exchg.getEndDist() < bestThreeOptSequence.getEndDist():
            bestThreeOptSequence = BC_exchg
    
    
    
    # case 3: D&E exchange
    #exchange to    (AB),(CE),(DF)
    if (j+1!=k):
    
        DE_exchg = TwoOpt(InitTour(points, tour, currentDist), j + 1, k)
        if DE_exchg.getEndDist() < bestThreeOptSequence.getEndDist():
            bestThreeOptSequence = DE_exchg
      
        
   
        
        
    ##################################################
    #                                                #
    #          3 case   two sequnece 2-exchange      #
    #                                                #
    ##################################################       
    # case 4:  case 2+ D&E exchange
    #exchange to    (AC),(BE),(DF)
    if   i!=j and k!=j+1:
        BC_DE_exchg = TwoOpt(BC_exchg, j + 1, k)
        if BC_DE_exchg.getEndDist() < bestThreeOptSequence.getEndDist():
            bestThreeOptSequence = BC_DE_exchg
        
        
    # case 5:  case 1+ B&C exchange
    #exchange to    (FC),(BD),(EA)
    if i!=j:      
        AF_BC_exchg = TwoOpt(AF_exchg, i, j)
        if AF_BC_exchg.getEndDist() < bestThreeOptSequence.getEndDist():
            bestThreeOptSequence = AF_BC_exchg
        
        
    # case 6:  case 1+ D&E exchange
    #exchange to    (FB),(CE),(DA)
    if (j+1!=k):    
        AF_DE_exchg = TwoOpt(AF_exchg, j + 1, k)
        if AF_DE_exchg.getEndDist() < bestThreeOptSequence.getEndDist():
            bestThreeOptSequence = AF_DE_exchg
        
    ##################################################
    #                                                #
    #          1 case   three sequnece 2-exchange      #
    #                                                #
    ##################################################            
    # case 7:  case 4+ A&F exchange
    #exchange to    (FC),(BE),(DA)
    if  i!=j and k!=j+1: 
        AF_BC_DE_exchg = TwoOpt(BC_DE_exchg, i, k)
        if AF_BC_DE_exchg.getEndDist() < bestThreeOptSequence.getEndDist():
            bestThreeOptSequence = AF_BC_DE_exchg
            
            
    return bestThreeOptSequence

def solve(points, tour, currentDist,tr_ofile,cutoff=30*60):
#     startTime = int(time.time())
    
    startStepTime = time.time()
#     currentDist, tour = neighborhood.solve(points)
    print("Method:3-opt")
    print("points: " + str(len(tour)) )
    
    print( "Initial tour:")
    print("distance: %.0f"%currentDist)
    print("Tour list:\n",str(tour))
    
    
    
    step = 0
    
    
    
    while True:
        # The best Tour_opt and distance.
        #startStepTime = int(time.time())
        bestDist = currentDist
  
        count = 0
        for i in range(1, len(tour) -1):  
            for j in range(i, len(tour) - 1):
                for k in range( j+1,len(tour)):

                    count += 1 
#                     if((i==(len(tour) -2)) and (j==(len(tour) -2))and (k==(len(tour)-1))):
#                         print("test1")
                    threeOpt = getBestThreeOpt(points, tour, currentDist, i, j, k)

                    if bestDist>threeOpt.getEndDist():
                        bestDist = threeOpt.getEndDist()
                        bestThreeOpt = threeOpt
                    #print(i,j,k,currentDist,bestDist)
        step += 1
        ElapsedTime=time.time() - startStepTime
        print("step: %d count:%d  time:%.2f dist: %.0f"%(step,count,ElapsedTime,bestDist))
        print("%.2f,%.0f"%(ElapsedTime,bestDist),file=tr_ofile)
        if bestDist == currentDist:
            # If no more improvement, we are at a local minima and are done.
            print("no more improvement")
            break
        
#         if bestDist == currentDist:
#             cnt=cnt+1
#             if cnt==3:
#                 # If no more improvement, we are at a local minima and are done.
#                 print("no more improvement")
#                 break
#         else:
#             cnt=0
       
        
        
        # Perform the Tour_opt.
        bestThreeOpt.swap();
        currentDist = bestDist
        if  ElapsedTime > cutoff:
            # Exceed time, return the best we've got.
            print("time end")
            break
    print("end tour\n" + str(tour))
    print("Result Distance:%.0f"%bestDist)
    return bestDist, tour
