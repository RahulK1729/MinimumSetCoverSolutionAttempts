import os
import sys
import time
import glob
from sa_core import SimulatedAnnealing

def read_instance(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        n, m = map(int, lines[0].strip().split())
        subsets = []
        for i in range(1, m + 1):
            subset = set(map(int, lines[i].strip().split()))
            subsets.append(subset)
    return n, subsets

def read_optimal_solution(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        opt_value = int(lines[0].strip())
        if len(lines) > 1 and lines[1].strip():
            opt_sets = list(map(int, lines[1].strip().split()))
        else:
            opt_sets = []
    return opt_value, opt_sets

def write_solution(filename, obj_value, solution, trace):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as f:
        f.write(f"{obj_value}\n")
        f.write(" ".join(map(str, [i + 1 for i in solution])) + "\n")
        for time_stamp, value in trace:
            f.write(f"{time_stamp:.2f},{value}\n")

def write_trace(filename, trace):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as f:
        for time_stamp, value in trace:
            f.write(f"{time_stamp:.2f} {value}\n")

def run_verification(data_dir, output_dir, time_limit=60, instances=None):
    """Run verification on multiple instances and produce a summary report"""
    
    # Create results directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Get list of instances to test
    if instances is None:
        # Use all .in files in data directory
        instances = []
        for pattern in ["test*.in", "small*.in", "large*.in"]:
            instances.extend(glob.glob(os.path.join(data_dir, pattern)))
    
    results = []
    
    for instance_file in instances:
        instance_name = os.path.basename(instance_file).split('.')[0]
        optimal_file = os.path.join(data_dir, f"{instance_name}.out")
        
        if not os.path.exists(optimal_file):
            print(f"Skipping {instance_name} (no matching .out file)")
            continue
            
        print(f"Testing {instance_name}...")
        
        # Read instance and optimal solution
        n, subsets = read_instance(instance_file)
        opt_value, opt_sets = read_optimal_solution(optimal_file)
        
        # Solve with simulated annealing
        sa = SimulatedAnnealing(n, subsets)
        start_time = time.time()
        best_obj, best_solution, trace = sa.solve(time_limit, start_time)
        end_time = time.time()
        runtime = end_time - start_time
        
        # Calculate gap from optimal
        gap = (best_obj - opt_value) / opt_value * 100 if opt_value > 0 else 0
        
        # Write solution and trace files
        solution_file = os.path.join(output_dir, f"{instance_name}_SA_{time_limit}.sol")
        trace_file = os.path.join(output_dir, f"{instance_name}_SA_{time_limit}.trace")
        write_solution(solution_file, best_obj, best_solution, trace)
        write_trace(trace_file, trace)
        
        # Store results for summary
        results.append({
            'instance': instance_name,
            'category': 'large' if instance_name.startswith('large') else 'small',
            'optimal': opt_value,
            'sa_value': best_obj,
            'gap': gap,
            'runtime': runtime,
            'iterations': len(trace),
            'universe_size': n,
            'subset_count': len(subsets)
        })
    
    # Write summary report
    report_file = os.path.join(output_dir, "verification_report.csv")
    with open(report_file, 'w') as f:
        f.write("Instance,Category,Optimal,SA_Value,Gap(%),Runtime(s),Iterations,UniverseSize,SubsetCount\n")
        for result in results:
            f.write(f"{result['instance']},{result['category']},{result['optimal']},{result['sa_value']},"
                   f"{result['gap']:.2f},{result['runtime']:.2f},{result['iterations']},"
                   f"{result['universe_size']},{result['subset_count']}\n")
    
    # Print summary to console grouped by category
    print("\nVerification Results:")
    print("=====================")
    
    # Function to print results for a category
    def print_category_results(category_name, category_results):
        if not category_results:
            return
            
        print(f"\n{category_name} Instances:")
        print(f"{'Instance':<10} {'Optimal':<8} {'SA Value':<8} {'Gap(%)':<8} {'Runtime(s)':<10}")
        print("-" * 60)
        
        total_gap = 0
        for result in sorted(category_results, key=lambda r: r['instance']):
            print(f"{result['instance']:<10} {result['optimal']:<8} {result['sa_value']:<8} "
                 f"{result['gap']:<8.2f} {result['runtime']:<10.2f}")
            total_gap += result['gap']
        
        avg_gap = total_gap / len(category_results) if category_results else 0
        optimal_count = sum(1 for r in category_results if r['gap'] == 0)
        better_count = sum(1 for r in category_results if r['gap'] < 0)
        worse_count = sum(1 for r in category_results if r['gap'] > 0)
        
        print("-" * 60)
        print(f"Average Gap: {avg_gap:.2f}%")
        print(f"Optimal Solutions: {optimal_count}/{len(category_results)} ({optimal_count/len(category_results)*100:.1f}%)")
        print(f"Better Solutions: {better_count}/{len(category_results)} ({better_count/len(category_results)*100:.1f}%)")
        print(f"Worse Solutions: {worse_count}/{len(category_results)} ({worse_count/len(category_results)*100:.1f}%)")
        print(f"Average Runtime: {sum(r['runtime'] for r in category_results)/len(category_results):.2f}s")
    
    # Group results by category
    small_results = [r for r in results if r['category'] == 'small' or r['instance'].startswith('test')]
    large_results = [r for r in results if r['category'] == 'large']
    
    # Print results by category
    print_category_results("Small/Test", small_results)
    print_category_results("Large", large_results)
    
    # Overall results
    total_gap = sum(r['gap'] for r in results)
    avg_gap = total_gap / len(results) if results else 0
    optimal_count = sum(1 for r in results if r['gap'] == 0)
    better_count = sum(1 for r in results if r['gap'] < 0)
    worse_count = sum(1 for r in results if r['gap'] > 0)
    
    print("\nOverall Results:")
    print("-" * 60)
    print(f"Total Instances: {len(results)}")
    print(f"Average Gap: {avg_gap:.2f}%")
    print(f"Optimal Solutions: {optimal_count}/{len(results)} ({optimal_count/len(results)*100:.1f}%)")
    print(f"Better Solutions: {better_count}/{len(results)} ({better_count/len(results)*100:.1f}%)")
    print(f"Worse Solutions: {worse_count}/{len(results)} ({worse_count/len(results)*100:.1f}%)")
    
    return results

if __name__ == "__main__":
    # Default parameters
    data_dir = "../Data"
    output_dir = "output"
    time_limit = 60
    
    # Parse command line arguments if provided
    if len(sys.argv) > 1:
        data_dir = sys.argv[1]
    if len(sys.argv) > 2:
        output_dir = sys.argv[2]
    if len(sys.argv) > 3:
        time_limit = int(sys.argv[3])
    
    # Run verification
    run_verification(data_dir, output_dir, time_limit) 