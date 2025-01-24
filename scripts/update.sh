#!/bin/bash

# This script updates each repo against a remote
# (It also updates the amech-dev repo.)
#
# Performs a pull --rebase followed by a push
#
# Arguments:
#   - Remote to update against (default: upstream)
#   - Branch to update (default: dev)
#   - Flags to add to the push command, e.g. --force (default: none)

set -e  # if any command fails, quit
REPOS=("autochem" "autoio" "autofile" "mechanalyzer" "mechdriver")
DIR=$( dirname -- $( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd ))

# 0. Read arguments
REMOTE=${1:-upstream}
BRANCH=${2:-dev}
FLAGS=${@:3}

# 1. Update the amech-dev repo
git checkout main
git pull https://github.com/Auto-Mech/amech-dev
pixi self-update
pixi install

# 2. Loop through each repo and update
echo "The following commands will be run in each repository:"
echo "    git checkout ${BRANCH}"
echo "    git pull --rebase ${REMOTE} ${BRANCH}"
echo "    git push ${FLAGS} origin ${BRANCH}"
read -p "Is this what you want to do? [y/n] " yn

if [[ $yn =~ ^[Yy]$ ]]; then
    for repo in ${REPOS[@]}
    do
        printf "\n*** Updating in ${DIR}/src/${repo} ***\n"
        (
            cd ${DIR}/src/${repo} && \
            git checkout ${BRANCH} && \
            git pull --rebase ${REMOTE} ${BRANCH} && \
            git push ${FLAGS} origin ${BRANCH}
        )
        printf "******\n"
    done
fi

if git config --get remote.origin.url | grep -i Auto-Mech > /dev/null; then
    echo "No fork of amech-dev found. Not attempting to push amech-dev."
else
    echo "You appear to be working on a fork of amech-dev."
    read -p "Do you want to push amech-dev changes to your fork? [y/n] " yn
    if [[ $yn =~ ^[Yy]$ ]]; then
        git push origin
    fi
fi

git checkout -
