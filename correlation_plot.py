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
import numpy as np

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
    sns.jointplot(data=final_df, x="CFD_score_(highest_CFD)", marginal_ticks=True, space=0.5,
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
    sns.jointplot(data=final_df, x='CRISTA_score_(highest_CRISTA)', marginal_ticks=True, space=0.5,
                  y="CFD_score_(highest_CFD)", kind="reg", joint_kws={'line_kws': {'color': 'orange'}})
    plt.xlim(0, 1)
    plt.ylim(0, 1)

    plt.tight_layout()
    plt.savefig(
        sys.argv[2]+f'correlation_CFDvCRISTA_top1000CRISTA.pdf')
    plt.clf()
    plt.close('all')

    # start figure to plot all in one plot (top1000 union with rank)
    plt.figure()
    # df list with all guides dfs
    df_guide_list = list()
    count_list = list()

    for guide in original_df["Spacer+PAM"].unique():

        # filter the df to obtain single guide targets
        df_guide = original_df.loc[(original_df['Spacer+PAM'] == guide)]
        df_guide['CFD_Rank'] = np.argsort(df_guide['CFD_score_(highest_CFD)'])
        df_guide['CRISTA_Rank'] = np.argsort(
            df_guide['CRISTA_score_(highest_CRISTA)'])
        df_guide['CFD_Rank'] += 1
        df_guide['CRISTA_Rank'] += 1

        df_guide_selected = df_guide.loc[(
            df_guide['CFD_Rank'] <= 1000) | (df_guide['CRISTA_Rank'] <= 1000)]

        df_guide_selected.loc[df_guide_selected['CFD_Rank']
                              > 1000, 'CFD_Rank'] = 1000
        df_guide_selected.loc[df_guide_selected['CRISTA_Rank']
                              > 1000, 'CRISTA_Rank'] = 1000

        df_guide_list.append(df_guide_selected)

        print('count for guide', guide)
        guide_list = list()
        guide_list.append(guide)
        print('count of targets in union top1000',
              len(df_guide_selected.index))
        guide_list.append(len(df_guide_selected.index))
        # CFD<100 & CRISTA<100
        print('CFD<=100 & CRISTA<=100')
        print(len(df_guide_selected[(df_guide_selected.CFD_Rank <= 100) & (
            df_guide_selected.CRISTA_Rank <= 100)].index))
        guide_list.append(len(df_guide_selected[(df_guide_selected.CFD_Rank <= 100) & (
            df_guide_selected.CRISTA_Rank <= 100)].index))
        # CFD<100 & CRISTA>100
        print('CFD<=100 & CRISTA>100')
        print(len(df_guide_selected[(df_guide_selected.CFD_Rank <= 100) & (
            df_guide_selected.CRISTA_Rank > 100)].index))
        guide_list.append(len(df_guide_selected[(df_guide_selected.CFD_Rank <= 100) & (
            df_guide_selected.CRISTA_Rank > 100)].index))
        # CFD>100 & CRISTA<100
        print('CFD>100 & CRISTA<=100')
        print(len(df_guide_selected[(df_guide_selected.CFD_Rank > 100) & (
            df_guide_selected.CRISTA_Rank <= 100)].index))
        guide_list.append(len(df_guide_selected[(df_guide_selected.CFD_Rank > 100) & (
            df_guide_selected.CRISTA_Rank <= 100)].index))
        # CFD>100 & CRISTA>100
        print('CFD>100 & CRISTA>100')
        print(len(df_guide_selected[(df_guide_selected.CFD_Rank > 100) & (
            df_guide_selected.CRISTA_Rank > 100)].index))
        guide_list.append(len(df_guide_selected[(df_guide_selected.CFD_Rank > 100) & (
            df_guide_selected.CRISTA_Rank > 100)].index))
        # append all counts to single list
        count_list.append(guide_list)

        plot = sns.JointGrid(data=df_guide_selected, x='CFD_Rank',
                             y='CRISTA_Rank', xlim=(1010, -10), ylim=(1010, -10), marginal_ticks=True)
        plot.plot_joint(sns.scatterplot, alpha=0.5)
        plot.plot_marginals(sns.histplot)

        plot.ax_joint.axvline(x=100)
        plot.ax_joint.axhline(y=100)
        plot.set_axis_labels('CFD Rank', 'CRISTA Rank')

        plt.tight_layout()
        # single guide figure
        plt.savefig(
            sys.argv[2]+f'scatter_rank_CFDvCRISTA_top1000_union_{guide}.pdf')
        plt.clf()
        plt.close('all')

    # whole figure
    final_df = pd.concat(df_guide_list)
    count_df = pd.DataFrame(count_list, columns=[
                            'sgRNA', 'CFD<=100&CRISTA<=100', 'CFD<=100 & CRISTA>100', 'CFD>100&CRISTA<=100', 'CFD>100&CRISTA>100'])
    count_df.to_csv(sys.argv[2]+'count_list_top1000_union.tsv',
                    sep='\t', na_rep='NA', index=False)

    print('whole figure')
    print('count of targets in union top1000',
          len(final_df.index))
    # CFD<100 & CRISTA<100
    print('CFD<=100 & CRISTA<=100')
    print(len(final_df[(final_df.CFD_Rank <= 100) & (
        final_df.CRISTA_Rank <= 100)].index))
    # CFD<100 & CRISTA>100
    print('CFD<=100 & CRISTA>100')
    print(len(final_df[(final_df.CFD_Rank <= 100) & (
        final_df.CRISTA_Rank > 100)].index))
    # CFD>100 & CRISTA<100
    print('CFD>100 & CRISTA<=100')
    print(len(final_df[(final_df.CFD_Rank > 100) & (
        final_df.CRISTA_Rank <= 100)].index))
    # CFD>100 & CRISTA>100
    print('CFD>100 & CRISTA>100')
    print(len(final_df[(final_df.CFD_Rank > 100) & (
        final_df.CRISTA_Rank > 100)].index))

    plot = sns.JointGrid(data=final_df, x='CFD_Rank',
                         y='CRISTA_Rank', xlim=(1010, -10), ylim=(1010, -10), marginal_ticks=True)
    plot.plot_joint(sns.scatterplot, alpha=0.5)
    plot.plot_marginals(sns.histplot)

    plot.ax_joint.axvline(x=100)
    plot.ax_joint.axhline(y=100)
    plot.set_axis_labels('CFD Rank', 'CRISTA Rank')

    plt.tight_layout()
    plt.savefig(sys.argv[2]+f'scatter_rank_CFDvCRISTA_top1000_union.pdf')
    plt.clf()
    plt.close('all')

    # start figure to plot all in one plot (top10000 union with rank)
    plt.figure()
    # df list with all guides dfs
    df_guide_list = list()

    for guide in original_df["Spacer+PAM"].unique():

        # filter the df to obtain single guide targets
        df_guide = original_df.loc[(original_df['Spacer+PAM'] == guide)]
        df_guide['CFD_Rank'] = np.argsort(df_guide['CFD_score_(highest_CFD)'])
        df_guide['CRISTA_Rank'] = np.argsort(
            df_guide['CRISTA_score_(highest_CRISTA)'])
        df_guide['CFD_Rank'] += 1
        df_guide['CRISTA_Rank'] += 1

        df_guide_selected = df_guide.loc[(
            df_guide['CFD_Rank'] <= 10000) | (df_guide['CRISTA_Rank'] <= 10000)]

        df_guide_selected.loc[df_guide_selected['CFD_Rank']
                              > 10000, 'CFD_Rank'] = 10000
        df_guide_selected.loc[df_guide_selected['CRISTA_Rank']
                              > 10000, 'CRISTA_Rank'] = 10000

        df_guide_list.append(df_guide_selected)

        print('count for guide', guide)
        print('count of targets in union top10000',
              len(df_guide_selected.index))
        # CFD<100 & CRISTA<100
        print('CFD<=100 & CRISTA<=100')
        print(len(df_guide_selected[(df_guide_selected.CFD_Rank <= 100) & (
            df_guide_selected.CRISTA_Rank <= 100)].index))
        # CFD<100 & CRISTA>100
        print('CFD<=100 & CRISTA>100')
        print(len(df_guide_selected[(df_guide_selected.CFD_Rank <= 100) & (
            df_guide_selected.CRISTA_Rank > 100)].index))
        # CFD>100 & CRISTA<100
        print('CFD>100 & CRISTA<=100')
        print(len(df_guide_selected[(df_guide_selected.CFD_Rank > 100) & (
            df_guide_selected.CRISTA_Rank <= 100)].index))
        # CFD>100 & CRISTA>100
        print('CFD>100 & CRISTA>100')
        print(len(df_guide_selected[(df_guide_selected.CFD_Rank > 100) & (
            df_guide_selected.CRISTA_Rank > 100)].index))

        plot = sns.JointGrid(data=df_guide_selected, x='CFD_Rank',
                             y='CRISTA_Rank', marginal_ticks=True)
        plot.plot_joint(sns.scatterplot, alpha=0.5)
        plot.plot_marginals(sns.histplot)

        plot.ax_joint.axvline(x=100)
        plot.ax_joint.axhline(y=100)
        plot.ax_joint.set_xscale('log')
        plot.ax_joint.set_yscale('log')
        plot.ax_joint.invert_yaxis()
        plot.ax_joint.invert_xaxis()
        plot.set_axis_labels('CFD Rank', 'CRISTA Rank')

        plt.tight_layout()
        # single guide figure
        plt.savefig(
            sys.argv[2]+f'scatter_rank_CFDvCRISTA_top10000_union_{guide}.pdf')
        plt.clf()
        plt.close('all')

    # whole figure
    final_df = pd.concat(df_guide_list)

    print('whole figure')
    print('count of targets in union top10000',
          len(final_df.index))
    # CFD<100 & CRISTA<100
    print('CFD<=100 & CRISTA<=100')
    print(len(final_df[(final_df.CFD_Rank <= 100) & (
        final_df.CRISTA_Rank <= 100)].index))
    # CFD<100 & CRISTA>100
    print('CFD<=100 & CRISTA>100')
    print(len(final_df[(final_df.CFD_Rank <= 100) & (
        final_df.CRISTA_Rank > 100)].index))
    # CFD>100 & CRISTA<100
    print('CFD>100 & CRISTA<=100')
    print(len(final_df[(final_df.CFD_Rank > 100) & (
        final_df.CRISTA_Rank <= 100)].index))
    # CFD>100 & CRISTA>100
    print('CFD>100 & CRISTA>100')
    print(len(final_df[(final_df.CFD_Rank > 100) & (
        final_df.CRISTA_Rank > 100)].index))

    plot = sns.JointGrid(data=final_df, x='CFD_Rank',
                         y='CRISTA_Rank', marginal_ticks=True)
    plot.plot_joint(sns.scatterplot, alpha=0.5)
    plot.plot_marginals(sns.histplot)

    plot.ax_joint.axvline(x=100)
    plot.ax_joint.axhline(y=100)
    plot.ax_joint.set_xscale('log')
    plot.ax_joint.set_yscale('log')
    plot.ax_joint.invert_yaxis()
    plot.ax_joint.invert_xaxis()
    plot.set_axis_labels('CFD Rank', 'CRISTA Rank')

    plt.tight_layout()
    plt.savefig(sys.argv[2]+f'scatter_rank_CFDvCRISTA_top10000_union.pdf')
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
