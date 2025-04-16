"""
Solution management for the Minimum Set Cover problem.
"""
import heapq
import random
from typing import List, Set, Tuple

def get_initial_solution(n: int, subsets: List[Set[int]], large_instance: bool = False, seed: int = 42) -> List[int]:
    """Generate an initial solution using a greedy approach.
    
    Args:
        n: Universe size
        subsets: List of sets representing available subsets
        large_instance: Flag for large problem instances
        seed: Random seed for reproducibility
        
    Returns:
        List of indices representing the initial solution
    """
    # Set random seed for any randomization in the greedy algorithm
    random.seed(seed)
    
    universe = set(range(1, n + 1))
    solution = []
    covered = set()
    
    # For large instances, use a more effective greedy approach
    if large_instance:
        # Create a priority queue of subsets ordered by coverage efficiency
        subset_queue = []
        for i, subset in enumerate(subsets):
            # Higher score for subsets that cover more uncovered elements
            if subset - covered:
                efficiency = len(subset - covered) / len(subset) if len(subset) > 0 else 0
                heapq.heappush(subset_queue, (-efficiency, -len(subset - covered), i))
        
        # Keep adding the most efficient subsets until fully covered
        while covered != universe and subset_queue:
            _, _, idx = heapq.heappop(subset_queue)
            newly_covered = subsets[idx] - covered
            if newly_covered:
                solution.append(idx)
                covered |= subsets[idx]
                
                # Update efficiencies of remaining subsets
                new_queue = []
                while subset_queue:
                    _, _, i = heapq.heappop(subset_queue)
                    new_uncovered = len(subsets[i] - covered)
                    if new_uncovered > 0:
                        efficiency = new_uncovered / len(subsets[i])
                        heapq.heappush(new_queue, (-efficiency, -new_uncovered, i))
                
                subset_queue = new_queue
    else:
        # Original greedy approach for small instances
        while covered != universe:
            best_subset_idx = max(range(len(subsets)), 
                                key=lambda i: len(subsets[i] - covered) if i not in solution else 0)
            solution.append(best_subset_idx)
            covered |= subsets[best_subset_idx]
        
    return solution

def evaluate_solution(solution: List[int], subsets: List[Set[int]], universe: Set[int]) -> Tuple[int, bool]:
    """Evaluate a solution's cost and feasibility.
    
    Args:
        solution: List of set indices
        subsets: List of sets representing available subsets
        universe: Set representing the universe
        
    Returns:
        Tuple of (cost, is_feasible)
    """
    if not solution:
        return 0, False
        
    covered = set().union(*[subsets[i] for i in solution])
    is_feasible = covered == universe
    return len(solution), is_feasible 