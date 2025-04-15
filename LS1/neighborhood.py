"""
Neighborhood generation for simulated annealing on the Minimum Set Cover problem.
"""
import random
from typing import List, Set, Tuple

def get_move_probabilities(iteration: int, solution_length: int, large_instance: bool) -> Tuple[float, float, float]:
    """Dynamically adjust move probabilities based on solution state and iteration.
    
    Args:
        iteration: Current iteration number
        solution_length: Length of current solution
        large_instance: Flag for large problem instances
        
    Returns:
        Tuple of (remove_prob, add_prob, swap_prob)
    """
    # For large instances, adapt the move strategy
    if large_instance:
        if solution_length > 20:
            # Favor removal for large solutions
            return 0.6, 0.2, 0.2
        else:
            # Balanced for medium solutions
            return 0.4, 0.4, 0.2
    
    # For small instances or early iterations
    if iteration < 100:
        # More exploration early on
        return 0.3, 0.5, 0.2
    else:
        # Standard probabilities
        return 0.4, 0.4, 0.2

def generate_neighbor(current: List[int], subsets: List[Set[int]], universe: Set[int], 
                      iteration: int, large_instance: bool) -> List[int]:
    """Generate a neighboring solution through smart random moves.
    
    Args:
        current: Current solution (list of set indices)
        subsets: List of sets representing available subsets
        universe: Set representing the universe
        iteration: Current iteration number
        large_instance: Flag for large problem instances
        
    Returns:
        New solution (list of set indices)
    """
    neighbor = current.copy()
    
    # Get dynamic move probabilities
    remove_prob, add_prob, swap_prob = get_move_probabilities(iteration, len(neighbor), large_instance)
    
    move_type = random.random()
    
    # REMOVAL MOVE
    if move_type < remove_prob and len(neighbor) > 0:
        # Identify redundant subsets that can be safely removed
        redundant_indices = []
        for idx_to_check in neighbor:
            # Check if removing this subset would maintain coverage
            temp_solution = [i for i in neighbor if i != idx_to_check]
            if temp_solution:
                covered = set().union(*[subsets[i] for i in temp_solution])
                if covered == universe:
                    redundant_indices.append(idx_to_check)
        
        if redundant_indices:
            # Remove a redundant subset with higher probability
            idx_to_remove = random.choice(redundant_indices if random.random() < 0.7 else neighbor)
            neighbor.remove(idx_to_remove)
        else:
            # Remove a random subset if no redundant ones found
            idx_to_remove = random.choice(neighbor)
            neighbor.remove(idx_to_remove)
    
    # ADDITION MOVE
    elif move_type < remove_prob + add_prob:
        # Find eligible subsets that could improve coverage
        current_covered = set().union(*[subsets[i] for i in neighbor]) if neighbor else set()
        uncovered = universe - current_covered
        
        # If there are uncovered elements, prioritize subsets covering them
        if uncovered and random.random() < 0.8:
            # Find subsets that cover at least one uncovered element
            helpful_subsets = []
            for i in range(len(subsets)):
                if i not in neighbor and subsets[i] & uncovered:
                    # Score by coverage of uncovered elements
                    score = len(subsets[i] & uncovered)
                    helpful_subsets.append((i, score))
            
            if helpful_subsets:
                # Select based on coverage score (with some randomness)
                helpful_subsets.sort(key=lambda x: x[1], reverse=True)
                # Select from top candidates with higher probability to top ones
                top_candidates = helpful_subsets[:max(3, len(helpful_subsets)//5)]
                idx_to_add = random.choices(
                    [c[0] for c in top_candidates],
                    weights=[c[1] for c in top_candidates],
                    k=1
                )[0]
                neighbor.append(idx_to_add)
                return neighbor
        
        # Otherwise, select a random subset not already in solution
        available = list(set(range(len(subsets))) - set(neighbor))
        if available:
            idx_to_add = random.choice(available)
            neighbor.append(idx_to_add)
    
    # SWAP MOVE
    else:
        if len(neighbor) > 0:
            available = list(set(range(len(subsets))) - set(neighbor))
            if available:
                # For large instances, try swapping out least useful subsets
                if large_instance and random.random() < 0.7:
                    # Calculate coverage uniqueness for each subset in solution
                    uniqueness_scores = []
                    for idx in neighbor:
                        subset = subsets[idx]
                        # How many elements are uniquely covered by this subset
                        unique_coverage = 0
                        for elem in subset:
                            covered_by_count = sum(1 for i in neighbor if i != idx and elem in subsets[i])
                            if covered_by_count == 0:
                                unique_coverage += 1
                        uniqueness_scores.append((idx, unique_coverage))
                    
                    # Sort by uniqueness (ascending = less unique first)
                    uniqueness_scores.sort(key=lambda x: x[1])
                    # Prefer to remove less unique subsets
                    idx_in_solution = uniqueness_scores[0][0] if uniqueness_scores else random.choice(neighbor)
                    solution_idx = neighbor.index(idx_in_solution)
                else:
                    # Standard random swap
                    solution_idx = random.choice(range(len(neighbor)))
                    idx_in_solution = neighbor[solution_idx]
                
                # Choose subset to add intelligently
                if large_instance and random.random() < 0.7:
                    # Evaluate potential swaps based on coverage
                    temp_solution = [i for i in neighbor if i != idx_in_solution]
                    current_covered = set().union(*[subsets[i] for i in temp_solution]) if temp_solution else set()
                    uncovered = universe - current_covered
                    
                    # Find subsets that cover uncovered elements
                    candidates = []
                    for idx in available:
                        coverage = len(subsets[idx] & uncovered)
                        if coverage > 0:
                            candidates.append((idx, coverage))
                    
                    if candidates:
                        # Select based on coverage (with some randomness)
                        candidates.sort(key=lambda x: x[1], reverse=True)
                        top_candidates = candidates[:max(3, len(candidates)//5)]
                        idx_to_add = random.choices(
                            [c[0] for c in top_candidates],
                            weights=[c[1] for c in top_candidates],
                            k=1
                        )[0]
                        neighbor[solution_idx] = idx_to_add
                        return neighbor
                
                # Fall back to random choice if smart selection failed
                idx_to_add = random.choice(available)
                neighbor[solution_idx] = idx_to_add
    
    return neighbor 