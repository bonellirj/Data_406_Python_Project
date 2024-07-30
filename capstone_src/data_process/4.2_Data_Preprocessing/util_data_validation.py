# %% Load libraries
import pandas as pd


# %%

df_user_original = pd.read_csv('../../../data_files/users_original.csv')
df_user_fact = pd.read_csv('../../../data_files/dataset_1_users/fact_users.csv')    
df_dim_user = pd.read_csv('../../../data_files/dataset_1_users/dim_Username.csv', dtype={1: str})

merged_df = pd.merge(df_user_fact, df_dim_user, left_on='UsernameId', right_on='Id', how='left')
merged_df.rename(columns={'Username': 'Username_fact'}, inplace=True)
merged_df = pd.merge(merged_df, df_user_original[['Username']], left_index=True, right_index=True, how='left', suffixes=('_fact', '_original'))
merged_df.rename(columns={'Username': 'Username_original'}, inplace=True)

inconsistencies = merged_df[merged_df['Username_fact'] != merged_df['Username_original']] 
total_inconsistencies = len(inconsistencies)
total_validations = len(merged_df)

print(f"Data validation for Username completed.")
print(f"Total validations: {total_validations}")
print(f"Total incorrect references: {total_inconsistencies}")

# # %%

# %%
