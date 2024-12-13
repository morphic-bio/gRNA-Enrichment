# gRNA-Enrichment

## Overview

This repository contains a [Bidepot-workflow-builder (Bwb)](https://github.com/BioDepot/BioDepot-workflow-builder) workflow to run MAGeCK count and a Jupyter Notebook for comparing the outputs of counts between samples from MSK (original data providers) and Bwb (reprocessed from the workflow).

## Workflow

**MAGeCK Count**: This step involves running the MAGeCK count tool (version 0.5.9.5) to quantify gRNA abundance from sequencing data.

## Comparison Analysis

**CompareCounts.ipynb**: A Jupyter Notebook is provided to compare the gRNA counts between the original MSK data and the reprocessed Bwb data.

## Requirements

- Bwb
- Python 3.x
    - Pandas
    - NumPy
- Jupyter Notebook

## References

This repository uses MAGeCK, a tool created by Li, et al.

Li, W., Xu, H., Xiao, T. et al. MAGeCK enables robust identification of essential genes from genome-scale CRISPR/Cas9 knockout screens. Genome Biol 15, 554 (2014). https://doi.org/10.1186/s13059-014-0554-4

- Installation can be found on [SOURCEFORGE](https://sourceforge.net/projects/mageck/)
- Source code can be found on [Bitbucket](https://bitbucket.org/liulab/mageck/src/master/)


## Acknowledgments

- MorPhiC MSK team for providing the original data and processing scripts.
- Contributors to the MAGeCK tool.