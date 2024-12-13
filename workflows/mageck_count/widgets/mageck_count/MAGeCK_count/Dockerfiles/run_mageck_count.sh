#!/bin/bash

# Make output directory
mkdir -p "$outputDir"

# Run mageck count with the provided flagged arguments
echo "mageck count $@"
eval mageck count "$@"

# Send outputs to the output directory
mv /outputs/* "$outputDir"
echo "Outputs moved to $outputDir"