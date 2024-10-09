#!/usr/bin/env bash

# Determine the user's working directory
WD=${INIT_CWD:-$(pwd)}

# Optionally, read in the subtask directory path with a `-p` argment
# (Must be the first argument)
NODE=${1}
LOG=${2:-"out.log"}
COMMAND=${3:-"automech run"}

echo "Arguments:"
echo "  NODE=${NODE}"
echo "  LOG=${LOG}"
echo "  COMMAND=${COMMAND}"

ACTIVATION_HOOK="$(pixi shell-hook)"
SCRIPT_HEADER='
    echo Running on $(hostname) in $(pwd)
    echo Process ID: $$
'
SCRIPT="
    ${SCRIPT_HEADER}
    echo Run command: ${COMMAND}
    ${COMMAND}
"

# Enter working directory and initiate job from the first SSH node
ssh ${NODE} /bin/env bash << EOF
    set -e
    cd ${WD}
    ${SCRIPT_HEADER}
    eval ${ACTIVATION_HOOK@Q}
    nohup sh -c ${SCRIPT@Q} > ${LOG} 2>&1 &
EOF