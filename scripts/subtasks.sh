#!/usr/bin/env bash

read -a NODES <<< "${@}"
FIRST_NODE=${NODES[0]}
NODES_CSV="$(printf '%s,' ${NODES[@]})"

ACTIVATION_HOOK="$(pixi shell-hook)"
RUN_COMMAND="automech subtasks run-adhoc -n ${NODES_CSV} -a ${ACTIVATION_HOOK@Q}"
SCRIPT_HEADER='
    echo Running on $(hostname) in $(pwd)
    echo Process ID: $$
'
SCRIPT="
    ${SCRIPT_HEADER}
    echo Run command: ${RUN_COMMAND}
    ${RUN_COMMAND}
"

ssh ${FIRST_NODE} /bin/env bash << EOF
    set -e
    cd $(pwd)
    ${SCRIPT_HEADER}
    eval ${ACTIVATION_HOOK@Q}
    nohup sh -c ${SCRIPT@Q} > sub.log 2>&1 &
EOF