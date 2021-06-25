#import utils
import time

from Tour_opt import InitTour, TwoOpt

#maxTimeToRun = 30* 60   #  30 minute

def solve(points, tour, currentDist,tr_ofile,cutoff):
    startTime = int(time.time())
    print("Method:2-opt")
    print("points: " + str(len(tour)))
#     print( "start tour\n" + str(tour))
    print( "Initial tour:")
    print("distance:",round(0.5+currentDist))
    print("Tour list:\n",str(tour))
    
    step = 0
    while True:
        # Calc the best Tour_opt and distance.
        startStepTime = time.time()
        bestDist = currentDist
        bestTwoOpt = None
        count = 0
        for i in range(1, len(tour) - 1):
            for j in range(i + 1, len(tour)):
                count += 1
                # 2-exchange   
                # (AB) (CD)  into
                # (AC) (BD       i=B  j=C
                BC_exchange = TwoOpt(InitTour(points, tour, currentDist), i, j)
                if BC_exchange.getEndDist() < bestDist:
                    bestDist = BC_exchange.getEndDist()
                    bestTwoOpt = BC_exchange
        #step += 1
        ElapsedTime=time.time() - startTime
        print("step: %d count:%d  time:%.2f dist:%.2f"%(step,count,ElapsedTime,round(0.5+bestDist)))
        print("%.2f,%d"%(ElapsedTime,round(0.5+bestDist)),file=tr_ofile)
        #print("%.2f"%(time.time() - startStepTime))
        #print("Tour:%.2f"%bestDist)
        if bestDist == currentDist:
            # If no more improvement we are at a local minima and are done.
            print("no more improvement")
            break
        # Perform the Tour_opt.
        bestTwoOpt.swap();
        currentDist = bestDist
        #solver.outputStep(step, 0, bestDist, tour)
        if  ElapsedTime - startTime > cutoff:
            # Exceed time, return the best we've got.
            print("time end")
            break
        step += 1
    print("end tour\n" , tour)
    print("Result Distance:%d"%round(0.5+bestDist))
    return bestDist, tour
