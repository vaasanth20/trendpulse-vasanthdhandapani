# Task 3 - Data Analysis
# This script loads cleaned_data.json and finds useful insights from the data.
# We analyse:
# - Average and highest/lowest scores
# - Which source has more records
# - Most popular programming languages (GitHub)
# - Most commented stories (Hacker News)
# - Score vs Comments relationship
# - Most used keywords in titles

import json


# ---- Find the average of a number field ----
def find_average(records, field):

    # Add up all values for the given field
    total = 0
    for record in records:
        total = total + record[field]

    # Divide by count to get the average
    average = total / len(records)

    # Round to 2 decimal places for cleanliness
    return round(average, 2)


# ---- Find the highest scored record ----
def find_highest(records):

    # Start by assuming the first record is the highest
    highest = records[0]

    # Compare every record against current highest
    for record in records:
        if record["score"] > highest["score"]:
            highest = record  # update if we find a higher one

    return highest


# ---- Find the lowest scored record ----
def find_lowest(records):

    # Start by assuming the first record is the lowest
    lowest = records[0]

    for record in records:
        if record["score"] < lowest["score"]:
            lowest = record  # update if we find a lower one

    return lowest


# ---- Count records by source ----
def count_by_source(records):

    # Dictionary to hold counts per source
    counts = {}

    for record in records:
        source = record["source"]

        # If source already exists in dict, add 1
        # Otherwise create it with value 1
        if source in counts:
            counts[source] = counts[source] + 1
        else:
            counts[source] = 1

    return counts


# ---- Count GitHub repos by programming language ----
def count_by_language(records):

    counts = {}

    for record in records:

        # Only process GitHub records
        if record["source"] == "github":
            lang = record["language"]

            if lang in counts:
                counts[lang] = counts[lang] + 1
            else:
                counts[lang] = 1

    return counts


# ---- Count HN stories by type (story / ask / show) ----
def count_by_type(records):

    counts = {}

    for record in records:

        # Only process Hacker News records
        if record["source"] == "hackernews":
            story_type = record["type"]

            if story_type in counts:
                counts[story_type] = counts[story_type] + 1
            else:
                counts[story_type] = 1

    return counts


# ---- Find top 5 most commented HN stories ----
def top_commented(records):

    # Filter only Hacker News records
    hn_stories = []
    for record in records:
        if record["source"] == "hackernews":
            hn_stories.append(record)

    # Sort HN stories by number of comments (bubble sort)
    for i in range(len(hn_stories)):
        for j in range(i + 1, len(hn_stories)):
            if hn_stories[j]["comments"] > hn_stories[i]["comments"]:
                hn_stories[i], hn_stories[j] = hn_stories[j], hn_stories[i]

    # Return top 5 with only the fields we need
    top = []
    for record in hn_stories[:5]:
        top.append({
            "title"   : record["title"],
            "comments": record["comments"],
            "score"   : record["score"]
        })
    return top


# ---- Find top 5 records by score ----
def top_5_by_score(records):

    # Records are already sorted by score from Task 2
    # So we just take the first 5
    top = []
    for record in records[:5]:
        top.append({
            "title" : record["title"],
            "score" : record["score"],
            "source": record["source"]
        })
    return top


# ---- Find most common words in titles ----
def common_words(records):

    # These are common English words that don't tell us anything useful
    stop_words = ["a", "an", "the", "and", "or", "for", "in", "of",
                  "to", "is", "with", "on", "by", "from", "at", "as",
                  "how", "why", "what", "are", "has", "have", "its",
                  "this", "that", "new", "via", "using"]

    # Dictionary to count how often each word appears
    word_count = {}

    for record in records:

        # Convert title to lowercase so "Python" and "python" are the same
        title = record["title"].lower()

        # Split title into individual words
        words = title.split()

        for word in words:

            # Remove special characters like () . , from the word
            clean_word = ""
            for char in word:
                if char.isalpha():           # only keep letters
                    clean_word = clean_word + char

            # Skip if word is empty, a stop word, or too short
            if clean_word and clean_word not in stop_words and len(clean_word) > 2:
                if clean_word in word_count:
                    word_count[clean_word] = word_count[clean_word] + 1
                else:
                    word_count[clean_word] = 1

    # Sort words by frequency (most common first)
    sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)

    # Return top 10 as a list of dicts
    top_words = []
    for word, count in sorted_words[:10]:
        top_words.append({"word": word, "count": count})

    return top_words


# ---- Collect score and comments together for scatter plot ----
def score_vs_comments(records):

    # We want to see if high score = high comments
    result = []

    for record in records:
        if record["source"] == "hackernews":
            result.append({
                "title"   : record["title"][:40],  # shorten long titles
                "score"   : record["score"],
                "comments": record["comments"]
            })

    return result


# ---- Main - this is where the script starts running ----

# Load the cleaned data from Task 2
with open("cleaned_data.json", "r") as f:
    data = json.load(f)

# Get the list of records
records = data["records"]
print("cleaned_data.json loaded!")
print("Total records:", len(records))

# Run all analysis functions
avg_score      = find_average(records, "score")
avg_comments   = find_average(records, "comments")
highest_record = find_highest(records)
lowest_record  = find_lowest(records)
source_counts  = count_by_source(records)
lang_counts    = count_by_language(records)
type_counts    = count_by_type(records)
top5_score     = top_5_by_score(records)
top5_comments  = top_commented(records)
keywords       = common_words(records)
score_comments = score_vs_comments(records)

# Print a quick summary to the terminal
print("\n--- Analysis Results ---")
print("Average score          :", avg_score)
print("Average comments (HN)  :", avg_comments)
print("Highest scored         :", highest_record["title"], "| Score:", highest_record["score"])
print("Most commented (HN)    :", top5_comments[0]["title"] if top5_comments else "N/A")
print("Records by source      :", source_counts)
print("HN story types         :", type_counts)
print("Top keywords           :", keywords)

# Save all results into a report file for Task 4 to use
report = {
    "total_records"    : len(records),
    "average_score"    : avg_score,
    "average_comments" : avg_comments,
    "highest_record"   : highest_record,
    "lowest_record"    : lowest_record,
    "source_counts"    : source_counts,
    "language_counts"  : lang_counts,
    "story_type_counts": type_counts,
    "top_5_by_score"   : top5_score,
    "top_5_by_comments": top5_comments,
    "top_keywords"     : keywords,
    "score_vs_comments": score_comments
}

with open("analysis_report.json", "w") as f:
    json.dump(report, f, indent=2)

print("\nReport saved to analysis_report.json")
print("Task 3 complete!")
