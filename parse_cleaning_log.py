# Alexey Vorobev
# APR2025

import os
import csv
from collections import Counter

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

# def save_to_csv(counts, output_path):
#     """Saves the count results to a CSV file."""
#     with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
#         writer = csv.writer(csvfile)
#         writer.writerow(["Pattern", "Count"])
#         for pattern, count in counts.items():
#             writer.writerow([pattern, count])

# def process_current_directory():
#     """Processes all .txt files in the current working directory."""
#     current_directory = os.getcwd()  # Get the current directory
#     for filename in os.listdir(current_directory):
#         if filename.endswith(".log"):  # Process only text files
#             file_path = os.path.join(current_directory, filename)
#             counts = count_occurrences(file_path)
#             output_path = os.path.join(current_directory, f"{os.path.splitext(filename)[0]}_counts.csv")
#             save_to_csv(counts, output_path)
#             print(f"Results saved to {output_path}")

# # Run the script in the current directory
# process_current_directory()

def save_individual_csv(counts, file_name):
    """Saves individual count results to a CSV file."""
    output_path = f"{os.path.splitext(file_name)[0]}_counts.csv"
    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Pattern", "Count"])
        for pattern, count in counts.items():
            writer.writerow([pattern, count])
    print(f"Results saved to {output_path}")

def save_combined_csv(results, all_files):
    """Saves combined results into a single CSV file."""
    combined_output_path = "combined_counts.csv"
    with open(combined_output_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        # Write header: "Pattern" followed by file names
        writer.writerow(["Pattern"] + all_files)

        # Write pattern counts per file
        for pattern in patterns:
            row = [pattern] + [results[file].get(pattern, 0) for file in all_files]
            writer.writerow(row)
    
    print(f"Combined results saved to {combined_output_path}")

def process_current_directory():
    """Processes all .log files in the current working directory and saves individual & combined CSVs."""
    current_directory = os.getcwd()  # Get the current directory
    results = {}
    all_files = []

    for filename in os.listdir(current_directory):
        if filename.endswith(".log"):  # Process only log files
            file_path = os.path.join(current_directory, filename)
            counts = count_occurrences(file_path)
            results[filename] = counts
            all_files.append(filename)
            save_individual_csv(counts, filename)

    # Save combined results
    if results:
        save_combined_csv(results, all_files)

# Run the script in the current directory
process_current_directory()
