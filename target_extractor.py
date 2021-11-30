import sys
import pandas as pd


original_df = pd.read_csv(sys.argv[1], sep="\t", index_col=False,
                          na_values=['n'])


alt_target_count_CFD = original_df.apply(lambda x: True
                                         if x['REF/ALT_origin_(highest_CFD)'] == "alt" else False, axis=1)
alt_target_count_MMvBUL = original_df.apply(lambda x: True
                                            if x['REF/ALT_origin_(fewest_mm+b)'] == "alt" else False, axis=1)

# Count number of True in the series
alt_target_count_CFD = len(
    alt_target_count_CFD[alt_target_count_CFD == True].index)

alt_target_count_MMvBUL = len(
    alt_target_count_MMvBUL[alt_target_count_MMvBUL == True].index)

on_target_df = original_df.loc[(
    original_df['Mismatches+bulges_(highest_CFD)'] <= 1)]

print(on_target_df, len(original_df.index),
      alt_target_count_CFD, alt_target_count_MMvBUL)
