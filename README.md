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

Assuming you have access to a pre-configured cluster, you will be able to run a first experiment---that measures the latency of GETs and UPDATEs of SWARM-KV, two other key-value stores, and raw disaggregated memory (figure 5)---in less than 30 minutes by:
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

**Optionnally**, if you want to generate the plots from the datapoints, the gateway also requires the following dependencies:
```sh
sudo apt install python3-packaging fonts-linuxlibertine
fc-cache -f -v
rm ~/.cache/matplotlib -rf
pip3 install --upgrade pip
pip3 install --upgrade importlib_resources matplotlib
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

Make sure your working path has no spaces or special characters (e.g. `/home/user/mydir-1/swarm-artifacts` is fine).

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

This should download `ycsb-0.12.0.tar.gz` in the current directory, and print `ycsb-0.12.0.tar.gz: OK` if the checksum matches.

### Deploying the Binaries

Zip the binaries and prepare their deployment via:
```sh
./bin/zip-binaries.sh
./prepare-deployment.sh # generates deployment.zip
```

Then, for each cluster server, you will need to:
- create a `swarm-artifacts` directory with the same path as the one on the gateway,
- send `deployment.zip` to said directory,
- unzip `deployment.zip` in said directory,
- untar `swarm-artifacts/ycsb-0.12.0.tar.gz` in said directory,
- rename the `swarm-artifacts/ycsb-0.12.0` directory to `swarm-artifacts/YCSB`,
- unzip `swarm-artifacts/bin/bin.zip` in the `swarm-artifacts/bin` directory.

On our pre-configured cluster, this can be done from the gateway via a single:
```sh
./send-deployment.sh
```

If anything goes wrong, or you want to clean workers, you can undo the deployment via `./undo-deployment.sh`. This will also delete remote logs.

Once the deployment is done, do not move the `swarm-artifacts` directory.

As a sanity check, the `swarm-artifact` directory of each worker should contain the `bin`, `experiments`, `scripts`, `workloads` and `YCSB` subdirectories.

## Running Experiments

### Experiments

Once the binaries are deployed, you can reproduce the results presented in our paper from the gateway by running the following scripts.
During the kick-the-tires period, we invite you to run the scripts of [figure 5](#figure-5) as a sanity check.

> Note: Due to differences in hardware and software configuration, you can expect the pre-configured cluster we provide to achieve up to both 10% higher latency and 10% lower throughput than the setup used in the accepted version of the paper.
> However, such degradations should not affect the behaviors and relative comparisons presented in the paper.

Each experiment takes roughly takes ~15-30 minutes to run.

#### Figure 5

```sh
experiments/fig5-latency-cdf.sh # run the experiment
./gather-logs.sh # retrieve the logs from the workers to the gateway
print-datapoints/fig5-latency-cdf.py # print the data points
plot-datapoints/fig5-latency-cdf.py # plot as pdf in output-plots/
```

#### Figure 6

```sh
experiments/fig6-limited-cache.sh # run the experiment
./gather-logs.sh # retrieve the logs from the workers to the gateway
print-datapoints/fig6-limited-cache.py # print the data points
plot-datapoints/fig6-limited-cache.py # plot as pdf in output-plots/
```

#### Figure 7

```sh
experiments/fig7-tput-latency.sh # run the experiment
./gather-logs.sh # retrieve the logs from the workers to the gateway
print-datapoints/fig7-tput-latency.py # print the data points
plot-datapoints/fig7-tput-latency.py # plot as pdf in output-plots/
```

#### Figure 8

```sh
experiments/fig8-scaling-clients.sh # run the experiment
./gather-logs.sh # retrieve the logs from the workers to the gateway
print-datapoints/fig8-scaling-clients.py # print the data points
plot-datapoints/fig8-scaling-clients.py # plot as pdf in output-plots/
```

#### Figure 9

```sh
experiments/fig9-value-sizes.sh # run the experiment
./gather-logs.sh # retrieve the logs from the workers to the gateway
print-datapoints/fig9-value-sizes.py # print the data points
plot-datapoints/fig9-value-sizes.py # plot as pdf in output-plots/
```

#### Figure 10

```sh
experiments/fig10-replication-factor.sh # run the experiment
./gather-logs.sh # retrieve the logs from the workers to the gateway
print-datapoints/fig10-replication-factor.py # print the data points
plot-datapoints/fig10-replication-factor.py # plot as pdf in output-plots/
```

#### Figure 11

```sh
experiments/fig11-failure.sh # run a shorter experiment that focuses on the key points
./gather-logs.sh # retrieve the logs from the workers to the gateway
print-datapoints/fig11-failure.py # print the data points
plot-datapoints/fig11-failure.py # plot as pdf in output-plots/
```

#### Figure 12

```sh
experiments/fig12-single-key.sh # run the experiment
./gather-logs.sh # retrieve the logs from the workers to the gateway
print-datapoints/fig12-single-key.py # print the data points
plot-datapoints/fig12-single-key.py # plot as pdf in output-plots/
```

#### Figure 13

```sh
experiments/fig13-metadata-buffers.sh # run the experiment
./gather-logs.sh # retrieve the logs from the workers to the gateway
print-datapoints/fig13-metadata-buffers.py # print the data points
plot-datapoints/fig13-metadata-buffers.py # plot as pdf in output-plots/
```

# Navigating the code

How to navigate the code is described in the [README of the swarm-kv repository](https://github.com/LPD-EPFL/swarm-kv?tab=readme-ov-file#navigating-the-code).
