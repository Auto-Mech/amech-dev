#!/usr/bin/env bash

# Optionally, read in the subtask directory path with a `-p` argment
# (Must be the first argument)
SUBTASK_PATH="subtasks"
while getopts ":p:" opt; do
  case $opt in
    p)
      SUBTASK_PATH=$OPTARG
      set -- "${@:3}" # remove flag and argument from list of nodes
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done

# Read in the list of nodes
read -a NODES <<< "${@}"
FIRST_NODE=${NODES[0]}
NODES_CSV="$(printf '%s,' ${NODES[@]})"

echo "Arguments:"
echo "  SUBTASK_PATH=${SUBTASK_PATH}"
echo "  NODES_CSV=${NODES_CSV}"

ACTIVATION_HOOK="$(pixi shell-hook)"
RUN_COMMAND="automech subtasks run-adhoc -p ${SUBTASK_PATH} -n ${NODES_CSV} -a ${ACTIVATION_HOOK@Q}"
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