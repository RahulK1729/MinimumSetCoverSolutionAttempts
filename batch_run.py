import os
import subprocess
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-inst", type=str)
    parser.add_argument("-alg", type=str, required=True, choices=["Approx", "BnB", "LS1", "LS2"])
    parser.add_argument("-time", type=int, required=True)
    parser.add_argument("-seed", type=int, default=42)
    args = parser.parse_args()

    for in_file in sorted(os.listdir(args.inst)):
        if not in_file.endswith(".in"):
            continue

        base_name = in_file[:-3]
        out_file = os.path.join(args.inst, base_name + ".out")

        if not os.path.exists(out_file):
            print(f"Skipping {in_file} (no matching .out file found)")
            continue

        print(f"Running {args.alg} on: {in_file} with {args.time}s cutoff")

        subprocess.run([
            "python3", "exec.py",
            "-inst", in_file,
            "-alg", args.alg,
            "-time", str(args.time),
            "-seed", str(args.seed)
        ])

if __name__ == "__main__":
    main()
