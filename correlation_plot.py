from operator import truediv
import sys
from traceback import print_tb
from turtle import color
import pandas as pd
import matplotlib
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib_venn import venn2
import warnings
from scipy import stats

# SUPPRESS ALL WARNINGS
warnings.filterwarnings("ignore")
# do not use X11
matplotlib.use('Agg')
# set matplotlib for pdf editing
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42


# INPUT
# ARGV1 INTEGRATED FILE
# ARGV2 OUTPUT FOLDER


def r2(x, y):
    return stats.pearsonr(x, y)[0] ** 2


def plot_correlation(guide, original_df_filtered):

    print('plotting')
    original_df_cfd_sort = original_df_filtered.sort_values(
        ['CFD_score_(highest_CFD)'], ascending=False)
    original_df_crista_sort = original_df_filtered.sort_values(
        ['CRISTA_score_(highest_CRISTA)'], ascending=False)

    # union of top100 CFD & CRISTA
    df_union_crista_cfd_100 = pd.concat(
        [original_df_crista_sort.head(100), original_df_cfd_sort.head(100)]).drop_duplicates()

    plt.figure()
    original_df_filtered.sort_values(
        ['CFD_score_(highest_CFD)'], ascending=False, inplace=True)
    sns.jointplot(x='CFD_score_(highest_CFD)', y='CRISTA_score_(highest_CRISTA)',
                  kind="reg", data=original_df_filtered, stat_func=r2)
    # sns.regplot(data=original_df_filtered, x='CFD_score_(highest_CFD)',
    #             y='CRISTA_score_(highest_CRISTA)', fit_reg=True, color='blue')
    plt.xlim(0, 1)
    plt.ylim(0, 1)

    plt.tight_layout()
    plt.savefig(sys.argv[2]+f'correlation_CFDvCRISTA_{guide}_no_filter.png')
    plt.clf()
    plt.close('all')

    plt.figure()

    ax = sns.regplot(data=df_union_crista_cfd_100, x="CFD_score_(highest_CFD)",
                     y="CRISTA_score_(highest_CRISTA)", fit_reg=False, marker="+", color="skyblue")

    df_union_crista_cfd_100.to_csv(sys.argv[2]+guide+'_union_CFDvCRISTA.tsv',
                                   sep='\t', na_rep='NA', index=False)

    ax.set(xlabel='CFD Score', ylabel='CRISTA Score')

    plt.tight_layout()
    plt.savefig(sys.argv[2]+f'correlation_CFDvCRISTA_{guide}_top100_union.pdf')
    plt.clf()
    plt.close('all')

    plt.figure()

    set_cfd = set(original_df_cfd_sort.head(100).index)
    set_crista = set(original_df_crista_sort.head(100).index)
    venn2([set_cfd, set_crista], ('CFD', 'CRISTA'))

    plt.tight_layout()
    plt.savefig(sys.argv[2]+f'venn_CFDvCRISTA_{guide}_top100_union.pdf')
    plt.clf()
    plt.close('all')

    plt.figure()

    cfd_crista_point_x_coordinates = list()
    cfd_crista_point_y_coordinates = list()
    sorted_cfd_index_list = list(original_df_cfd_sort['index'])
    sorted_crista_index_list = list(
        original_df_crista_sort['index'])

    for pos, index in enumerate(sorted_cfd_index_list[:100]):
        cfd_crista_point_x_coordinates.append(pos+1)
        cfd_crista_point_y_coordinates.append(
            sorted_crista_index_list.index(index)+1)

    ax = sns.scatterplot(
        x=cfd_crista_point_x_coordinates, y=cfd_crista_point_y_coordinates, marker='+', color="skyblue")
    ax.set(xlabel='CFD Rank', ylabel='CRISTA Rank')
    plt.yscale('log')
    ax.margins(0.05)
    plt.xticks([1, 20, 40, 60, 80, 100])
    # plt.ticklabel_format(style='plain', axis='y')

    plt.tight_layout()
    plt.savefig(sys.argv[2]+f'scatter_rank_CFDvCRISTA_{guide}_top100.pdf')
    plt.clf()
    plt.close('all')


print('start processing')
original_df = pd.read_csv(sys.argv[1], sep="\t", index_col=False,
                          na_values=['n'])

# filter df to remove on-targets and mutant on-targets
original_df = original_df.loc[(
    original_df['Mismatches+bulges_(fewest_mm+b)'] > 1)]

# correlation plot exec
for guide in original_df["Spacer+PAM"].unique():
    df_guide = original_df.loc[(original_df['Spacer+PAM'] == guide)]
    # reset index after guide extraction
    df_guide.reset_index(inplace=True)
    # start correlation plots
    plot_correlation(guide, df_guide)
