from benchutils import metrics, plotting

(SIM,DT,NUM) = glob_wildcards("data/simulations/{simname}/{datetime}_sample_{sample_num}/reads/anonymous_reads.fq")

METHODS = ["kraken2", "metaphlan2", "shogun"]

rule all:
    input:
        expand("analyses/{simname}/{datetime}_sample_{sample_num}.done",
               simname=SIM,
               datetime=DT,
               sample_num=NUM)
    shell:
        "rm {input}"

rule allplots:
    input:
        abserrorplot = "analyses/{simname}/plots/{datetime}_sample_{sample_num}.genus.abserrorplot.ext",
        profilecorrplot = "analyses/{simname}/plots/{datetime}_sample_{sample_num}.genus.profilecorrplot.ext"
    output:
        "analyses/{simname}/{datetime}_sample_{sample_num}.done"
    shell:
        "touch analyses/{wildcards.simname}/{wildcards.datetime}_sample_{wildcards.sample_num}.done"

rule absolute_error_plot:
    input:
        "analyses/{simname}/summaries/{datetime}_sample_{sample_num}.genus.abserror.txt"
    output:
        "analyses/{simname}/plots/{datetime}_sample_{sample_num}.genus.abserrorplot.ext"
    run:
        plotting.absolute_error_plot(input, output)

rule profile_correlation_plot:
    input:
        "analyses/{simname}/summaries/{datetime}_sample_{sample_num}.genus.profilecorr.txt"
    output:
        "analyses/{simname}/plots/{datetime}_sample_{sample_num}.genus.profilecorrplot.ext"
    run:
        plotting.correlation_plot(input, output)

rule benchmark_absolute_error:
    input:
         true_profile = "data/simulations/{simname}/taxonomic_profile_{sample_num}.txt",
         obs_profiles = expand("analyses/{{simname}}/profiles/{method}/{{datetime}}_sample_{{sample_num}}.genus.profile.txt", method=METHODS)
    output:
          abserror = "analyses/{simname}/summaries/{datetime}_sample_{sample_num}.genus.abserror.txt",
    run:
        metrics.absolute_error(input.obs_profiles, input.true_profile, output.abserror)

rule benchmark_profile_correlation:
    input:
         true_profile = "data/simulations/{simname}/taxonomic_profile_{sample_num}.txt",
         obs_profiles = expand("analyses/{{simname}}/profiles/{method}/{{datetime}}_sample_{{sample_num}}.genus.profile.txt", method=METHODS)
    output:
          profilecorr = "analyses/{simname}/summaries/{datetime}_sample_{sample_num}.genus.profilecorr.txt"
    run:
        metrics.correlation(input.obs_profiles, input.true_profile, output.profilecorr)

rule kraken2:
    input:
        "data/simulations/{simname}/{datetime}_sample_{sample_num}/reads/anonymous_reads.fq"
    output:
        "analyses/{simname}/profiles/kraken2/{datetime}_sample_{sample_num}.genus.profile.txt"
    conda:
        "envs/taxa-benchmark.yml"
    shell:
        "touch analyses/{wildcards.simname}/profiles/kraken2/{wildcards.datetime}_sample_{wildcards.sample_num}.genus.profile.txt"

rule metaphlan2:
    input:
        "data/simulations/{simname}/{datetime}_sample_{sample_num}/reads/anonymous_reads.fq"
    output:
        "analyses/{simname}/profiles/metaphlan2/{datetime}_sample_{sample_num}.genus.profile.txt"
    conda:
        "envs/taxa-benchmark.yml"
    shell:
        "touch analyses/{wildcards.simname}/profiles/metaphlan2/{wildcards.datetime}_sample_{wildcards.sample_num}.genus.profile.txt"

rule shogun:
    input:
        "data/simulations/{simname}/{datetime}_sample_{sample_num}/reads/anonymous_reads.fq"
    output:
        "analyses/{simname}/profiles/shogun/{datetime}_sample_{sample_num}.genus.profile.txt"
    conda:
        "envs/taxa-benchmark.yml"
    shell:
        "touch analyses/{wildcards.simname}/profiles/shogun/{wildcards.datetime}_sample_{wildcards.sample_num}.genus.profile.txt"

# rule kraken2_transformer
# rule metaphlan2_transformer
# rule shogun_transformer
