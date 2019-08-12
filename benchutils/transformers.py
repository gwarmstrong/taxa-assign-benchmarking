import os

def kraken2_all_to_rank(all_rank_summary, output_rank_summaries, ranks):
    for output_, rank_ in zip(output_rank_summaries, ranks):
        os.system("touch {}".format(output_))
           

