"""
Temperature control functions for simulated annealing.
"""
import math

def calculate_acceptance_probability(old_cost, new_cost, old_feasible, new_feasible, 
                                    temp, iter_count, is_large):
    """Calculate probability of accepting a new solution."""
    # Always accept if new solution is better and feasible
    if new_feasible and (not old_feasible or new_cost < old_cost):
        return 1.0
    
    # Never accept infeasible solutions
    if not new_feasible:
        return 0.0
    
    # Accept equally good solutions with medium probability
    # This helps explore plateaus in the solution space
    if new_cost == old_cost:
        return 0.5
    
    # Standard Metropolis criterion for worse solutions
    delta = old_cost - new_cost
    
    # More aggressive acceptance in early stages for large instances
    # Promotes exploration of the solution space
    if is_large and iter_count < 500:
        return min(1.0, math.exp(delta / (temp * 0.8)))
    
    # Standard Metropolis formula
    return math.exp(delta / temp)

def update_temperature(temp, cooling_rate, iter_count, last_improv, 
                      reheat_interval, init_temp, is_large):
    """Update temperature according to cooling schedule."""
    # Apply cooling based on problem size and search progress
    if is_large:
        # Faster cooling when stuck in a region without improvement
        if iter_count - last_improv > 500:
            temp *= (cooling_rate ** 2)
        else:
            temp *= cooling_rate
    else:
        # Standard cooling for small instances
        temp *= cooling_rate
    
    # Periodic reheating to escape local optima
    if iter_count % reheat_interval == 0:
        if is_large:
            # More aggressive reheating for large instances
            temp = max(temp, init_temp * 0.7)
        else:
            # Moderate reheating for small instances
            temp = max(temp, init_temp * 0.5)
    
    return temp 