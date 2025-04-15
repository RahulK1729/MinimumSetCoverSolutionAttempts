"""
Utility functions for file I/O and data management for the Minimum Set Cover problem.
"""

def read_instance(filename):
    """Read a problem instance from a file.
    
    Args:
        filename: Path to the input file
        
    Returns:
        Tuple of (n, subsets) where n is the universe size and subsets is a list of sets
    """
    with open(filename, 'r') as f:
        # First line contains n and m
        n, m = map(int, f.readline().strip().split())
        subsets = []
        for _ in range(m):
            subset = set(map(int, f.readline().strip().split()))
            subsets.append(subset)
    return n, subsets

def write_solution(filename, obj_value, solution, trace):
    """Write the solution to a file.
    
    Args:
        filename: Output file path
        obj_value: Objective value (number of sets)
        solution: List of set indices (0-based)
        trace: List of (time, value) tuples tracking solution improvements
    """
    with open(filename, 'w') as f:
        f.write(f"{obj_value}\n")
        f.write(" ".join(map(str, [i + 1 for i in solution])) + "\n")
        for time_stamp, value in trace:
            f.write(f"{time_stamp:.2f},{value}\n")

def write_trace(filename, trace):
    """Write the trace to a file.
    
    Args:
        filename: Output trace file path
        trace: List of (time, value) tuples tracking solution improvements
    """
    with open(filename, 'w') as f:
        for time_stamp, value in trace:
            f.write(f"{time_stamp:.2f} {value}\n") 