# This script combines all csv files in the current folder
# It assumes all csv files in this folder have the same header/formats

import os
import pandas as pd

combined_csv_file = "combined_csv.csv"

df = None
for root, dirs_list, files_list in os.walk('.'):
	for file_name in files_list:
		extension = os.path.splitext(file_name)[-1]

		if os.path.splitext(file_name)[-1] == '.csv' and file_name != combined_csv_file:
			
			df_temp = pd.read_csv(file_name, index_col=False)

			if df_temp is None:
				df = df_temp
			else:
				df = pd.concat([df,df_temp], axis=0, ignore_index=True)

df.to_csv(combined_csv_file, index=False)