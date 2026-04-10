# Task 4 - Visualization
# This script reads analysis_report.json and creates charts using matplotlib.
# We create 6 charts:
# 1. Records by Source       - bar chart
# 2. Top 5 by Score          - horizontal bar chart
# 3. Top 5 by Comments       - horizontal bar chart
# 4. GitHub Languages        - pie chart
# 5. Score vs Comments       - scatter plot
# 6. Top Keywords            - bar chart

# matplotlib is a Python library used to draw charts and graphs
import json
import matplotlib.pyplot as plt


# ---- Chart 1: Records by Source (Bar Chart) ----
def chart_source_counts(source_counts):

    # Get the labels (github, hackernews) and values (counts)
    sources = list(source_counts.keys())
    counts  = list(source_counts.values())

    # Create a new figure with a specific size (width=6, height=4 inches)
    plt.figure(figsize=(6, 4))

    # Draw the bar chart with custom colors
    plt.bar(sources, counts, color=["#4C9BE8", "#E8844C"])

    # Add title and axis labels
    plt.title("Number of Records by Source")
    plt.xlabel("Source")
    plt.ylabel("Count")

    # Add count numbers on top of each bar
    for i in range(len(sources)):
        plt.text(i, counts[i] + 0.1, str(counts[i]), ha="center")

    # Adjust layout so nothing gets cut off
    plt.tight_layout()

    # Save the chart as a PNG image file
    plt.savefig("chart1_source_counts.png")

    # Close the chart to free memory before making the next one
    plt.close()
    print("Saved chart1_source_counts.png")


# ---- Chart 2: Top 5 Records by Score (Horizontal Bar Chart) ----
def chart_top5_score(top5_records):

    titles = []
    scores = []

    for record in top5_records:
        title = record["title"]

        # Shorten title if it's too long so it fits on the chart
        if len(title) > 30:
            title = title[:30] + "..."

        titles.append(title)
        scores.append(record["score"])

    plt.figure(figsize=(8, 5))

    # barh = horizontal bar chart (better for long labels)
    plt.barh(titles, scores, color="#6BCB77")

    plt.title("Top 5 Records by Score")
    plt.xlabel("Score")
    plt.tight_layout()
    plt.savefig("chart2_top5_score.png")
    plt.close()
    print("Saved chart2_top5_score.png")


# ---- Chart 3: Top 5 Most Commented HN Stories (Horizontal Bar Chart) ----
def chart_top5_comments(top5_comments):

    titles   = []
    comments = []

    for record in top5_comments:
        title = record["title"]

        # Shorten title if too long
        if len(title) > 30:
            title = title[:30] + "..."

        titles.append(title)
        comments.append(record["comments"])

    plt.figure(figsize=(8, 5))
    plt.barh(titles, comments, color="#FF9F43")
    plt.title("Top 5 Most Commented HN Stories")
    plt.xlabel("Number of Comments")
    plt.tight_layout()
    plt.savefig("chart3_top5_comments.png")
    plt.close()
    print("Saved chart3_top5_comments.png")


# ---- Chart 4: GitHub Language Distribution (Pie Chart) ----
def chart_languages(language_counts):

    # Remove None or N/A entries - they are not useful in a pie chart
    clean_langs = {}
    for lang, count in language_counts.items():
        if lang and lang != "None" and lang != "N/A":
            clean_langs[lang] = count

    # Get labels and values from the cleaned dictionary
    labels = list(clean_langs.keys())
    values = list(clean_langs.values())

    plt.figure(figsize=(6, 6))

    # autopct="%1.1f%%" shows percentage on each slice
    # startangle=90 rotates the chart so it starts from the top
    plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)

    plt.title("GitHub Repos by Language")
    plt.tight_layout()
    plt.savefig("chart4_languages.png")
    plt.close()
    print("Saved chart4_languages.png")


# ---- Chart 5: Score vs Comments (Scatter Plot) ----
def chart_score_vs_comments(score_comments):

    # Separate out scores and comments into two lists
    scores   = []
    comments = []

    for item in score_comments:
        scores.append(item["score"])
        comments.append(item["comments"])

    plt.figure(figsize=(7, 5))

    # scatter() draws one dot per story
    # s=80 controls the size of each dot
    plt.scatter(scores, comments, color="#C77DFF", s=80)

    plt.title("HN Stories: Score vs Comments")
    plt.xlabel("Score")
    plt.ylabel("Number of Comments")
    plt.tight_layout()
    plt.savefig("chart5_score_vs_comments.png")
    plt.close()
    print("Saved chart5_score_vs_comments.png")


# ---- Chart 6: Top Keywords (Bar Chart) ----
def chart_keywords(keywords):

    # Extract words and their counts from the list of dicts
    words  = [item["word"]  for item in keywords]
    counts = [item["count"] for item in keywords]

    plt.figure(figsize=(8, 5))
    plt.bar(words, counts, color="#4CC9F0")
    plt.title("Top Keywords in Titles")
    plt.xlabel("Keyword")
    plt.ylabel("Frequency")

    # Rotate x-axis labels so they don't overlap
    plt.xticks(rotation=30, ha="right")

    plt.tight_layout()
    plt.savefig("chart6_keywords.png")
    plt.close()
    print("Saved chart6_keywords.png")


# ---- Main - this is where the script starts running ----

# Load the analysis report from Task 3
with open("analysis_report.json", "r") as f:
    report = json.load(f)

print("analysis_report.json loaded!")

# Print a quick summary
print("Total records  :", report["total_records"])
print("Average score  :", report["average_score"])
print("Avg comments   :", report["average_comments"])

# Call each chart function with the relevant data from the report
chart_source_counts(report["source_counts"])
chart_top5_score(report["top_5_by_score"])
chart_top5_comments(report["top_5_by_comments"])
chart_languages(report["language_counts"])
chart_score_vs_comments(report["score_vs_comments"])
chart_keywords(report["top_keywords"])

print("\nAll 6 charts saved!")
print("Task 4 complete!")
