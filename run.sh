EXEC_PATH=$(dirname "$0")
clear
source $EXEC_PATH/env/bin/activate && python3 $EXEC_PATH/main.py $1 $2 && deactivate
