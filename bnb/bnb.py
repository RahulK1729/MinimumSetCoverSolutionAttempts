import time

def greedy_lower_bound(universe, subsets, covered):
    """
    Computes a greedy lower bound for the minimum number of subsets needed
    to cover the remaining elements in the universe not yet covered.

    Parameters:
    - universe: Set of all elements to be covered.
    - subsets: List of subsets available for covering the universe.
    - covered: Set of elements already covered.

    Returns:
    - A lower bound estimate (int) of the additional subsets needed to cover the remaining elements.
    - Returns float('inf') if it's impossible to cover all remaining elements.
    """
    remaining = universe - covered
    count = 0

    # Filter subsets to keep only those that cover some of the remaining elements
    subsets = [s for s in subsets if s & remaining]

    while remaining:
        # Choose the subset that covers the largest number of uncovered elements
        best_subset = max(subsets, key=lambda s: len(s & remaining), default=None)

        # If its not possible
        if not best_subset or not (best_subset & remaining):
            return float("inf")  

        remaining -= best_subset
        count += 1

    return count


def branch_and_bound(n, subsets, cutoff_time, start_time):
    """
    Solves the Set Cover problem using a branch-and-bound approach.

    Parameters:
    - n: Number of elements in the universe (1 to n).
    - subsets: List of sets, each representing a subset of the universe.
    - cutoff_time: Maximum allowed time for execution (in seconds).
    - start_time: Time when the algorithm started running.

    Returns:
    - best_score: Minimum number of subsets needed to cover the universe.
    - best_solution: List of indices of the subsets forming the best solution.
    - trace: List of tuples (elapsed_time, current_best_score) recorded during search.
    """
    universe = set(range(1, n + 1))  # Define the universe of elements to cover
    best_score = float("inf")       # REPLACE WITH TIGHTER UPPER BOUND FROM APPROX
    best_solution = []              # Best set of subset indices found so far
    trace = []                      # Track (elapsed_time, score) updates for analysis

    # Sort for slightly faster convergence
    subsets = sorted(enumerate(subsets), key=lambda x: -len(x[1]))

    # Memoization dictionary
    memo = {}

    def recurse(index, covered, selected_indices):
        """
        Recursive function for exploring subset combinations using branch-and-bound.

        Parameters:
        - index: Current index in the sorted subset list.
        - covered: Set of elements currently covered.
        - selected_indices: List of selected subset indices so far.
        """
        nonlocal best_score, best_solution, trace

        # End if time limit is exceeded
        if time.time() - start_time > cutoff_time:
            return

        # Found a valid solution covering the universe
        if covered == universe:
            if len(selected_indices) < best_score or (
                len(selected_indices) == best_score and selected_indices < best_solution
            ):
                best_score = len(selected_indices)
                best_solution = selected_indices[:]
                trace.append((time.time() - start_time, best_score))
            return

        # Exhausted all subsets without covering the universe
        if index == len(subsets):
            return

        # Memoization check
        key = (index, frozenset(covered))
        if key in memo and len(selected_indices) >= memo[key]:
            return
        memo[key] = len(selected_indices)

        # Compute a greedy lower bound from current state
        remaining_subsets = subsets[index:]
        lb = greedy_lower_bound(universe, [s for _, s in remaining_subsets], covered)

        if lb == 0:
            # All remaining elements can be covered with no additional subset
            recurse(len(subsets), universe, selected_indices)
            return

        # Prune the branch if even the best-case estimate exceeds the best score found
        if len(selected_indices) + lb >= best_score:
            return

        subset_idx, subset = subsets[index]

        # Include the current subset in the solution
        recurse(
            index + 1,
            covered | subset,
            selected_indices + [subset_idx]
        )

        # Exclude the current subset and move to the next
        recurse(
            index + 1,
            covered,
            selected_indices
        )

    recurse(0, set(), [])

    # Return the best result found within the cutoff time
    best_solution.sort()
    return best_score, best_solution, trace
