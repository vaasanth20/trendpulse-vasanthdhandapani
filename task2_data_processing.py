# ============================================================
# TrendPulse — Task 2: Clean the Data & Save as CSV
# ============================================================
# What this script does (in simple words):
#   1. Loads the JSON file saved by Task 1 into a Pandas DataFrame
#   2. Cleans the data step by step (duplicates, nulls, bad types, etc.)
#   3. Saves the cleaned data as a CSV file for Task 3 to use
#
# Needs: data/trends_YYYYMMDD.json  (output from Task 1)
# Makes: data/trends_clean.csv
# ============================================================

# --- Import the libraries we need ---

import pandas as pd   # Pandas is used for working with tables of data (DataFrames)
import os             # Used to look for files in folders
import glob           # Used to search for files that match a pattern (like *.json)


# ============================================================
# SECTION 1 — Find and Load the JSON File
# ============================================================

# glob.glob() searches a folder and returns a list of file paths
# that match the given pattern.
# "data/trends_*.json" means: any file inside data/ that starts
# with "trends_" and ends with ".json"
json_files = glob.glob("data/trends_*.json")

# If the list is empty, no matching file was found — stop the script
if len(json_files) == 0:
    print("ERROR: No JSON file found in the data/ folder.")
    print("Please run task1_data_collection.py first.")
    exit()  # Stop the script here

# Sort the list so the most recent file (latest date in name) comes last
# then pick the last one with [-1]
json_files.sort()                  # Sort alphabetically (dates sort correctly this way)
json_file_path = json_files[-1]    # Take the last file = most recent date

print(f"Found file: {json_file_path}")


# ----------------------------------------------------------
# STEP 1: Load the JSON file into a Pandas DataFrame
# ----------------------------------------------------------

# pd.read_json() reads a JSON file and turns it into a DataFrame
# A DataFrame is like an Excel spreadsheet — rows and columns
df = pd.read_json(json_file_path)

# len(df) gives us the number of rows in the DataFrame
print(f"\nLoaded {len(df)} stories from {json_file_path}")

# Show the first 3 rows so we can see what the raw data looks like
print("\nFirst 3 rows of raw data:")
print(df.head(3))   # .head(3) shows the first 3 rows


# ============================================================
# SECTION 2 — Clean the Data (Step by Step)
# ============================================================

print("\n--- Cleaning the data ---\n")


# ----------------------------------------------------------
# Clean Step A: Remove duplicate rows
# ----------------------------------------------------------

# A duplicate row is one where post_id appears more than once.
# We keep only the FIRST occurrence and drop the rest.
# subset=["post_id"] means: only check the post_id column for duplicates
# keep="first" means: keep the first row and remove the others
# inplace=True means: change the DataFrame directly (don't create a new one)
df.drop_duplicates(subset=["post_id"], keep="first", inplace=True)

# Print how many rows we have now
print(f"After removing duplicates: {len(df)}")


# ----------------------------------------------------------
# Clean Step B: Remove rows with missing important values
# ----------------------------------------------------------

# dropna() removes rows that have missing (NaN/None) values
# subset=["post_id", "title", "score"] means: only check these 3 columns
# If ANY of these 3 fields is missing, the whole row is removed
# inplace=True means: apply the change directly to df
df.dropna(subset=["post_id", "title", "score"], inplace=True)

# Print how many rows remain after removing nulls
print(f"After removing nulls: {len(df)}")


# ----------------------------------------------------------
# Clean Step C: Fix data types
# ----------------------------------------------------------

# When loading from JSON, numbers can sometimes be stored as text ("42")
# or floating point (42.0) instead of whole numbers (42).
# We use .astype(int) to make sure score and num_comments are integers.

# Convert the "score" column to integer
# int() turns a value like 42.0 into 42
df["score"] = df["score"].astype(int)

# Convert the "num_comments" column to integer
# We first fill any missing values with 0 (using fillna) before converting
# because astype(int) will crash if there are any NaN values left
df["num_comments"] = df["num_comments"].fillna(0).astype(int)

print("Data types fixed: score and num_comments are now integers.")


# ----------------------------------------------------------
# Clean Step D: Remove low-quality stories (score < 5)
# ----------------------------------------------------------

# We only want stories that got at least 5 upvotes on HackerNews.
# df["score"] >= 5  creates a True/False list for every row.
# We use that list to KEEP only the rows where it is True.
df = df[df["score"] >= 5]

# Print how many rows remain after removing low-score stories
print(f"After removing low scores: {len(df)}")


# ----------------------------------------------------------
# Clean Step E: Strip extra whitespace from the title column
# ----------------------------------------------------------

# .str.strip() removes any leading or trailing spaces from every title.
# Example: "  Hello World  " becomes "Hello World"
# This is important because spaces can cause problems in analysis later.
df["title"] = df["title"].str.strip()

print("Whitespace stripped from title column.")


# ============================================================
# SECTION 3 — Save the Cleaned Data as a CSV File
# ============================================================

print("\n--- Saving cleaned data ---\n")

# Make sure the data/ folder exists before saving
# exist_ok=True means: don't throw an error if the folder already exists
os.makedirs("data", exist_ok=True)

# The output CSV file path (fixed name, not date-stamped)
output_csv_path = "data/trends_clean.csv"

# to_csv() saves the DataFrame as a comma-separated values file
# index=False means: don't write the row numbers (0, 1, 2 ...) as a column
df.to_csv(output_csv_path, index=False)

# Confirm how many rows were saved
print(f"Saved {len(df)} rows to {output_csv_path}")


# ----------------------------------------------------------
# Print a summary: how many stories per category
# ----------------------------------------------------------

print("\nStories per category:")

# value_counts() counts how many times each category appears
# It returns a Series sorted from most to least by default
category_counts = df["category"].value_counts()

# Loop through each category and print the name + count neatly
for category_name, count in category_counts.items():
    # {category_name:<15} left-aligns the name in a 15-character wide space
    # {count} just prints the number next to it
    print(f"  {category_name:<15} {count}")


print("\nAll done! trends_clean.csv is ready for Task 3.")
