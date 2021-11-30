#!/usr/bin/env python

import sys
import time
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
# from upsetplot import generate_counts
from upsetplot import UpSet
# import matplotlib as mpl
from upsetplot import from_memberships
import warnings
import matplotlib
import math
# import matplotlib.ticker as tkr

# SUPPRESS ALL WARNINGS
warnings.filterwarnings("ignore")
# do not use X11
matplotlib.use('Agg')


def annotation_analysis(row, on_target_dict):
    categories_list = list()

    if 'nan' not in str(row['PAM_creation_(highest_CFD)']):
        categories_list.append('PAM creation')
    if 'CDS' in str(row['Annotation_GENCODE']):
        categories_list.append('CDS')
        if 'nan' not in str(row['Gene_description']):
            categories_list.append('TSG')
    if 'nan' not in str(row['Annotation_ENCODE']):
        categories_list.append('cCRE')
    if str(row['Chromosome']) == on_target_dict[str(row['Spacer+PAM'])]:
        categories_list.append('Same chr')
    if len(categories_list):
        return (','.join(categories_list))
    else:
        return 'empty'


def num_of_decimal_zeros(float_number):
    if float_number == 0:
        return math.pow(10, -5)  # 0.00001
    decimals = str(float_number).split('.')[1]
    count_zeros = 0
    for decimal in decimals:
        if decimal == '0':
            count_zeros += 1
        else:
            break
    # add 1 to respect the exp representation (10^-1 will have count_zeros=0, but should be 1)
    return math.pow(10, -(count_zeros+1))


def generate_distribution_plot_MMBUL(original_df):
    filtered_df = original_df.loc[(
        original_df["Mismatches+bulges_(fewest_mm+b)"] <= 4)]
    filtered_df["Variant_MAF_(fewest_mm+b)"] = filtered_df["Variant_MAF_(fewest_mm+b)"].fillna(-1)

    # If multiple AFs (haplotype with multiple SNPs), take min AF
    # Approximation until we have haplotype frequencies
    filtered_df["AF"] = filtered_df["Variant_MAF_(fewest_mm+b)"].astype(
        str).str.split(',')
    filtered_df["AF"] = filtered_df["AF"].apply(lambda x: min(x))
    filtered_df["AF"] = pd.to_numeric(filtered_df["AF"])
    filtered_df.sort_values(
        ['Mismatches+bulges_(fewest_mm+b)'], inplace=True, ascending=True)

    andamento_ALT_MAF005 = list()
    andamento_ALT_MAF05 = list()
    andamento_ALT_MAF0 = list()
    altTarget_MAF005 = 0
    altTarget_MAF05 = 0
    altTarget_MAF0 = 0

    for index, row in filtered_df.iterrows():
        if row['AF'] > 0.005:
            altTarget_MAF005 += 1
        if row['AF'] > 0.05:
            altTarget_MAF05 += 1
        if row['AF'] >= 0:
            altTarget_MAF0 += 1
        andamento_ALT_MAF005.append(altTarget_MAF005)
        andamento_ALT_MAF05.append(altTarget_MAF05)
        andamento_ALT_MAF0.append(altTarget_MAF0)

    plt.plot(andamento_ALT_MAF0, label='MAF>0')
    plt.plot(andamento_ALT_MAF005, label='MAF>0.005')
    plt.plot(andamento_ALT_MAF05, label='MAF>0.05')

    plt.ylabel('ALT Targets')
    plt.xlabel('Targets')
    plt.title(
        'Distribution of targets with different MAFs filtered with MM+BUL <= 4')
    plt.legend()

    plt.tight_layout()
    plt.savefig(out_folder+'distribution_plt_MMBUL.png')
    plt.clf()
    plt.close('all')


def generate_upset_plot_MMBUL(original_df):
    # MMBUL analysis
    df_alt = original_df.loc[(original_df['REF/ALT_origin_(fewest_mm+b)']
                              == 'alt') & (original_df['Mismatches+bulges_(fewest_mm+b)'] <= 4)]

    # create dict
    on_target_dict = dict()
    for guide in df_alt["Spacer+PAM"].unique():
        on_target_dict[str(guide)] = 'empty'

    # extract on-target chr
    try:
        on_target_chr = original_df.loc[(
            original_df['Mismatches+bulges_(fewest_mm+b)'] == 0)]
        on_target_guide = on_target_chr.iloc[0]['Spacer+PAM']
        on_target_chr = on_target_chr.iloc[0]['Chromosome']
        on_target_dict[str(on_target_guide)] = str(on_target_chr)
    except:
        print('on target not found for guide')
    # create empty categories col
    df_alt['Categories'] = 'empty'

    # process df to obtain categories of belonging for each target
    for index in df_alt.index:
        categories_list = list()
        if 'CDS' in str(df_alt.loc[index, 'Annotation_GENCODE']):
            categories_list.append('CDS')
        if 'nan' not in str(df_alt.loc[index, 'Annotation_ENCODE']):
            categories_list.append('ENCODE')
        if 'nan' not in str(df_alt.loc[index, 'Gene_description']) and 'CDS' in str(df_alt.loc[index, 'Annotation_GENCODE']):
            categories_list.append('TSG')
        if str(df_alt.loc[index, 'Chromosome']) == on_target_dict[str(df_alt.loc[index, 'Spacer+PAM'])]:
            categories_list.append('On-Target_Chromosome')
        if len(categories_list):
            df_alt.loc[index, 'Categories'] = ','.join(categories_list)

    # remove targets with empty categories
    df_alt = df_alt.loc[(df_alt['Categories'] != 'empty')]
    # collect categories per target
    categories_per_target = from_memberships(
        df_alt.Categories.str.split(','), data=df_alt)
    # print(categories_per_target)
    # create figure
    figu = plt.figure()
    upset_plot = UpSet(categories_per_target, show_counts=True,
                       sort_by='cardinality', sort_categories_by=None)
    upset_plot.plot(fig=figu)
    plt.title('ALT targets overlapping categories filtered with MM+BUL <= 4')
    # plt.tight_layout()
    plt.savefig(out_folder+'overlapping_alt_targets_categories_MMBUL.png')
    plt.clf()
    plt.close('all')


def generate_heatmap_CFD(original_df):
    df_heatmap = original_df[[
        'CFD_score_(highest_CFD)', 'Variant_MAF_(highest_CFD)']]
    # df_heatmap = df_heatmap.loc[(df_heatmap["CFD_score_(highest_CFD)"] >= 0.1)]

    # MAF conversion and filtering
    df_heatmap["Variant_MAF_(highest_CFD)"] = df_heatmap["Variant_MAF_(highest_CFD)"].fillna(-1)
    df_heatmap["Variant_MAF_(highest_CFD)"] = df_heatmap["Variant_MAF_(highest_CFD)"].astype(
        str).str.split(',')
    df_heatmap["Variant_MAF_(highest_CFD)"] = df_heatmap["Variant_MAF_(highest_CFD)"].apply(
        lambda x: min(x))
    df_heatmap["Variant_MAF_(highest_CFD)"] = pd.to_numeric(
        df_heatmap["Variant_MAF_(highest_CFD)"], downcast="float")
    df_heatmap = df_heatmap.loc[(df_heatmap['Variant_MAF_(highest_CFD)']) >= 0]
    # conversion to count of decimal zeros
    df_heatmap["Variant_MAF_(highest_CFD)"] = df_heatmap["Variant_MAF_(highest_CFD)"].apply(
        lambda x: num_of_decimal_zeros(x))

    # CFD score rounding to 1 decimal
    df_heatmap['CFD_score_(highest_CFD)'] = df_heatmap['CFD_score_(highest_CFD)'].astype(
        float)
    df_heatmap['CFD_score_(highest_CFD)'] = df_heatmap['CFD_score_(highest_CFD)'].apply(
        lambda x: round(x, 1))

    # print(df_heatmap)

    df_table = df_heatmap.groupby(
        ["Variant_MAF_(highest_CFD)", "CFD_score_(highest_CFD)"]).size().reset_index(name="Value")
    table = df_table.pivot('CFD_score_(highest_CFD)',
                           'Variant_MAF_(highest_CFD)', 'Value')

    # print(table)

    cbar_ticks = [10**0, 10**1, 10**2, 10**3, 10**4, 10**5, 10**6, 10**7]
    vmax = 10**7
    vmin = 10**0
    # formatter = tkr.ScalarFormatter(useMathText=True)
    log_norm = LogNorm(vmin=vmin, vmax=vmax)
    # formatter.set_scientific(True)

    figu = plt.figure()
    plt_heatmap = sns.heatmap(table, annot=True, vmax=vmax, vmin=vmin, norm=log_norm,
                              cbar_kws={"ticks": cbar_ticks})
    plt_heatmap.collections[0].colorbar.ax.yaxis.set_ticks([], minor=True)
    # print(plt_heatmap.get_xticks())
    plt_heatmap.set_xticks([x - 0.5 for x in plt_heatmap.get_xticks()])
    plt_heatmap.set_yticks([x - 0.5 for x in plt_heatmap.get_yticks()])
    plt_heatmap.set_yticklabels(
        labels=plt_heatmap.get_yticklabels(), fontsize=8)
    plt_heatmap.set_xticklabels(
        labels=plt_heatmap.get_xticklabels(), fontsize=8)
    plt_heatmap.invert_yaxis()
    # plt_heatmap.invert_xaxis()
    plt.tight_layout()
    plt.savefig(out_folder+'heatmap_CFD.png')
    plt.clf()
    plt.close('all')


def generate_distribution_plot_CFD(original_df):
    filtered_df = original_df
    # filtered_df = original_df.loc[(
    #     original_df["CFD_score_(highest_CFD)"] >= 0.1)]
    filtered_df["Variant_MAF_(highest_CFD)"] = filtered_df["Variant_MAF_(highest_CFD)"].fillna(-1)

    # If multiple AFs (haplotype with multiple SNPs), take min AF
    # Approximation until we have haplotype frequencies
    filtered_df["AF"] = filtered_df["Variant_MAF_(highest_CFD)"].astype(
        str).str.split(',')
    filtered_df["AF"] = filtered_df["AF"].apply(lambda x: min(x))
    filtered_df["AF"] = pd.to_numeric(filtered_df["AF"], downcast="float")
    # sort over CFD
    # filtered_df.sort_values(['CFD_score_(highest_CFD)'],
    #                         inplace=True, ascending=False)

    plt.figure()
    for guide in filtered_df['Spacer+PAM'].unique():
        print('analyzing guide', guide)
        guide_df = filtered_df.loc[(filtered_df['Spacer+PAM'] == guide)]
        af_list = guide_df['AF'].tolist()
        andamenti = list()

        for permutation in range(10):
            # andamento_ALT_MAF005 = list()
            # andamento_ALT_MAF05 = list()
            andamento_ALT_MAF0 = list()
            # altTarget_MAF005 = 0
            # altTarget_MAF05 = 0
            altTarget_MAF0 = 0
            np.random.shuffle(af_list)

            for af in af_list:
                # if af > 0.005:
                #     altTarget_MAF005 += 1
                # if af > 0.05:
                #     altTarget_MAF05 += 1
                if af >= 0:
                    altTarget_MAF0 += 1
                # andamento_ALT_MAF005.append(altTarget_MAF005)
                # andamento_ALT_MAF05.append(altTarget_MAF05)
                andamento_ALT_MAF0.append(altTarget_MAF0)

            # andamenti con distribuzione andamento di ogni guida
            andamenti.append(andamento_ALT_MAF0)
            print('done permutation number', permutation+1)

        # read values to generate plot
        andamentiArray = np.array(andamenti)
        # print(andamentiArray)
        media = np.mean(andamentiArray, axis=0)
        # mediana = np.median(andamentiArray, axis=0)
        # print('media', media)
        standarddev = np.std(andamentiArray, axis=0)
        standarderr = standarddev/np.sqrt(np.amax(andamentiArray))
        z_score = 1.96  # for confidence 95%
        lowerbound = np.negative(media-(z_score*standarderr))
        upperbound = media+(z_score*standarderr)
        # lowerbound = np.negative(np.amin(andamentiArray, axis=0))
        # upperbound = np.amax(andamentiArray, axis=0)
        # print('mediana', mediana)
        print('media', media)
        print('lower', lowerbound)
        print('upper', upperbound)
        # allMedie.append(media)
        plt.plot(media)
        # plt.plot(mediana, label=str(guide))
        plt.fill_between(range(len(media)), lowerbound,
                         upperbound, alpha=0.10)
        # plt.plot(andamento_ALT_MAF0, label='MAF>0')
        # plt.plot(andamento_ALT_MAF005, label='MAF>0.005')
        # plt.plot(andamento_ALT_MAF05, label='MAF>0.05')

    plt.ylabel('ALT Targets')
    plt.xlabel('Targets')
    plt.title('Distribution of targets with different MAFs filtered with MAF>0')
    plt.legend()

    plt.tight_layout()
    plt.savefig(out_folder+'distribution_plt_CFD.png')
    plt.clf()
    plt.close('all')


def generate_upset_plot_CFD(original_df):
    # CFD analysis
    # df_alt = original_df.loc[(original_df['REF/ALT_origin_(highest_CFD)']== 'alt') & (original_df["CFD_score_(highest_CFD)"] >= 0.1)]
    df_alt = original_df.loc[(
        original_df['REF/ALT_origin_(highest_CFD)'] == 'alt')]

    # create dict
    on_target_dict = dict()
    for guide in df_alt["Spacer+PAM"].unique():
        on_target_dict[str(guide)] = 'empty'

    # extract on-target chr
    try:
        on_target_chr = original_df.loc[(
            original_df['Mismatches+bulges_(highest_CFD)'] == 0)]
        on_target_guide = on_target_chr.iloc[0]['Spacer+PAM']
        on_target_chr = on_target_chr.iloc[0]['Chromosome']
        on_target_dict[str(on_target_guide)] = str(on_target_chr)
    except:
        print('on target not found for guide')

    # compute analysis to compute annotations
    df_alt['Categories'] = df_alt.apply(
        lambda row: annotation_analysis(row, on_target_dict), axis=1)

    # remove targets with empty categories
    df_alt = df_alt.loc[(df_alt['Categories'] != 'empty')]

    # collect categories per target
    categories_per_target = from_memberships(
        df_alt.Categories.str.split(','), data=df_alt)

    # create figure
    figu = plt.figure()
    upset_plot = UpSet(categories_per_target, show_counts=True,
                       sort_by='cardinality', sort_categories_by=None)
    upset_plot.plot(fig=figu)
    plt.title('ALT targets overlapping categories filtered with CFD >= 0.1')
    # plt.tight_layout()
    plt.savefig(out_folder+'overlapping_alt_targets_categories_CFD.png')
    plt.clf()
    plt.close('all')


inTargets = sys.argv[1]  # read targets
out_folder = sys.argv[2]  # folder for output images

print('starting generating distribution and upset plots')
# create dataframe with file
original_df = pd.read_csv(inTargets, sep="\t", index_col=False,
                          na_values=['n'])

# call to plot generation CFD
generate_distribution_plot_CFD(original_df)
# generate_upset_plot_CFD(original_df)
# generate_heatmap_CFD(original_df)
# generate_upset_log_barplot_CFD()
# call to plot generation MM_BUL
# generate_distribution_plot_MMBUL(original_df)
# generate_upset_plot_MMBUL(original_df)
