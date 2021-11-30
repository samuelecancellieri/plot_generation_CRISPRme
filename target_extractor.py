import sys
import pandas as pd


original_df = pd.read_csv(sys.argv[1], sep="\t", index_col=False,
                          na_values=['n'])


alt_target_count_CFD = original_df.apply(lambda x: True
                                         if x['REF/ALT_origin_(highest_CFD)'] == "alt" else False, axis=1)
alt_target_count_MMvBUL = original_df.apply(lambda x: True
                                            if x['REF/ALT_origin_(fewest_mm+b)'] == "alt" else False, axis=1)

# Count number of True in the series
original_df['alt_target_cfd'] = len(
    alt_target_count_CFD[alt_target_count_CFD == True].index)

original_df['alt_target_mmvbul'] = len(
    alt_target_count_MMvBUL[alt_target_count_MMvBUL == True].index)

original_df['total_target'] = len(original_df.index)

on_target_df = original_df.loc[(
    original_df['Mismatches+bulges_(highest_CFD)'] <= 1)]

print(on_target_df[['Spacer+PAM', 'Chromosome',
                    'Start_coordinate_(highest_CFD)', 'Aligned_protospacer+PAM_REF_(highest_CFD)',
                    'Annotation_closest_gene_name', 'total_target', 'alt_target_cfd', 'alt_target_mmvbul']])
