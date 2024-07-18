#!/bin/bash

# This script runs an editable pip install inside each repo, placing their python
# libraries in the environment path

set -e  # if any command fails, quit
REPOS=("autochem" "autoio" "autofile" "mechanalyzer" "mechdriver")
DIR=$( dirname -- $( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd ))

# 1. Enter the script directory and start the pixi shell
(
    cd ${DIR}

    # 2. Loop through each repo and execute the install command
    for repo in ${REPOS[@]}
    do
        printf "\n*** Installing ${DIR}/src/${repo} ***\n"
        (
            cd src/${repo} && \
            pip install -e . --no-deps
        )
        printf "******\n"
    done
)
