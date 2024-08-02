# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

# %%
# Load the dataset
original_file = '../../../data_files/users_original.csv'
df_original = pd.read_csv(original_file)

print(df_original.head())

print(df_original.describe())

df_original.hist(bins=30, figsize=(15, 10))
plt.suptitle('Histogram of Numeric Columns')
plt.show()

corr = df_original.corr()
plt.figure(figsize=(12, 8))
sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title('Correlation Matrix')
plt.show()


categorical_columns = ['CityId', 'DeviceId', 'PlatformId', 'Device classId', 'OS versionId', 'App versionId']

plt.figure(figsize=(15, 10))
for i, column in enumerate(categorical_columns, 1):
    plt.subplot(3, 2, i)
    sns.countplot(data=df_original, x=column)
    plt.title(f'Count Plot of {column}')
    plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# Scatter plot for Sessions vs. Time in app Seconds with Plotly
fig = px.scatter(df_original, x='Sessions', y='Time in app Seconds', color='PlatformId',
                 hover_data=['UsernameId', 'CityId', 'DeviceId', 'Device classId', 'OS versionId', 'App versionId'])
fig.update_layout(title='Sessions vs. Time in app Seconds',
                  xaxis_title='Sessions',
                  yaxis_title='Time in app Seconds')
fig.show()


# Boxplot for numeric columns
plt.figure(figsize=(15, 10))
sns.boxplot(data=df_original[['Sessions', 'Time in app Seconds', 'Screens', 'Events', 'Gestures']])
plt.title('Boxplot of Numeric Columns')
plt.xticks(rotation=45)
plt.show()


# Mean and sum of Sessions by CityId
mean_sessions_by_city = df_original.groupby('CityId')['Sessions'].mean().reset_index()
sum_sessions_by_city = df_original.groupby('CityId')['Sessions'].sum().reset_index()

fig = go.Figure()
fig.add_trace(go.Bar(x=mean_sessions_by_city['CityId'], y=mean_sessions_by_city['Sessions'],
                     name='Mean Sessions'))
fig.add_trace(go.Bar(x=sum_sessions_by_city['CityId'], y=sum_sessions_by_city['Sessions'],
                     name='Sum Sessions'))

fig.update_layout(barmode='group', title='Mean and Sum of Sessions by CityId',
                  xaxis_title='CityId', yaxis_title='Sessions')
fig.show()

