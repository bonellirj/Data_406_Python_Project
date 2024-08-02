# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.deterministic import DeterministicProcess
from statsmodels.api import OLS
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error
import seaborn as sns

# Function to replace values ​​below the threshold with the mean
def replace_below_threshold_with_mean(df, threshold=1000):
    mean_value = df['total_sessions'].mean()
    df['total_sessions'] = df['total_sessions'].apply(lambda x: mean_value if x < threshold else x)
    return df

def plot_forecast(df, city_name):
    df['session_week'] = pd.to_datetime(df['session_week'])
    df.set_index('session_week', inplace=True)
    
    all_weeks = pd.date_range(start=df.index.min(), end=df.index.max(), freq='W-MON')
    df = df.reindex(all_weeks, fill_value=df['total_sessions'].mean())
    
    # Descriptive Statistics
    print(f"Descriptive Statistics for {city_name}:")
    print(df.describe())

    train = df.iloc[:-4]
    test = df.iloc[-4:]

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
    forecast = forecast_linear_trend_seasonality(train, steps)

    difference = test['total_sessions'] - forecast

    results_df = pd.DataFrame({
        'Date': test.index,
        'Forecast': forecast,
        'Actual': test['total_sessions'],
        'Difference': difference
    }).round(2)

    
    print(f"Forecast Model Evaluation for {city_name}:")
    print(results_df)
    print("- " * 20)
    results_df = evaluate_forecasts(test['total_sessions'], forecast)
    print(results_df)

    plt.figure(figsize=(12, 6))
    plt.plot(train.index, train['total_sessions'], label='Training', color='blue')
    plt.plot(test.index, test['total_sessions'], label='Test', color='green')
    plt.plot(test.index, forecast, label='Forecast', linestyle='--', color='orange')
    plt.plot(
        [train.index[-1], test.index[0]], 
        [train['total_sessions'].iloc[-1], test['total_sessions'].iloc[0]], 
        color='blue', linestyle='--'
    )
    plt.plot(
        [test.index[-1], test.index[0]], 
        [test['total_sessions'].iloc[-1], forecast.iloc[0]], 
        color='orange', linestyle='--'
    )

    plt.xlabel('Week Number')
    plt.ylabel('Total Sessions')
    plt.title(f'Weekly Session Forecast for {city_name}')
    plt.legend()
    plt.show()

# Dados das cidades
data_boa_vista = {
    'session_week': ['2024-01-29', '2024-02-05', '2024-02-12', '2024-02-19', '2024-02-26', '2024-03-04', '2024-03-11', '2024-03-18', '2024-03-25', '2024-04-01', '2024-04-08', '2024-04-15', '2024-04-22', '2024-04-29', '2024-05-06', '2024-05-13', '2024-05-20'],
    'total_sessions': [18775, 33502, 7292, 8, 10408, 80136, 19614, 5, 1, 49512, 11251, 75464, 47584, 1, 5, 23570, 38077]
}
df_boa_vista = pd.DataFrame(data_boa_vista)
df_boa_vista = replace_below_threshold_with_mean(df_boa_vista)
plot_forecast(df_boa_vista, "Boa Vista")

data_manaus = {
    'session_week': ['2024-01-29', '2024-02-05', '2024-02-12', '2024-02-19', '2024-02-26', '2024-03-04', '2024-03-11', '2024-03-18', '2024-03-25', '2024-04-01', '2024-04-08', '2024-04-15', '2024-04-22', '2024-04-29', '2024-05-06', '2024-05-13', '2024-05-20'],
    'total_sessions': [267596, 457332, 90146, 39, 141799, 1023879, 212527, 40, 56, 614899, 128612, 1080874, 673890, 51, 173, 335745, 591358]
}
df_manaus = pd.DataFrame(data_manaus)
df_manaus = replace_below_threshold_with_mean(df_manaus)
plot_forecast(df_manaus, "Manaus")

data_porto_velho = {
    'session_week': ['2024-01-29', '2024-02-05', '2024-02-12', '2024-02-19', '2024-02-26', '2024-03-04', '2024-03-11', '2024-03-18', '2024-03-25', '2024-04-01', '2024-04-08', '2024-04-15', '2024-04-22', '2024-04-29', '2024-05-06', '2024-05-13', '2024-05-20'],
    'total_sessions': [11634, 20985, 4493, 5, 5553, 45649, 10220, 3, 3, 28959, 5822, 40163, 24868, 3, 12, 8936, 17036]
}
df_porto_velho = pd.DataFrame(data_porto_velho)
df_porto_velho = replace_below_threshold_with_mean(df_porto_velho)
plot_forecast(df_porto_velho, "Porto Velho")
