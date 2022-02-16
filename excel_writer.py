import sys
import pandas as pd

print('start processing')
# df with targets
original_df = pd.read_csv(sys.argv[1], sep="\t", index_col=False,
                          na_values=['n'], usecols=['Spacer+PAM', 'Chromosome',
                                                    'Start_coordinate_(highest_CFD)',
                                                    'Aligned_protospacer+PAM_REF_(highest_CFD)',
                                                    'Aligned_protospacer+PAM_ALT_(highest_CFD)',
                                                    'Mismatches+bulges_(highest_CFD)',
                                                    'CFD_score_(highest_CFD)',
                                                    'CFD_risk_score_(highest_CFD)',
                                                    'Start_coordinate_(fewest_mm+b)',
                                                    'Aligned_protospacer+PAM_REF_(fewest_mm+b)',
                                                    'Aligned_protospacer+PAM_ALT_(fewest_mm+b)',
                                                    'Mismatches+bulges_(fewest_mm+b)',
                                                    'CFD_score_(fewest_mm+b)',
                                                    'CFD_risk_score_(highest_CFD)',
                                                    'Start_coordinate_(highest_CRISTA)',
                                                    'Aligned_protospacer+PAM_REF_(highest_CRISTA)',
                                                    'Aligned_protospacer+PAM_ALT_(highest_CRISTA)',
                                                    'Mismatches+bulges_(highest_CRISTA)',
                                                    'CRISTA_score_(highest_CRISTA)',
                                                    'CRISTA_risk_score_(highest_CRISTA)',
                                                    'Annotation_GENCODE',
                                                    'Annotation_closest_gene_name',
                                                    'Annotation_ENCODE'])
# excel writer
writer = pd.ExcelWriter(sys.argv[2]+'guide_sheets.xlsx')
# user sort criteria
sort_criteria = sys.argv[3]

for guide in original_df['Spacer+PAM'].unique():
    # filter df for guide
    guide_df = original_df.loc[(original_df['Spacer+PAM'] == guide)]

    # # select specific columns
    # guide_df = guide_df[['Spacer+PAM', 'Chromosome',
    #                      'Start_coordinate_(highest_CFD)',
    #                      'Aligned_protospacer+PAM_REF_(highest_CFD)',
    #                      'Aligned_protospacer+PAM_ALT_(highest_CFD)',
    #                      'Mismatches+bulges_(highest_CFD)',
    #                      'CFD_score_(highest_CFD)',
    #                      'CFD_risk_score_(highest_CFD)',
    #                      'Start_coordinate_(fewest_mm+b)',
    #                      'Aligned_protospacer+PAM_REF_(fewest_mm+b)',
    #                      'Aligned_protospacer+PAM_ALT_(fewest_mm+b)',
    #                      'Mismatches+bulges_(fewest_mm+b)',
    #                      'CFD_score_(fewest_mm+b)',
    #                      'CFD_risk_score_(highest_CFD)',
    #                      'Start_coordinate_(highest_CRISTA)',
    #                      'Aligned_protospacer+PAM_REF_(highest_CRISTA)',
    #                      'Aligned_protospacer+PAM_ALT_(highest_CRISTA)',
    #                      'Mismatches+bulges_(highest_CRISTA)',
    #                      'CRISTA_score_(highest_CRISTA)',
    #                      'CRISTA_risk_score_(highest_CRISTA)',
    #                      'Annotation_GENCODE',
    #                      'Annotation_closest_gene_name',
    #                      'Annotation_ENCODE']]

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
    guide_df.to_excel(writer, sheet_name=str(guide), na_rep='NA')

# save the writer to excel file
writer.save()
