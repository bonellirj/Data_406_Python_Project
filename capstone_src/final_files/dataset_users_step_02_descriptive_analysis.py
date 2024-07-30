# %% 
import pandas as pd


df_user_fact = pd.read_csv('../../../data_files/dataset_1_users/fact_users.csv')  



#  %% Time in app validation
def convert_to_seconds(time_str):
    numbers = re.findall(r'\d+', time_str)
    
    if 'sec' in time_str:
        return int(numbers[0]) 
    if 'min' in time_str:
        minutes = int(numbers[0])
        seconds = int(numbers[1]) if len(numbers) > 1 else 0
        return minutes * 60 + seconds
    elif 'hr' in time_str:
        hours = int(numbers[0])
        minutes = int(numbers[1]) if len(numbers) > 1 else 0
        seconds = int(numbers[2]) if len(numbers) > 2 else 0
        return hours * 3600 + minutes * 60 + seconds
    elif 'day' in time_str:
        days = int(numbers[0])
        return days * 86400
    else:
        return 0
    
df_user_fact['Time in app Seconds'] = df_user_fact['Time in app'].apply(convert_to_seconds)

result = df_user_fact[df_user_fact['Time in app Seconds'] == 0]

print("Numero de registros zerados: ", len(result))
print(result['Time in app'].unique())



# %% Test user validation

df_user_fact = df_user_fact[df_user_fact['UsernameId'] != 0]
df_user_fact.to_csv('../../../data_files/dataset_1_users/fact_users.csv', index=False)



# %%
df_city = pd.read_csv('../../../data_files/dataset_1_users/dim_City.csv')  
df_city_manual = pd.read_csv('../../../data_files/dataset_1_users/dim_City_Manual.csv')  

df_merged = pd.merge(df_city, df_city_manual, on='City', how='outer', indicator=True)

print(df_merged['_merge'].value_counts())
print(df_merged[df_merged['_merge'] != 'both'])
# %%
