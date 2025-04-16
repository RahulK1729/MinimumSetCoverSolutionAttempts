import random
import time

def is_cover(universe, subsets, selected):
    """Check if the selected subsets cover the universe"""
    covered = set()
    for idx in selected:
        covered.update(subsets[idx])
    return covered.issuperset(universe)

def evaluate(subsets, solution):
    """Evaluate a solution (binary vector), return size and selected indices"""
    selected = [i for i in range(len(subsets)) if solution[i]]
    return len(selected), selected

def get_random_solution(universe, subsets, seed):
    """Generate a random initial solution that covers the universe"""
    random.seed(seed)
    solution = [False] * len(subsets)
    covered = set()
    # Randomly add subsets until we cover the universe
    while not covered.issuperset(universe):
        idx = random.randint(0, len(subsets) - 1)
        solution[idx] = True
        covered.update(subsets[idx])
    return solution

def hill_climbing(universe, subsets, cutoff_time, seed):
    """Hill climbing local search algorithm"""
    start_time = time.time()
    trace = []
    
    # Initialize with a random feasible solution
    current_sol = get_random_solution(universe, subsets, seed)
    best_size, best_selected = evaluate(subsets, current_sol)
    trace.append((time.time() - start_time, best_size))
    
    improved = True
    while improved and (time.time() - start_time) < cutoff_time:
        improved = False
        
        # Evaluate all possible single-flip neighbors
        for i in range(len(subsets)):
            # Flip the i-th subset
            neighbor = current_sol.copy()
            neighbor[i] = not neighbor[i]
            
            # Check if neighbor is feasible
            n_size, n_selected = evaluate(subsets, neighbor)
            if is_cover(universe, subsets, n_selected):
                # If neighbor is better, move to it
                if n_size < best_size:
                    current_sol = neighbor
                    best_size = n_size
                    best_selected = n_selected
                    trace.append((time.time() - start_time, best_size))
                    improved = True
                    break  # First-improvement strategy
        
    return best_size, best_selected, trace

def LS2(n, subsets, time, seed):
    universe = set(range(1, n + 1))
    solution_size, selected_subsets, trace = hill_climbing(universe, subsets, time, seed)
    return solution_size, selected_subsets, trace