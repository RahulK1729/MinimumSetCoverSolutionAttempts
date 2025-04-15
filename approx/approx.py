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
    with open("data/"+path, 'r') as f:
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

    unc = set(range(1, n+1))

    sel_ind = []

    subsets = list(enumerate(subsets))

    while unc:
        best = max(subsets, key=lambda x: len(x[1] & unc))
        index, s = best

        if not s & unc:
            break
        unc -= s
        sel_ind.append(index+1)
        subsets.remove(best)

    return sel_ind

"""
Write the given solution in the proper format to the proper directory as specified
"""
def write(file, sel_ind):
    with open(file, 'w') as f:
        f.write(f"{len(sel_ind)}\n")
        f.write(" ".join(map(str, sorted(sel_ind))) + "\n")

"""
Main function that calls helper functions to parse inputs, perform minimum set cover approximation, and output results
based on the specified format
"""
def perform_approx(path, time, seed):

    random.seed(seed)

    n, subsets = parse_input(path)
    sel_ind = set_cover(n, subsets)

    inst = path.split('/')[-1].split(".")[0]

    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "output")
    os.makedirs(output_dir, exist_ok=True)

    out_path = os.path.join(output_dir, f"{inst}_Approx_{time}.sol")
    write(out_path, sel_ind)

if __name__ == "__main__":
    perform_approx()