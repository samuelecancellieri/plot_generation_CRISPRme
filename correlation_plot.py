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


print('start processing')
original_df = pd.read_csv(sys.argv[1], sep="\t", index_col=False,
                          na_values=['n'], nrows=1000)

original_df = original_df.head(1000)

plt.figure()
ax = sns.scatterplot(x="CFD_score_(highest_CFD)",
                     y="CRISTA_score_(highest_CRISTA)", data=original_df)
sns.lmplot(x="CFD_score_(highest_CFD)",
           y="CRISTA_score_(highest_CRISTA)", data=original_df)

ax.set_title("Score correlation CFD vs CRISTA")
print(stats.pearsonr(original_df['CFD_score_(highest_CFD)'],
                     original_df['CRISTA_score_(highest_CRISTA)']))

# plt.scatter(original_df['CFD_score_(highest_CFD)'],
#             original_df['CRISTA_score_(highest_CRISTA)'])
plt.tight_layout()
plt.savefig(sys.argv[2]+'correlation_CFDvCRISTA.pdf')
plt.clf()
plt.close('all')
