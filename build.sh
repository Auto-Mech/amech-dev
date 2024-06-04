#!/bin/bash

# This script builds conda packages for each repo using rattler-build
# At the end, it prints the command for uploading them

set -e  # if any command fails, quit
REPOS=("autochem" "autoio" "autofile" "mechanalyzer" "mechdriver")
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# 1. Enter the source directory
(
    cd ${SCRIPT_DIR}

    # 2. Run rattler-build for each repository
    for repo in ${REPOS[@]}
    do
        printf "\n*** Building ${SCRIPT_DIR}/src/${repo} ***\n"
        (
            rattler-build build -r src/${repo}/.
        )
        printf "******\n"
    done

    echo "You can upload your packages with the following command:"
    echo "  rattler-build upload anaconda -o Auto-Mech output/noarch/*.conda"
    echo "which will upload the following artifacts to Anaconda.org:"
    ls -la output/noarch/*.conda
)
