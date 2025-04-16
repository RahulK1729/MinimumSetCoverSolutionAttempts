# util file
import os

def read_instance(relative_path):
    # Resolve the full path relative to this script's location
    base_dir = os.path.dirname(__file__)
    full_path = os.path.join(base_dir, "..", relative_path)

    with open(full_path, "r") as f:
        lines = f.readlines()
        n, m = map(int, lines[0].strip().split())
        subsets = []
        for i in range(1, m + 1): # First value is count
            subset = set(map(int, lines[i].strip().split()[1:]))
            subsets.append(subset)
    return n, subsets

def write_solution(file_prefix, method, cutoff, solution, used_indices, seed=None):
    name_parts = [file_prefix, method, str(cutoff)]
    if seed is not None:
        name_parts.append(str(seed))
    sol_filename = f"{'_'.join(name_parts)}.sol"
    with open(os.path.join("output", sol_filename), "w") as f:
        f.write(f"{solution}\n")
        f.write(" ".join(str(i + 1) for i in used_indices) + "\n")

def write_trace(file_prefix, method, cutoff, trace_list, seed=None):
    name_parts = [file_prefix, method, str(cutoff)]
    if seed is not None:
        name_parts.append(str(seed))
    trace_filename = f"{'_'.join(name_parts)}.trace"
    with open(os.path.join("output", trace_filename), "w") as f:
        for t, q in trace_list:
            f.write(f"{t:.2f} {q}\n")
