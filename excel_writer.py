import sys
import pandas as pd

print('start processing')

if len(sys.argv[:]) < 4:
    print('some input is missing, please provide input')
    print('integrated.tsv out_dir sort_criteria(CFD/CRISTA/fewest)')
    exit(1)

# df with targets
original_df = pd.read_csv(sys.argv[1], sep="\t", index_col=False,
                          na_values=['n'])
# excel writer
writer = pd.ExcelWriter(sys.argv[2]+'guide_sheets.xlsx')
# user sort criteria
sort_criteria = sys.argv[3]

for guide in original_df['Spacer+PAM'].unique():
    # filter df for guide
    guide_df = original_df.loc[(original_df['Spacer+PAM'] == guide)]

    drop_criteria = ''
    # sort df using user criteria
    if 'CFD' in sort_criteria:
        guide_df.sort_values('CFD_score_(highest_CFD)',
                             ascending=False, inplace=True)
        drop_criteria = ('fewest_mm+b', 'highest_CRISTA')
        guide_df['REF_Mismatches+bulges_(highest_CFD)'] = guide_df['Seed_mismatches+bulges_REF_(highest_CFD)'] + \
            guide_df['Non_seed_mismatches+bulges_REF_(highest_CFD)']
    elif 'CRISTA' in sort_criteria:
        guide_df.sort_values('CRISTA_score_(highest_CRISTA)',
                             ascending=False, inplace=True)
        drop_criteria = ('fewest_mm+b', 'highest_CFD')
        guide_df['REF_Mismatches+bulges_(highest_CRISTA)'] = guide_df['Seed_mismatches+bulges_REF_(highest_CRISTA)'] + \
            guide_df['Non_seed_mismatches+bulges_REF_(highest_CRISTA)']
    elif 'fewest' in sort_criteria:
        guide_df.sort_values('Mismatches+bulges_(fewest_mm+b)',
                             ascending=True, inplace=True)
        drop_criteria = ('highest')
        guide_df['REF_Mismatches+bulges_(fewest_mm+b)'] = guide_df['Seed_mismatches+bulges_REF_(fewest_mm+b)'] + \
            guide_df['Non_seed_mismatches+bulges_REF_(fewest_mm+b)']

    # columns_to_drop = list()
    # for column in list(guide_df.columns):
    #     if any(criteria in column for criteria in drop_criteria):
    #         columns_to_drop.append(column)
    # guide_df.drop(columns_to_drop, axis=1, inplace=True)

    # extract top 1000 rows for each guide
    guide_df = guide_df.head(1000)

    # generate excel sheets
    guide_df.to_excel(writer, sheet_name=str(guide), na_rep='NA', index=False)

# save the writer to excel file
writer.save()
writer.close()
