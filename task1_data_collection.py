# Task 1 - Data Collection
# This script fetches trending data from the internet and saves it to a file.

import requests
import json

# ---- Fetch trending repos from GitHub ----
def fetch_github():
    print("Fetching data from GitHub...")

    url = "https://api.github.com/search/repositories"

    # We are searching for popular repos created after 2024
    params = {
        "q": "created:>2024-01-01",
        "sort": "stars",
        "order": "desc",
        "per_page": 20
    }

    response = requests.get(url, params=params)
    data = response.json()

    repos = []

    for item in data["items"]:
        repo = {
            "title": item["name"],
            "description": item["description"],
            "stars": item["stargazers_count"],
            "language": item["language"],
            "url": item["html_url"]
        }
        repos.append(repo)

    print("GitHub data fetched! Total repos:", len(repos))
    return repos


# ---- Fetch top stories from Hacker News ----
def fetch_hackernews():
    print("Fetching data from Hacker News...")

    # Step 1: Get the list of top story IDs
    ids_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    ids_response = requests.get(ids_url)
    story_ids = ids_response.json()

    # Step 2: Get details of the first 35 stories
    stories = []

    for story_id in story_ids[:35]:
        story_url = "https://hacker-news.firebaseio.com/v0/item/" + str(story_id) + ".json"
        story_response = requests.get(story_url)
        story = story_response.json()

        item = {
            "title": story.get("title", ""),
            "score": story.get("score", 0),
            "url": story.get("url", ""),
            "author": story.get("by", "")
        }
        stories.append(item)

    print("Hacker News data fetched! Total stories:", len(stories))
    return stories


# ---- Save data to a JSON file ----
def save_data(github_data, hackernews_data):
    all_data = {
        "github": github_data,
        "hackernews": hackernews_data
    }

    with open("raw_data.json", "w") as f:
        json.dump(all_data, f, indent=2)

    print("Data saved to raw_data.json")


# ---- Main ----
github_data = fetch_github()
hackernews_data = fetch_hackernews()
save_data(github_data, hackernews_data)

print("Task 1 complete!")
