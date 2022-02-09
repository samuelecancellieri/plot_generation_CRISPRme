from math import ceil
import sys
# import time
# import random
# import pandas as pd
# from pandas.core.indexes.api import all_indexes_same
# import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
# from matplotlib.colors import LogNorm
# from upsetplot import generate_counts
# from upsetplot import UpSet
# import matplotlib as mpl
# from upsetplot import from_memberships
import warnings
import matplotlib
import matplotlib.patches as mpatches

# import math
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

target_file = open(sys.argv[1], 'r')
sample_file = open(sys.argv[2], 'r')
sample_dict = dict()
pop_dict = dict()
color_dict = {'AFR': 'tab:orange', 'AMR': 'tab:brown', 'CSA': 'tab:blue',
              'EAS': 'tab:pink', 'EUR': 'tab:red', 'MEA': 'tab:purple', 'OCE': 'tab:green'}


for line in sample_file:
    split = line.strip().split('\t')
    if '#' in line:
        continue
    # split[0] = sample
    # split[1] = pop
    # split[2] = super_pop
    if split[2] not in sample_dict:
        sample_dict[split[2]] = dict()
    if split[1] not in sample_dict[split[2]]:
        sample_dict[split[2]][split[1]] = dict()
    # sampledict[superpop][pop][sample]=set() will contain the indices of targets for the samples
    sample_dict[split[2]][split[1]][split[0]] = set()
    # pop_dict[split[0]] = [split[1], split[2]]

for index, target in enumerate(target_file):
    if 'CFD' in target:
        continue
    split = target.strip().split('\t')
    samples = split[22].split(',')  # position in old integrated of samples
    for sample in samples:
        # pop = pop_dict[sample][0]
        for superpop in sample_dict:
            for pop in sample_dict[superpop]:
                try:
                    # try inserting index in correct dict, if not continue and try again
                    sample_dict[superpop][pop][sample].add(index)
                except:
                    continue


def printDensityPlot(superpop_dict: dict, superpop: str):
    # create figure and set axis
    # plt.figure()
    fig = plt.figure()
    ax = plt.subplot(111)
    for pop in superpop_dict:  # for each population in superpopulation
        andamenti = list()
        permutationList = list()
        for sample in superpop_dict[pop]:
            # append samples to list to permute
            permutationList.append(sample)
        print('DOING POP PLOT FOR: ', pop)
        for permutation in range(0, 100):
            np.random.shuffle(permutationList)
            andamento = list()
            alreadyAddedTargets = set()
            for sample in permutationList:
                alreadyAddedTargets = alreadyAddedTargets.union(
                    superpop_dict[pop][sample])
                andamento.append(len(alreadyAddedTargets))
            andamenti.append(andamento)
        # read values to generate plot
        andamentiArray = np.array(andamenti)
        media = np.mean(andamentiArray, axis=0)
        standarddev = np.std(andamentiArray, axis=0)
        standarderr = standarddev/np.sqrt(len(list(superpop_dict[pop])))
        z_score = 1.96  # for confidence 95%
        lowerbound = media-(z_score*standarderr)
        upperbound = media+(z_score*standarderr)
        # allMedie.append(media)
        ax.plot(media, label=str(pop))
        ax.fill_between(range(len(media)), lowerbound,
                        upperbound, alpha=0.10)

    plt.title(superpop+'_with diffCFD >=' + str(0.1) +
              ' and CI '+str(95)+'%'+' and CFD score >='+str(0.2))
    plt.xlabel('# Individuals')
    plt.ylabel('# Cumulative Targets')

    # legend handles
    # AFR = mpatches.Patch(color='tab:orange', label="AFR")
    # AMR = mpatches.Patch(color='tab:brown', label="AMR")
    # CSA = mpatches.Patch(color='tab:blue', label="CSA")
    # EAS = mpatches.Patch(color='tab:pink', label="EAS")
    # EUR = mpatches.Patch(color='tab:red', label="EUR")
    # MEA = mpatches.Patch(color='tab:purple', label="MEA")
    # OCE = mpatches.Patch(color='tab:green', label="OCE")

    # move legend outside plot by reducing plot dimensions
    # box = ax.get_position()
    # ax.set_position([box.x0, box.y0 + box.height * 0.1,
    #                  box.width, box.height * 0.9])

    # # # Put a legend below current axis
    # ax.legend(loc='upper center', fontsize=8, bbox_to_anchor=(
    #     0.5, -0.05), ncol=ceil(len(list(superpop_dict[pop]))/2))

    # plt.gca().add_artist(plt.legend(fontsize=8, loc='upper center', handles=[
    #     AFR, AMR, CSA, EAS, EUR, MEA, OCE], title='Super Populations', bbox_to_anchor=(0.5, -0.05), ncol=len(color_dict.keys())))

    # ax.tight_layout()
    plt.legend(fontsize=8)
    plt.savefig(sys.argv[3]+superpop+'_with_diffCFD_'+str(0.1) +
                'and_CI_95_and_CFD_score_'+str(0.2)+'.pdf')


# print(sample_dict)
for superpop in sample_dict:
    superpop_dict = sample_dict[superpop]
    printDensityPlot(superpop_dict, superpop)
