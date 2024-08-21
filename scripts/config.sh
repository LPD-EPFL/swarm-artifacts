# Use the absolute path
ROOT_DIR="$( realpath -sm  "$( dirname "${BASH_SOURCE[0]}" )"/.. )"
BIN_DIR="${ROOT_DIR}"/bin
LOG_DIR="${ROOT_DIR}"/logs
WORKLOAD_DIR="${ROOT_DIR}"/workloads
YCSB_BIN="${ROOT_DIR}"/YCSB/bin/ycsb.sh

TMUX_SESSION=oops

FIRST_MACHINE=1
FIRST_SERVER=$FIRST_MACHINE
SERVER_MACHINES=4
FIRST_CLIENT=$(($FIRST_MACHINE + $SERVER_MACHINES))
CLIENT_MACHINES=4
MACHINE_COUNT=$(($SERVER_MACHINES + $CLIENT_MACHINES))
REGISTRY_MACHINE=machine1

# Set ssh names of the machines
machine1=w7
machine2=w8
machine3=w6
machine4=w5
machine5=w1
machine6=w2
machine7=w3
machine8=w4

# Set fqdn names of the machines (use `hostname -f`)
machine1hostname=swarm-${machine1}
machine2hostname=swarm-${machine2}
machine3hostname=swarm-${machine3}
machine4hostname=swarm-${machine4}
machine5hostname=swarm-${machine5}
machine6hostname=swarm-${machine6}
machine7hostname=swarm-${machine7}
machine8hostname=swarm-${machine8}


# Memcached does not run with root access
#PONY_HAVE_SUDO_ACCESS=false
#PONY_SUDO_ASKS_PASS=false
#PONY_SUDO_PASS="MyPass"

# Do not edit below this line
machine2ssh () {
    local m=$1
    echo "${!m}"
}

machine2hostname () {
    local m=$1
    local m_hn=${m}hostname
    echo "${!m_hn}"
}

export DORY_REGISTRY_IP=$(machine2hostname $REGISTRY_MACHINE)
