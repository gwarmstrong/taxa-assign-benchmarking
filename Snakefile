from benchutils import abserror, profilecorr

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

rule abserrorplot:
    input:
        "analyses/{simname}/summaries/{datetime}_sample_{sample_num}.genus.abserror.txt"
    output:
        "analyses/{simname}/plots/{datetime}_sample_{sample_num}.genus.abserrorplot.ext"
    shell:
        """
        python scripts/abserrorplot.py -i {input} -o {output}
        touch analyses/{wildcards.simname}/plots/{wildcards.datetime}_sample_{wildcards.sample_num}.genus.abserrorplot.ext
        """


rule profilecorrplot:
    input:
        "analyses/{simname}/summaries/{datetime}_sample_{sample_num}.genus.profilecorr.txt"
    output:
        "analyses/{simname}/plots/{datetime}_sample_{sample_num}.genus.profilecorrplot.ext"
    shell:
        """
        python scripts/profilecorrplot.py -i {input} -o {output}
        touch analyses/{wildcards.simname}/plots/{wildcards.datetime}_sample_{wildcards.sample_num}.genus.profilecorrplot.ext
        """

rule benchmarkerrors:
    input:
        true_profile = "data/simulations/{simname}/taxonomic_profile_{sample_num}.txt",
        obs_profiles = expand("analyses/{{simname}}/profiles/{method}/{{datetime}}_sample_{{sample_num}}.genus.profile.txt", method=METHODS)
    output:
        abserror = "analyses/{simname}/summaries/{datetime}_sample_{sample_num}.genus.abserror.txt",
        profilecorr = "analyses/{simname}/summaries/{datetime}_sample_{sample_num}.genus.profilecorr.txt"
    run:
       abserror.profile(input.obs_profiles, input.true_profile, output.abserror) 
       profilecorr.profile(input.obs_profiles, input.true_profile, output.profilecorr) 

#     shell:
#         """
#         python scripts/abserror.py --i-predicted-profiles {input.obs_profiles} --i-true-profile {input.true_profile} --o-abserror {output.abserror}
#         python scripts/profilecorr.py --i-predicted-profiles {input.obs_profiles} --i-true-profile {input.true_profile} --o-profile-corr {output.abserror}
#         touch analyses/{wildcards.simname}/summaries/{wildcards.datetime}_sample_{wildcards.sample_num}.genus.abserror.txt
#         touch analyses/{wildcards.simname}/summaries/{wildcards.datetime}_sample_{wildcards.sample_num}.genus.profilecorr.txt
#         """

rule kraken2:
    input:
        "data/simulations/{simname}/{datetime}_sample_{sample_num}/reads/anonymous_reads.fq"
    output:
        "analyses/{simname}/profiles/kraken2/{datetime}_sample_{sample_num}.genus.profile.txt"
    shell:
        "touch analyses/{wildcards.simname}/profiles/kraken2/{wildcards.datetime}_sample_{wildcards.sample_num}.genus.profile.txt"

rule metaphlan2:
    input:
        "data/simulations/{simname}/{datetime}_sample_{sample_num}/reads/anonymous_reads.fq"
    output:
        "analyses/{simname}/profiles/metaphlan2/{datetime}_sample_{sample_num}.genus.profile.txt"
    shell:
        "touch analyses/{wildcards.simname}/profiles/metaphlan2/{wildcards.datetime}_sample_{wildcards.sample_num}.genus.profile.txt"

rule shogun:
    input:
        "data/simulations/{simname}/{datetime}_sample_{sample_num}/reads/anonymous_reads.fq"
    output:
        "analyses/{simname}/profiles/shogun/{datetime}_sample_{sample_num}.genus.profile.txt"
    shell:
        "touch analyses/{wildcards.simname}/profiles/shogun/{wildcards.datetime}_sample_{wildcards.sample_num}.genus.profile.txt"

