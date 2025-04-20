# Minimum Set Cover Solution Approaches

This repository contains implementations of algorithms to solve the Minimum Set Cover problem for CSE 6140.

## Project Structure

The repository is organized into modules for different solution approaches:

- **LS2**: Hill Climbing implementation

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

## Verification Results

The simulated annealing implementation was tested on all instances with the following results:

### Small/Test Instances
- **Optimal Solutions**: 73.9% (17/23)
- **Better than Optimal**: 8.7% (2/23) 
- **Worse than Optimal**: 17.4% (4/23)
- **Average Gap**: 3.26%
- **Average Runtime**: <0.01s

### Large Instances
- **Optimal Solutions**: 8.3% (1/12)
- **Better than Optimal**: 0.0% (0/12)
- **Worse than Optimal**: 91.7% (11/12)
- **Average Gap**: 40.34%
- **Average Runtime**: 1.28s

### Overall Results
- **Total Instances**: 35
- **Optimal Solutions**: 51.4% (18/35)
- **Better than Optimal**: 5.7% (2/35)
- **Worse than Optimal**: 42.9% (15/35)
- **Average Gap**: 15.97%

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

### Algorithm-Specific Execution

Alternatively, algorithms can be run directly from their respective modules:

#### Simulated Annealing (LS1)
```
cd LS1
python main.py <instance_file> <solution_file> <cutoff_time>
```

#### Branch and Bound (bnb)
```
cd bnb
python exec.py -inst <instance_file> -alg BnB -time <cutoff_time>
```

### Verification
```
cd LS1
python verify.py <data_dir> <output_dir> <cutoff_time>
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

## Notes

The simulated annealing implementation performs exceptionally well on small instances, even finding better solutions than the known optimals in some cases. Performance decreases on larger instances, but still provides reasonable approximations within the time limit.
