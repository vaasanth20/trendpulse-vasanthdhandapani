# Task 2 - Data Processing
# This script loads raw_data.json, cleans the data, and saves it to cleaned_data.json.
# Cleaning means:
# - Removing empty or None values
# - Converting unix timestamps to readable dates
# - Making sure all records have the same structure (same fields)

import json
from datetime import datetime, timezone

# UTC timezone object - used when converting timestamps
UTC = timezone.utc


# ---- Clean a single text value ----
def clean_text(text):

    # If the value is None, return empty string instead of crashing
    if text is None:
        return ""

    # If it's not a string (e.g. a number), return empty string
    if not isinstance(text, str):
        return ""

    # Remove spaces from the beginning and end of the text
    text = text.strip()

    return text


# ---- Convert unix timestamp to a readable date ----
def unix_to_date(timestamp):

    # If no timestamp is given, return empty string
    if not timestamp:
        return ""

    # datetime.fromtimestamp converts a unix number like 1700000000
    # into a proper date like "2023-11-14 22:13 UTC"
    dt = datetime.fromtimestamp(timestamp, tz=UTC)

    # Format it as a human readable string
    return dt.strftime("%Y-%m-%d %H:%M UTC")


# ---- Clean GitHub data ----
def clean_github(repos):
    print("Cleaning GitHub data...")

    # List to store all cleaned repos
    cleaned = []

    for repo in repos:

        # Skip this repo if it has no title (useless record)
        if not repo["title"]:
            continue

        # Build a clean version of the repo with a standard structure
        clean_repo = {
            "source"     : "github",                      # where this data came from
            "title"      : clean_text(repo["title"]),     # repo name
            "description": clean_text(repo["description"]), # what it does
            "score"      : repo["stars"],                  # we use stars as the score
            "language"   : clean_text(repo["language"]),  # programming language
            "url"        : clean_text(repo["url"]),        # link to repo
            "comments"   : 0,                              # GitHub repos have no comments here
            "posted_on"  : "",                             # no post date for GitHub
            "type"       : "repository"                    # always a repository
        }

        # Add to our cleaned list
        cleaned.append(clean_repo)

    print("GitHub records cleaned:", len(cleaned))
    return cleaned


# ---- Clean Hacker News data ----
def clean_hackernews(stories):
    print("Cleaning Hacker News data...")

    # List to store all cleaned stories
    cleaned = []

    for story in stories:

        # Skip this story if it has no title
        if not story.get("title", ""):
            continue

        # Build a clean version of the story with a standard structure
        # .get() is used everywhere so we don't crash if a field is missing
        clean_story = {
            "source"     : "hackernews",
            "title"      : clean_text(story.get("title", "")),
            "description": "",                                    # HN stories have no description
            "score"      : story.get("score", 0),                 # upvote count
            "language"   : "N/A",                                 # no language for news stories
            "url"        : clean_text(story.get("url", "")),
            "comments"   : story.get("comments", 0),              # number of comments
            "posted_on"  : unix_to_date(story.get("time", 0)),    # convert to readable date
            "type"       : clean_text(story.get("type", "story")) # story / ask / show
        }

        # Add to our cleaned list
        cleaned.append(clean_story)

    print("Hacker News records cleaned:", len(cleaned))
    return cleaned


# ---- Remove duplicate titles ----
def remove_duplicates(records):

    # Keep track of titles we have already seen
    seen_titles = []

    # List to store only unique records
    unique_records = []

    for record in records:

        # Only add if we haven't seen this title before
        if record["title"] not in seen_titles:
            seen_titles.append(record["title"])
            unique_records.append(record)

    # How many were removed
    removed = len(records) - len(unique_records)
    print("Duplicates removed:", removed)
    return unique_records


# ---- Sort records by score (highest first) ----
def sort_by_score(records):

    # Bubble sort - compares each pair and swaps if out of order
    for i in range(len(records)):
        for j in range(i + 1, len(records)):

            # If the next record has a higher score, swap them
            if records[j]["score"] > records[i]["score"]:
                records[i], records[j] = records[j], records[i]

    return records


# ---- Main - this is where the script starts running ----

# Load the raw data that was saved by Task 1
with open("raw_data.json", "r") as f:
    raw_data = json.load(f)

print("raw_data.json loaded!")

# Clean each data source separately
github_clean     = clean_github(raw_data["github"])
hackernews_clean = clean_hackernews(raw_data["hackernews"])

# Merge both cleaned lists into one big list
all_records = github_clean + hackernews_clean

# Remove any duplicates
all_records = remove_duplicates(all_records)

# Sort everything by score so highest ranked items come first
all_records = sort_by_score(all_records)

# Prepare the final output structure
cleaned_output = {
    "total_records": len(all_records),  # total count
    "records"      : all_records        # the actual data
}

# Save the cleaned data to a new file for Task 3 to use
with open("cleaned_data.json", "w") as f:
    json.dump(cleaned_output, f, indent=2)

print("Cleaned data saved to cleaned_data.json")
print("Total records:", len(all_records))
print("Task 2 complete!")
