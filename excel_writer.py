import sys
import pandas as pd

print('start processing')

if len(sys.argv[:]) < 4:
    print('some input is missing, please provide input')
    print('integrated.tsv out_dir sort_criteria')
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

    # sort df using user criteria
    if 'CFD' in sort_criteria:
        guide_df.sort_values('CFD_score_(highest_CFD)',
                             ascending=False, inplace=True)
    elif 'CRISTA' in sort_criteria:
        guide_df.sort_values('CRISTA_score_(highest_CRISTA)',
                             ascending=False, inplace=True)
    elif 'mmbul' in sort_criteria:
        guide_df.sort_values('Mismatches+bulges_(fewest_mm+b)',
                             ascending=True, inplace=True)

    # extract top 1000 rows for each guide
    guide_df = guide_df.head(1000)

    # generate excel sheets
    guide_df.to_excel(writer, sheet_name=str(guide), na_rep='NA', index=False)

# save the writer to excel file
writer.save()
writer.close()
