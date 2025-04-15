import os
import subprocess

DATA_DIR = "data"
CUTOFF_TIME = 60  # can modify
METHOD = "BnB"

def main():
    for i in range(1, 19):
        in_file = f"small{i}.in"
        # in_file = f"large{i}.in"
        base_name = in_file[:-3]  # Remove the .in extension
        out_file = os.path.join(DATA_DIR, base_name + ".out")
        
        if os.path.exists(out_file):
            in_path = in_file  # Pass just the filename, not 'data/'
            print(f"Running BnB on: {in_file}")
            subprocess.run([
                "python3", "exec.py",
                "-inst", in_path,
                "-alg", METHOD,
                "-time", str(CUTOFF_TIME)
            ])
        else:
            print(f"Skipping {in_file} (no matching .out file found)")

if __name__ == "__main__":
    main()
