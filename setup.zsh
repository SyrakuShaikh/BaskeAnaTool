#export PATH=/afs/ihep.ac.cn/soft/common/python27_sl65/bin:$PATH
# BaskDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BaskDIR="$(realpath "$(dirname "$0")")"
# echo "$BaskDIR"
export PYTHONPATH=${BaskDIR}:$PYTHONPATH
source /besfs/users/lihb/software/SL6/python-2.7.16/thispython.sh

# shellcheck source=short/setup.sh
source "${BaskDIR}/short/setup.zsh"
# shellcheck source=SimAndRec/setup.sh
cd ${BaskDIR}/SimAndRec 
python addSimor.py
cd ${BaskDIR}
source "${BaskDIR}/SimAndRec/setup.zsh"
