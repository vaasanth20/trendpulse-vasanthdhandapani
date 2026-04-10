# ============================================================
# TrendPulse — Task 4: Visualizations
# ============================================================
# What this script does (in simple words):
#   1. Loads the analysed CSV file from Task 3
#   2. Creates Chart 1 — horizontal bar chart of top 10 stories by score
#   3. Creates Chart 2 — bar chart of story count per category
#   4. Creates Chart 3 — scatter plot of score vs comments
#   5. Combines all 3 into one dashboard image (bonus)
#   6. Saves every chart as a PNG file inside the outputs/ folder
#
# Needs: data/trends_analysed.csv   (output from Task 3)
# Makes: outputs/chart1_top_stories.png
#        outputs/chart2_categories.png
#        outputs/chart3_scatter.png
#        outputs/dashboard.png  (bonus)
# ============================================================

# --- Import the libraries we need ---

import pandas as pd              # Pandas  — loads and works with the CSV table
import matplotlib.pyplot as plt  # Matplotlib — draws charts and saves them as images
import os                        # Used to create the outputs/ folder


# ============================================================
# SECTION 1 — Setup: Load data and create output folder
# ============================================================

# The path to the analysed CSV that Task 3 created
csv_file_path = "data/trends_analysed.csv"

# Check the file exists before trying to open it
if not os.path.exists(csv_file_path):
    print(f"ERROR: File not found — {csv_file_path}")
    print("Please run task3_analysis.py first.")
    exit()   # Stop the script if the file is missing

# Load the CSV into a Pandas DataFrame
df = pd.read_csv(csv_file_path)

print(f"Loaded {len(df)} rows from {csv_file_path}")

# Create the outputs/ folder if it does not already exist
# exist_ok=True means: don't throw an error if it already exists
os.makedirs("outputs", exist_ok=True)

print("Output folder ready: outputs/\n")


# ============================================================
# SECTION 2 — Chart 1: Top 10 Stories by Score
# ============================================================

print("Drawing Chart 1: Top 10 Stories by Score...")

# --- Prepare the data for this chart ---

# Sort the DataFrame by score from highest to lowest
# ascending=False means highest score comes first
df_sorted = df.sort_values("score", ascending=False)

# Take only the first 10 rows — these are the top 10 stories
top10 = df_sorted.head(10)

# Some titles are very long and won't fit on the chart nicely.
# We shorten any title longer than 50 characters by cutting it at 47
# and adding "..." at the end to show it was trimmed.
short_titles = []              # Start with an empty list
for title in top10["title"]:   # Loop through each title in the top 10
    if len(title) > 50:
        # Slice the first 47 characters and add "..."
        short_titles.append(title[:47] + "...")
    else:
        # Title is short enough — keep it as-is
        short_titles.append(title)

# --- Draw the chart ---

# Create a new figure (the blank canvas) with a specific size
# figsize=(10, 6) means 10 inches wide and 6 inches tall
fig, ax = plt.subplots(figsize=(10, 6))

# barh() draws a HORIZONTAL bar chart
# short_titles goes on the y-axis (labels on the left)
# top10["score"] goes on the x-axis (bar lengths)
# color sets the colour of all bars
ax.barh(short_titles, top10["score"], color="steelblue")

# Reverse the y-axis so the highest score appears at the TOP
# By default matplotlib puts the first item at the bottom
ax.invert_yaxis()

# Add a title to the chart
ax.set_title("Top 10 HackerNews Stories by Score", fontsize=14)

# Label the x-axis (horizontal axis)
ax.set_xlabel("Score (Upvotes)")

# Label the y-axis (vertical axis)
ax.set_ylabel("Story Title")

# tight_layout() automatically adjusts spacing so labels don't get cut off
plt.tight_layout()

# Save the chart as a PNG image BEFORE calling plt.show()
# This is important — plt.show() clears the figure, so save first
plt.savefig("outputs/chart1_top_stories.png")

print("  Saved: outputs/chart1_top_stories.png")

# Close the figure to free memory before drawing the next chart
plt.close()


# ============================================================
# SECTION 3 — Chart 2: Stories per Category
# ============================================================

print("Drawing Chart 2: Stories per Category...")

# --- Prepare the data for this chart ---

# value_counts() counts how many stories belong to each category
# It returns a Series: index = category names, values = counts
category_counts = df["category"].value_counts()

# Get the category names (the labels for the x-axis)
category_names = category_counts.index.tolist()   # Convert index to a plain list

# Get the counts (the heights of the bars)
category_values = category_counts.values.tolist() # Convert values to a plain list

# Choose a different colour for each bar
# We pick 5 colours manually — one for each category
bar_colors = ["steelblue", "tomato", "mediumseagreen", "goldenrod", "mediumpurple"]

# --- Draw the chart ---

# Create a new figure
fig, ax = plt.subplots(figsize=(9, 5))

# bar() draws a VERTICAL bar chart
# category_names goes on the x-axis
# category_values sets the height of each bar
# color assigns a different colour to each bar
ax.bar(category_names, category_values, color=bar_colors)

# Add a title
ax.set_title("Number of Stories per Category", fontsize=14)

# Label the axes
ax.set_xlabel("Category")
ax.set_ylabel("Number of Stories")

# Add the exact count number on top of each bar so it's easy to read
for i, value in enumerate(category_values):
    # ax.text() places text at position (x, y) on the chart
    # i         = the x position (matches the bar index)
    # value + 0.2 = slightly above the top of the bar
    # str(value)  = the text to show
    # ha="center" = centre-align the text over the bar
    ax.text(i, value + 0.2, str(value), ha="center", fontsize=11)

plt.tight_layout()

# Save before closing
plt.savefig("outputs/chart2_categories.png")

print("  Saved: outputs/chart2_categories.png")

plt.close()


# ============================================================
# SECTION 4 — Chart 3: Score vs Comments (Scatter Plot)
# ============================================================

print("Drawing Chart 3: Score vs Comments...")

# --- Separate popular and non-popular stories ---

# df["is_popular"] is a column of True/False values (added in Task 3)
# We use it to split the DataFrame into two groups

# Keep only rows where is_popular is True
popular = df[df["is_popular"] == True]

# Keep only rows where is_popular is False
not_popular = df[df["is_popular"] == False]

# --- Draw the chart ---

fig, ax = plt.subplots(figsize=(9, 6))

# scatter() draws one dot for each story
# x = score (horizontal position of the dot)
# y = num_comments (vertical position of the dot)
# label = the text that will appear in the legend
# alpha = transparency of the dots (0.0 = invisible, 1.0 = solid)
#         0.7 makes overlapping dots easier to see

# Plot not-popular stories first (so popular ones appear on top)
ax.scatter(
    not_popular["score"],        # x values
    not_popular["num_comments"], # y values
    color="cornflowerblue",      # dot colour for not-popular
    label="Not Popular",         # legend label
    alpha=0.7,                   # slight transparency
    s=60                         # dot size in points²
)

# Plot popular stories on top
ax.scatter(
    popular["score"],            # x values
    popular["num_comments"],     # y values
    color="tomato",              # dot colour for popular
    label="Popular",             # legend label
    alpha=0.8,                   # slightly less transparent
    s=80                         # slightly bigger dots so they stand out
)

# Add a title and axis labels
ax.set_title("Score vs Number of Comments", fontsize=14)
ax.set_xlabel("Score (Upvotes)")
ax.set_ylabel("Number of Comments")

# ax.legend() draws the legend box using the label= values we set above
ax.legend(title="Story Type")

plt.tight_layout()

plt.savefig("outputs/chart3_scatter.png")

print("  Saved: outputs/chart3_scatter.png")

plt.close()


# ============================================================
# SECTION 5 — BONUS: Dashboard (all 3 charts in one image)
# ============================================================

print("Drawing Dashboard (bonus)...")

# plt.subplots(1, 3) creates ONE row of THREE side-by-side chart areas
# figsize=(20, 6) makes the overall figure wide enough for 3 charts
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 6))

# Give the whole dashboard an overall title
# y=1.02 moves the title slightly above the charts so it doesn't overlap
fig.suptitle("TrendPulse Dashboard", fontsize=18, fontweight="bold", y=1.02)

# ----------------------------------------------------------
# Dashboard Panel 1 — Top 10 Stories (reuse the top10 data)
# ----------------------------------------------------------

ax1.barh(short_titles, top10["score"], color="steelblue")
ax1.invert_yaxis()                                    # Highest score at top
ax1.set_title("Top 10 Stories by Score", fontsize=11)
ax1.set_xlabel("Score")
ax1.set_ylabel("Story Title")

# ----------------------------------------------------------
# Dashboard Panel 2 — Stories per Category (reuse category data)
# ----------------------------------------------------------

ax2.bar(category_names, category_values, color=bar_colors)
ax2.set_title("Stories per Category", fontsize=11)
ax2.set_xlabel("Category")
ax2.set_ylabel("Count")

# Add count labels on top of each bar (same as Chart 2)
for i, value in enumerate(category_values):
    ax2.text(i, value + 0.2, str(value), ha="center", fontsize=9)

# ----------------------------------------------------------
# Dashboard Panel 3 — Score vs Comments (reuse popular/not_popular)
# ----------------------------------------------------------

ax3.scatter(
    not_popular["score"],
    not_popular["num_comments"],
    color="cornflowerblue",
    label="Not Popular",
    alpha=0.7,
    s=50
)
ax3.scatter(
    popular["score"],
    popular["num_comments"],
    color="tomato",
    label="Popular",
    alpha=0.8,
    s=65
)
ax3.set_title("Score vs Comments", fontsize=11)
ax3.set_xlabel("Score")
ax3.set_ylabel("Comments")
ax3.legend(title="Story Type", fontsize=8)

# ----------------------------------------------------------
# Save the dashboard
# ----------------------------------------------------------

# tight_layout() with a small rect makes room for the suptitle above
plt.tight_layout(rect=[0, 0, 1, 0.97])

plt.savefig("outputs/dashboard.png", bbox_inches="tight")

print("  Saved: outputs/dashboard.png")

plt.close()


# ============================================================
# Final summary
# ============================================================

print("\nAll charts saved to outputs/:")
print("  outputs/chart1_top_stories.png")
print("  outputs/chart2_categories.png")
print("  outputs/chart3_scatter.png")
print("  outputs/dashboard.png  (bonus)")
print("\nPipeline complete! collect -> clean -> analyse -> visualise")
