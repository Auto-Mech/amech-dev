#!/bin/bash

# This script builds conda packages for each repo using rattler-build
# At the end, it prints the command for uploading them

set -e  # if any command fails, quit
rattler-build build -r .recipe/

echo "You can upload your packages with the following command:"
echo "  rattler-build upload anaconda -o Auto-Mech output/noarch/*.conda"
echo "which will upload the following artifacts to Anaconda.org:"
ls -la output/noarch/*.conda
