# %%

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_parquet('../../../data_files/output_directory/unified_sessions.parquet')

# Converter 'Session duration' para segundos
def convert_session_duration(duration):
    try:
        if isinstance(duration, str):
            if 'sec' in duration:
                return int(duration.split()[0])
            elif 'min' in duration:
                minutes, seconds = map(int, duration.split()[0].split(':'))
                return minutes * 60 + seconds
        elif isinstance(duration, (int, float)):
            return int(duration)
    except ValueError:
        return np.nan
    return np.nan

df['Session duration'] = df['Session duration'].apply(convert_session_duration)

# Descriptive Statistics
def descriptive_statistics(df):
    summary = df.describe(include='all')
    return summary

# Display summary statistics
summary_stats = descriptive_statistics(df)
print(summary_stats)

# Save summary statistics to a CSV file for reference
summary_stats.to_csv('../../../data_files/output_directory/summary_statistics.csv', index=True)

# Visualization of some key statistics

# Example: Distribution of Session Duration
plt.figure(figsize=(10, 6))
sns.histplot(df['Session duration'].dropna(), bins=30, kde=True)
plt.title('Distribution of Session Duration')
plt.xlabel('Session Duration (seconds)')
plt.ylabel('Frequency')
plt.savefig('../../../data_files/output_directory/session_duration_distribution.png')
plt.show()

# Example: Boxplot of Session Duration by Platform
plt.figure(figsize=(10, 6))
sns.boxplot(x='Platform', y='Session duration', data=df)
plt.title('Session Duration by Platform')
plt.xlabel('Platform')
plt.ylabel('Session Duration (seconds)')
plt.savefig('../../../data_files/output_directory/session_duration_by_platform.png')
plt.show()

# Example: Countplot of Events
plt.figure(figsize=(10, 6))
sns.countplot(x='Events', data=df, order=df['Events'].value_counts().iloc[:10].index)
plt.title('Top 10 Most Frequent Events')
plt.xlabel('Event')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.savefig('../../../data_files/output_directory/top_10_events.png')
plt.show()

# Example: Summary of missing values
missing_values = df.isnull().sum()
missing_values = missing_values[missing_values > 0]
print(missing_values)

# Save missing values summary to a CSV file
missing_values.to_csv('../../../data_files/output_directory/missing_values_summary.csv', index=True)

print("Data exploration and descriptive statistics analysis completed.")


# %%

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_parquet('../../../data_files/output_directory/unified_sessions.parquet')

# Function to convert session duration to seconds
def convert_session_duration(duration):
    if isinstance(duration, str):
        try:
            if 'sec' in duration:
                return int(float(duration.split()[0]))
            elif 'min' in duration:
                time_parts = duration.split()[0].split(':')
                if len(time_parts) == 2:
                    minutes, seconds = map(int, time_parts)
                else:
                    minutes, seconds = int(time_parts[0]), 0
                return minutes * 60 + seconds
        except ValueError:
            # Handle any conversion errors
            return np.nan
    return duration

# Apply conversion
df['Session duration'] = df['Session duration'].apply(convert_session_duration)

# Remove rows with NaN values in 'Session duration' after conversion
df = df.dropna(subset=['Session duration'])

# Ensure 'Session duration' is numeric
df['Session duration'] = pd.to_numeric(df['Session duration'], errors='coerce')

# Function to remove outliers
def remove_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

# Remove outliers from Session duration
df_filtered = remove_outliers(df, 'Session duration')

# Descriptive Statistics
def descriptive_statistics(df):
    summary = df.describe(include='all')
    return summary

# Display summary statistics
summary_stats = descriptive_statistics(df_filtered)
print(summary_stats)

# Save summary statistics to a CSV file for reference
summary_stats.to_csv('../../../data_files/output_directory/summary_statistics_filtered.csv', index=True)

# Visualization of some key statistics

# Example: Distribution of Session Duration
plt.figure(figsize=(10, 6))
sns.histplot(df_filtered['Session duration'].dropna(), bins=30, kde=True)
plt.title('Distribution of Session Duration')
plt.xlabel('Session Duration (seconds)')
plt.ylabel('Frequency')
plt.savefig('../../../data_files/output_directory/session_duration_distribution_filtered.png')
plt.show()

# Example: Boxplot of Session Duration by Platform
plt.figure(figsize=(10, 6))
sns.boxplot(x='Platform', y='Session duration', data=df_filtered)
plt.title('Session Duration by Platform')
plt.xlabel('Platform')
plt.ylabel('Session Duration (seconds)')
plt.savefig('../../../data_files/output_directory/session_duration_by_platform_filtered.png')
plt.show()

# Example: Countplot of Events
plt.figure(figsize=(10, 6))
sns.countplot(x='Events', data=df_filtered, order=df_filtered['Events'].value_counts().iloc[:10].index)
plt.title('Top 10 Most Frequent Events')
plt.xlabel('Event')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.savefig('../../../data_files/output_directory/top_10_events_filtered.png')
plt.show()

# Distribution of Sessions by City
city_counts = df_filtered['City'].value_counts()
top_5_cities = city_counts.head(5)
other_cities = city_counts.iloc[5:].sum()

# Plot proportion of top 5 cities vs others
plt.figure(figsize=(10, 6))
labels = list(top_5_cities.index) + ['Others']
sizes = list(top_5_cities.values) + [other_cities]
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
plt.title('Proportion of Top 5 Cities vs Others')
plt.savefig('../../../data_files/output_directory/city_proportion_pie.png')
plt.show()

# Plot distribution among the top 5 cities
plt.figure(figsize=(10, 6))
sns.barplot(x=top_5_cities.index, y=top_5_cities.values)
plt.title('Distribution of Sessions Among Top 5 Cities')
plt.xlabel('City')
plt.ylabel('Number of Sessions')
plt.savefig('../../../data_files/output_directory/top_5_cities_bar.png')
plt.show()

# Example: Summary of missing values
missing_values = df_filtered.isnull().sum()
missing_values = missing_values[missing_values > 0]
print(missing_values)

# Save missing values summary to a CSV file
missing_values.to_csv('../../../data_files/output_directory/missing_values_summary_filtered.csv', index=True)

print("Data exploration and descriptive statistics analysis completed.")
