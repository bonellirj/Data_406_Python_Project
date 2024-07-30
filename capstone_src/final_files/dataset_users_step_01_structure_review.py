# %% Load libraries
import pandas as pd
import plotly.express as px
import re
import unidecode


# %% Load data
origial_file = '../../../data_files/users_original.csv'

columns_to_use = ['Username', 'City', 'Sessions', 'Time in app', 'Device', 
                  'OS version', 'Platform', 'App version', 'Screens', 'Events', 
                  'Gestures', 'Device class']

df_original = pd.read_csv(origial_file, usecols=columns_to_use)

def clean_app_version(version):
    return re.sub(r'\s*\([^)]*\)', '', str(version))

def clean_unidecode(text):
    return unidecode.unidecode(str(text))

df_original['App version'] = df_original['App version'].apply(clean_app_version)
df_original['City'] = df_original['City'].apply(clean_unidecode)

print( df_original.describe(include='all') )


# %%

def create_df_dim(df_base, column_name, column_id_name):

    if column_name not in df_base.columns:
        raise ValueError("The specified column name doesn't exist in DataFrame.")
    
    df_dim = pd.DataFrame(df_base[column_name].dropna().unique(), columns=[column_name])

    df_dim.sort_values(by=column_name, inplace=True)

    df_dim.reset_index(drop=True, inplace=True)
    df_dim.index += 1
    df_dim.reset_index(inplace=True)
    
    df_dim.columns = [column_id_name, column_name]

    return df_dim


def update_df_fact(df_fact, df_dim, column_name, column_id, column_number, column_id_name):

    df_fact = pd.merge(df_fact, df_dim[[column_name, column_id]], on=column_name, how='left')

    df_fact.drop([column_name], axis=1, inplace=True)

    new_column_name = column_name + column_id_name

    df_fact.rename(columns={column_id: new_column_name}, inplace=True)
    column_temp = df_fact.pop(new_column_name)
    df_fact.insert(column_number, new_column_name, column_temp)

    df_fact[new_column_name] = pd.to_numeric(df_fact[new_column_name], errors='coerce').fillna(0).astype(int)

    return df_fact


def df_fact(df_original, column_name, column_id_name, column_order_number): 

    df_dim = create_df_dim(df_original, column_name, column_id_name)
    
    df_dim.to_csv(f'../../../data_files/dataset_1_users/dim_{column_name.replace(" ","_")}.csv', index=False)

    df_fact_local = update_df_fact(df_original, df_dim, column_name, column_id_name, 
                                  column_order_number, column_id_name)
    
    
    # validate_data(df_fact_local, df_original, df_dim, column_name, column_id_name)
    
    return df_fact_local


def df_fact_city(df_original, column_name, column_id_name, column_order_number): 

    df_dim_city = pd.read_csv('../../../data_files/dataset_1_users/dim_City_Manual.csv')

    df_fact_local = update_df_fact(df_original, df_dim_city, column_name, column_id_name, 
                                  column_order_number, column_id_name)
        
    return df_fact_local






df_user_fact = df_original.copy()

df_user_fact = df_fact(df_user_fact, 'Username', 'Id', 0)
df_user_fact = df_fact_city(df_user_fact, 'City', 'Id', 1)
df_user_fact = df_fact(df_user_fact, 'Device', 'Id', 2)
df_user_fact = df_fact(df_user_fact, 'Platform', 'Id', 3)
df_user_fact = df_fact(df_user_fact, 'Device class', 'Id', 4)
df_user_fact = df_fact(df_user_fact, 'OS version', 'Id', 5)
df_user_fact = df_fact(df_user_fact, 'App version', 'Id', 6)




print(df_user_fact.head())
df_user_fact.to_csv('../../../data_files/dataset_1_users/fact_users.csv', index=False)


# %%
