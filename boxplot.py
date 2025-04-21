import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Define paths
ls1_file = 'experiment_data/LS1_results.csv'
ls2_file = 'experiment_data/LS2_results.csv'
output_dir = 'graphs'
output_path = os.path.join(output_dir, 'running_time_boxplot.png')

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Read the data from CSV
ls1_data = pd.read_csv(ls1_file)
ls2_data = pd.read_csv(ls2_file)

# Tag the algorithm type
ls1_data['Algorithm'] = 'LS1'
ls2_data['Algorithm'] = 'LS2'

# Combine the datasets
combined_data = pd.concat([ls1_data, ls2_data])

# Generate the box plot
plt.figure(figsize=(10, 6))
sns.boxplot(x='Algorithm', y='Runtime', data=combined_data)

# Set title and labels
plt.title('Box Plot of Running Times for LS1 and LS2 Algorithms', fontsize=16)
plt.xlabel('Algorithm', fontsize=12)
plt.ylabel('Running Time (seconds)', fontsize=12)

# Save the plot
plt.tight_layout()
plt.savefig(output_path)
plt.close()

# Confirmation message
print(f"Created box plot of running times.")
print(f"Graph saved to: {output_path}")
