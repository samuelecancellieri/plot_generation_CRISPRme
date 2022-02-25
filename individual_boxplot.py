from email import header
import fileinput
import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
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


def count_personal_and_private(sample_list: list):
    for sample in sample_list.strip().split(','):
        if sample not in sample_dict.keys():
            # personal,private
            sample_dict[sample] = [0, 0]
        sample_dict[sample][0] += 1
        if len(sample_list) == 1:
            sample_dict[sample][1] += 1


for line in file_in:
    split = line.strip().split('\t')
    # extract samples str from target line
    count_personal_and_private(split[22])

sample_dict.pop('NA', None)

# list containing ratio for 1000G,HGDP,BOTH
boxplot_values = [[], [], []]
for sample in sample_dict:
    ratio = 0
    if sample_dict[sample][0] != 0:  # if personal is not zero
        # ratio=private/personal
        ratio = sample_dict[sample][1]/sample_dict[sample][0]
    if 'HGDP' in sample:
        boxplot_values[1].append(ratio)
    else:
        boxplot_values[0].append(ratio)
    boxplot_values[2].append(ratio)
print(boxplot_values)

plt.figure()
plt.boxplot(boxplot_values)
plt.tight_layout()
plt.savefig(
    out_folder+f"boxplot_1000G_HGDP_both.pdf")
plt.clf()
plt.close('all')
