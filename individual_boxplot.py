import sys
import re
from traceback import print_tb
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import warnings
# SUPPRESS ALL WARNINGS
warnings.filterwarnings("ignore")
# do not use X11
matplotlib.use('Agg')
# set matplotlib for pdf editing
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
plt.style.use('seaborn-paper')

# df = pd.read_csv(sys.argv[1], sep="\t",
#                  index_col=False, na_values=['n'], usecols=['Variant_samples_(highest_CFD)'])
file_in = open(sys.argv[1], 'r')
file_in.readline()  # skip header
out_folder = sys.argv[2]
sample_dict = dict()


def count_personal_and_private(sample_string: str):
    sample_list = sample_string.strip().split(',')
    # print(sample_string)
    only_1000G = False
    only_HGDP = False
    if 'HGDP' not in sample_string:
        only_1000G = True
    if re.match('HG[0-9]|NA[0-9]', sample_string) is None:
        only_HGDP = True
    # print('re.match:', re.match('HG[0-9]|NA[0-9]', sample_string))
    # print('1000G:', only_1000G, 'HGDP:', only_HGDP)
    for sample in sample_list:
        if sample not in sample_dict.keys():
            # personal,private,only
            sample_dict[sample] = [0, 0, 0]
        sample_dict[sample][0] += 1
        if len(sample_list) == 1:
            sample_dict[sample][1] += 1
        if only_1000G:
            sample_dict[sample][2] += 1
        if only_HGDP:
            sample_dict[sample][2] += 1


for line in file_in:
    split = line.strip().split('\t')
    # extract samples str from target line
    if str(split[22]) == 'NA':
        continue
    count_personal_and_private(str(split[22]))

sample_dict.pop('NA', None)
sample_dict.pop('n', None)
# print(sample_dict)
# list containing ratio for 1000G_shared,1000G_only,HGDP_shared,HGDP_private
boxplot_values = [[], [], [], []]
for sample in sample_dict:
    # calculate ratio with shared targets
    ratio = 0  # shared_ratio
    if sample_dict[sample][0] != 0:  # if personal is not zero
        # ratio=private/personal
        ratio = sample_dict[sample][1]/sample_dict[sample][0]
    if 'HGDP' in sample:
        boxplot_values[2].append(ratio)
    else:
        boxplot_values[0].append(ratio)
    # calculate ratio with only targets
    ratio = 0  # only_ratio
    if sample_dict[sample][2] != 0:  # if only is not zero
        # ratio=private/only
        ratio = sample_dict[sample][1]/sample_dict[sample][2]
    if 'HGDP' in sample:
        boxplot_values[3].append(ratio)
    else:
        boxplot_values[1].append(ratio)

df_1000G = pd.DataFrame(
    {'1000G_shared': boxplot_values[0], '1000G_only': boxplot_values[1]})

df_hgdp = pd.DataFrame(
    {'HGDP_shared': boxplot_values[2], 'HGDP_only': boxplot_values[3]})

print(df_1000G)
print(df_hgdp)

# 1000G DISTPLOT
plt.figure(figsize=(20, 20))
# plt.boxplot(boxplot_values)
sns.displot(df_1000G, kind="kde", bw_adjust=2)
# sns.boxplot(data=boxplot_values)
plt.xlabel('Dataset of variant targets')
plt.ylabel('Ratio of private targets/personal targets')
plt.tight_layout()
plt.savefig(
    out_folder+f"1000G_boxplot.pdf")
plt.clf()
plt.close('all')

# HGDP DISTPLOT
plt.figure(figsize=(20, 20))
# plt.boxplot(boxplot_values)
sns.displot(df_hgdp, kind="kde", bw_adjust=2)
# sns.boxplot(data=boxplot_values)
plt.xlabel('Dataset of variant targets')
plt.ylabel('Ratio of private targets/personal targets')
plt.tight_layout()
plt.savefig(
    out_folder+f"HGDP_boxplot.pdf")
plt.clf()
plt.close('all')
