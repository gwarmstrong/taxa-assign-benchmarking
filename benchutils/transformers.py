import os
import pandas as pd

kraken_rank_dictionary = {
    'C': 'class',
    'P': 'phylum',
    'F': 'family',
    'G': 'genus',
    'O': 'order',
    'S': 'species'  # TODO convert to strain to species using ETE toolkit (it
    # gets kind of tricky because kraken gives pretty high res species
    # estimates
}

kraken_columns = ['PERCENTAGE', 'lca_read_count', 'read_count', 'rank',
                  '@@TAXID', 'TAXNAME']

#  Order: o__, Family: f__, Genus: g__, Species: s__]
def kraken2_all_to_rank(all_rank_summary, output_rank_summaries, ranks):
    # TODO finsih docs
    """Converts a summary of all ranks from kraken into rank-wise profiles
    similar to the CAMI-SIM output

    Parameters
    ----------
    all_rank_summary
    output_rank_summaries
    ranks

    Returns
    -------

    """
    # TODO COULD be split into two format functions: one to reformat,
    #  and one to split on rank
    # TODO give error for invalid rank value
    all_ranks = pd.read_csv(all_rank_summary, sep='\t')
    all_ranks.columns = kraken_columns
    # TODO for kraken is it okay to just take the first part (drop the number)
    all_ranks['rank'] = all_ranks['rank'].str[0]
    all_ranks = all_ranks.loc[all_ranks['rank'].isin(kraken_rank_dictionary)]
    all_ranks['RANK'] = [kraken_rank_dictionary[key] for key in
                         all_ranks['rank']]
    keep_cols = ['@@TAXID', 'RANK', 'TAXNAME', 'PERCENTAGE']
    for output_, rank in zip(output_rank_summaries, ranks):
        sub_df = all_ranks.loc[all_ranks['RANK'] == rank]
        sub_df_matching = sub_df[keep_cols]
        sub_df_matching.to_csv(output_, sep='\t', index=False)
