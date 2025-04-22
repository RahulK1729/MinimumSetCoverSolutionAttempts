"""
This file is responsible for taking in the input from terminal as specified in the instructions document and assigning
the job to the specified algorithm.
"""

import argparse
import os
import time
import sys
from bnb.utils import read_instance, write_solution, write_trace
from bnb.bnb import branch_and_bound
from approx.approx import perform_approx
from LS2.hillclimbing import LS2
from LS1.sa_core import SimulatedAnnealing


"""
Perform the specified algorithm once on that particular instance
"""
def run_single_instance(inst_path, alg, time_limit, seed):
    instance_name = os.path.basename(inst_path).split('.')[0]
    n, subsets = read_instance(inst_path)

    os.makedirs("output", exist_ok=True)
    start_time = time.time()

    if alg == "BnB":
        best_score, best_set, trace = branch_and_bound(n, subsets, time_limit, start_time)
        write_solution(instance_name, alg, time_limit, best_score, best_set)
        write_trace(instance_name, alg, time_limit, trace)
    elif alg == "Approx":
        perform_approx(inst_path, time_limit, seed)
    elif alg == "LS1":
        # Run Simulated Annealing algorithm
        sa = SimulatedAnnealing(n, subsets, seed=seed)
        best_score, best_set, trace = sa.solve(time_limit, start_time)
        
        # Print runtime information
        end_time = time.time()
        runtime = end_time - start_time
        print(f"LS1 completed in {runtime:.2f} seconds with score {best_score}")
        
        # Write solution and trace files
        write_solution(instance_name, alg, time_limit, best_score, best_set, seed)
        write_trace(instance_name, alg, time_limit, trace, seed)
    elif alg == "LS2":
        best_score, best_set, trace = LS2(n, subsets, time_limit, start_time)
        write_solution(instance_name, alg, time_limit, best_score, best_set, seed)
        write_trace(instance_name, alg, time_limit, trace, seed)
    else:
        print(f"Algorithm {alg} not implemented.")

"""
Determine user input from terminal, parse it, and then run a loop through each .in file in the directory specified in -inst argument,
performing the specified algorithm from -alg on it using the run_single_instance() function
"""
def main():
    sys.setrecursionlimit(100000)
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-inst", type=str, required=True)
    parser.add_argument("-alg", type=str, required=True, choices=["BnB", "Approx", "LS1", "LS2"])
    parser.add_argument("-time", type=int, required=True)
    parser.add_argument("-seed", type=int, default=42)
    args = parser.parse_args()

    inst_path = args.inst
    if os.path.isdir(inst_path):
        for in_file in sorted(os.listdir(inst_path)):
            if not in_file.endswith(".in"):
                continue

            print(f"Running {args.alg} on: {in_file} with {args.time}s cutoff")
            run_single_instance(os.path.join(inst_path, in_file), args.alg, args.time, args.seed)
    elif os.path.isfile(inst_path):
        run_single_instance(inst_path, args.alg, args.time, args.seed)
    else:
        print(f"{inst_path} not valid")

if __name__ == "__main__":
    main()
