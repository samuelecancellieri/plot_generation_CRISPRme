import sys
import pandas as pd
import matplotlib
import seaborn as sns
from matplotlib import pyplot as plt
import warnings
from scipy import stats
# SUPPRESS ALL WARNINGS
warnings.filterwarnings("ignore")
# do not use X11
matplotlib.use('Agg')
# set matplotlib for pdf editing
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42


def plot_correlation(original_df_filtered):
    print('plotting')
    original_df_cfd_sort = original_df_filtered.sort_values(
        ['CFD_score_(highest_CFD)'], ascending=False)
    original_df_crista_sort = original_df_filtered.sort_values(
        ['CRISTA_score_(highest_CRISTA)'], ascending=False)

    df_union_crista_cfd = pd.concat(
        [original_df_crista_sort.head(100), original_df_cfd_sort.head(100)]).drop_duplicates()

    plt.figure()

    ax = sns.displot(
        data=original_df_filtered, x="CFD_score_(highest_CFD)", y="CRISTA_score_(highest_CRISTA)", kind="kde", color='orange')

    # sns.regplot(data=original_df_filtered.head(100), x="CFD_score_(highest_CFD)",
    #             y="CRISTA_score_(highest_CRISTA)", fit_reg=True, marker="+", color="skyblue")

    sns.scatterplot(x="CFD_score_(highest_CFD)",
                    y="CRISTA_score_(highest_CRISTA)", data=df_union_crista_cfd, marker='+', color="skyblue")
    # sns.lmplot(x="CFD_score_(highest_CFD)",
    #            y="CRISTA_score_(highest_CRISTA)", data=original_df_filtered)
    ax.set(xlabel='CFD Score', ylabel='CRISTA Score')

    ax.set_title("Score correlation CFD vs CRISTA top")

    print(stats.pearsonr(original_df_filtered['CFD_score_(highest_CFD)'],
                         original_df_filtered['CRISTA_score_(highest_CRISTA)']))

    plt.tight_layout()
    plt.savefig(sys.argv[2]+'correlation_CFDvCRISTA_top.pdf')
    plt.clf()
    plt.close('all')


print('start processing')
original_df = pd.read_csv(sys.argv[1], sep="\t", index_col=False,
                          na_values=['n'], nrows=100000)

original_df = original_df.loc[(
    original_df['Mismatches+bulges_(highest_CFD)'] > 1)]
# correlation with top1000 rows
plot_correlation(original_df)
# correlation with top100 rows
# plot_correlation(100, original_df)
