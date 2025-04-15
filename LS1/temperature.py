"""
Temperature management for simulated annealing.
"""
import math

def calculate_acceptance_probability(old_cost, new_cost, old_feasible, new_feasible, 
                                    temperature, iteration, large_instance):
    """Calculate probability of accepting new solution with adaptive criteria.
    
    Args:
        old_cost: Cost of current solution
        new_cost: Cost of new solution
        old_feasible: Feasibility of current solution
        new_feasible: Feasibility of new solution
        temperature: Current temperature
        iteration: Current iteration number
        large_instance: Flag for large problem instances
        
    Returns:
        Probability of accepting the new solution
    """
    # Always accept feasible solutions better than current
    if new_feasible and (not old_feasible or new_cost < old_cost):
        return 1.0
    # Never accept infeasible solutions
    elif not new_feasible:
        return 0.0
    
    # For equal solutions, accept with medium probability to explore plateau
    if new_cost == old_cost:
        return 0.5
        
    # Calculate standard Metropolis acceptance based on cost difference
    delta = old_cost - new_cost
    
    # For large instances, use more aggressive acceptance in early stages
    if large_instance and iteration < 500:
        # Boost acceptance probability for early diversification
        return min(1.0, math.exp(delta / (temperature * 0.8)))
    
    return math.exp(delta / temperature)

def update_temperature(temperature, cooling_rate, iteration, last_improvement, reheat_frequency, 
                      initial_temp, large_instance):
    """Update temperature according to cooling schedule and reheating strategy.
    
    Args:
        temperature: Current temperature
        cooling_rate: Cooling rate
        iteration: Current iteration number
        last_improvement: Iteration when last improvement was found
        reheat_frequency: How often to reheat
        initial_temp: Initial temperature
        large_instance: Flag for large problem instances
        
    Returns:
        Updated temperature
    """
    # Apply cooling
    if large_instance:
        # Use adaptive cooling for large instances
        if iteration - last_improvement > 500:
            # Faster cooling when stuck
            temperature *= (cooling_rate ** 2)
        else:
            temperature *= cooling_rate
    else:
        # Standard cooling for small instances
        temperature *= cooling_rate
    
    # Apply reheating if needed
    if iteration % reheat_frequency == 0:
        if large_instance:
            # More aggressive reheating for large instances
            temperature = max(temperature, initial_temp * 0.7)
        else:
            temperature = max(temperature, initial_temp * 0.5)
            
    return temperature 