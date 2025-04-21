"""
Entry point for running simulated annealing on Minimum Set Cover.
"""
import sys
import time
from LS1.sa_core import SimulatedAnnealing
from LS1.utils import read_instance, write_solution

def main():
    """Process args and run the SA algorithm."""
    # Validate command-line arguments
    if len(sys.argv) != 4:
        print("Usage: python main.py instance_file solution_file cutoff_time")
        sys.exit(1)

    # Parse command line arguments
    inst_file = sys.argv[1]    # Input problem file
    out_file = sys.argv[2]     # Output solution file
    time_limit = float(sys.argv[3])  # Time cutoff in seconds

    # Load problem instance
    n, subsets = read_instance(inst_file)
    
    # Create and run SA solver
    sa = SimulatedAnnealing(n, subsets)
    start = time.time()
    best_cost, best_sol, trace = sa.solve(time_limit, start)
    
    # Write results to output file
    write_solution(out_file, best_cost, best_sol, trace)

if __name__ == "__main__":
    main() 