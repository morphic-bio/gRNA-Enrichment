# Description: Combine count summary statistics from each fastq file by sample.
#
# Usage:
# python sample_count_stats.py --input_dir <input_dir> --stats_file <output_file> --sample_names <sample_names>

#
# Example:
# python sample_count_stats.py --input_dir ./counts_dir --stats_file ./combined_counts.txt --sample_names sample1 sample2

import argparse
import glob
import pandas as pd
import os
import json

def sample_count_stats(input_dir: str, output_stats: str, sample_names: list[str]):
    """
    Combine count summary statistics from each fastq file by sample.

    Parameters
    ----------
    input_dir : str
        Directory containing .txt files with summary statistics.
    output_stats : str
        Output file name for the stats.
    sample_names : list
        List of sample names.

    Returns
    -------
    None

    """
    
    summary_dfs = pd.DataFrame(columns=["Sample", "SampleReads", "SampleMapped", "SamplePercentMapped", "TotalsgRNAs"])

    for sample in sample_names:
        file_pattern = f"{input_dir}/*{sample}*.countsummary.txt"
        files = glob.glob(file_pattern)
        dataframes = [pd.read_csv(file, sep='\t') for file in files]
        combined_df = pd.concat(dataframes)
        sample_summary = pd.DataFrame({
            "Sample": sample,
            "SampleReads": combined_df["Reads"].sum(),
            "SampleMapped": combined_df["Mapped"].sum(),
            "SamplePercentMapped": combined_df["Mapped"].sum() * 100 / combined_df["Reads"].sum(),
            "TotalsgRNAs": combined_df["TotalsgRNAs"].iloc[0]
            # TODO: RECALCULATE ZEROCOUNTS AND GINI INDEX FROM THE COMBINED DATAFRAME
            # "SampleZerocounts": combined_df["Zerocounts"].sum(),
            # "SampleAverageGiniIndex": combined_df["GiniIndex"].mean()
        }, index=[sample])

        # Concatenate the new row to the summary dataframe
        summary_dfs = pd.concat([summary_dfs, sample_summary], ignore_index=True)
    
    # Export the combined dataframe to a .txt file
    summary_dfs.to_csv(output_stats, sep='\t', index=False)

def reformat_list(input_list: list[str]) -> list[str]:
    """
    If the input list contains a single string that is a JSON/comma list, parse it and return the list.
    For example, if the input list is ['["sample1", "sample2"]'], this function will return ['sample1', 'sample2'].

    Parameters
    ----------
    input_list : list
        List to reformat (most likely one element of multiple file paths).
    
    Returns
    -------
    list
        Reformatted list of strings.

    """

    if len(input_list) == 1 and isinstance(input_list[0], str):
        try:
            # Try to parse the first element as a JSON list
            parsed = json.loads(input_list[0])
            if isinstance(parsed, list):  # Ensure it's a list
                return parsed
        except json.JSONDecodeError:
            pass  # Ignore if it's not a valid JSON string
        
        # Check if the string is a comma-separated list
        if ',' in input_list[0]:
            return input_list[0].strip('[]').split(',')
            
    return input_list  # Return as is if no changes needed

def main():
    parser = argparse.ArgumentParser(description='Combine count summary statistics from each fastq file by sample.')
    parser.add_argument('--input_dir', type=str, help='Directory containing .txt files with summary statistics.')
    parser.add_argument('--stats_file', type=str, help='Output stats file name.')
    parser.add_argument('--sample_names', type=str, nargs='+', help='List of sample names.')
    args = parser.parse_args()

    # Reformat the sample names list if needed
    sample_names = reformat_list(args.sample_names)

    # Make output directory for the output file if it doesn't exist already
    os.makedirs(os.path.dirname(args.stats_file), exist_ok=True)

    # Make the stats file
    sample_count_stats(args.input_dir, args.stats_file, sample_names)

if __name__ == "__main__":
    main()