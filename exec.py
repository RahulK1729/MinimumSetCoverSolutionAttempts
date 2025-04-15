# exec.py
import argparse
import time
import os
from bnb.utils import read_instance, write_solution, write_trace
from bnb.bnb import branch_and_bound
from approx.approx import perform_approx
import sys

if __name__ == "__main__":
    sys.setrecursionlimit(100000)

    parser = argparse.ArgumentParser()
    parser.add_argument("-inst", type=str)
    parser.add_argument("-alg", type=str, choices=["BnB", "Approx", "LS1", "LS2"])
    parser.add_argument("-time", type=int)
    parser.add_argument("-seed", type=int, default=None)
    args = parser.parse_args()

    instance_name = os.path.basename(args.inst).split('.')[0]
    file_path = os.path.join("data", args.inst)
    n, subsets = read_instance(file_path)

    os.makedirs("output", exist_ok=True)
    start_time = time.time()

    if args.alg == "BnB":
        best_score, best_set, trace = branch_and_bound(n, subsets, args.time, start_time)
        write_solution(instance_name, args.alg, args.time, best_score, best_set)
        write_trace(instance_name, args.alg, args.time, 