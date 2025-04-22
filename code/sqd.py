import os
import matplotlib.pyplot as plt
import csv

# Constants
trace_dir = "experiment_data"  # Location where the CSV files are stored
output_dir = "graphs"
os.makedirs(output_dir, exist_ok=True)

# Read results from the CSV file
def read_results(filename):
    results = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip the header row
        for row in reader:
            if len(row) == 4:
                instance, run_id, optimal, runtime = row
                try:
                    run_id = int(run_id)
                    optimal = int(optimal)
                    runtime = float(runtime)
                    results.append((instance, run_id, optimal, runtime))
                except ValueError:
                    # Handle any rows where conversion fails
                    print(f"[!] Skipping invalid row: {row}")
    return results

# Read LS1 and LS2 result files
ls1_results = read_results("experiment_data/LS1_results.csv")
ls2_results = read_results("experiment_data/LS2_results.csv")

# Combine the results of both LS1 and LS2
results = ls1_results + ls2_results

# Function to compute solution quality distribution
def compute_sqd(results, time_threshold):
    solution_qualities = []
    for instance, run_id, optimal, runtime in results:
        if runtime <= time_threshold:  # Only consider runs completed within the time threshold
            solution_quality = (optimal - runtime) / optimal  # Define solution quality as relative difference
            solution_qualities.append(solution_quality)
    return solution_qualities

# Plot Solution Quality Distributions (SQD)
time_thresholds = [5, 10, 15, 20]  # Define time thresholds in seconds
for time_threshold in time_thresholds:
    plt.figure(figsize=(8, 6))

    # Compute solution quality for all runs under the time threshold
    solution_qualities = compute_sqd(results, time_threshold)

    # Plot the distribution of solution qualities
    plt.hist(solution_qualities, bins=20, alpha=0.75, color='blue', label=f'Time ≤ {time_threshold}s')

    plt.title(f"Solution Quality Distribution for Time ≤ {time_threshold}s")
    plt.xlabel("Solution Quality (Relative to Optimal)")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.legend()

    # Save the plot
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"sqd_time_{time_threshold}.png"))
    plt.close()
    print(f"Saved SQD plot for Time ≤ {time_threshold}s")
