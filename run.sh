SCRIPT=$(readlink -f "$0")
EXEC_PATH=$(dirname "$SCRIPT")
source $EXEC_PATH/venv/bin/activate && python3 $EXEC_PATH/main.py $1 $2 && deactivate
