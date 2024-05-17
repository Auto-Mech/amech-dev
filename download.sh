#!/bin/bash

# 0. First argument is the GitHub username. The second, optional, argument is the branch
# of the Git repo, which defaults (for now) to `dev`.
export USERNAME=${1}
export BRANCH=${2:-dev}
echo "Checking out ${BRANCH} branches for GitHub user ${USERNAME}..."

# 1. Enter the source directory
cd src

# 2. Loop through each repo and download it
export REPOS=("autochem" "autoio" "autofile" "mechanalyzer" "mechdriver")
for repo in ${REPOS[@]}
do
    # a. Clone the repo
    echo "Setting up the ${repo} repo..."
    git clone git@github.com:${USERNAME}/${repo}.git
    # b. Enter the repo
    (
        cd ${repo}
        # c. Add Auto-Mech as a remote
        git remote add upstream https://github.com/Auto-Mech/${repo}
        # d. Fetch the requested branch, check it out, and push it to origin
        git checkout -b ${BRANCH}
        git pull --rebase upstream ${BRANCH}
        git push -u origin ${BRANCH}
    )
done
