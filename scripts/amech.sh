#!/usr/bin/env bash

# Determine the user's working directory
WD=${INIT_CWD:-$(pwd)}

# Optionally, read in the subtask directory path with a `-p` argment
# (Must be the first argument)
NODE=${1}
LOG=${2:-"out.log"}

echo "Arguments:"
echo "  NODE=${NODE}"
echo "  LOG=${LOG}"

ACTIVATION_HOOK="$(pixi shell-hook)"
RUN_COMMAND="automech run"
SCRIPT_HEADER='
    echo Running on $(hostname) in $(pwd)
    echo Process ID: $$
'
SCRIPT="
    ${SCRIPT_HEADER}
    echo Run command: ${RUN_COMMAND}
    ${RUN_COMMAND}
"

# Enter working directory and initiate job from the first SSH node
ssh ${NODE} /bin/env bash << EOF
    set -e
    cd ${WD}
    ${SCRIPT_HEADER}
    eval ${ACTIVATION_HOOK@Q}
    nohup sh -c ${SCRIPT@Q} > ${LOG} 2>&1 &
EOF