import os
import matplotlib.pyplot as plt
import csv

# Constants
input_dir = "experiment_data"
output_dir = "graphs"
os.makedirs(output_dir, exist_ok=True)

instances = ["large1", "large10"]
algorithms = ["LS1", "LS2"]
qrtd_thresholds = [0.5, 0.25, 0.1]  # 1%, 0.8%, 0.5%

colors = ['tab:blue', 'tab:green', 'tab:red']

# Optimal solutions for large1 and large10
optimal_solutions = {
    "large1": 50,
    "large10": 221
}

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


# Calculate the QRTD times
def compute_qrtd_times(results, optimal, q_star):
    threshold = optimal * (1 + q_star)
    times = []
    for instance, run_id, optimal_value, runtime in results:
        if optimal_value <= threshold:
            times.append(runtime)
    return times

# Plot QRTD for each instance
for instance in instances:
    plt.figure(figsize=(8, 6))

    for algo in algorithms:
        # Load the results for each algorithm
        file_name = os.path.join(input_dir, f"{algo}_results.csv")
        results = read_results(file_name)
        run_files = [res for res in results if instance in res[0]]  # Filter results for the instance

        if len(run_files) < 1:
            print(f"[!] No results found for {instance} {algo}")
            continue

        for idx, q_star in enumerate(qrtd_thresholds):
            times = compute_qrtd_times(run_files, optimal_solutions[instance], q_star)
            valid_times = sorted(times)
            cdf_x = valid_times
            cdf_y = [i / len(valid_times) for i in range(1, len(valid_times) + 1)]
            label = f"{algo}, q*={q_star*100:.1f}%"
            linestyle = '-' if algo == "LS1" else '--'
            plt.plot(cdf_x, cdf_y, label=label, color=colors[idx], linestyle=linestyle)

    plt.title(f"QRTD for {instance}")
    plt.xlabel("Time (s)")
    plt.ylabel("Fraction of runs ≤ q*")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"qrtd_{instance}.png"))
    plt.close()
    print(f"[✓] Saved QRTD plot for {instance}")
