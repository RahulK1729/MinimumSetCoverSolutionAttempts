import os
import csv
import argparse
import time
import random
from bnb.bnb import branch_and_bound
from bnb.utils import read_instance
from approx.approx import perform_approx
from LS2.hillclimbing import LS2
from LS1.sa_core import SimulatedAnnealing

# Ensure the 'experiment_data' directory exists
output_dir = 'experiment_data'
os.makedirs(output_dir, exist_ok=True)

# Function to write results to CSV
def write_to_csv(file_path, instance, run, score, runtime):
    # Check if file exists, if not, write the header
    file_exists = os.path.isfile(file_path)
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Instance', 'Run', 'Score', 'Runtime'])  # Writing header
        writer.writerow([instance, run, score, runtime])  # Writing result

# Define the algorithm functions
def run_algorithm(alg, instance_path, time_limit, runs, seed):
    instance_name = os.path.basename(instance_path).split('.')[0]
    n, subsets = read_instance(instance_path)

    start_time = time.time()

    if alg == "BnB":
        # Run Branch and Bound
        best_score, best_set, trace = branch_and_bound(n, subsets, time_limit, start_time)
        return best_score, trace, start_time

    elif alg == "Approx":
        start_time = time.time()
        perform_approx(instance_path, time_limit, seed)
        # Try to read score from output file
        output_path = f"output/{instance_name}_Approx_{time_limit}.sol"
        try:
            with open(output_path, 'r') as f:
                score_line = f.readline().strip()
                score = int(score_line)
        except Exception:
            score = ""
        return score, [], start_time

    elif alg == "LS1":
        # Run Simulated Annealing (LS1)
        sa = SimulatedAnnealing(n, subsets, seed=seed)
        best_score, best_set, trace = sa.solve(time_limit, start_time)
        return best_score, trace, start_time

    elif alg == "LS2":
        # Run Hill Climbing (LS2)
        best_score, best_set, trace = LS2(n, subsets, time_limit, start_time)
        return best_score, trace, start_time
    else:
        raise ValueError(f"Algorithm {alg} not recognized.")

# Main function to handle input and execution
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-inst", type=str, required=True, help="Path to instance file or directory")
    parser.add_argument("-alg", type=str, required=True, choices=["BnB", "Approx", "LS1", "LS2"], help="Algorithm to run")
    parser.add_argument("-time", type=int, required=True, help="Time cutoff in seconds")
    parser.add_argument("-runs", type=int, required=True, help="Number of times to run the algorithm")
    parser.add_argument("-seed", type=int, default=None, help="Random seed for reproducibility")

    args = parser.parse_args()

    # If no seed is provided, generate a random seed
    if args.seed is None:
        args.seed = random.randint(0, 2**32 - 1)  # Generate a random seed
    print(f"Using seed: {args.seed}")

    # Determine the output CSV file based on the chosen algorithm
    csv_path = os.path.join(output_dir, f'{args.alg}_results.csv')
    print(f"Writing results to: {csv_path}")

    # Run the algorithm multiple times
    if os.path.isdir(args.inst):
        for in_file in sorted(os.listdir(args.inst)):
            if not in_file.endswith(".in"):
                continue
            instance_path = os.path.join(args.inst, in_file)

            # Repeat the algorithm the specified number of times
            for run in range(1, args.runs + 1):
                print(f"Running {args.alg} on {instance_path} (Run {run}/{args.runs})")
                best_score, trace, start_time = run_algorithm(args.alg, instance_path, args.time, args.runs, args.seed)
                end_time = time.time()
                runtime = end_time - start_time
                print(f"Run {run}: Best Score = {best_score}, Runtime = {runtime:.2f}s")

                # Write results to CSV
                write_to_csv(csv_path, instance_path, run, best_score, runtime)

    elif os.path.isfile(args.inst):
        # If instance is a single file, run it as well
        instance_path = args.inst
        for run in range(1, args.runs + 1):
            print(f"Running {args.alg} on {instance_path} (Run {run}/{args.runs})")
            best_score, trace, start_time = run_algorithm(args.alg, instance_path, args.time, args.runs, args.seed)
            end_time = time.time()
            runtime = end_time - start_time
            print(f"Run {run}: Best Score = {best_score}, Runtime = {runtime:.2f}s")

            # Write results to CSV
            write_to_csv(csv_path, instance_path, run, best_score, runtime)

    else:
        print(f"{args.inst} is not a valid file or directory.")

if __name__ == "__main__":
    main()
    
