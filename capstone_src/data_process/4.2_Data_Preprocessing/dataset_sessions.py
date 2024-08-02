# %%

import pandas as pd
import os

# %%

files = [
    '../../../data_files/output_directory/sessions_01.csv', '../../../data_files/output_directory/sessions_02.csv',
    '../../../data_files/output_directory/sessions_03.csv', '../../../data_files/output_directory/sessions_04.csv',
    '../../../data_files/output_directory/sessions_05.csv', '../../../data_files/output_directory/sessions_06.csv',
    '../../../data_files/output_directory/sessions_07.csv', '../../../data_files/output_directory/sessions_08.csv',
    '../../../data_files/output_directory/sessions_09.csv', '../../../data_files/output_directory/sessions_10.csv',
    '../../../data_files/output_directory/sessions_11.csv', '../../../data_files/output_directory/sessions_12.csv'
]

output_parquet = '../../../data_files/output_directory/unified_sessions.parquet'

df_list = []

for file in files:
    df = pd.read_csv(file, delimiter=';')
    df_list.append(df)

unified_df = pd.concat(df_list, ignore_index=True)

unified_df.to_parquet(output_parquet, index=False)

print("Todos os arquivos CSV foram unificados em um único arquivo Parquet.")

# %%

parquet_file = '../../../data_files/output_directory/unified_sessions.parquet'
df = pd.read_parquet(parquet_file)
pd.set_option('display.precision', 0)
df.describe(include='all')

# %%
df.head()
