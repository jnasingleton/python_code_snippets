#This script extracts a sample from a full csv file

import pandas as pd

#csv_file is the source file to load
#csv_samplefile is the sample to extract (ie. filtered from the source file)
csv_file = "tbl_output.csv"
csv_samplefile = "year-over-year_sample.csv"

df = pd.read_csv(csv_file)

# Filter on year_pre
year_pre_desired = 2005
df = df[df['year_pre']==year_pre_desired]

# Filter on level2
#level2_desired = None
df = df[df['level2'].isnull()]

df.to_csv(csv_samplefile, encoding = 'utf-8', index = False)