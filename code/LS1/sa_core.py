"""
Core implementation of simulated annealing for the Minimum Set Cover problem.
"""
import time
import random
from typing import List, Set, Tuple

from LS1.solution import get_initial_solution, evaluate_solution
from LS1.neighborhood import generate_neighbor
from LS1.temperature import calculate_acceptance_probability, update_temperature

class SimulatedAnnealing:
    """Simulated annealing solver for Minimum Set Cover."""
    
    def __init__(self, n: int, subsets: List[Set[int]], initial_temp: float = 100.0,
                 cooling_rate: float = 0.95, min_temp: float = 0.1, seed: int = 42):
        # Initialize problem parameters
        self.n = n
        self.subsets = subsets
        self.universe = set(range(1, n + 1))
        
        # SA parameters
        self.init_temp = initial_temp
        self.cool_rate = cooling_rate
        self.min_temp = min_temp
        self.seed = seed
        
        # Set random seed for reproducibility
        random.seed(self.seed)
        
        # Precompute metrics to speed up evaluation
        self.subset_sizes = [len(s) for s in subsets]
        self.indices = list(range(len(subsets)))
        self.coverage_ratio = [len(s) / n for s in subsets]
        
        # Calculate frequency of each element for smarter moves
        self.elem_freq = {}
        for e in self.universe:
            self.elem_freq[e] = sum(1 for s in subsets if e in s)
            
        # Params for large instances
        self.reheat_interval = 1000
        self.is_large = n > 100 or len(subsets) > 100
        if self.is_large:
            # Use slower cooling for large instances
            self.cool_rate = 0.98
    
    def solve(self, cutoff_time: float, start_time: float) -> Tuple[int, List[int], List[Tuple[float, int]]]:
        # Reset random seed for each run
        random.seed(self.seed)
        
        # Get greedy starting solution
        curr_sol = get_initial_solution(self.n, self.subsets, self.is_large)
        curr_cost, curr_feasible = evaluate_solution(curr_sol, self.subsets, self.universe)
        
        # Initialize best solution tracking
        best_sol = curr_sol.copy()
        best_cost = curr_cost
        
        # Set up temperature and progress tracking
        temp = self.init_temp
        trace = [(time.time() - start_time, best_cost)]
        
        # Iteration counters
        iter_count = 0
        plateau_len = 0
        last_improv = 0
        
        # Set stopping criteria based on problem size
        max_stagnation = 5000 if self.is_large else 2000
        
        # Main SA loop
        while time.time() - start_time < cutoff_time and temp > self.min_temp:
            # Get neighboring solution
            neighbor = generate_neighbor(
                curr_sol, 
                self.subsets, 
                self.universe, 
                iter_count, 
                self.is_large
            )
            
            # Evaluate new solution
            neighbor_cost, neighbor_feasible = evaluate_solution(neighbor, self.subsets, self.universe)
            
            # Calculate probability of accepting this neighbor
            accept_prob = calculate_acceptance_probability(
                curr_cost, 
                neighbor_cost, 
                curr_feasible, 
                neighbor_feasible, 
                temp, 
                iter_count, 
                self.is_large
            )
            
            # Decide whether to accept the neighbor
            if random.random() < accept_prob:
                curr_sol = neighbor
                curr_cost = neighbor_cost
                curr_feasible = neighbor_feasible
                
                # Check if we found a better solution
                if curr_feasible and curr_cost <= best_cost:
                    if curr_cost < best_cost:
                        # New best solution found
                        best_sol = curr_sol.copy()
                        best_cost = curr_cost
                        trace.append((time.time() - start_time, best_cost))
                        plateau_len = 0
                        last_improv = iter_count
                    elif curr_cost == best_cost:
                        # Equal quality solution found
                        plateau_len += 1
                        # Store alternative solutions occasionally
                        if plateau_len % 100 == 0 and curr_sol != best_sol:
                            alt_sol = curr_sol.copy()
            
            # Cool down temperature according to schedule
            temp = update_temperature(
                temp, 
                self.cool_rate, 
                iter_count, 
                last_improv, 
                self.reheat_interval, 
                self.init_temp, 
                self.is_large
            )
            
            iter_count += 1
            
            # Early stopping if no improvement for a while
            if iter_count - last_improv > max_stagnation:
                break
        
        # Return (cost, solution, history)
        return best_cost, sorted(best_sol), trace 