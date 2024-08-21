# Overview

SWARM is a wait-free replication protocol for shared data in disaggregated memory that provides 1-RTT reads and writes.

SWARM-KV is an RDMA-based disaggregated key-value store that leverages SWARM to offer 1-RTT GETs and UPDATEs.

This repository contains the artifacts and the instructions needed to reproduce the experiments in our SOSP paper.
More precisely, it contains:
* Instructions on how to configure a cluster to deploy and run the experiments.
* Instructions on how to build and deploy the payloads of the experiments.
* Instructions on how to launch the experiments and obtain the results.

## Claims

By running the experiments, you should be able to reproduce the numbers shown in:
* **Figure 5**: Latency CDFs for SWARM-KV, two other key-value stores (DM-ABD and FUSEE), and raw disaggregated memory.
* **Figure 6**: Per-client throughput-latency graphs for SWARM-KV and DM-ABD.
* **Figure 7**: Throughput and latency of SWARM-KV and DM-ABD for varying numbers of clients and parallel operations.
* **Figure 8**: Throughput and latency of SWARM-KV for YCSB workloads A and B, and varying value sizes; compared with a variant of SWARM-KV without in-place updates.
* **Figure 9**: Median latency and per-client throughput of SWARM-KV and DM-ABD for different numbers of replicas.
* **Figure 10**: Latency and throughput of a SWARM-KV client before and after the failure of a memory node.
* **Figure 11**: Latency CDFs for SWARM-KV and DM-ABD with a single key-value pair under stress and 16 clients.
* **Figure 12**: Latency CDFs for SWARM-KV for 64 clients and a varying number of metadata buffers.

## Getting Started Instructions

Assuming you have access to a pre-configured cluster, you will be able to run a first experiment---
that measures the latency of GETs and UPDATEs of SWARM-KV, two other key-value stores, and raw disaggregated memory (figure 5)---in less than 30 minutes by:
1. Connecting to the pre-configured cluster's gateway,
2. [Building and deploying the evaluation binaries](#Building-and-Deploying-the-Binaries),
3. [Running the scripts for figure 5](#Running-Experiments).

# Detailed instructions

This section will guide you on how to configure, build, and run all the experiments **from scratch**.
If you have access to a pre-configured cluster, skip to [building and deploying the binaries](#Building-and-Deploying-the-Binaries).

## Cluster Configuration

### Cluster Prerequisites

Running all experiments requires:
* a cluster of 8 machines connected via an InfiniBand fabric,
* Ubuntu 20.04 (different systems may work, but they have not been tested),
* all machines having the following ports open: 7000-7100, 11211, 18515, 9998.

### Deployment Dependencies

#### Gateway Dependencies

The artifacts are built and packaged into binaries. Subsequently, these binaries are deployed from a *gateway* machine (e.g., your laptop).
The gateway machine requires the following depencencies installed to be able to execute the deployment (and evaluation) scripts:
```sh
sudo apt install -y coreutils gawk python3 zip tmux
```

#### Cluster Machine Dependencies

The cluster machines, assuming they are already setup for InfiniBand+RDMA, require the following dependencies to be able to execute the binaries:
```sh
sudo apt install -y coreutils gawk python3 zip tmux gcc numactl libmemcached-dev memcached openjdk-8-jre-headless
```

The proper version of Mellanox OFED's InfiniBand drivers can be installed on the cluster machines via:
```sh
wget http://www.mellanox.com/downloads/ofed/MLNX_OFED-5.3-1.0.0.1/MLNX_OFED_LINUX-5.3-1.0.0.1-ubuntu20.04-x86_64.tgz
tar xf MLNX_OFED_LINUX-5.3-1.0.0.1-ubuntu20.04-x86_64.tgz
sudo ./mlnxofedinstall
```

### Build Dependencies

To build the evaluation binaries, you need the dependencies below.
> *Note*: You can build and package the binaries in a cluster machine, the gateway or another machine. It is important, however, that you build the binaries in a machine with the same distro/version as the cluster machines, otherwise the binaries may not work. For example, you can use a docker container to build and package the binaries. Alternatively, you can use one of the machines in the cluster.

Install the required dependencies on a vanilla Ubuntu 20.04 installation via:
```sh
sudo apt update
sudo apt -y install \
    python3 python3-pip \
    gawk build-essential cmake ninja-build \
    git libssl-dev \
    libmemcached-dev \
    libibverbs-dev # only if Mellanox OFED is not installed.
pip3 install --upgrade "conan>=1.63.0,<2.0.0"
```

## Building and Deploying the Binaries

Assuming all the machines in your cluster have the same configuration, you need to:
* build all the necessary binaries, for example in a deployment machine,
* package them and deploy them on all 8 machines.

### Recursively Cloning this Repository

First, clone this repository on the gateway, including the swarm-kv submodule, via:
```sh
git clone https://github.com/LPD-EPFL/swarm-artifacts.git --recurse-submodules
cd swarm-artifacts
```

If you are not using our pre-configured cluster, set the proper FQDN of the cluster's machines in `scripts/config.sh`.

### Building the Binaries

Build the evaluation binaries via:
```sh
./bin/swarm-kv/build.sh distclean buildclean clean # cleans potential leftovers
./bin/swarm-kv/build.sh swarm-kv fusee
./bin/swarm-kv/build.sh swarm-kv fusee # due to conan concurrency issues, the first command might run into missing dependencies 
```

Binaries for SWARM-KV and FUSEE will appear in `bin/swarm-kv/swarm-kv/build/bin` and `bin/swarm-kv/fusee/build/bin`, respectively.

### Downloading YCSB

Download YCSB binaries via:
```sh
./download-ycsb.sh
```

This should download `ycsb-0.12.0.tar.gz` in the current directory.

### Deploying the Binaries

Zip the binaries and prepare their deployment via:
```sh
./bin/zip-binaries.sh
./prepare-deployment.sh # generates deployment.zip
```

To deploy, you will need to:
- send `deployment.zip` to all the cluster's servers,
- unzip `deployment.zip` in the `~/swarm-artifacts` directory,
- untar `~/swarm-artifacts/ycsb-0.12.0.tar.gz` in the `~/swarm-artifacts` directory,
- rename the `~/swarm-artifacts/ycsb-0.12.0` directory to `~/swarm-artifacts/YCSB`,
- unzip `~/swarm-artifacts/bin/bin.zip` in the `~/swarm-artifacts/bin` directory.

On our pre-configured cluster, this can be done via:
```sh
./send-deployment.sh
```

As a sanity check, the `~/swarm-artifacts` directory should contain the `bin`, `experiments`, `scripts`, `workloads` and `YCSB` subfolders.

## Running Experiments

### Experiments

Once the binaries are deployed, you can reproduce the results presented in our paper from the gateway by running the following scripts.
During the kick-the-tires period, we invite you to run the scripts of [figure 5](#figure-5) as a sanity check.

#### Figure 5

```sh
experiments/fig5-latency-cdf.sh # run the experiment
./gather-logs.sh # retrieve the logs from the workers to the gateway
print-datapoints/fig5-latency-cdf.py # print the data points
```

#### Figure 6

```sh
experiments/fig6-tput-latency.sh # run the experiment
./gather-logs.sh # retrieve the logs from the workers to the gateway
print-datapoints/fig6-tput-latency.py # print the data points
```

#### Figure 7

```sh
experiments/fig7-scaling-clients.sh # run the experiment
./gather-logs.sh # retrieve the logs from the workers to the gateway
print-datapoints/fig7-scaling-clients.py # print the data points
```

#### Figure 8

```sh
experiments/fig8-value-sizes.sh # run the experiment
./gather-logs.sh # retrieve the logs from the workers to the gateway
print-datapoints/fig8-value-sizes.py # print the data points
```

#### Figure 9

```sh
experiments/fig9-replication-factor.sh # run the experiment
./gather-logs.sh # retrieve the logs from the workers to the gateway
print-datapoints/fig9-replication-factor.py # print the data points
```

#### Figure 10

```sh
experiments/fig10-failure.sh # run a shorter experiment that focuses on the key points
./gather-logs.sh # retrieve the logs from the workers to the gateway
print-datapoints/fig10-failure.py # print the data points
```

#### Figure 11

```sh
experiments/fig11-single-key.sh # run the experiment
./gather-logs.sh # retrieve the logs from the workers to the gateway
print-datapoints/fig11-single-key.py # print the data points
```

#### Figure 12

```sh
experiments/fig12-metadata-buffers.sh # run the experiment
./gather-logs.sh # retrieve the logs from the workers to the gateway
print-datapoints/fig12-metadata-buffers.py # print the data points
```
