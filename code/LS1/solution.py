"""
Solution creation and evaluation for the Minimum Set Cover problem.
"""
import heapq
import random
from typing import List, Set, Tuple

def get_initial_solution(n: int, subsets: List[Set[int]], is_large: bool = False, seed: int = 42) -> List[int]:
    """Generate initial solution using greedy strategy."""
    # Set random seed for reproducibility
    random.seed(seed)
    
    # Setup
    universe = set(range(1, n + 1))
    selected = []
    covered = set()
    
    # Use more advanced greedy approach for large instances
    if is_large:
        # Use priority queue for efficient subset selection
        candidates = []
        for idx, subset in enumerate(subsets):
            # Find sets that cover uncovered elements
            uncovered_gain = len(subset - covered)
            if uncovered_gain > 0:
                # Score by efficiency (more uncovered elements = better)
                eff_score = uncovered_gain / len(subset) if len(subset) > 0 else 0
                heapq.heappush(candidates, (-eff_score, -uncovered_gain, idx))
        
        # Keep adding sets until everything is covered
        while covered != universe and candidates:
            # Get best candidate
            _, _, idx = heapq.heappop(candidates)
            new_elems = subsets[idx] - covered
            
            if new_elems:  # If this set covers new elements
                # Add to solution
                selected.append(idx)
                covered |= subsets[idx]
                
                # Update priorities for remaining candidates
                updated_candidates = []
                while candidates:
                    _, _, i = heapq.heappop(candidates)
                    new_gain = len(subsets[i] - covered)
                    if new_gain > 0:
                        eff_score = new_gain / len(subsets[i])
                        heapq.heappush(updated_candidates, (-eff_score, -new_gain, i))
                
                candidates = updated_candidates
    else:
        # Simple greedy for small instances - faster and nearly as good
        while covered != universe:
            # Find subset covering most uncovered elements
            best_idx = max(range(len(subsets)), 
                          key=lambda i: len(subsets[i] - covered) if i not in selected else 0)
            selected.append(best_idx)
            covered |= subsets[best_idx]
        
    return selected

def evaluate_solution(solution: List[int], subsets: List[Set[int]], universe: Set[int]) -> Tuple[int, bool]:
    """Evaluate solution cost and feasibility."""
    if not solution:
        return 0, False
    
    # Get all elements covered by current solution
    covered = set().union(*[subsets[i] for i in solution])
    
    # Check if all elements are covered
    is_valid = covered == universe
    
    # Return solution size and validity
    return len(solution), is_valid 