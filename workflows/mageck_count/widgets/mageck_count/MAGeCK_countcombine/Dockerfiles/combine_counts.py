# Description: Combine gene expression counts from multiple samples into a single file.

# Usage:
# python combine_counts.py --input_dir <input_dir> --output_file <output_file> --sample_names <sample_names>

# Example:
# python combine_counts.py --input_dir ./counts_dir --output_file ./combined_counts.txt --sample_names sample1 sample2

import os
import pandas as pd
import glob
import argparse
import re
import json

def combine_counts(input_dir: str, output_file: str, sample_names: list[str]):
    """ 
    Combine gene expression counts from multiple samples into a single file.
    
    Parameters
    ----------
    input_dir : str
        Directory containing .txt files with gene expression counts.
    output_file : str
        Output file name for the combined counts.
    sample_names : list
        List of sample names to process
    
    Returns
    -------
    None

    """

    # Dictionary to store dataframes for each sample
    sample_dfs = {}

    for sample_name in sample_names:
        # Get all .txt files in the input directory
        txt_files = glob.glob(os.path.join(input_dir, "*.txt"))

        for file in txt_files:
            # Check if the sample name is part of the file name
            if re.search(sample_name, os.path.basename(file)):
                # Read the file into a dataframe
                df = pd.read_csv(file, sep='\t')

                # If sample already exists in dictionary, sum the counts
                if sample_name in sample_dfs:
                    sample_dfs[sample_name] = pd.concat([sample_dfs[sample_name], df]).groupby(['sgRNA', 'Gene'], as_index=False).sum()
                else:
                    sample_dfs[sample_name] = df

    # Combine all sample dataframes into one
    combined_df = pd.DataFrame()
    for sample_name, df in sample_dfs.items():

        # Add all counts from columns after the first two columns (sgRNA and Gene) to the sample name column. Integer output
        df[sample_name] = df.iloc[:, 2:].sum(axis=1).astype(int)

        # Drop all columns except the sgRNA, Gene, and sample name columns
        df = df[['sgRNA', 'Gene', sample_name]]

        # df = df.rename(columns={'gene expression counts': sample_name})
        if combined_df.empty:
            combined_df = df
        else:
            combined_df = pd.merge(combined_df, df, on=['sgRNA', 'Gene'], how='outer')

    # Export the combined dataframe to a .txt file
    combined_df.to_csv(output_file, sep='\t', index=False)

def reformat_list(input_list: list[str]) -> list[str]:
    """
    If the input list contains a single string that is a JSON/comma list, parse it and return the list.

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
    parser = argparse.ArgumentParser(description='Combine gene expression counts from multiple samples.')
    parser.add_argument('--input_dir', type=str, help='Directory containing .txt files with gene expression counts.')
    parser.add_argument('--output_file', type=str, help='Output file name for the combined counts.')
    parser.add_argument('--sample_names', type=str, nargs='+', help='List of sample names to process.')
    args = parser.parse_args()

    # Reformat the sample names list if needed
    sample_names = reformat_list(args.sample_names)

    # Make output directory for the output file if it doesn't exist already
    os.makedirs(os.path.dirname(args.output_file), exist_ok=True)

    # Combine the counts
    combine_counts(args.input_dir, args.output_file, sample_names)

if __name__ == "__main__":
    main()
