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


def plot_correlation(original_df):
    original_df_filtered = original_df

    plt.figure()

    ax = sns.displot(
        data=original_df_filtered, x="CFD_score_(highest_CFD)", y="CRISTA_score_(highest_CRISTA)", kind="kde", rug=True, color='orange')

    # sns.regplot(data=original_df_filtered, x="CFD_score_(highest_CFD)",
    #             y="CRISTA_score_(highest_CRISTA)", fit_reg=True, marker="+", color="skyblue")

    # ax = sns.scatterplot(x="CFD_score_(highest_CFD)",
    #                      y="CRISTA_score_(highest_CRISTA)", data=original_df_filtered)
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
                          na_values=['n'])
# correlation with top1000 rows
plot_correlation(original_df)
# correlation with top100 rows
# plot_correlation(100, original_df)
