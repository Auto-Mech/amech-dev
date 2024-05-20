#!/bin/bash

set -e  # if any command fails, quit
REPOS=("autochem" "autoio" "autofile" "mechanalyzer" "mechdriver")
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# 0. Read argument: The branch to update (default: dev)
REMOTE=${1:-upstream}
BRANCH=${2:-dev}
FLAGS=${@:3}

echo "Execute the following commands in each repository?"
echo "    git checkout ${BRANCH}"
echo "    git pull --rebase ${REMOTE} ${BRANCH}"
echo "    git push ${FLAGS} origin ${BRANCH}"
read -p "Press enter to confirm "

# 2. Loop through each repo and execute the command
for repo in ${REPOS[@]}
do
    printf "\n*** Updating in ${SCRIPT_DIR}/src/${repo} ***\n"
    (
        cd ${SCRIPT_DIR}/src/${repo} && \
        git checkout ${BRANCH} && \
        git pull --rebase ${REMOTE} ${BRANCH} && \
        git push ${FLAGS} origin ${BRANCH}
    )
    printf "******\n"
done