This repo contains the scripts used for generating the plots of the manuscript describing CRISPRme: "Human genetic diversity alters off-target outcomes of therapeutic gene editing"

A brief description of each script with expected input and output is provided below.

- ALT_analysis_plots.py, used to create the upset plot and heatmap in Fig5. The script takes as input a .tsv file created by CRISPRme (integrated_results.tsv) and a destination ouput folder.
-- Example call: python ALT_analysis_plots.py some_search.integrated_results.tsv outfolder/

- CRISPRme_plots.py, used to create all the reference/alternative dot plots (Fig1c,Fig2a,Fig5c,SuppFig4,etc). The script takes as input a .tsv file created by CRISPRme (integrated_results.tsv).
-- Example call: python CRISPRme_plots.py some_search.integrated_results.tsv

- correlation_plot.py, used to create the correlation plot in SuppFig2. The script takes as input a .tsv file created by CRISPRme (integrated_results.tsv) and a destination ouput folder.
-- Example call: python correlation_plot.py some_search.integrated_results.tsv outfolder/

- distribution_HGDP_sg1617.py, used to create the population plots in Fig2b and SuppFig3. The script takes as input a .tsv file created by CRISPRme (integrated_results.tsv), tabulated sample metadata file (sampleID population superpopulation) and a destination ouput folder.
-- Example call: python distribution_HGDP_sg1617.py some_search.integrated_results.tsv sample_data.txt outfolder/
