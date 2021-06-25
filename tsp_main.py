import argparse as ap
from BnB import BnB_run
import MstApprox
import LS1solver

from TSP_GA import*

main_parser = ap.ArgumentParser()
main_parser.add_argument('-inst',type = str)
main_parser.add_argument('-alg',type = str)
main_parser.add_argument('-time',type = int, default = 600)
main_parser.add_argument('-seed',type = int, default = 9999)
arguments = main_parser.parse_args()

input_file = "./DATA/" + arguments.inst + ".tsp"

if arguments.alg == 'BnB':
    BnB_run(arguments.inst,arguments.time)
if arguments.alg == 'Approx':
    approx_mst = MstApprox.MstApprox(arguments.inst, arguments.seed, arguments.time)
    approx_mst.generate_tour()
if arguments.alg =='LS1':
    LS1solver.solve_opt(arguments.inst, 'LS1', arguments.time, arguments.seed)
if arguments.alg == 'LS2':
    option=1 #0 if option is to input filename, 1 if option is to input filepath
    if (option):
        filepath=arguments.inst
    else:
        filepath=input_file
    myTSP=TSP_GA_main(filepath,arguments.time,arguments.seed)
    myTSP.console(1)
    # myTSP.log()
    myTSP.writefile()

