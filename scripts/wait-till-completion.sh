
set -u

SCRIPT_DIR="$( realpath -sm "$( dirname "${BASH_SOURCE[0]}" )" )"
source "$SCRIPT_DIR"/config.sh

MACHINE=$1
TMUX_SESSION=$2
LIMIT=$3

echo -n "Running"
for i in $(seq 1 $LIMIT); do
  echo -n "."
  sleep .9
  "$SCRIPT_DIR"/remote-invoker-completed.sh $1 $2
  if [ $? -eq 0 ]; then
    echo "  ✓"
    exit 0
  fi
done
echo " × Unresponsive! ×"
exit 1