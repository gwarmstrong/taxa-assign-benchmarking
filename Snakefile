from benchutils import metrics, plotting, transformers

# filename = "anonymous_reads.fq"
# (SIM,DT,NUM) = glob_wildcards("data/simulations/{simname}/{datetime}_sample_{sample_num}/reads/anonymous_reads.fq")
#
filename = "medium_anon_reads.fq"
(SIM,DT,NUM) = glob_wildcards("data/simulations/{simname}/{datetime}_sample_{sample_num}/reads/" + filename)

METHODS = ["kraken2", "metaphlan2", "shogun"]

# TODO auprc vs. l2 score curve 
# TODO benchmarks for memory/time

RANKS = config["ranks"]

rule all:
    input:
        expand("analyses/{simname}/{datetime}_sample_{sample_num}.{rank}.done",
               simname=SIM,
               datetime=DT,
               sample_num=NUM,
               rank=RANKS)
    shell:
        "rm {input}"

rule allplots:
    input:
        absolute_errorplot = "analyses/{simname}/plots/{datetime}_sample_{sample_num}.{rank}.absolute_errorplot.ext",
        correlationplot = "analyses/{simname}/plots/{datetime}_sample_{sample_num}.{rank}.correlationplot.ext"
    output:
        "analyses/{simname}/{datetime}_sample_{sample_num}.{rank}.done"
    shell:
        """
        touch {output}
        """

rule absolute_error_plot:
    input:
        "analyses/{simname}/summaries/{datetime}_sample_{sample_num}.{rank}.absolute_error.txt"
    output:
        "analyses/{simname}/plots/{datetime}_sample_{sample_num}.{rank}.absolute_errorplot.ext"
    run:
        plotting.absolute_error_plot(input, output)

rule profile_correlation_plot:
    input:
        "analyses/{simname}/summaries/{datetime}_sample_{sample_num}.{rank}.correlation.txt"
    output:
        "analyses/{simname}/plots/{datetime}_sample_{sample_num}.{rank}.correlationplot.ext"
    run:
        plotting.correlation_plot(input, output)

rule benchmark_absolute_error:
    input:
         true_profile = "data/simulations/{simname}/taxonomic_profile_{sample_num}.txt",
         obs_profiles = expand("analyses/{{simname}}/profiles/{method}/{{datetime}}_sample_{{sample_num}}.{{rank}}.profile.txt", method=METHODS)
    output:
          absolute_error = "analyses/{simname}/summaries/{datetime}_sample_{sample_num}.{rank}.absolute_error.txt",
    run:
        metrics.profile_error(input.obs_profiles, input.true_profile, output.absolute_error, wildcards.rank, methods=METHODS, metric='absolute_error')

rule benchmark_profile_correlation:
    input:
         true_profile = "data/simulations/{simname}/taxonomic_profile_{sample_num}.txt",
         obs_profiles = expand("analyses/{{simname}}/profiles/{method}/{{datetime}}_sample_{{sample_num}}.{{rank}}.profile.txt", method=METHODS)
    output:
          correlation = "analyses/{simname}/summaries/{datetime}_sample_{sample_num}.{rank}.correlation.txt"
    run:
        metrics.profile_error(input.obs_profiles, input.true_profile, output.correlation, wildcards.rank, methods=METHODS, metric='correlation')

rule kraken2_rank:
    input:
        "analyses/{simname}/profiles/kraken2/{datetime}_sample_{sample_num}._all.profile.txt"
    output:
        expand("analyses/{{simname}}/profiles/kraken2/{{datetime}}_sample_{{sample_num}}.{rank}.profile.txt", rank=RANKS)
    run:
        transformers.kraken2_all_to_rank(str(input), output, ranks=RANKS)

rule kraken2_all:
    input:
        "data/simulations/{simname}/{datetime}_sample_{sample_num}/reads/" + filename
    output:
        "analyses/{simname}/profiles/kraken2/{datetime}_sample_{sample_num}._all.profile.txt"
    conda:
        "envs/taxa-benchmark.yml"
    shell:
        # TODO filter for given level (should maybe be a seperate step)
        """
        kraken2 --db {config[kraken_db]} --use-names --report {output} {input} 
        """

rule metaphlan2:
    input:
        "data/simulations/{simname}/{datetime}_sample_{sample_num}/reads/" + filename
    output:
        expand("analyses/{{simname}}/profiles/metaphlan2/{{datetime}}_sample_{{sample_num}}.{{rank}}.profile.txt", rank=RANKS)
    resources:
        mem_gb=64
    conda:
        "envs/taxa-benchmark.yml"
    shell:
        # TODO add ability to change desired taxa level
        # may need to remove old metaphlan bowtie indices
        """
        rm -f {input}.bowtie2out.txt
        touch {output}
        # metaphlan2.py {input} --input_type fastq --tax_lev 'g' > {output}        
        """

rule shogun:
    input:
        "data/simulations/{simname}/{datetime}_sample_{sample_num}/reads/" + filename
    output:
        expand("analyses/{{simname}}/profiles/shogun/{{datetime}}_sample_{{sample_num}}.{{rank}}.profile.txt", rank=RANKS)
    conda:
        "envs/taxa-benchmark.yml"
    shell:
        "touch {output}"

# rule kraken2_transformer
# rule metaphlan2_transformer
# rule shogun_transformer
