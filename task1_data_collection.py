# ============================================================
# TrendPulse — Task 1: Fetch Data from API
# ============================================================
# What this script does (in simple words):
#   1. Asks HackerNews for its top 500 story IDs
#   2. Fetches details (title, score, author …) for each story
#   3. Puts each story into one of 5 categories based on keywords
#   4. Saves up to 25 stories per category into a JSON file
# ============================================================

# --- Import the libraries we need ---

import requests   # used to make HTTP requests (like opening a URL)
import json       # used to read and write JSON data
import os         # used to create folders on the computer
import time       # used to pause the script (sleep)
from datetime import datetime   # used to get the current date and time


# ============================================================
# SECTION 1 — Settings (things we can easily change later)
# ============================================================

# The base URL for every HackerNews API call
BASE_URL = "https://hacker-news.firebaseio.com/v0"

# A header that tells the server who is making the request
# It is good practice to identify your app in every request
HEADERS = {"User-Agent": "TrendPulse/1.0"}

# We want at most 25 stories per category
MAX_PER_CATEGORY = 25

# We will look through the first 500 top stories to find our 125
STORY_POOL_SIZE = 500

# ============================================================
# SECTION 2 — Category keywords
# ============================================================
# This is a dictionary.
# Each KEY is a category name (a string).
# Each VALUE is a list of keywords.
# If a story's title contains ANY keyword from a list,
# that story belongs to that category.

CATEGORIES = {
    "technology":    ["ai", "software", "tech", "code", "computer",
                      "data", "cloud", "api", "gpu", "llm"],

    "worldnews":     ["war", "government", "country", "president",
                      "election", "climate", "attack", "global"],

    "sports":        ["nfl", "nba", "fifa", "sport", "game", "team",
                      "player", "league", "championship"],

    "science":       ["research", "study", "space", "physics", "biology",
                      "discovery", "nasa", "genome"],

    "entertainment": ["movie", "film", "music", "netflix", "game",
                      "book", "show", "award", "streaming"],
}


# ============================================================
# SECTION 3 — Helper Function: assign a category to a story
# ============================================================

def assign_category(title):
    """
    Look at the story title and return which category it belongs to.
    If the title does not match any keyword, return None (meaning: skip it).
    """

    # Convert the title to lowercase so matching is case-insensitive
    # Example: "AI" and "ai" and "Ai" all become "ai"
    title_lower = title.lower()

    # Loop through each category and its list of keywords
    for category_name, keyword_list in CATEGORIES.items():

        # Loop through every keyword in this category's list
        for keyword in keyword_list:

            # Check if the keyword appears anywhere inside the title
            if keyword in title_lower:

                # Found a match! Return this category immediately
                return category_name

    # If we checked every category and found nothing, return None
    return None


# ============================================================
# SECTION 4 — Helper Function: safely fetch a URL
# ============================================================

def fetch_json(url):
    """
    Open a URL and return the data as a Python object (dict or list).
    If anything goes wrong (no internet, bad URL, etc.), just return None
    instead of crashing the whole script.
    """

    try:
        # Make the GET request to the given URL
        # timeout=10 means: give up if the server takes more than 10 seconds
        response = requests.get(url, headers=HEADERS, timeout=10)

        # raise_for_status() will throw an error if the server returned
        # a bad status code like 404 (Not Found) or 500 (Server Error)
        response.raise_for_status()

        # Convert the response body from JSON text to a Python object and return it
        return response.json()

    except requests.exceptions.RequestException as error:
        # This catches ALL network-related errors (timeout, DNS fail, bad status, etc.)
        print(f"  [WARNING] Could not fetch {url}  Reason: {error}")
        return None  # Return None so the caller knows it failed

    except json.JSONDecodeError as error:
        # This catches the case where the server replied but with invalid JSON
        print(f"  [WARNING] Bad JSON from {url}  Reason: {error}")
        return None  # Return None so the caller knows it failed


# ============================================================
# SECTION 5 — Main script starts here
# ============================================================

# Print a friendly header so the user knows the script started
print("=" * 60)
print("TrendPulse — Task 1: Data Collection")
print("=" * 60)


# ----------------------------------------------------------
# STEP 1: Get the list of top story IDs from HackerNews
# ----------------------------------------------------------

print(f"\nStep 1: Fetching the top {STORY_POOL_SIZE} story IDs...")

# Build the URL for the top stories endpoint
top_stories_url = f"{BASE_URL}/topstories.json"

# Call our helper function to fetch the list of IDs
all_ids = fetch_json(top_stories_url)

# If the fetch failed (returned None), we cannot continue — stop the script
if all_ids is None:
    print("ERROR: Could not get story IDs. Check your internet connection.")
    exit()  # Stop the script right here

# HackerNews returns thousands of IDs; we only want the first 500
# List slicing: all_ids[0:500] means "take items from index 0 up to (not including) 500"
story_ids = all_ids[:STORY_POOL_SIZE]

print(f"  OK — got {len(story_ids)} story IDs.")


# ----------------------------------------------------------
# STEP 2: Fetch each story's details and sort into categories
# ----------------------------------------------------------

print("\nStep 2: Fetching story details and categorising...\n")

# Create an empty list for each category to hold its stories
# This is a dictionary where each value starts as an empty list []
buckets = {
    "technology":    [],
    "worldnews":     [],
    "sports":        [],
    "science":       [],
    "entertainment": [],
}

# Record the current date and time ONCE before the loop starts
# so every story in this run gets the exact same timestamp
collected_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Loop through every story ID we collected in Step 1
for story_id in story_ids:

    # --- Early exit check ---
    # Count how many categories are already full (have 25 stories)
    full_buckets = 0
    for cat in buckets:
        if len(buckets[cat]) >= MAX_PER_CATEGORY:
            full_buckets += 1

    # If ALL 5 categories are full, we have our 125 stories — stop looping
    if full_buckets == len(CATEGORIES):
        print("  All categories are full — stopping early to save time.")
        break

    # --- Fetch this story's details ---
    # Build the URL for this specific story using its ID
    item_url = f"{BASE_URL}/item/{story_id}.json"

    # Fetch the story data (returns a dictionary or None on failure)
    story = fetch_json(item_url)

    # If the fetch failed, skip this story and move to the next one
    if story is None:
        continue   # 'continue' jumps back to the top of the for loop

    # Some HN items are "job" posts or deleted posts with no title — skip them
    if "title" not in story or story["title"] is None:
        continue

    # Get the title from the story dictionary
    title = story["title"]

    # Use our helper function to decide which category this story belongs to
    category = assign_category(title)

    # If no keyword matched, this story doesn't fit any category — skip it
    if category is None:
        continue

    # If this category's bucket already has 25 stories, skip — bucket is full
    if len(buckets[category]) >= MAX_PER_CATEGORY:
        continue

    # --- Build the record we want to save ---
    # We only save the specific fields listed in the assignment spec.
    # .get("field", default) safely reads a field; returns default if missing.
    record = {
        "post_id":      story.get("id"),            # Unique story ID (integer)
        "title":        title,                       # Story headline (string)
        "category":     category,                    # Our assigned category (string)
        "score":        story.get("score", 0),       # Upvote count (integer)
        "num_comments": story.get("descendants", 0), # Comment count — HN calls it "descendants"
        "author":       story.get("by", "unknown"),  # Username of the poster
        "collected_at": collected_at,                # Timestamp we recorded before the loop
    }

    # Add this record to the correct bucket
    buckets[category].append(record)

    # Print progress so the user can see something happening
    count_so_far = len(buckets[category])   # How many we have in this category now
    print(f"  [{category:>13}]  ({count_so_far}/{MAX_PER_CATEGORY})  {title[:65]}")


# ----------------------------------------------------------
# Inter-category sleep — 2 seconds per category (5 total)
# The spec says: one sleep per category, NOT per individual story
# ----------------------------------------------------------

print("\n  Waiting 2 seconds between categories (as required)...")

# Loop through each category name and sleep once per category
for category_name in CATEGORIES:
    time.sleep(2)   # Pause for 2 seconds
    print(f"  Slept 2 s  ->  done with category: {category_name}")


# ----------------------------------------------------------
# STEP 3: Save all stories to a JSON file
# ----------------------------------------------------------

print("\nStep 3: Saving stories to a JSON file...")

# Flatten all five buckets into one big list
# We loop through each bucket and add every story into all_stories
all_stories = []   # Start with an empty list

for category_name in buckets:
    # buckets[category_name] is a list of story dictionaries
    # We add every item from that list into all_stories
    for story_record in buckets[category_name]:
        all_stories.append(story_record)

# Create the "data" folder if it does not already exist
# exist_ok=True means: don't throw an error if the folder already exists
os.makedirs("data", exist_ok=True)

# Build the output filename using today's date
# strftime("%Y%m%d") formats the date as e.g. "20240115"
date_string = datetime.now().strftime("%Y%m%d")
output_file = f"data/trends_{date_string}.json"

# Open the file for writing ("w" mode) with UTF-8 encoding
# The 'with' block automatically closes the file when done
with open(output_file, "w", encoding="utf-8") as f:

    # json.dump() converts the Python list to JSON text and writes it to the file
    # indent=2 makes the JSON file nicely formatted and easy to read
    json.dump(all_stories, f, indent=2, ensure_ascii=False)

# ----------------------------------------------------------
# Print the final summary
# ----------------------------------------------------------

# This is the exact format the spec expects to see in the console
print(f"\nCollected {len(all_stories)} stories. Saved to {output_file}")

# Print a per-category breakdown as a bonus — helpful for checking thin buckets
print("\nBreakdown by category:")
for cat_name in buckets:
    count = len(buckets[cat_name])   # How many stories ended up in this bucket
    print(f"  {cat_name:>13} : {count} stories")

print("\nAll done!")
