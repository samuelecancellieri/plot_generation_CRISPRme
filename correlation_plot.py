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
    # lists containing the x and y coordinates to build the rank plot for whole file
    x_coordinates_list = list()
    y_coordinates_list = list()

    for guide in original_df["Spacer+PAM"].unique():

        # filter the df to obtain single guide targets
        df_guide = original_df.loc[(original_df['Spacer+PAM'] == guide)]
        # reset index to use as x position for rank
        df_guide.reset_index(inplace=True)

        print('plotting for guide:', guide)
        # sorting the df in CFD and CRISTA order saving in different dfs
        original_df_cfd_sort = df_guide.sort_values(
            ['CFD_score_(highest_CFD)'], ascending=False)
        original_df_crista_sort = df_guide.sort_values(
            ['CRISTA_score_(highest_CRISTA)'], ascending=False)

        original_df_cfd_sort.head(1000).to_csv(sys.argv[2]+guide+'_top1000_CFD.tsv',
                                               sep='\t', na_rep='NA', index=False)
        original_df_crista_sort.head(1000).to_csv(sys.argv[2]+guide+'_top1000_CRISTA.tsv',
                                                  sep='\t', na_rep='NA', index=False)

        # created the df of union, dropping the duplicate targets that appears in both
        top1000_union_CFDvCRISTA = pd.concat([original_df_cfd_sort.head(
            1000), original_df_crista_sort.head(1000)]).drop_duplicates()

        top1000_union_CFDvCRISTA.to_csv(sys.argv[2]+guide+'top1000_union.tsv',
                                        sep='\t', na_rep='NA', index=False)

        # create the list for the current analysis
        cfd_crista_point_x_coordinates = list()
        cfd_crista_point_y_coordinates = list()
        real_y_coordinates = list()
        # sort values in the union by CFD, then extract the index list ordered to use as x coordinates
        top1000_union_CFDvCRISTA.sort_values(
            ['CFD_score_(highest_CFD)'], ascending=False, inplace=True)
        sorted_cfd_index_list = list(top1000_union_CFDvCRISTA['index'])
        # sort values in the union by CRISTA, then extract the index list ordered to use as y coordinates
        top1000_union_CFDvCRISTA.sort_values(
            ['CRISTA_score_(highest_CRISTA)'], ascending=False, inplace=True)
        sorted_crista_index_list = list(top1000_union_CFDvCRISTA['index'])

        # for each target in top1000 list of CFD ordered, find the position of the target if ordered by CRISTA (y coordinate), if not found return 1000 as y
        # for pos, index in enumerate(sorted_cfd_index_list[:1000]):
        for pos, index in enumerate(sorted_cfd_index_list):
            try:
                y_coordinate = sorted_crista_index_list.index(index)
            except:
                continue
            if y_coordinate < 1000:
                cfd_crista_point_y_coordinates.append(y_coordinate+1)
                cfd_crista_point_x_coordinates.append(pos+1)
            else:
                cfd_crista_point_y_coordinates.append(1000)
                cfd_crista_point_x_coordinates.append(pos+1)

        union_file = open(sys.argv[2]+'union_file.tsv', 'w')
        union_file.write(
            'Spacer+PAM\tCFD_Score\tCRISTA_Score\tCFD_Rank\tCRISTA_Rank\n')
        for index, elem in enumerate(sorted_cfd_index_list):
            try:
                crista_index = str(top1000_union_CFDvCRISTA.iloc[sorted_crista_index_list.index(elem)
                                                                 ]['CRISTA_score_(highest_CRISTA)'])
            except:
                crista_index = 'out_of_list'
            save = str(guide)+'\t' + str(top1000_union_CFDvCRISTA.iloc[elem+1]['CFD_score_(highest_CFD)'])+'\t'+crista_index+'\t'+str(
                elem)+'\t'+crista_index+'\n'
            union_file.write(save)

        # extend the list for plotting the whole distribution
        x_coordinates_list.extend(cfd_crista_point_x_coordinates)
        y_coordinates_list.extend(cfd_crista_point_y_coordinates)

    # jointplot for x and y coordinates for ranking cfd and crista score
    plot = sns.jointplot(x=x_coordinates_list, y=y_coordinates_list, marginal_ticks=True, space=0.5,
                         kind="reg", xlim=(1000, 0), ylim=(1000, 0), joint_kws={'line_kws': {'color': 'orange'}})

    plot.ax_joint.axvline(x=100)
    plot.ax_joint.axhline(y=100)
    plot.set_axis_labels('CFD Rank', 'CRISTA Rank')

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
