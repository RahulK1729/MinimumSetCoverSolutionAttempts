# Set Cover Solver - Branch and Bound

This folder contains the code to solves the Set Cover problem using an exact **Branch-and-Bound** approach.

- `bnb.py` – Branch-and-bound algorithm implementation.
- `exec.py` – Driver script for running experiments.
- `utils.py` – File I/O utilities for reading input and writing `.sol` and `.trace` files.
- `data/` – Contains input datasets like `large1.in`, `large2.in`, etc.
- `output/` – Stores generated `.sol` and `.trace` files.

## How to Run

### Command Format:
```bash
python3 exec.py -inst <filename> -alg BnB -time <cutoff_in_seconds> -seed <random_seed>
```

The branch and bound algorithm will return the optimal number of subsets however in cases where there are multiple optimal combinations, the indices chosen may differ.

I made batch_run.py to generate the output for all the data at once to make my life easy.