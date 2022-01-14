import sys
import pandas as pd

# original_df = pd.read_csv(sys.argv[1], sep="\t", index_col=False,
#                           na_values=['n'])
target_file = open(sys.argv[1], 'w')
sample_file = open(sys.argv[2], 'r')
sample_dict = dict()
pop_dict = dict()
for line in sample_file:
    split = line.strip().split('\t')
    if '#' in line:
        continue
    #split[0] = sample
    #split[1] = pop
    if split[1] not in sample_dict:
        sample_dict[split[1]] = dict()

    sample_dict[split[1]][split[0]] = set()
    pop_dict[split[0]] = split[1]


# sg1617 = 'CTAACAGTTGCTTTTATCACNNN'

# sg1617_df = original_df.loc[original_df['Spacer+PAM'] == sg1617]
# sg1617_df = sg1617_df.loc[(sg1617_df['CFD_score_(highest_CFD)']
#                           >= 0.2 & sg1617_df['CFD_risk_score_(highest_CFD)'] >= 0.1)]
# sg1617_df = sg1617_df.loc[(sg1617_df['Variant_samples_(highest_CFD)'].str.contains(
#     'HGDP') & ~sg1617_df['Variant_samples_(highest_CFD)'].str.contains('NA'))]


for index, target in enumerate(target_file):
    split = target.strip().split('\t')
    samples = split[22].split(',')
    for sample in samples:
        pop = pop_dict[sample]
        sample_dict[pop][sample].add(index)

print(sample_dict)
