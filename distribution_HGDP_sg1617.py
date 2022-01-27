import sys
import time
import random
import pandas as pd
from pandas.core.indexes.api import all_indexes_same
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
# from upsetplot import generate_counts
from upsetplot import UpSet
# import matplotlib as mpl
from upsetplot import from_memberships
import warnings
import matplotlib
import math
# SUPPRESS ALL WARNINGS
warnings.filterwarnings("ignore")
# do not use X11
matplotlib.use('Agg')
# set matplotlib for pdf editing
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42


# INPUT
# ARGV1 TARGETS
# ARGV2 SAMPLEFILE
# ARGV3 OUTPUT_DIR

# original_df = pd.read_csv(sys.argv[1], sep="\t", index_col=False,
#                           na_values=['n'])
target_file = open(sys.argv[1], 'r')
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


def printDensityPlot():
    # create figure and set axis
    plt.figure()
    for pop in sample_dict:  # for each superpopulation
        andamenti = list()
        permutationList = list()
        for sample in sample_dict[pop]:
            # append samples to list to permute
            permutationList.append(sample)
        print('DOING POP PLOT FOR: ', pop)
        for permutation in range(0, 100):
            np.random.shuffle(permutationList)
            andamento = list()
            alreadyAddedTargets = set()
            for sample in permutationList:
                alreadyAddedTargets = alreadyAddedTargets.union(
                    sample_dict[pop][sample])
                andamento.append(len(alreadyAddedTargets))
            andamenti.append(andamento)
        # read values to generate plot
        andamentiArray = np.array(andamenti)
        media = np.mean(andamentiArray, axis=0)
        standarddev = np.std(andamentiArray, axis=0)
        standarderr = standarddev/np.sqrt(len(list(sample_dict[pop])))
        z_score = 1.96  # for confidence 95%
        lowerbound = media-(z_score*standarderr)
        upperbound = media+(z_score*standarderr)
        # allMedie.append(media)
        plt.plot(media, label=str(pop))
        plt.fill_between(range(len(media)), lowerbound,
                         upperbound, alpha=0.10)

    plt.title('populations_with diffCFD >=' + str(0.1) +
              ' and CI '+str(95)+'%'+' and CFD score >='+str(0.2))
    plt.xlabel('# Individuals')
    plt.ylabel('# Cumulative Targets')
    # plt.legend()
    plt.tight_layout()
    plt.savefig(sys.argv[3]+'_allpop_with_diffCFD_'+str(0.1) +
                'and_CI_95_and_CFD_score_'+str(0.2)+'.pdf')


for index, target in enumerate(target_file):
    if 'CFD' in target:
        continue
    split = target.strip().split('\t')
    samples = split[22].split(',')  # position in old integrated of samples
    for sample in samples:
        pop = pop_dict[sample]
        sample_dict[pop][sample].add(index)

# print(sample_dict)
printDensityPlot()
