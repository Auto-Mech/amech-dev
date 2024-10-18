#!/bin/bash

# This script downloads each forked repo from the user's GitHub, checks out the dev
# branch and updates it against the main Auto-Mech repo
#
# Arguments:
#   - GitHub username (required)
#   - Repo branch (default: dev)

set -e  # if any command fails, quit
REPOS=("autochem" "autoio" "autofile" "mechanalyzer" "mechdriver")
DIR=$( dirname -- $( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd ))

# 0. Read arguments
USERNAME=${1}
UPSTREAM=${2}
MODE=${3}
BRANCH=${4:-dev}

if [ -z "${1}" ]; then
    read -p "Please enter your GitHub username: " USERNAME
fi
echo "Next, press enter to choose the default values, unless you know what you are doing..."
if [ -z "${2}" ]; then
    read -p "  Update against Auto-Mech upstream? (yes [default] or no): " UPSTREAM
    UPSTREAM=${UPSTREAM:-yes}
fi
if [ -z "${3}" ]; then
    read -p "  How would you like to clone? (ssh [default] or http): " MODE
    MODE=${MODE:-ssh}
fi

echo "Arguments:"
echo "  Username - ${USERNAME}"
echo "  Update   - ${UPSTREAM}"
echo "  Mode     - ${MODE}"
echo "  Branch   - ${BRANCH}"
read -p "Is this correct? If so, press enter to continue"

CLONE_PREFIX="https://github.com/${USERNAME}"
if [ "${MODE}" == "ssh" ]; then
    CLONE_PREFIX="git@github.com:${USERNAME}"
fi

# 1. Enter the source directory
(
    cd ${DIR}/src

    # 2. Loop through each repo and download it
    for repo in ${REPOS[@]}
    do
        # a. Clone the repo
        printf "\n*** Cloning from ${CLONE_PREFIX}/${repo}.git ***\n"
        git clone ${CLONE_PREFIX}/${repo}.git
        # b. If it worked, enter the repo, add Auto-Mech as a remote, and add the branch
        # both locally and on GitHub
        if [ "${UPSTREAM}" == "yes" ]; then
            (
                # i. Enter the repository
                cd ${repo}
                # ii. If the desired branch isn't the default one, fetch it from origin and
                # switch to it
                branch=$( git branch | tr -d [*] | xargs )
                if [[ ${branch} != ${BRANCH} ]]; then
                    git fetch origin ${BRANCH} && \
                    git branch ${BRANCH} FETCH_HEAD && \
                    git checkout ${BRANCH}
                fi
                # iii. Rebase the selected branch against upstream
                git remote add upstream https://github.com/Auto-Mech/${repo} && \
                git pull --rebase upstream ${BRANCH} && \
                git push origin ${BRANCH}
            )
        fi
        printf "******\n"
    done
)
