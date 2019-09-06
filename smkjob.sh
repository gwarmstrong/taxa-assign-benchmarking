snakemake -p --use-conda --cluster-config cluster.json --cluster "qsub -l mem={cluster.mem_gb}gb -l walltime={cluster.time} -o cluster -e cluster" -j 10 --latency-wait 120 --configfile config.yaml
