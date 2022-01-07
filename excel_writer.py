import sys
import pandas as pd

print('start processing')
original_df = pd.read_csv(sys.argv[1], sep="\t", index_col=False,
                          na_values=['n'])

writer = pd.ExcelWriter(sys.argv[2]+'guide_sheets.xlsx')

for guide in original_df['Spacer+PAM'].unique():
    guide_df = original_df.loc[(original_df['Spacer+PAM'] == guide)]

    guide_df = guide_df[guide_df[['Spacer+PAM', 'Chromosome',
                                  'Start_coordinate_(highest_CFD)',
                                  'Aligned_protospacer+PAM_REF_(highest_CFD)',
                                  'Aligned_protospacer+PAM_ALT_(highest_CFD)',
                                  'Mismatches+bulges_(highest_CFD)',
                                  'CFD_score_(highest_CFD)',
                                  'Start_coordinate_(fewest_mm+b)',
                                  'Aligned_protospacer+PAM_REF_(fewest_mm+b)',
                                  'Aligned_protospacer+PAM_ALT_(fewest_mm+b)',
                                  'Mismatches+bulges_(fewest_mm+b)',
                                  'CFD_score_(fewest_mm+b)',
                                  'Start_coordinate_(highest_CRISTA)',
                                  'Aligned_protospacer+PAM_REF_(highest_CRISTA)',
                                  'Aligned_protospacer+PAM_ALT_(highest_CRISTA)',
                                  'Mismatches+bulges_(highest_CRISTA)',
                                  'CRISTA_score_(highest_CRISTA)',
                                  'Annotation_GENCODE'
                                  'Annotation_closest_gene_name',
                                  'Annotation_ENCODE']]]

    # extract top 1000 rows for each guide
    guide_df = guide_df.head(1000)

    # generate excel sheets
    guide_df.to_excel(writer, sheet_name=str(guide))

# save the writer to excel file
writer.save()
