# %%
import pandas as pd
import re


# %%
file_path = '../../../data_files/Screens.csv'
df = pd.read_csv(file_path)
df.head()

df_result = df[['Screen name', 'Visit count', 'Avg. visit duration']]
df_result.head()

df_result.describe(include='all')

df_result.info()    

# %%

classification_rules = {
    'SplashScreen': 'Home',
    '/product/': 'Products Info',
    '/start/catalog/': 'Categories',
    '/category/': 'Categories',
    '/list/': 'Product List',
    '/start/super_offers/Super%20Ofertas/454': 'Super Offers',
    '/search/': 'Search',
    '/start/cart/': 'Cart',
    '/cart/checkout/': 'Checkout',
    '/start/profile/signin/checkout': 'Checkout',
    '/start/signin/': 'Sign in',
    '/start/menu/': 'Profile',
    '/start/profile/my_orders/': 'My orders',
    '/start/profile/my_order_details': 'My orders',
    '/start/profile/my_payments/': 'My payments',
    '/start/profile/loan/': 'Loans',
    '/start/profile/favorites/': 'Favorited Products',
    '/start/profile/my_medals/': 'Badges',
    '/start/profile/minha_conta/': 'My account',
    '/start/profile/store_credit/': 'Credit balance',
    '/start/profile/bonus/bonus_history/': 'Bonus points'
}

def classify_screen_name(screen_name):
    for key, value in classification_rules.items():
        if screen_name.startswith(key):
            return value
    return 'Unknown'

df['Feature'] = df['Screen name'].apply(classify_screen_name)

def convert_to_seconds(duration):
    if 'min' in duration:
        minutes, seconds = map(int, re.findall(r'\d+', duration))
        return minutes * 60 + seconds
    else:
        return int(re.findall(r'\d+', duration)[0])

df['avg_visit_duration_seconds'] = df['Avg. visit duration'].apply(convert_to_seconds)

df['duration_total_seconds'] = df['avg_visit_duration_seconds'] * df['Visit count']

df_result = df[['Screen name', 'Feature', 'Visit count', 'Avg. visit duration', 'avg_visit_duration_seconds', 'duration_total_seconds']]

output_path = '../../../data_files/Screen_Feature.csv'
df_result.to_csv(output_path, index=False)

print(df_result)

# %%
df_result.info()

# %%

file_path = '../../../data_files/Screen_Feature.csv'
df = pd.read_csv(file_path)

df_aggregated = df.groupby('Feature').agg({
    'Visit count': 'sum',
    'duration_total_seconds': 'sum'
}).reset_index()

df_aggregated.rename(columns={
    'Feature': 'Feature',
    'Visit count': 'Feature Visit Count',
    'duration_total_seconds': 'Feature Duration Total Seconds'
}, inplace=True)

df_aggregated['Feature Avg Visit Duration'] = df_aggregated['Feature Duration Total Seconds'] / df_aggregated['Feature Visit Count']
df_aggregated['Feature Avg Visit Duration'] = df_aggregated['Feature Avg Visit Duration'].round(0).astype(int)

def convert_seconds_to_mmss(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02}:{seconds:02}"

df_aggregated['Feature Avg Visit Duration Formatted'] = df_aggregated['Feature Avg Visit Duration'].apply(convert_seconds_to_mmss)

print(df_aggregated)

output_path = '../../../data_files/Feature_Aggregates.csv'
df_aggregated.to_csv(output_path, index=False)


# %%
import pandas as pd
file_path = '../../../data_files/Screens.csv'
df = pd.read_csv(file_path)
df.head()