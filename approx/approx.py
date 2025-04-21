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

        # form the subsets from which we want to select
        subsets = []

        # make subsets in an integer form where each space separated number is added
        for l in lines[1:]:
            t = list(map(int, l.split()))
            subsets.append(set(t[1:]))
    
    return n, subsets

"""
Perform minimum set cover approximation based on the size and subsets given
"""
def set_cover(n, subsets):
    # form indexed list to make it easier to parse
    subsets = list(enumerate(subsets))

    sel_ind = []

    # uncovered set, initialized to all elements being uncovered
    unc = set(range(1, n+1))

    # continue loop until there is nothing left in uncovered (ie all elements have been covered)
    while unc:
        # find best subset containing the most elements that are also in uncovered set
        best = max(subsets, key=lambda x: len(x[1] & unc))
        index, s = best

        # if there is no best subset, then there is no need to continue the problem, automatically break out
        if not s & unc:
            break

        # remove now covered elements from the uncovered set
        unc -= s

        # remove the selected subset from the list of subsets to choose
        subsets.remove(best)

        # add the index of the subset that we determine as part of the approximation solution
        sel_ind.append(index+1)

    return sel_ind

"""
Main function that calls helper functions to parse inputs, perform minimum set cover approximation, and output results
based on the specified format
"""
def perform_approx(path, time, seed):

    random.seed(seed)

    # perform the approximation algorithm
    n, subsets = parse_input(path)
    sel_ind = set_cover(n, subsets)

    inst = path.split('/')[-1].split(".")[0]

<<<<<<< HEAD
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    output_dir = os.path.join(project_root, "output")

=======
    # add output to its namesake folder in the root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent = os.path.dirname(script_dir)
    output_dir = os.path.join(parent, "output")
>>>>>>> 0ab2fd31769a413d5505fa906dc00696848de11b
    os.makedirs(output_dir, exist_ok=True)

    # name files according to convention and write
    out_path = os.path.join(output_dir, f"{inst}_Approx_{time}.sol")
    with open(out_path, 'w') as f:
        f.write(f"{len(sel_ind)}\n")
        f.write(" ".join(map(str, sorted(sel_ind))) + "\n")

if __name__ == "__main__":
    perform_approx()