import sys
import pandas as pd

df = pd.read_csv(sys.argv[1], sep="\t",
                 index_col=False, na_values=['n'], usecols=['Variant_samples_(highest_CFD)'])
out_folder = sys.argv[2]
sample_dict = dict()


def count_personal_and_private(row: pd.Series):
    sample_list = str(row['Variant_samples_(highest_CFD)']).strip().split(',')
    for sample in sample_list:
        if sample not in sample_dict.keys():
            # personal,private,ratio
            sample_dict[sample] = (0, 0, 0)
        sample_dict[sample][0] += 1
        if len(sample_list) == 1:
            sample_dict[sample][1] += 1


df.apply(count_personal_and_private, axis=1)
sample_dict.pop('NA', None)

for sample in sample_dict:
    if sample_dict[sample][0] != 0:  # if personal is not zero
        # ratio=private/personal
        sample_dict[sample][2] = sample_dict[sample][1]/sample_dict[sample][0]
