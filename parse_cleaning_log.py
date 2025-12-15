# Alexey Vorobev
# APR2025 --> DEC2025

"""
This script scans .log files for specific error patterns and counts their occurrences.
It generates individual CSV files for each log and a combined CSV file with all results.
Results are saved in a time-stamped output directory.

Example of use:
    python analyze_logs.py /path/to/log/files
"""

import os
import sys
import csv
from collections import Counter
from datetime import datetime

# Define the patterns to search for
patterns = [
    "Below minimum length",
    "Too many unknown bases",
    "Found adapter dimer in R2",
    "Highly variable quality scores",
    "Common region not found",
    "Below minimum median quality",
    "Below complexity threshold"
]

def count_occurrences(file_path):
    """Counts occurrences of specified strings in a file."""
    counts = Counter()
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            for pattern in patterns:
                if pattern in line:
                    counts[pattern] += 1
    return counts

def save_individual_csv(counts, file_name, output_dir):
    """Saves individual count results to a CSV file in the output directory."""
    output_path = os.path.join(output_dir, f"{os.path.splitext(file_name)[0]}_counts.csv")
    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Pattern", "Count"])
        for pattern, count in counts.items():
            writer.writerow([pattern, count])
    print(f"Results saved to {output_path}")

def save_combined_csv(results, all_files, output_dir):
    """Saves combined results into a single CSV file with date in the filename."""
    date_str = datetime.now().strftime("%Y%m%d")
    combined_output_path = os.path.join(output_dir, f"combined_counts_{date_str}.csv")
    with open(combined_output_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        # Write header: "Pattern" followed by file names
        writer.writerow(["Pattern"] + all_files)
        # Write pattern counts per file
        for pattern in patterns:
            row = [pattern] + [results[file].get(pattern, 0) for file in all_files]
            writer.writerow(row)
    print(f"Combined results saved to {combined_output_path}")

def process_directory(log_dir):
    """Processes all .log files in the given directory and saves results in a time-stamped folder."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join(log_dir, f"results_{timestamp}")
    os.makedirs(output_dir, exist_ok=True)

    results = {}
    all_files = []

    for filename in os.listdir(log_dir):
        if filename.endswith(".log"):
            file_path = os.path.join(log_dir, filename)
            counts = count_occurrences(file_path)
            results[filename] = counts
            all_files.append(filename)
            save_individual_csv(counts, filename, output_dir)

    if results:
        save_combined_csv(results, all_files, output_dir)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_logs.py /path/to/log/files")
        sys.exit(1)
    log_dir = sys.argv[1]
    if not os.path.isdir(log_dir):
        print(f"Error: {log_dir} is not a valid directory.")
        sys.exit(1)
    process_directory(log_dir)
