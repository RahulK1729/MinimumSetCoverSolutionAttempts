"""
File handling utilities for the Minimum Set Cover problem.
"""

def read_instance(filename):
    """Parse problem instance from file."""
    with open(filename, 'r') as f:
        # Get universe size and subset count
        n, m = map(int, f.readline().strip().split())
        
        # Read each subset
        subsets = []
        for _ in range(m):
            # Convert line to set of integers
            subset = set(map(int, f.readline().strip().split()))
            subsets.append(subset)
            
    return n, subsets

def write_solution(filename, obj_value, solution, trace):
    """Save solution to output file."""
    with open(filename, 'w') as f:
        # Write objective value (number of sets)
        f.write(f"{obj_value}\n")
        
        # Write selected set indices (1-indexed)
        f.write(" ".join(map(str, [i + 1 for i in solution])) + "\n")
        
        # Write trace data
        for timestamp, value in trace:
            f.write(f"{timestamp:.2f},{value}\n")

def write_trace(filename, trace):
    """Save execution trace to file."""
    with open(filename, 'w') as f:
        # Each line has timestamp and solution value
        for timestamp, value in trace:
            f.write(f"{timestamp:.2f} {value}\n") 