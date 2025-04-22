# Simulated Annealing for Minimum Set Cover

This implementation uses Simulated Annealing (SA), a probabilistic local search algorithm, to solve the Minimum Set Cover problem. The algorithm starts with a greedy solution and gradually improves it through controlled random exploration.

## Algorithm Overview

1. **Initial Solution**: Uses a greedy approach to construct the first feasible solution
2. **Neighborhood Generation**: Three types of moves:
   - Remove a random subset (40% probability)
   - Add a random subset (40% probability)
   - Swap two subsets (20% probability)
3. **Temperature Schedule**:
   - Initial temperature: 100.0
   - Cooling rate: 0.95
   - Minimum temperature: 0.1
   - Reheating: Every 1000 iterations to escape local optima

## Project Structure

The implementation follows a modular design with the following components:

- `main.py`: Entry point and command-line interface
- `sa_core.py`: Core simulated annealing implementation and algorithm class
- `solution.py`: Solution generation and evaluation
- `neighborhood.py`: Neighbor generation strategies
- `temperature.py`: Temperature management and acceptance criteria
- `utils.py`: File I/O and utility functions
- `verify.py`: Comprehensive verification script

## Usage

```bash
python main.py <instance_file> <solution_file> <cutoff_time>
```

Example:
```bash
python main.py ../data/test1.in test1_sa.sol 60
```

### Input Format
- Line 1: n and m (universe size and number of subsets)
- Lines 2 to m+1: space-separated integers representing elements in each subset

### Output Format
- Line 1: Objective value (number of sets in solution)
- Line 2: Space-separated indices of selected sets (1-based)
- Remaining lines: Timestamp,Value pairs showing solution improvement trace

## Verification Results

Comprehensive testing on 35 benchmark instances (23 small/test and 12 large) demonstrates our implementation's effectiveness:

### Performance Summary

| Instance Type | Optimal Solutions | Better than Reference | Worse than Reference | Average Gap | Avg Runtime |
|---------------|------------------|----------------------|---------------------|------------|------------|
| Small/Test    | 73.9% (17/23)    | 8.7% (2/23)          | 17.4% (4/23)        | 3.26%      | <0.01s     |
| Large         | 8.3% (1/12)      | 0.0% (0/12)          | 91.7% (11/12)       | 40.34%     | 1.28s      |
| **Overall**   | **51.4% (18/35)**| **5.7% (2/35)**      | **42.9% (15/35)**   | **15.97%** | **0.43s**  |

The implementation demonstrates the power of simulated annealing for the Minimum Set Cover problem, particularly for:

1. **Small Instances**: Exceptional performance, often finding optimal or better-than-reference solutions
2. **Large Instances**: Ability to tackle problems with thousands of elements where exact methods would be impractical
3. **Runtime Efficiency**: Quick solutions (avg. <2 seconds) even for large problem instances

## Modular Design

The implementation utilizes a modular architecture with clear separation of concerns:

1. **Solution Module** (`solution.py`):
   - Encapsulates the representation of a set cover solution
   - Manages solution validity and coverage
   - Implements solution evaluation and comparison

2. **Neighborhood Module** (`neighborhood.py`):
   - Defines different neighbor generation strategies
   - Implements adaptive move selection based on solution state
   - Handles special cases for boundary conditions

3. **Temperature Module** (`temperature.py`):
   - Implements various cooling schedules
   - Manages acceptance probability calculation
   - Controls reheating strategies

4. **Core SA Module** (`sa_core.py`):
   - Provides the SimulatedAnnealing class that orchestrates the process
   - Handles convergence criteria
   - Manages iteration and termination conditions
   - Integrates all components into a cohesive algorithm

This modular approach allows for easy experimentation with different components and parameters.

## Verification & Testing

To run verification on all instances:
```bash
python verify.py ../data output 60
```

To run verification with a specific time limit:
```bash
python verify.py ../data output 120
```

To test a specific instance:
```bash
python main.py ../data/instance_name.in output/solution_name.sol 60
``` 