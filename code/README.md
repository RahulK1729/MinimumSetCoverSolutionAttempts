# Minimum Set Cover Solution Approaches

This repository contains implementations of algorithms to solve the Minimum Set Cover problem for CSE 6140.

## Project Structure

The repository is organized into modules for different solution approaches:

- **LS2**: Hill Climbing implementation
  - First-improvement approach
  - Deterministic based on seeding

- **LS1**: Simulated Annealing (SA) implementation
  - Modular design with separate components:
    - `main.py`: Entry point for running the algorithm
    - `sa_core.py`: Core simulated annealing implementation
    - `temperature.py`: Temperature scheduling strategies
    - `neighborhood.py`: Neighbor generation functions
    - `solution.py`: Solution representation and evaluation
    - `utils.py`: File I/O and utility functions
    - `verify.py`: Comprehensive testing and validation
  - Includes verification script for evaluating solution quality

- **bnb**: Branch and Bound implementation
  - Exact algorithm approach
  - Includes pruning techniques and memoization for faster convergence
 
- **Approx**: Approximation implementation
  - Greedy approximation algorithm implementation
  - Finds the "best" subset that contains the most elements that are not yet included
  - Adds the "best" subset to the solution and continues until all elements are included 

- **data**: Test instances
  - Test cases of varying sizes (small, large)
  - Includes known optimal solutions (.out files)

## Usage

### Using the Main Executable

All algorithms can be executed using the main `exec.py` script at the root directory:

```
python exec.py -inst <instance_file_or_directory> -alg <algorithm> -time <cutoff_time> [-seed <random_seed>]
```

Where:
- `<instance_file_or_directory>`: Path to an instance file (.in) or directory containing instance files
- `<algorithm>`: One of "BnB", "Approx", "LS1", or "LS2"
- `<cutoff_time>`: Time limit in seconds
- `<random_seed>`: (Optional) Random seed for reproducibility

Examples:
```
# Run Simulated Annealing (LS1) on a single file
python exec.py -inst data/test1.in -alg LS1 -time 60 -seed 42

# Run Simulated Annealing on all files in a directory
python exec.py -inst data/ -alg LS1 -time 60
```

### Batch Experiment Runner
This script allows you to run all algorithms across multiple problem instances and collect performance results.

### Features
Runs BnB, Approx, LS1, and LS2 on all .in files in a directory

Allows repeated runs per instance for more robust results

Records solution score and runtime for each run

Stores results in separate CSV files for each algorithm

### Output
The results are saved in the experiment_results/ directory:

BnB_results.csv

Approx_results.csv

LS1_results.csv

LS2_results.csv

Each CSV file contains the following columns:
Instance, Run, Score, Runtime

### Usage

Run a single algorithm multiple times on all instances
To run a specific algorithm on all instances in a directory multiple times, use:
'''
python experiment_runner.py -inst <data_directory> -alg <algorithm> -time <cutoff_seconds> -runs <number_of_runs>
'''

Example:
To run the Branch and Bound (BnB) algorithm 1 time on each instance in the data/ directory with a 60-second cutoff:
'''
python experiment_runner.py -inst data/ -alg BnB -time 60 -runs 1
'''
This command will execute the BnB algorithm once per instance, with a 60-second time limit per run, and store the results in the BnB_results.csv file.

Run a single algorithm multiple times on a single instance
'''
python experiment_runner.py -inst <data_file> -alg <algorithm> -time <cutoff_seconds> -runs <number_of_runs>
'''

Example
To run the BnB algorithm 5 times on the data/test1.in file with a 60-second cutoff per run:
'''
python experiment_runner.py -inst data/test1.in -alg BnB -time 60 -runs 5
'''
This will run the BnB algorithm 5 times on test1.in, with a 60-second time limit for each run, and store the results in the BnB_results.csv.
