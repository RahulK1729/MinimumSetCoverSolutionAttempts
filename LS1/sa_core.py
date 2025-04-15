"""
Core simulated annealing implementation for the Minimum Set Cover problem.
"""
import time
import random
from typing import List, Set, Tuple

from solution import get_initial_solution, evaluate_solution
from neighborhood import generate_neighbor
from temperature import calculate_acceptance_probability, update_temperature

class SimulatedAnnealing:
    """Simulated annealing solver for the Minimum Set Cover problem."""
    
    def __init__(self, n: int, subsets: List[Set[int]], initial_temp: float = 100.0,
                 cooling_rate: float = 0.95, min_temp: float = 0.1):
        """Initialize the simulated annealing solver.
        
        Args:
            n: Universe size
            subsets: List of sets representing available subsets
            initial_temp: Initial temperature
            cooling_rate: Cooling rate
            min_temp: Minimum temperature
        """
        self.n = n
        self.subsets = subsets
        self.universe = set(range(1, n + 1))
        self.initial_temp = initial_temp
        self.cooling_rate = cooling_rate
        self.min_temp = min_temp
        
        # Precompute subset information for faster evaluation
        self.subset_sizes = [len(s) for s in subsets]
        self.subset_indices = list(range(len(subsets)))
        self.subset_coverage_ratio = [len(s) / n for s in subsets]
        
        # Precompute element frequencies for smarter moves
        self.element_frequency = {}
        for e in self.universe:
            self.element_frequency[e] = sum(1 for s in subsets if e in s)
            
        # Adaptation parameters
        self.reheat_frequency = 1000
        self.large_instance = n > 100 or len(subsets) > 100
        if self.large_instance:
            self.cooling_rate = 0.98
    
    def solve(self, cutoff_time: float, start_time: float) -> Tuple[int, List[int], List[Tuple[float, int]]]:
        """Run the simulated annealing algorithm.
        
        Args:
            cutoff_time: Maximum runtime in seconds
            start_time: Start time of the algorithm
            
        Returns:
            Tuple of (best_cost, best_solution, trace)
        """
        # Generate initial solution using greedy approach
        current_solution = get_initial_solution(self.n, self.subsets, self.large_instance)
        current_cost, current_feasible = evaluate_solution(current_solution, self.subsets, self.universe)
        
        best_solution = current_solution.copy()
        best_cost = current_cost
        
        temperature = self.initial_temp
        trace = [(time.time() - start_time, best_cost)]
        
        iteration = 0
        plateau_count = 0
        last_improvement = 0
        
        # Adjust max iterations based on problem size
        max_no_improvement = 5000 if self.large_instance else 2000
        
        # Main simulated annealing loop
        while time.time() - start_time < cutoff_time and temperature > self.min_temp:
            # Generate neighbor with smart move selection
            neighbor = generate_neighbor(
                current_solution, 
                self.subsets, 
                self.universe, 
                iteration, 
                self.large_instance
            )
            
            # Evaluate the neighbor
            neighbor_cost, neighbor_feasible = evaluate_solution(neighbor, self.subsets, self.universe)
            
            # Determine whether to accept using smarter probability
            acceptance_prob = calculate_acceptance_probability(
                current_cost, 
                neighbor_cost, 
                current_feasible, 
                neighbor_feasible, 
                temperature, 
                iteration, 
                self.large_instance
            )
            
            if random.random() < acceptance_prob:
                current_solution = neighbor
                current_cost = neighbor_cost
                current_feasible = neighbor_feasible
                
                # Handle improvement tracking
                if current_feasible and current_cost <= best_cost:
                    # Reset counters if we found a better solution
                    if current_cost < best_cost:
                        best_solution = current_solution.copy()
                        best_cost = current_cost
                        trace.append((time.time() - start_time, best_cost))
                        plateau_count = 0
                        last_improvement = iteration
                    # Count equal solutions for plateau detection
                    elif current_cost == best_cost:
                        plateau_count += 1
                        # Record different but equally good solutions occasionally
                        if plateau_count % 100 == 0 and current_solution != best_solution:
                            alternative_solution = current_solution.copy()
            
            # Update temperature according to cooling schedule
            temperature = update_temperature(
                temperature, 
                self.cooling_rate, 
                iteration, 
                last_improvement, 
                self.reheat_frequency, 
                self.initial_temp, 
                self.large_instance
            )
            
            iteration += 1
            
            # Early termination if no improvement for too long
            if iteration - last_improvement > max_no_improvement:
                break
        
        return best_cost, sorted(best_solution), trace 