# ============================================================
# TrendPulse — Task 3: Analysis with Pandas & NumPy
# ============================================================
# What this script does (in simple words):
#   1. Loads the clean CSV file made by Task 2
#   2. Explores the data — prints shape, first rows, averages
#   3. Uses NumPy to calculate statistics on the score column
#   4. Adds two new columns: engagement and is_popular
#   5. Saves the updated table to a new CSV for Task 4
#
# Needs: data/trends_clean.csv   (output from Task 2)
# Makes: data/trends_analysed.csv
# ============================================================

# --- Import the libraries we need ---

import pandas as pd    # Pandas  — works with tables of data (DataFrames)
import numpy  as np    # NumPy   — fast maths on lists of numbers (arrays)
import os              # Used to create folders if they don't exist


# ============================================================
# SECTION 1 — Load and Explore the Data
# ============================================================

# The path to the cleaned CSV file that Task 2 created
csv_file_path = "data/trends_clean.csv"

# Check that the file actually exists before trying to open it
# os.path.exists() returns True if the file is there, False if not
if not os.path.exists(csv_file_path):
    print(f"ERROR: File not found — {csv_file_path}")
    print("Please run task2_data_processing.py first.")
    exit()   # Stop the script if the file is missing

# pd.read_csv() reads a CSV file and loads it into a DataFrame
# A DataFrame is like a spreadsheet — rows (stories) and columns (fields)
df = pd.read_csv(csv_file_path)

# ----------------------------------------------------------
# Print the shape of the DataFrame
# ----------------------------------------------------------

# df.shape returns a tuple like (114, 7) meaning 114 rows and 7 columns
rows, columns = df.shape   # Unpack the tuple into two separate variables

print(f"Loaded data: ({rows}, {columns})")
print(f"  → {rows} stories, {columns} columns\n")

# ----------------------------------------------------------
# Print the first 5 rows
# ----------------------------------------------------------

# .head(5) returns the first 5 rows of the DataFrame
print("First 5 rows:")
print(df.head(5))
print()   # Blank line for readability

# ----------------------------------------------------------
# Print average score and average num_comments
# ----------------------------------------------------------

# .mean() calculates the average of all values in a column
average_score    = df["score"].mean()
average_comments = df["num_comments"].mean()

# round(..., 2) rounds the number to 2 decimal places
print(f"Average score   : {round(average_score, 2)}")
print(f"Average comments: {round(average_comments, 2)}")


# ============================================================
# SECTION 2 — Basic Analysis with NumPy
# ============================================================

print("\n--- NumPy Stats ---\n")

# Convert the "score" column to a NumPy array
# A NumPy array is like a Python list but much faster for maths
score_array = np.array(df["score"])

# ----------------------------------------------------------
# Mean — the average value
# np.mean() adds all values and divides by the count
# ----------------------------------------------------------
mean_score = np.mean(score_array)
print(f"Mean score   : {round(mean_score, 2)}")

# ----------------------------------------------------------
# Median — the middle value when sorted
# np.median() sorts the values and picks the one in the middle
# Useful because it is not affected by very high or low outliers
# ----------------------------------------------------------
median_score = np.median(score_array)
print(f"Median score : {round(median_score, 2)}")

# ----------------------------------------------------------
# Standard deviation — how spread out the values are
# A small std means scores are close together
# A large std means scores vary a lot
# np.std() calculates this for us
# ----------------------------------------------------------
std_score = np.std(score_array)
print(f"Std deviation: {round(std_score, 2)}")

# ----------------------------------------------------------
# Max and Min — the highest and lowest score
# np.max() finds the largest value in the array
# np.min() finds the smallest value in the array
# ----------------------------------------------------------
max_score = np.max(score_array)
min_score = np.min(score_array)

print(f"Max score    : {max_score}")
print(f"Min score    : {min_score}")

# ----------------------------------------------------------
# Which category has the most stories?
# ----------------------------------------------------------

# value_counts() counts how many rows belong to each category
# It returns a Series sorted from highest to lowest count
category_counts = df["category"].value_counts()

# .index[0] gives the name of the top category (highest count)
top_category = category_counts.index[0]

# .iloc[0] gives the count of the top category
top_category_count = category_counts.iloc[0]

print(f"\nMost stories in: {top_category} ({top_category_count} stories)")

# ----------------------------------------------------------
# Which story has the most comments?
# ----------------------------------------------------------

# df["num_comments"].idxmax() returns the INDEX (row number)
# of the row with the highest num_comments value
most_commented_index = df["num_comments"].idxmax()

# Use .loc[] to get the full row at that index
most_commented_row = df.loc[most_commented_index]

# Pull out the title and comment count from that row
most_commented_title    = most_commented_row["title"]
most_commented_comments = most_commented_row["num_comments"]

print(f'\nMost commented story: "{most_commented_title}"')
print(f"  — {most_commented_comments} comments")


# ============================================================
# SECTION 3 — Add New Columns
# ============================================================

print("\n--- Adding new columns ---\n")

# ----------------------------------------------------------
# New column 1: engagement
# Formula: num_comments / (score + 1)
# This measures how much discussion a story gets per upvote.
# We add 1 to score to avoid dividing by zero if score is 0.
# ----------------------------------------------------------

# Calculate engagement for every row at once (Pandas does this automatically)
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# Round engagement to 4 decimal places to keep it tidy
df["engagement"] = df["engagement"].round(4)

print("Added column: engagement  (= num_comments / (score + 1))")

# ----------------------------------------------------------
# New column 2: is_popular
# Formula: True if score > average score, else False
# We already calculated average_score above, so we reuse it here.
# ----------------------------------------------------------

# df["score"] > average_score creates a True/False value for every row
# True  → this story's score is above average  → popular
# False → this story's score is at or below average → not popular
df["is_popular"] = df["score"] > average_score

print(f"Added column: is_popular  (True if score > {round(average_score, 2)})")

# Show how many stories are popular vs not popular
popular_count     = df["is_popular"].sum()        # True counts as 1, so sum = count of True
not_popular_count = len(df) - popular_count        # The rest are not popular

print(f"  → Popular stories    : {popular_count}")
print(f"  → Not popular stories: {not_popular_count}")


# ============================================================
# SECTION 4 — Save the Updated DataFrame to CSV
# ============================================================

print("\n--- Saving results ---\n")

# Make sure the data/ folder exists
# exist_ok=True means: don't crash if the folder already exists
os.makedirs("data", exist_ok=True)

# The output file path for the analysed data
output_csv_path = "data/trends_analysed.csv"

# to_csv() saves the DataFrame to a CSV file
# index=False means: do NOT save the row numbers as an extra column
df.to_csv(output_csv_path, index=False)

# Print a confirmation message so the user knows it worked
print(f"Saved to {output_csv_path}")
print(f"  → {len(df)} rows, {len(df.columns)} columns")
print(f"  → Columns: {list(df.columns)}")

print("\nAll done! trends_analysed.csv is ready for Task 4.")
