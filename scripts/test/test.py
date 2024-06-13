import pandas as pd
import numpy as np

# Create a DataFrame with the initial value
file_path = "data\\serverdata.csv"
df = pd.read_csv(file_path)

# Generate random increments between 1 and 3
num_rows = len(
    df["votes"]
)  # Example size, you can adjust this to match your actual data size
increments = np.random.normal(loc=3, scale=2, size=num_rows - 1)
increments = np.clip(np.round(increments), 0, 6).astype(int)

# Calculate the cumulative sum to simulate the vote increments
df["votes"] = [1000] + list(1000 + np.cumsum(increments))

# Save the DataFrame to a CSV file
file_path = "data\\serverdata.csv"
df.to_csv(file_path, index=False)
