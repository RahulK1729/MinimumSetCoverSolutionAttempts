import time

def greedy_lower_bound(universe, subsets, covered):
    remaining = universe - covered
    count = 0
    subsets = [s for s in subsets if s & remaining]  # Only keep helpful subsets

    while remaining:
        best_subset = max(subsets, key=lambda s: len(s & remaining), default=None)
        if not best_subset or not (best_subset & remaining):
            return float("inf")  # Can't cover remaining elements
        remaining -= best_subset
        count += 1

    return count

def branch_and_bound(n, subsets, cutoff_time, start_time):
    universe = set(range(1, n + 1))
    best_score = float("inf") # REPLACE WITH TIGHER UPPER BOUND FROM APPROX
    best_solution = []
    trace = []

    # Optional: sort subsets by size descending
    subsets = sorted(enumerate(subsets), key=lambda x: -len(x[1]))

    memo = {}  # For memoization

    def recurse(index, covered, selected_indices):
        nonlocal best_score, best_solution, trace

        if time.time() - start_time > cutoff_time:
            return

        if covered == universe:
            if len(selected_indices) < best_score or (
                len(selected_indices) == best_score and selected_indices < best_solution
            ):
                best_score = len(selected_indices)
                best_solution = selected_indices[:]
                trace.append((time.time() - start_time, best_score))
            return

        if index == len(subsets):
            return

        key = (index, frozenset(covered))
        if key in memo and len(selected_indices) >= memo[key]:
            return
        memo[key] = len(selected_indices)

        # Prune with greedy lower bound
        remaining_subsets = subsets[index:]
        lb = greedy_lower_bound(universe, [s for _, s in remaining_subsets], covered)
        if lb == 0:
            recurse(len(subsets), universe, selected_indices)
            return
        if len(selected_indices) + lb >= best_score:
            return

        subset_idx, subset = subsets[index]

        # Include current subset
        recurse(
            index + 1,
            covered | subset,
            selected_indices + [subset_idx]
        )

        # Exclude current subset
        recurse(
            index + 1,
            covered,
            selected_indices
        )

    recurse(0, set(), [])
    best_solution.sort()
    return best_score, best_solution, trace
