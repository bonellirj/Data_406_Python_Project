# %%
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt

print('Starting...')

useCols = ['Device time', 'Session ID', 'City']
files = ['../../../data_files/sessions_01.csv',
         '../../../data_files/sessions_02.csv',
         '../../../data_files/sessions_03.csv',
         '../../../data_files/sessions_04.csv',
         '../../../data_files/sessions_05.csv',
         '../../../data_files/sessions_06.csv',
         '../../../data_files/sessions_07.csv',
         '../../../data_files/sessions_08.csv',
         '../../../data_files/sessions_09.csv',
         '../../../data_files/sessions_10.csv',
         '../../../data_files/sessions_11.csv',
         '../../../data_files/sessions_12.csv']

print('uploading files.')


dfs = [pd.read_csv(file, usecols=useCols) for file in files]

print('files uploaded.')

df = pd.concat(dfs, ignore_index=True)

print('unified files.')

# df = df[['Device time', 'Session ID', 'City']]

df['City'] = df['City'].astype('category')

# df = df[df['City'] == 'Manaus']

df['Device time'] = pd.to_datetime(df['Device time'], errors='coerce')
df = df.dropna(subset=['Device time'])

print('files uploaded.')

df = df[(df['Device time'].dt.year == 2024) & (df['Device time'] >= '2024-04-03')]

df['day'] = df['Device time'].dt.to_period('D')
daily_sessions = df.groupby('day').size().reset_index(name='sessions')

daily_sessions['day'] = daily_sessions['day'].dt.to_timestamp()

daily_sessions.set_index('day', inplace=True)

print('MIN and MAX:', daily_sessions.index.min(), daily_sessions.index.max())

print("day,totalSessions")
for date, sessions in daily_sessions.iterrows():
    print(f"{date.date()},{sessions['sessions']}")


# train_size = int(len(daily_sessions) * 0.8)
# train, test = daily_sessions[:train_size], daily_sessions[train_size:]

# model = SARIMAX(train['sessions'], order=(1, 1, 1), seasonal_order=(1, 1, 1, 7))
# model_fit = model.fit(disp=False)

# forecast_steps = len(test)  
# forecast = model_fit.forecast(steps=forecast_steps)

# plt.figure(figsize=(10, 6))
# plt.plot(daily_sessions.index, daily_sessions['sessions'], label='Histórico')
# plt.plot(forecast.index, forecast, label='Previsão', linestyle='--')
# plt.axvline(train.index[-1], color='red', linestyle='--', label='Início da Previsão')
# plt.xlabel('Data')
# plt.ylabel('Número de Sessões')
# plt.title('Previsão de Sessões por Dia (Rio de Janeiro - 2024)')
# plt.legend()
# # plt.show()

# future_steps = 30
# future_forecast = model_fit.forecast(steps=future_steps)
# # print(future_forecast)

# # %% Load data

# %%
