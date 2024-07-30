# %%
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt


file = '../../../data_files/crashes_dates.csv'

df = pd.read_csv(file, delimiter=',')

model = ARIMA(df['total_sessions'], order=(5, 1, 0))  # (p, d, q) pode ser ajustado conforme necessário
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

# Definir os dados diretamente no script
# data = {
#     'session_date': ['2024-02', '2024-03', '2024-04', '2024-05'],
#     'total_sessions': [911101, 1548628, 2781157, 1019480]
# }

data = {
    'session_date': [5, 6, 7, 9, 10, 11, 14, 15, 16, 17, 18, 20, 21, 22],
    'total_sessions': [267018, 515887, 128196, 127745, 1135033, 285850, 674635, 120354, 1188408, 797696, 65, 351771, 667564, 144]
}

df = pd.DataFrame(data)

# Ajustar os dados para que a coluna 'session_date' seja interpretada como um índice datetime mensal
df['session_date'] = pd.to_datetime(df['session_date'], format='%Y-%m')
df.set_index('session_date', inplace=True)
df = df.asfreq('MS')  # Definir a frequência como mensal, no início do mês

# Definir o intervalo de valores para p, d, q
p = d = q = range(0, 3)
pdq = list(itertools.product(p, d, q))

best_aic = float('inf')
best_pdq = None

# Encontrar os melhores parâmetros usando AIC
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

# Ajustar o modelo ARIMA com os melhores parâmetros
model = ARIMA(df['total_sessions'], order=best_pdq)
model_fit = model.fit()

# Fazer previsões
forecast_steps = 3  # número de meses para prever
forecast = model_fit.get_forecast(steps=forecast_steps)
forecast_index = pd.date_range(start=df.index[-1] + pd.offsets.MonthBegin(1), periods=forecast_steps, freq='MS')
forecast_series = pd.Series(forecast.predicted_mean.values, index=forecast_index)
conf_int = forecast.conf_int()

# Plotar os resultados
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['total_sessions'], label='Histórico')
plt.plot(forecast_series.index, forecast_series, label='Previsão', linestyle='--')

# Plotar intervalos de confiança
plt.fill_between(forecast_series.index, conf_int.iloc[:, 0], conf_int.iloc[:, 1], color='pink', alpha=0.3)

plt.xlabel('Data')
plt.ylabel('Total de Sessões')
plt.title('Previsão de Sessões por Mês')
plt.legend()
plt.show()

# Exibir previsões e intervalos de confiança
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

# Ensure all weeks are present by reindexing
all_weeks = pd.Index(range(df.index.min(), df.index.max() + 1))
df = df.reindex(all_weeks, fill_value=0)

# Verify the data
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

# Calculate confidence intervals with more gradual widening effect
conf_int = forecast.conf_int()
scaling_factor = np.linspace(0.5, 0.5, forecast_steps)  # More gradual increase from 1 to 1.5
conf_int.iloc[:, 0] *= scaling_factor
conf_int.iloc[:, 1] *= scaling_factor

conf_int_df = pd.DataFrame(conf_int, index=forecast_index)

plt.figure(figsize=(12, 6))
plt.plot(df.index, df['total_sessions'], label='Historical', color='blue')
plt.plot(forecast_series.index, forecast_series, label='Forecast', linestyle='--')
plt.fill_between(forecast_series.index, conf_int_df.iloc[:, 0], conf_int_df.iloc[:, 1], color='pink', alpha=0.3)

# Adding a line to connect the last historical point to the first forecast point with the same style as the historical line
plt.plot(
    [df.index[-1], forecast_series.index[0]], 
    [df['total_sessions'].iloc[-1], forecast_series.iloc[0]], 
    color='blue'
)
# pendencias:
# Adicionar tabela de resultados:
#   - Resultado realizado
#   - Resultado previsto
#   - Acurácia
# Separar por cidade

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

# Função de previsão
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

# Avaliação do modelo
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

# Gerar a previsão

steps = len(test)
# steps = 2
forecast = forecast_linear_trend_seasonality(train, steps)


# Avaliar a previsão
results = evaluate_forecasts(test['total_sessions'], forecast)
print("Forecast Model Evaluation:")
print(results)

# Plotar os resultados
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['total_sessions'], label='Historical')
plt.plot(test.index, forecast, label='Forecast', linestyle='--')

# Adicionar uma linha de conexão entre o último ponto histórico e o primeiro ponto da previsão
# plt.plot(
#     [train.index[-1], test.index[0]], 
#     [train['total_sessions'].iloc[-1], forecast.iloc[0]], 
#     color='blue'
# )

plt.xlabel('Week Number')
plt.ylabel('Total Sessions')
plt.title('Weekly Session Forecast')
plt.legend()
plt.show()

