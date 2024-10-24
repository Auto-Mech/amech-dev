#!/bin/bash

# This script runs a command inside each repo in src/
#
# Arguments:
#   - Command to run (default: git status)

set -e  # if any command fails, quit
REPOS=("autochem" "autoio" "autofile" "mechanalyzer" "mechdriver")
DIR=$( dirname -- $( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd ))

# 0. Read arguments
COMMAND="${@:-status}"

# 1. If running something other than git status, confirm
if [[ "${COMMAND}" != "status" ]]; then
    read -p "Execute 'git ${COMMAND}' in each repository? Press enter to confirm "
fi

# 2. Loop through each repo and execute the command
for repo in ${REPOS[@]}
do
    printf "\n*** Running 'git ${COMMAND}' in ${DIR}/src/${repo} ***\n"
    (
        cd ${DIR}/src/${repo} && git ${COMMAND}
    )
    printf "******\n"
done