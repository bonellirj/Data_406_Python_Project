# %% Load libraries
import pandas as pd
import plotly.express as px


# %% Load data
df = pd.read_csv('../../../data_files/users_original.csv')

# %% Check for missing values
df.describe(include='all') 
pd.set_option('display.precision', 0)
df['Sessions'].describe(include='all')  


# %%
df_filtered = df[df['Sessions'] > 499]

fig = px.histogram(df_filtered, x='Sessions', nbins=100, title='Sessions Distribution')
fig.update_layout(
    xaxis_title='Total Sessions',
    yaxis_title='Frequency',
    bargap=0.2,  
    template='plotly_white' 
)
fig.show()

# %%
