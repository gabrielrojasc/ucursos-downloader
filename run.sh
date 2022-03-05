EXEC_PATH=$(dirname "$0")
source $EXEC_PATH/env/bin/activate && python3 $EXEC_PATH/main.py && deactivate
