"""
Neighborhood generation for the simulated annealing algorithm.
"""
import random
from typing import List, Set, Tuple

def get_move_probabilities(iter_count: int, sol_size: int, is_large: bool) -> Tuple[float, float, float]:
    """Get dynamic move probabilities based on solution state."""
    # For large instances, adjust strategy based on solution size
    if is_large:
        if sol_size > 20:
            # For oversized solutions, prioritize removal
            return 0.6, 0.2, 0.2
        else:
            # Balanced approach for reasonable-sized solutions
            return 0.4, 0.4, 0.2
    
    # For small instances, adapt based on search progress
    if iter_count < 100:
        # Early stage - more exploration (favor additions)
        return 0.3, 0.5, 0.2
    else:
        # Later stage - balanced approach
        return 0.4, 0.4, 0.2

def generate_neighbor(curr_sol: List[int], subsets: List[Set[int]], universe: Set[int], 
                      iter_count: int, is_large: bool) -> List[int]:
    """Create neighboring solution through strategic moves."""
    # Make a copy to avoid modifying the original
    neighbor = curr_sol.copy()
    
    # Determine move type probabilities
    remove_prob, add_prob, swap_prob = get_move_probabilities(iter_count, len(neighbor), is_large)
    
    # Select a move type randomly according to probabilities
    move_type = random.random()
    
    # ===== REMOVAL MOVE =====
    if move_type < remove_prob and len(neighbor) > 0:
        # Look for redundant subsets (those we can safely remove)
        redundant = []
        for idx in neighbor:
            # Check if solution remains valid without this subset
            temp_sol = [i for i in neighbor if i != idx]
            if temp_sol:
                covered = set().union(*[subsets[i] for i in temp_sol])
                if covered == universe:
                    redundant.append(idx)
        
        if redundant:
            # Prefer removing redundant subsets most of the time
            # but occasionally remove randomly to escape local optima
            idx_to_remove = random.choice(redundant if random.random() < 0.7 else neighbor)
            neighbor.remove(idx_to_remove)
        else:
            # No redundant subset - remove randomly and accept if feasible
            idx_to_remove = random.choice(neighbor)
            neighbor.remove(idx_to_remove)
    
    # ===== ADDITION MOVE =====
    elif move_type < remove_prob + add_prob:
        # Calculate current coverage
        curr_covered = set().union(*[subsets[i] for i in neighbor]) if neighbor else set()
        uncovered = universe - curr_covered
        
        # If some elements are uncovered, try to target them
        if uncovered and random.random() < 0.8:
            # Find subsets that cover at least one uncovered element
            candidates = []
            for i in range(len(subsets)):
                if i not in neighbor and subsets[i] & uncovered:
                    # Score by how many uncovered elements this subset covers
                    uncovered_count = len(subsets[i] & uncovered)
                    candidates.append((i, uncovered_count))
            
            if candidates:
                # Sort by coverage and select from top candidates
                # with preference to those covering more elements
                candidates.sort(key=lambda x: x[1], reverse=True)
                top_k = candidates[:max(3, len(candidates)//5)]
                idx_to_add = random.choices(
                    [c[0] for c in top_k],
                    weights=[c[1] for c in top_k],
                    k=1
                )[0]
                neighbor.append(idx_to_add)
                return neighbor
        
        # Otherwise, add a random subset not already in solution
        available = list(set(range(len(subsets))) - set(neighbor))
        if available:
            idx_to_add = random.choice(available)
            neighbor.append(idx_to_add)
    
    # ===== SWAP MOVE =====
    else:
        if len(neighbor) > 0:
            # Get available subsets (not in solution)
            available = list(set(range(len(subsets))) - set(neighbor))
            if available:
                # For large instances, try more intelligent swaps
                if is_large and random.random() < 0.7:
                    # Calculate uniqueness of each subset in solution
                    # (how many elements would become uncovered if removed)
                    unique_scores = []
                    for idx in neighbor:
                        subset = subsets[idx]
                        unique_count = 0
                        # Count elements uniquely covered by this subset
                        for elem in subset:
                            covered_elsewhere = sum(1 for i in neighbor if i != idx and elem in subsets[i])
                            if covered_elsewhere == 0:
                                unique_count += 1
                        unique_scores.append((idx, unique_count))
                    
                    # Prefer to swap out less critical subsets
                    unique_scores.sort(key=lambda x: x[1])
                    idx_to_remove = unique_scores[0][0] if unique_scores else random.choice(neighbor)
                    position = neighbor.index(idx_to_remove)
                else:
                    # Random selection for small instances
                    position = random.choice(range(len(neighbor)))
                    idx_to_remove = neighbor[position]
                
                # Choose replacement intelligently for large instances
                if is_large and random.random() < 0.7:
                    # Check what would be uncovered after removal
                    temp_sol = [i for i in neighbor if i != idx_to_remove]
                    temp_covered = set().union(*[subsets[i] for i in temp_sol]) if temp_sol else set()
                    needed_coverage = universe - temp_covered
                    
                    # Find subsets that help cover the gap
                    swap_candidates = []
                    for idx in available:
                        coverage = len(subsets[idx] & needed_coverage)
                        if coverage > 0:
                            swap_candidates.append((idx, coverage))
                    
                    if swap_candidates:
                        # Choose based on coverage with some randomness
                        swap_candidates.sort(key=lambda x: x[1], reverse=True)
                        top_candidates = swap_candidates[:max(3, len(swap_candidates)//5)]
                        idx_to_add = random.choices(
                            [c[0] for c in top_candidates],
                            weights=[c[1] for c in top_candidates],
                            k=1
                        )[0]
                        neighbor[position] = idx_to_add
                        return neighbor
                
                # Fall back to random choice
                idx_to_add = random.choice(available)
                neighbor[position] = idx_to_add
    
    return neighbor 