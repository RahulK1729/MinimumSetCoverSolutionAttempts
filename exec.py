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
