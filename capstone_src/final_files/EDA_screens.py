# %% Load necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset (assuming the dataset is named 'screens.csv')
df = pd.read_csv('screens.csv')

# Display the first few rows of the dataframe
df.head()

# %% Step 1: Inspect the dataset
# Display the first few rows of the dataframe
df.head()

# %% Step 2: Check for missing values
missing_values = df.isnull().sum()
print("Missing values in each column:\n", missing_values)

# Visualize missing values
plt.figure(figsize=(10, 8))
sns.heatmap(df.isnull(), cbar=False, cmap='viridis')
plt.title("Missing Values Heatmap")
plt.show()

# %% Step 3: Statistical summary of the dataset
summary_stats = df.describe()
print("Summary statistics:\n", summary_stats)

# %% Step 4: Data type information
data_types = df.dtypes
print("Data types of each column:\n", data_types)

# %% Step 5: Correlation matrix
# Select only the numeric columns
numeric_df = df.select_dtypes(include=[np.number])
correlation_matrix = numeric_df.corr()

# Plot the correlation matrix
plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm', vmin=-1, vmax=1)
plt.title("Correlation Matrix")
plt.show()

# %% Step 6: Visualize the distribution of numerical features
numerical_columns = numeric_df.columns

plt.figure(figsize=(14, 12))
for i, column in enumerate(numerical_columns):
    plt.subplot(len(numerical_columns) // 2 + 1, 2, i + 1)
    sns.histplot(df[column], bins=50, kde=True, color='blue')
    plt.title(f'{column} Distribution')
plt.tight_layout()
plt.show()

# %% Step 7: Box plots to detect outliers
plt.figure(figsize=(14, 12))
for i, column in enumerate(numerical_columns):
    plt.subplot(len(numerical_columns) // 2 + 1, 2, i + 1)
    sns.boxplot(x=df[column], color='green')
    plt.title(f'{column} Boxplot')
    plt.tight_layout()
