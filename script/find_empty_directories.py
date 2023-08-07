import os
import pandas as pd
import unicodedata

# The base directory
base_dir = "/Users/treenulbo/Downloads/NUGU_엣더룸_상품목록"

# Initialize an empty list to hold the names of empty directories
empty_dirs = []

# Walk through the base directory
for dirpath, dirnames, filenames in os.walk(base_dir, topdown=False):
    if not dirnames and not filenames:  # This means the directory is empty
        empty_dirs.append(dirpath)
        os.rmdir(dirpath)  # remove empty directories

# Print the names of all removed directories
for dir in empty_dirs:
    print(f"Removed empty directory: {dir}")

# Initialize a DataFrame to hold the directory names and filenames
df = pd.DataFrame(columns=["Directory", "Filename"])

# Now, walk through the directory again and add all filenames to the DataFrame
for dirpath, dirnames, filenames in os.walk(base_dir):
    for filename in filenames:
        dir_name = os.path.basename(dirpath)
        dir_name = unicodedata.normalize("NFC", dir_name)
        df.loc[len(df)] = [dir_name, filename]  # Add a new row to the DataFrame

# Save the DataFrame to a CSV file
df.to_csv("filenames.csv", index=False, encoding="utf-8-sig")
