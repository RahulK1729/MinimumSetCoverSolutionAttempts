# Minimum Set Cover Solution Approaches

This repository contains implementations of algorithms to solve the Minimum Set Cover problem for CSE 6140.

## Project Structure

The repository is organized into modules for different solution approaches:

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

### Simulated Annealing (LS1)
```
cd LS1
python main.py <instance_file> <solution_file> <cutoff_time> -seed <random_seed>
```

### Branch and Bound (bnb)
```
cd bnb
python batch_run.py -inst <instance_file> -alg BnB -time <cutoff_time> -seed <random_seed>
```

### Approximation (Approx)
```
cd approx
python batch_run.py -inst <instance_file> -alg Approx -time <cutoff_time> -seed <random_seed>
```

### Verification
```
cd LS1
python verify.py <data_dir> <output_dir> <cutoff_time>
```

## Notes

The simulated annealing implementation performs exceptionally well on small instances, even finding better solutions than the known optimals in some cases. Performance decreases on larger instances, but still provides reasonable approximations within the time limit.
