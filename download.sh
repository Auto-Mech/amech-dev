#!/bin/bash

set -e  # if any command fails, quit

# 0. First argument is the GitHub username. The second, optional, argument is the branch
# of the Git repo, which defaults (for now) to `dev`.
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
USERNAME=${1}
BRANCH=${2:-dev}

if [ -z "${1}" ]; then
    read -p "Please enter your GitHub username: " USERNAME
fi

echo "GitHub username: '${USERNAME}' | Branch to check out: '${BRANCH}'"
read -p "Is this correct? If so, press enter to continue"

# 1. Enter the source directory
(
    cd ${SCRIPT_DIR}/src

    # 2. Loop through each repo and download it
    REPOS=("autochem" "autoio" "autofile" "mechanalyzer" "mechdriver")
    for repo in ${REPOS[@]}
    do
        # a. Clone the repo
        printf "\n*** Cloning from git@github.com:${USERNAME}/${repo}.git ***\n"
        git clone git@github.com:${USERNAME}/${repo}.git
        # b. If it worked, enter the repo, add Auto-Mech as a remote, and add the branch
        # both locally and on GitHub
        (
            cd ${repo} && \
            git remote add upstream https://github.com/Auto-Mech/${repo} && \
            git checkout -b ${BRANCH} && \
            git pull --rebase upstream ${BRANCH} && \
            git push -u origin ${BRANCH}
        )
        printf "******\n"
    done
)