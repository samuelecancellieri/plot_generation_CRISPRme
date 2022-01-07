import sys
import pandas as pd
import matplotlib
from matplotlib import pyplot as plt
# SUPPRESS ALL WARNINGS
warnings.filterwarnings("ignore")
# do not use X11
matplotlib.use('Agg')
# set matplotlib for pdf editing
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42


print('start processing')
original_df = pd.read_csv(sys.argv[1], sep="\t", index_col=False,
                          na_values=['n'])

original_df = original_df.head(1000)

plt.figure()
plt.scatter(original_df['CFD_score_(highest_CFD)'],
            original_df['CRISTA_score_(highest_CRISTA)'])
plt.tight_layout()
plt.savefig(sys.argv[2]+'correlation_CFDvCRISTA.pdf')
plt.clf()
plt.close('all')
