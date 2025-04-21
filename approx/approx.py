"""
This approx.py file is the greedy algorithm that approximates the minimum set cover problem. 
It will parse the input file, perform the minimum set cover approximation algorithm, and then 
write its solution as a .sol file in the output directory
"""

import sys
import time
import random
import os

"""
Determine the input size and subsets from the first line of the input file
"""
def parse_input(path):
    with open(path, 'r') as f:
        lines = f.readlines()

        n, m = map(int, lines[0].split())

        subsets = []

        for l in lines[1:]:
            t = list(map(int, l.split()))
            subsets.append(set(t[1:]))
    
    return n, subsets

"""
Perform minimum set cover approximation based on the size and subsets given
"""
def set_cover(n, subsets):
    subsets = list(enumerate(subsets))

    sel_ind = []

    unc = set(range(1, n+1))

    while unc:
        best = max(subsets, key=lambda x: len(x[1] & unc))
        index, s = best

        if not s & unc:
            break
        unc -= s
        subsets.remove(best)
        sel_ind.append(index+1)

    return sel_ind

"""
Main function that calls helper functions to parse inputs, perform minimum set cover approximation, and output results
based on the specified format
"""
def perform_approx(path, time, seed):

    random.seed(seed)

    n, subsets = parse_input(path)
    sel_ind = set_cover(n, subsets)

    inst = path.split('/')[-1].split(".")[0]

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    output_dir = os.path.join(project_root, "output")

    os.makedirs(output_dir, exist_ok=True)

    out_path = os.path.join(output_dir, f"{inst}_Approx_{time}.sol")
    with open(out_path, 'w') as f:
        f.write(f"{len(sel_ind)}\n")
        f.write(" ".join(map(str, sorted(sel_ind))) + "\n")

if __name__ == "__main__":
    perform_approx()