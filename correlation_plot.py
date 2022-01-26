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
plt.style.use('seaborn-poster')
sns.set_context("paper")


# INPUT
# ARGV1 INTEGRATED FILE
# ARGV2 OUTPUT FOLDER

def plot_correlation(original_df_filtered):

    # start figure to plot all in one plot (scatter correlation CFD)
    plt.figure(figsize=(20, 20))

    for guide in original_df["Spacer+PAM"].unique():

        df_guide = original_df.loc[(original_df['Spacer+PAM'] == guide)]

        print('plotting for guide:', guide)
        original_df_cfd_sort = df_guide.sort_values(
            ['CFD_score_(highest_CFD)'], ascending=False)
        original_df_crista_sort = df_guide.sort_values(
            ['CRISTA_score_(highest_CRISTA)'], ascending=False)

        sns.jointplot(data=original_df_cfd_sort.head(1000), x="CFD_score_(highest_CFD)",
                      y="CRISTA_score_(highest_CRISTA)", kind="reg", joint_kws={'line_kws': {'color': 'yellow'}})

    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.tight_layout()

    plt.savefig(
        sys.argv[2]+f'correlation_CFDvCRISTA_{guide}_top1000CFD.pdf')
    plt.clf()
    plt.close('all')

    # start figure to plot all in one plot (scatter correlation CRISTA)
    plt.figure(figsize=(20, 20))

    for guide in original_df["Spacer+PAM"].unique():

        df_guide = original_df.loc[(original_df['Spacer+PAM'] == guide)]

        print('plotting for guide:', guide)
        original_df_cfd_sort = df_guide.sort_values(
            ['CFD_score_(highest_CFD)'], ascending=False)
        original_df_crista_sort = df_guide.sort_values(
            ['CRISTA_score_(highest_CRISTA)'], ascending=False)

        sns.jointplot(data=original_df_crista_sort.head(1000), x="CFD_score_(highest_CFD)",
                      y="CRISTA_score_(highest_CRISTA)", kind="reg", joint_kws={'line_kws': {'color': 'yellow'}})
    plt.xlim(0, 1)
    plt.ylim(0, 1)

    plt.tight_layout()
    plt.savefig(
        sys.argv[2]+f'correlation_CFDvCRISTA_{guide}_top1000CRISTA.pdf')
    plt.clf()
    plt.close('all')

    # start figure to plot all in one plot (top1000 union with rank)
    plt.figure(figsize=(20, 20))

    for guide in original_df["Spacer+PAM"].unique():

        df_guide = original_df.loc[(original_df['Spacer+PAM'] == guide)]
        df_guide.reset_index(inplace=True)

        print('plotting for guide:', guide)
        original_df_cfd_sort = df_guide.sort_values(
            ['CFD_score_(highest_CFD)'], ascending=False)
        original_df_crista_sort = df_guide.sort_values(
            ['CRISTA_score_(highest_CRISTA)'], ascending=False)

        cfd_crista_point_x_coordinates = list()
        cfd_crista_point_y_coordinates = list()
        sorted_cfd_index_list = list(original_df_cfd_sort['index'])
        sorted_crista_index_list = list(
            original_df_crista_sort['index'])

        for pos, index in enumerate(sorted_cfd_index_list[:1000]):
            cfd_crista_point_x_coordinates.append(pos+1)
            try:
                cfd_crista_point_y_coordinates.append(
                    sorted_crista_index_list.index(index)+1)
            except:
                cfd_crista_point_y_coordinates.append(1001)

        ax = sns.scatterplot(
            x=cfd_crista_point_x_coordinates, y=cfd_crista_point_y_coordinates, marker='+', color="skyblue")
        ax.set(xlabel='CFD Rank', ylabel='CRISTA Rank')

    plt.xlim(1, 1000)
    plt.ylim(1, 1000)
    plt.xticks([1, 100, 1000])
    plt.yticks([1, 100, 1000])
    ax.invert_xaxis()
    ax.invert_yaxis()
    ax.margins(0.05)
    # plt.hlines(100, 1, 10000)
    # plt.vlines(100, 1, 10000)

    plt.tight_layout()
    plt.savefig(sys.argv[2]+f'scatter_rank_CFDvCRISTA_{guide}_top100.pdf')
    plt.clf()
    plt.close('all')


print('start processing')
original_df = pd.read_csv(sys.argv[1], sep="\t", index_col=False,
                          na_values=['n'])

# filter df to remove on-targets and mutant on-targets
# original_df = original_df.loc[(
#     original_df['Mismatches+bulges_(fewest_mm+b)'] > 1)]
plot_correlation(original_df)
# correlation plot exec
# for guide in original_df["Spacer+PAM"].unique():
#     df_guide = original_df.loc[(original_df['Spacer+PAM'] == guide)]
#     # reset index after guide extraction
#     df_guide.reset_index(inplace=True)
#     # start correlation plots
#     plot_correlation(guide, df_guide)
