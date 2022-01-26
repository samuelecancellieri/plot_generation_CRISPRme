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
# plt.style.use('seaborn-poster')
sns.set_context("paper")


# INPUT
# ARGV1 INTEGRATED FILE
# ARGV2 OUTPUT FOLDER

def plot_correlation(original_df):

    # start figure to plot all in one plot (scatter correlation CFD)
    plt.figure()
    data_frames_list = list()

    for guide in original_df["Spacer+PAM"].unique():

        df_guide = original_df.loc[(original_df['Spacer+PAM'] == guide)]

        original_df_cfd_sort = df_guide.sort_values(
            ['CFD_score_(highest_CFD)'], ascending=False)
        data_frames_list.append(original_df_cfd_sort.head(1000))

    final_df = pd.concat(data_frames_list)
    sns.jointplot(data=final_df, x="CFD_score_(highest_CFD)",
                  y="CRISTA_score_(highest_CRISTA)", kind="reg", joint_kws={'line_kws': {'color': 'orange'}})
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.tight_layout()

    plt.savefig(
        sys.argv[2]+f'correlation_CFDvCRISTA_top1000CFD.pdf')
    plt.clf()
    plt.close('all')

    # start figure to plot all in one plot (scatter correlation CRISTA)
    plt.figure()
    data_frames_list = list()

    for guide in original_df["Spacer+PAM"].unique():

        df_guide = original_df.loc[(original_df['Spacer+PAM'] == guide)]

        original_df_crista_sort = df_guide.sort_values(
            ['CRISTA_score_(highest_CRISTA)'], ascending=False)
        data_frames_list.append(original_df_crista_sort.head(1000))

    final_df = pd.concat(data_frames_list)
    sns.jointplot(data=final_df, x="CFD_score_(highest_CFD)",
                  y="CRISTA_score_(highest_CRISTA)", kind="reg", joint_kws={'line_kws': {'color': 'orange'}})
    plt.xlim(0, 1)
    plt.ylim(0, 1)

    plt.tight_layout()
    plt.savefig(
        sys.argv[2]+f'correlation_CFDvCRISTA_top1000CRISTA.pdf')
    plt.clf()
    plt.close('all')

    # start figure to plot all in one plot (top1000 union with rank)
    plt.figure()
    x_coordinates_list = list()
    y_coordinates_list = list()

    for guide in original_df["Spacer+PAM"].unique():

        df_guide = original_df.loc[(original_df['Spacer+PAM'] == guide)]
        df_guide.reset_index(inplace=True)

        print('plotting for guide:', guide)
        original_df_cfd_sort = df_guide.sort_values(
            ['CFD_score_(highest_CFD)'], ascending=False)
        original_df_crista_sort = df_guide.sort_values(
            ['CRISTA_score_(highest_CRISTA)'], ascending=False)

        top1000_union_CFDvCRISTA = pd.concat([original_df_cfd_sort.head(
            1000), original_df_crista_sort.head(1000)]).drop_duplicates()

        cfd_crista_point_x_coordinates = list()
        cfd_crista_point_y_coordinates = list()
        top1000_union_CFDvCRISTA.sort_values(
            ['CFD_score_(highest_CFD)'], ascending=False, inplace=True)
        sorted_cfd_index_list = list(top1000_union_CFDvCRISTA['index'])
        top1000_union_CFDvCRISTA.sort_values(
            ['CRISTA_score_(highest_CRISTA)'], ascending=False, inplace=True)
        sorted_crista_index_list = list(top1000_union_CFDvCRISTA['index'])

        for pos, index in enumerate(sorted_cfd_index_list[:1000]):
            cfd_crista_point_x_coordinates.append(pos+1)
            try:
                cfd_crista_point_y_coordinates.append(
                    sorted_crista_index_list.index(index)+1)
            except:
                cfd_crista_point_y_coordinates.append(1001)

        x_coordinates_list.extend(cfd_crista_point_x_coordinates)
        y_coordinates_list.extend(cfd_crista_point_y_coordinates)

        # sns.scatterplot(x=cfd_crista_point_x_coordinates,
        #                 y=cfd_crista_point_y_coordinates, marker='+', color="skyblue")
        # sns.jointplot(x=cfd_crista_point_x_coordinates, y=cfd_crista_point_y_coordinates,
        #               kind="reg", joint_kws={'line_kws': {'color': 'orange'}})
    # ax1 = sns.scatterplot(
    #     x=cfd_crista_point_x_coordinates, y=cfd_crista_point_y_coordinates, marker='+', color="skyblue")
    # ax2 = sns.histplot(x=cfd_crista_point_x_coordinates,
    #                     y=cfd_crista_point_y_coordinates, kde=True)
    # ax1.set(xlabel='CFD Rank', ylabel='CRISTA Rank')
    # ax1.invert_xaxis()
    # ax1.invert_yaxis()
    # ax2.set(xlabel='CFD Rank', ylabel='CRISTA Rank')
    # ax2.invert_xaxis()
    # ax2.invert_yaxis()
    # sns.JointGrid(ax1, ax2)
    sns.jointplot(x=x_coordinates_list, y=y_coordinates_list,
                  kind="reg", joint_kws={'line_kws': {'color': 'orange'}})
    # sns.scatterplot(x=x_coordinates_list, y=y_coordinates_list,
    # marker='o', color="skyblue")
    # plt.xlim(1, 1000)
    # plt.ylim(1, 1000)
    # plt.xticks([1, 100, 1000])
    # plt.yticks([1, 100, 1000])
    # ax.set(xlabel='CFD Rank', ylabel='CRISTA Rank')
    # ax.invert_xaxis()
    # ax.invert_yaxis()
    # ax.margins(0.1)
    # plt.hlines(100, 1, 1000)
    plt.vlines(1, 1, 2000)

    plt.tight_layout()
    plt.savefig(sys.argv[2]+f'scatter_rank_CFDvCRISTA_top1000_union.pdf')
    plt.clf()
    plt.close('all')


print('start processing')
original_df = pd.read_csv(sys.argv[1], sep="\t", index_col=False,
                          na_values=['n'], usecols=['Spacer+PAM', 'CFD_score_(highest_CFD)', 'CRISTA_score_(highest_CRISTA)'])
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
