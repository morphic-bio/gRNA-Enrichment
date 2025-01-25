#!/bin/bash

# Make output directory
mkdir -p "$outputDir"

# Run mageck test with the provided flagged arguments
echo "mageck test $@"
eval mageck test "$@"

# Send outputs to the output directory
mv /outputs/* "$outputDir"
echo "Outputs moved to $outputDir"