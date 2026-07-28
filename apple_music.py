import matplotlib.pyplot as plt
import pandas as pd

from get_data import apple_fp

file_path = apple_fp()

df = pd.read_csv(file_path, low_memory=False, escapechar="\\")


# todo just edit the csv?
# make a copy first :eyes:
name_counts = df["Song Name"].value_counts()
plt.figure(figsize=(10, 6))
name_counts.plot(kind="bar")
plt.title("Count of Names")
plt.xlabel("Song Name")
plt.ylabel("Count")
plt.show()
