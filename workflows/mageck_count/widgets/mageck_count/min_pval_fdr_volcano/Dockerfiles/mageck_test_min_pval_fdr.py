### This script extracts the minimum p-value and FDR values from MAGeCK test output for a screen.
### It also generates volcano plots for the minimum p-value and FDR dataframes.
#
# Usage:
# python mageck_test_min_pval_fdr.py --input_dir <input_dir> --output_dir <output_dir> --screen <screen_name> --volcano
# --y_axis_threshold <y_axis_threshold> --x_axis_threshold <x_axis_threshold>
#
# Example:
# python mageck_test_min_pval_fdr.py --input_dir ./mageck_test_output --output_dir ./output --screen screen1 --volcano --y_axis_threshold 0.05 --x_axis_threshold 1.0

import os
import pandas as pd
import glob
import argparse
import plotly
import dash_bio
import numpy as np

def get_min_and_fdr(input_dir: str, output_dir: str, screen: str):
    """
    Extract the minimum p-value and FDR values from MAGeCK test output for a screen.

    Parameters:
    ----------
    input_dir : str
        Directory containing MAGeCK test outputs (with *gene_summary_txt files).
    output_dir : str
        Output directory.
    screen : str
        Screen/prefix name from MAGeCK test to extract (files inside --input_dir).

    Returns:
    -------
    mageck_test_gene_summary_filtered_min_pval : pd.DataFrame
        DataFrame containing the filtered gene summary with minimum p-values.
    mageck_test_gene_summary_filtered_min_fdr : pd.DataFrame
        DataFrame containing the filtered gene summary with minimum FDR values.

    """
    
    # Detect the file pattern for the gene summary files
    file_pattern = f"{input_dir}/*{screen}*gene_summary.txt"
    mageck_test_gene_summary = glob.glob(file_pattern)
    if not mageck_test_gene_summary:
        raise FileNotFoundError(f"No files found matching pattern: {file_pattern}")
    
    print("Extracting minimum p-value and FDR values...")

    # Read the first file found (assuming all files have the same structure)
    mageck_test_gene_summary = pd.read_csv(mageck_test_gene_summary[0], sep='\t')

    # Extract the relevant columns and rename them
    mageck_test_gene_summary_filtered = mageck_test_gene_summary.loc[:, ['id', 'num', 'neg|lfc', 'neg|p-value', 'neg|fdr', 'pos|p-value', 'pos|fdr']]
    mageck_test_gene_summary_filtered.columns = mageck_test_gene_summary_filtered.columns.str.replace('|', '_', regex=False)
    mageck_test_gene_summary_filtered = mageck_test_gene_summary_filtered.rename(columns = {'neg_lfc': 'lfc'})

    # Extract the minimum p-value and FDR values
    mageck_test_gene_summary_filtered['min_p-value'] = mageck_test_gene_summary_filtered[['neg_p-value', 'pos_p-value']].min(axis=1)
    mageck_test_gene_summary_filtered['min_fdr'] = mageck_test_gene_summary_filtered[['neg_fdr', 'pos_fdr']].min(axis=1)
    mageck_test_gene_summary_filtered_min_pval = mageck_test_gene_summary_filtered[['id', 'num', 'lfc', 'min_p-value']]
    mageck_test_gene_summary_filtered_min_fdr = mageck_test_gene_summary_filtered[['id', 'num', 'lfc', 'min_fdr']]

    # Sort the dataframes by the minimum p-value and FDR values followed by the log fold change followed by the gene id
    mageck_test_gene_summary_filtered_min_pval_sorted = mageck_test_gene_summary_filtered_min_pval.sort_values(by=['min_p-value', 'lfc', 'id'], ascending=[True, True, True])
    mageck_test_gene_summary_filtered_min_fdr_sorted = mageck_test_gene_summary_filtered_min_fdr.sort_values(by=['min_fdr', 'lfc', 'id'], ascending=[True, True, True])

    # Paths to output files
    min_pval_file = os.path.join(output_dir, f"{screen}_gene_min_pval_summary.txt")
    min_fdr_file = os.path.join(output_dir, f"{screen}_gene_min_fdr_summary.txt")

    # Export the filtered dataframes to .txt files
    mageck_test_gene_summary_filtered_min_pval_sorted.to_csv(min_pval_file, sep='\t', index=False)
    mageck_test_gene_summary_filtered_min_fdr_sorted.to_csv(min_fdr_file, sep='\t', index=False)

    print("Exported minimum p-value summary to:", min_pval_file)
    print("Exported minimum FDR summary to:", min_fdr_file)

    return mageck_test_gene_summary_filtered_min_pval, mageck_test_gene_summary_filtered_min_fdr

def make_volcano_plots(pval_dataframe: pd.DataFrame, 
                       fdr_dataframe: pd.DataFrame, 
                       output_dir: str, 
                       screen: str,
                       y_val_threshold: float = 0.05,
                       x_axis_threshold: float = 1.0):
    """
    Create volcano plots for the minimum p-value and FDR dataframes.

    Parameters:
    ----------
    pval_dataframe : pd.DataFrame
        DataFrame containing the minimum p-value data.
    fdr_dataframe : pd.DataFrame
        DataFrame containing the minimum FDR data.
    output_dir : str
        Output directory for the plots.
    screen : str
        Screen/prefix name for the plots.
    y_val_threshold : float, optional
        Y-axis threshold for the volcano plots (default is 0.05).
    x_axis_threshold : float, optional
        X-axis threshold for the volcano plots (default is 1.0).
    
    Returns:
    -------
    None
    """

    print("Creating volcano plots...")

    # Create the volcano plot for minimum p-value
    fig_pval = dash_bio.VolcanoPlot(
    dataframe=pval_dataframe,
    effect_size = "lfc",
    gene = "id",
    snp = None,
    p = "min_p-value",   
    logp = True,
    xlabel = "Log Fold Change (LFC)",
    ylabel = "-log10(p-value)",
    effect_size_line = [-x_axis_threshold, x_axis_threshold],
    genomewideline_value = -np.log10(y_val_threshold),
    effect_size_line_width = 3,
    genomewideline_width = 2,
    title = dict(text=f"{screen}Volcano Plot (min p-value)", xanchor='center', yanchor='top')
    )

    # Create the volcano plot for minimum FDR
    fig_fdr = dash_bio.VolcanoPlot(
    dataframe=fdr_dataframe,
    effect_size = "lfc",
    gene = "id",
    snp = None,
    p = "min_fdr",
    logp = True,
    xlabel = "Log Fold Change (LFC)",
    ylabel = "-log10(FDR)",
    effect_size_line = [-x_axis_threshold, x_axis_threshold],
    genomewideline_value = -np.log10(y_val_threshold),
    effect_size_line_width = 3,
    genomewideline_width = 2,
    title = dict(text=f"{screen}Volcano Plot (min FDR)", xanchor='center', yanchor='top')
    )

    # Save the plots as HTML files
    plotly.offline.plot(fig_pval, filename=os.path.join(output_dir, f"{screen}_volcano_plot_min_pval.html"), auto_open=False)
    plotly.offline.plot(fig_fdr, filename=os.path.join(output_dir, f"{screen}_volcano_plot_min_fdr.html"), auto_open=False)

    print(f"Volcano plots saved to: {output_dir}, open in a web browser to view.")


    

def main():
    parser = argparse.ArgumentParser(description="Extract the minimum p-value and FDR values from MAGeCK test output for a screen.")
    parser.add_argument("--input_dir", type=str, required=True, help="Directory containing MAGeCK test outputs (with *gene_summary_txt files).")
    parser.add_argument("--output_dir", type=str, required=True, help="Output directory.")
    parser.add_argument("--screen", type=str, required=True, help="Screen/prefix name from MAGeCK test to extract (files inside --input_dir).")
    parser.add_argument("--volcano", action="store_true", required=False, help="Include this flag to generate volcano plots.")
    parser.add_argument("--y_axis_threshold", type=float, default=0.05, required=False, help="Y-axis threshold for volcano plots (p-value & FDR adjusted p-value).")
    parser.add_argument("--x_axis_threshold", type=float, default=1.0, required=False, help="X-axis threshold for volcano plots (log2 fold change).")

    args = parser.parse_args()

    # Create the output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Call the function with the provided arguments
    pval_df, fdr_df = get_min_and_fdr(args.input_dir, args.output_dir, args.screen)

    # If volcano flag is set, create the volcano plots
    if args.volcano:
        make_volcano_plots(pval_df, fdr_df, args.output_dir, args.screen, args.y_axis_threshold, args.x_axis_threshold)
    


if __name__ == "__main__":
    main()