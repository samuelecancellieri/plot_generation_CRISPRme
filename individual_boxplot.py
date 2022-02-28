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
plt.style.use('seaborn-paper')

df_single_search = pd.read_csv(sys.argv[1], sep="\t", index_col=False, na_values=[
                               'n'], usecols=['Variant_samples_(highest_CFD)'])
df_double_search = pd.read_csv(sys.argv[2], sep="\t", index_col=False, na_values=[
                               'n'], usecols=['Variant_samples_(highest_CFD)'])
sample_file = open(sys.argv[3], 'r')
out_folder = sys.argv[4]


def count_ratio(boxplot_values, sample_dict: dict):
    for sample in sample_dict:
        # calculate ratio with shared targets
        ratio = 0  # shared_ratio
        if sample_dict[sample][1] != 0:  # if personal is not zero
            # ratio=private/personal
            ratio = sample_dict[sample][0]/sample_dict[sample][1]
        boxplot_values.append(ratio)


def count_personal_and_private(sample_string: str, sample_dict: dict):
    sample_list = sample_string.strip().split(',')
    for sample in sample_list:
        try:
            sample_dict[sample][1] += 1
            if len(sample_list) == 1:
                sample_dict[sample][0] += 1
        except:
            continue


sample_dict_single = dict()
sample_dict_double = dict()
for line in sample_file:
    if '#' in line:
        continue
    splitted = line.strip().split('\t')
    # [private,personal]
    sample_dict_single[splitted[0]] = [0, 0]
    sample_dict_double[splitted[0]] = [0, 0]
# analyze search
df_single_search['Variant_samples_(highest_CFD)'].apply(
    lambda x: count_personal_and_private(str(x), sample_dict_single))
df_double_search['Variant_samples_(highest_CFD)'].apply(
    lambda x: count_personal_and_private(str(x), sample_dict_double))

# list containing lists ratio for private_single_search/personal_single_search
boxplot_values_single_search = []
# private_double_search/personal_double_search
boxplot_values_double_search = []
count_ratio(boxplot_values_single_search, sample_dict_single)
count_ratio(boxplot_values_double_search, sample_dict_double)


df_complete = pd.DataFrame(
    {'1000G': boxplot_values_single_search, '1000G+HGDP': boxplot_values_double_search})

# DISTPLOT
plt.figure(figsize=(20, 20))
# plt.boxplot(boxplot_values)
sns.displot(df_complete, kind="kde")
# sns.boxplot(data=boxplot_values)
plt.xlabel('Ratio of private/personal targets')
plt.ylabel('Density')
plt.tight_layout()
plt.savefig(
    out_folder+f"1000G_boxplot.pdf")
plt.clf()
plt.close('all')
