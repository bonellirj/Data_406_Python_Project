# %%
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt


file = '../../../data_files/crashes_dates.csv'

df = pd.read_csv(file, delimiter=',')

model = ARIMA(df['total_sessions'], order=(5, 1, 0))  
model_fit = model.fit()

forecast_steps = 90  
forecast = model_fit.forecast(steps=forecast_steps)

plt.figure(figsize=(12, 6))
plt.plot(df.index, df['total_sessions'], label='Histórico')
plt.plot(forecast.index, forecast, label='Previsão', linestyle='--')
plt.xlabel('Data')
plt.ylabel('Total de Sessões')
plt.title('Previsão de Sessões por Dia')
plt.legend()
plt.show()

print(forecast)



# %%   FORCASTING MONTHLY SESSIONS
import itertools
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt


data = {
    'session_date': [5, 6, 7, 9, 10, 11, 14, 15, 16, 17, 18, 20, 21, 22],
    'total_sessions': [267018, 515887, 128196, 127745, 1135033, 285850, 674635, 120354, 1188408, 797696, 65, 351771, 667564, 144]
}

df = pd.DataFrame(data)

df['session_date'] = pd.to_datetime(df['session_date'], format='%Y-%m')
df.set_index('session_date', inplace=True)
df = df.asfreq('MS')  

p = d = q = range(0, 3)
pdq = list(itertools.product(p, d, q))

best_aic = float('inf')
best_pdq = None

for param in pdq:
    try:
        model = ARIMA(df['total_sessions'], order=param)
        model_fit = model.fit()
        if model_fit.aic < best_aic:
            best_aic = model_fit.aic
            best_pdq = param
    except:
        continue

print(f'Best ARIMA parameters: {best_pdq} with AIC: {best_aic}')

model = ARIMA(df['total_sessions'], order=best_pdq)
model_fit = model.fit()

forecast_steps = 3  
forecast = model_fit.get_forecast(steps=forecast_steps)
forecast_index = pd.date_range(start=df.index[-1] + pd.offsets.MonthBegin(1), periods=forecast_steps, freq='MS')
forecast_series = pd.Series(forecast.predicted_mean.values, index=forecast_index)
conf_int = forecast.conf_int()

plt.figure(figsize=(12, 6))
plt.plot(df.index, df['total_sessions'], label='Histórico')
plt.plot(forecast_series.index, forecast_series, label='Previsão', linestyle='--')

plt.fill_between(forecast_series.index, conf_int.iloc[:, 0], conf_int.iloc[:, 1], color='pink', alpha=0.3)

plt.xlabel('Data')
plt.ylabel('Total de Sessões')
plt.title('Previsão de Sessões por Mês')
plt.legend()
plt.show()

print(forecast_series)
print(conf_int)



# %%   FORCASTING WEEKLY SESSIONS ARIMA
import itertools
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

data = {
    'session_week_number': [5, 6, 7, 9, 10, 11, 14, 15, 16, 17, 18, 20, 21, 22],
    'total_sessions': [267018, 515887, 128196, 127745, 1135033, 285850, 674635, 120354, 1188408, 797696, 65, 351771, 667564, 144]
}

df = pd.DataFrame(data)
df.set_index('session_week_number', inplace=True)

all_weeks = pd.Index(range(df.index.min(), df.index.max() + 1))
df = df.reindex(all_weeks, fill_value=0)

print(df)

p = d = q = range(0, 3)
pdq = list(itertools.product(p, d, q))

best_aic = float('inf')
best_pdq = None

for param in pdq:
    try:
        model = ARIMA(df['total_sessions'], order=param)
        model_fit = model.fit()
        if model_fit.aic < best_aic:
            best_aic = model_fit.aic
            best_pdq = param
    except:
        continue

print(f'Best ARIMA parameters: {best_pdq} with AIC: {best_aic}')

model = ARIMA(df['total_sessions'], order=best_pdq)
model_fit = model.fit()

forecast_steps = 8
forecast = model_fit.get_forecast(steps=forecast_steps)
forecast_index = range(df.index[-1] + 1, df.index[-1] + 1 + forecast_steps)
forecast_series = pd.Series(forecast.predicted_mean.values, index=forecast_index)

conf_int = forecast.conf_int()
scaling_factor = np.linspace(0.5, 0.5, forecast_steps) 
conf_int.iloc[:, 0] *= scaling_factor
conf_int.iloc[:, 1] *= scaling_factor

conf_int_df = pd.DataFrame(conf_int, index=forecast_index)

plt.figure(figsize=(12, 6))
plt.plot(df.index, df['total_sessions'], label='Historical', color='blue')
plt.plot(forecast_series.index, forecast_series, label='Forecast', linestyle='--')
plt.fill_between(forecast_series.index, conf_int_df.iloc[:, 0], conf_int_df.iloc[:, 1], color='pink', alpha=0.3)

plt.plot(
    [df.index[-1], forecast_series.index[0]], 
    [df['total_sessions'].iloc[-1], forecast_series.iloc[0]], 
    color='blue'
)

plt.xlabel('Week Number')
plt.ylabel('Total Sessions')
plt.title('Weekly Session Forecast')
plt.legend()
plt.show()

print(forecast_series)
print(conf_int_df)




# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.deterministic import DeterministicProcess
from statsmodels.api import OLS
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error

# Dados
data = {
    'session_week': ['2024-01-29', '2024-02-05', '2024-02-12', '2024-02-26', '2024-03-04', '2024-03-11', '2024-04-01', '2024-04-08', '2024-04-15', '2024-04-22', '2024-04-29', '2024-05-13', '2024-05-20', '2024-05-27'],
    'total_sessions': [267018, 515887, 128196, 127745, 1135033, 285850, 674635, 120354, 1188408, 797696, 65, 351771, 667564, 144]
}

df = pd.DataFrame(data)

df['session_week'] = pd.to_datetime(df['session_week'])
df.set_index('session_week', inplace=True)

all_weeks = pd.date_range(start=df.index.min(), end=df.index.max(), freq='W-MON')
df = df.reindex(all_weeks, fill_value=df['total_sessions'].mean())

print(df.head())

train = df[:'2024-04-22']
test = df['2024-04-29':]

def forecast_linear_trend_seasonality(train, steps):
    dates = train.index
    dp = DeterministicProcess(index=dates,
                              constant=True,
                              order=1,
                              seasonal=True,
                              drop=True)
    X = dp.in_sample()
    y = train['total_sessions']
   
    model = OLS(y, X).fit()
   
    X_fore = dp.out_of_sample(steps=steps)
    forecast = model.predict(X_fore)
   
    return forecast

def evaluate_forecasts(test, *forecasts):
    metrics = ['MAE', 'RMSE', 'MAPE']
    results = {}
 
    for i, forecast in enumerate(forecasts):
        mae = mean_absolute_error(test, forecast)
        rmse = np.sqrt(mean_squared_error(test, forecast))
        mape = mean_absolute_percentage_error(test, forecast)
        results[f'Model {i+1}'] = [mae, rmse, mape]
 
    results_df = pd.DataFrame(results, index=metrics)
    return results_df


steps = len(test)
# steps = 2
forecast = forecast_linear_trend_seasonality(train, steps)


results = evaluate_forecasts(test['total_sessions'], forecast)
print("Forecast Model Evaluation:")
print(results)

plt.figure(figsize=(12, 6))
plt.plot(df.index, df['total_sessions'], label='Historical')
plt.plot(test.index, forecast, label='Forecast', linestyle='--')

plt.xlabel('Week Number')
plt.ylabel('Total Sessions')
plt.title('Weekly Session Forecast')
plt.legend()
plt.show()

