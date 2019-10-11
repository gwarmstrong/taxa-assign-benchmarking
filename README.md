[![Build Status](https://travis-ci.org/gwarmstrong/taxa-assign-benchmarking.svg?branch=master)](https://travis-ci.org/gwarmstrong/taxa-assign-benchmarking)
[![Coverage Status](https://coveralls.io/repos/github/gwarmstrong/taxa-assign-benchmarking/badge.svg?branch=master)](https://coveralls.io/github/gwarmstrong/taxa-assign-benchmarking?branch=master)

*This repository is under active development, many backwards incompatible changes are likely.*

# taxa-assign-benchmarking
This repo is a Snakemake workflow for benchmarking taxonomy assignments. The
goal of this project is to reduce the amount of work put into setting up and
formatting results from taxonomic profilers.

Currently, the input depends on having 
[CAMISIM](https://github.com/CAMI-challenge/CAMISIM.git) formatted reads folders
as input.

## Install

There are no releases of this software currently. It can be installed
via git and bash in the following way:
```bash
git clone https://github.com/gwarmstrong/taxa-assign-benchmarking.git
cd taxa-assign-benchmarking
conda env create -n taxa-benchmarking -f ci/requirements.txt
conda activate taxa-benchmarking
pip install -e .
```

## Usage

TODO: better explanations of file hierarchies

This tool makes use of `snakemake`'s CLI. You can begin by directly copying a
simulation's output from CAMISIM into the `data/simulations/` directory.
Additionally, if there are any methods that you have pre-computed the profile for,
you can put them into the `data/profiles/` directory. Once the input files are
configured appropriately, you can run the snakemake workflow with a command
similar to the following on a cluster:

```bash
snakemake -p --use-conda \
    --cluster-config cluster.json \
    --cluster "qsub -l mem={cluster.mem_gb}gb -l walltime={cluster.time} -o cluster -e cluster" \
    -j 10 \
    --latency-wait 120 \
    --configfile config.yaml
```

The command following `--cluster` may differ depending upon your specific cluster.

Example `config.yaml` and `cluster.json` files are included in the base directory
of this repo.
