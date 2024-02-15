import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load your dataset
# Replace 'your_dataset.csv' with the actual file path or URL of your dataset
df = pd.read_csv('....')
# Display the first 5 rows to inspect the data
print("First 5 rows:")
print(df.head())
# Display the last 5 rows to inspect the data
print("\nLast 5 rows:")
print(df.tail())

# 1. Handling missing values
df = df.dropna()
# 2. Removing duplicates
df = df.drop_duplicates()
# Replace spaces with underscores in column names
df.columns = df.columns.str.replace(' ', '_')
# Convert 'List Price' and 'Selling Price' to numeric data type
df['List_Price'] = pd.to_numeric(df['List_Price'], errors='coerce')
df['Selling_Price'] = pd.to_numeric(df['Selling_Price'], errors='coerce')

# Data Exploration (EDA)
# Plot histograms for 'List Price' and 'Selling Price' using seaborn
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
sns.histplot(df['List_Price'].dropna(), bins=20, color='blue', kde=True)
plt.title('Histogram of List Price')

plt.subplot(1, 2, 2)
sns.histplot(df['Selling_Price'].dropna(), bins=20, color='green', kde=True)
plt.title('Histogram of Selling Price')

plt.tight_layout()
plt.show()
