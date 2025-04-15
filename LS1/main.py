"""
Main driver script for the simulated annealing algorithm.
"""
import sys
import time
from sa_core import SimulatedAnnealing
from utils import read_instance, write_solution

def main():
    """Main function to parse arguments and run the algorithm."""
    if len(sys.argv) != 4:
        print("Usage: python main.py instance_file solution_file cutoff_time")
        sys.exit(1)

    instance_file = sys.argv[1]
    solution_file = sys.argv[2]
    cutoff_time = float(sys.argv[3])

    # Read instance
    n, subsets = read_instance(instance_file)
    
    # Initialize and run simulated annealing
    sa = SimulatedAnnealing(n, subsets)
    start_time = time.time()
    best_cost, best_solution, trace = sa.solve(cutoff_time, start_time)
    
    # Write solution
    write_solution(solution_file, best_cost, best_solution, trace)

if __name__ == "__main__":
    main() 