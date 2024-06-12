import matplotlib.pyplot as plt
import pandas as pd
from io import StringIO

# Provided CSV data as a string
csv_data = """
YYYY-MM-DD HH:MM,players,votes
2024-06-12 06:40,677,7544
2024-06-12 06:45,677,7544
2024-06-12 06:50,677,7544
2024-06-12 06:55,677,7544
2024-06-12 07:00,677,7544
2024-06-12 07:05,696,7546
2024-06-12 07:10,696,7546
2024-06-12 07:15,696,7546
2024-06-12 07:20,696,7546
2024-06-12 07:25,696,7546
2024-06-12 07:30,734,7548
2024-06-12 07:35,734,7548
2024-06-12 07:40,734,7548
2024-06-12 07:45,734,7548
2024-06-12 07:50,768,7549
2024-06-12 07:55,768,7549
2024-06-12 08:00,768,7549
2024-06-12 08:05,768,7549
2024-06-12 08:10,768,7549
2024-06-12 08:15,831,7549
2024-06-12 08:20,831,7549
2024-06-12 08:25,831,7549
2024-06-12 08:30,831,7549
2024-06-12 08:35,831,7549
2024-06-12 08:40,846,7551
2024-06-12 08:45,846,7551
2024-06-12 08:50,846,7551
2024-06-12 08:55,846,7551
2024-06-12 09:00,892,7552
2024-06-12 09:05,892,7552
2024-06-12 09:10,892,7552
2024-06-12 09:15,892,7552
2024-06-12 09:20,892,7552
2024-06-12 09:25,939,7552
2024-06-12 09:30,939,7552
2024-06-12 09:35,939,7552
2024-06-12 09:40,939,7552
2024-06-12 09:45,962,7552
2024-06-12 09:50,962,7552
2024-06-12 09:55,962,7552
2024-06-12 10:00,962,7552
2024-06-12 10:05,962,7552
2024-06-12 10:10,978,7552
2024-06-12 10:15,978,7552
2024-06-12 10:20,978,7552
"""

# Read the data into a DataFrame
data = pd.read_csv(StringIO(csv_data), parse_dates=["YYYY-MM-DD HH:MM"])

# Create a figure and a set of subplots
fig, ax1 = plt.subplots(figsize=(12, 6))

# Plot players over time on the first y-axis
ax1.plot(
    data["YYYY-MM-DD HH:MM"], data["players"], label="Players", marker="o", color="b"
)
ax1.set_xlabel("Time")
ax1.set_ylabel("Players", color="b")
ax1.tick_params(axis="y", labelcolor="b")

# Create a second y-axis sharing the same x-axis
ax2 = ax1.twinx()
ax2.plot(data["YYYY-MM-DD HH:MM"], data["votes"], label="Votes", marker="x", color="r")
ax2.set_ylabel("Votes", color="r")
ax2.tick_params(axis="y", labelcolor="r")

# Adding title
plt.title("Players and Votes Over Time")

# Rotating date labels for better readability
# fig.autofmt_xdate()

# Show the plot
plt.tight_layout()
plt.show()
