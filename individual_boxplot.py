import sys
import re
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
plt.style.use('seaborn-poster')

# df = pd.read_csv(sys.argv[1], sep="\t",
#                  index_col=False, na_values=['n'], usecols=['Variant_samples_(highest_CFD)'])
file_in = open(sys.argv[1], 'r')
file_in.readline()  # skip header
out_folder = sys.argv[2]
sample_dict = dict()

HG_PATTERN = 'HG[0-9]'


def count_personal_and_private(sample_list: str):
    sample_string = sample_list
    sample_list = sample_list.strip().split(',')
    only_1000G = False
    only_HGDP = False
    if 'HGDP' not in sample_list:
        only_1000G = True
    if 'NA' not in sample_list and (re.match(HG_PATTERN, sample_string) == False):
        only_HGDP = True
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
    count_personal_and_private(split[22])

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
    if sample_dict[sample][0] != 0:  # if personal is not zero
        # ratio=private/only
        ratio = sample_dict[sample][1]/sample_dict[sample][2]
    if 'HGDP' in sample:
        boxplot_values[3].append(ratio)
    else:
        boxplot_values[1].append(ratio)

for count, elem in enumerate(boxplot_values):
    plt.figure()
    # plt.boxplot(boxplot_values)
    sns.displot(elem, kind="kde")
    # sns.boxplot(data=boxplot_values)
    plt.xlabel('Dataset of variant targets')
    plt.ylabel('Ratio of private targets/personal targets')
    plt.tight_layout()
    plt.savefig(
        out_folder+f"{count}_boxplot_1000G_HGDP_both.pdf")
    plt.clf()
    plt.close('all')
