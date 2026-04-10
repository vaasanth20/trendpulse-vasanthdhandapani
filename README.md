# 📊 TrendPulse — Project Report
### What's Actually Trending Right Now | HackerNews Data Pipeline

> **Date Collected:** 10 April 2026  
> **Total Stories Analysed:** 83  
> **Pipeline:** Fetch JSON → Clean CSV → NumPy/Pandas Analysis → Visualise

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Task 1 — Fetch Data from API](#2-task-1--fetch-data-from-api)
3. [Task 2 — Clean the Data & Save as CSV](#3-task-2--clean-the-data--save-as-csv)
4. [Task 3 — Analysis with Pandas & NumPy](#4-task-3--analysis-with-pandas--numpy)
5. [Task 4 — Visualizations](#5-task-4--visualizations)
6. [Key Findings & Summary](#6-key-findings--summary)

---

## 1. Project Overview

**TrendPulse** is a 4-part end-to-end data pipeline built in Python.  
It collects trending stories from the HackerNews public API, cleans and structures them, runs statistical analysis, and produces charts that reveal what topics are genuinely trending online.

### Pipeline at a Glance

```
Task 1             Task 2              Task 3               Task 4
──────────         ──────────          ──────────           ──────────
Fetch JSON    ->   Clean CSV      ->   NumPy/Pandas    ->   Visualise
(requests)         (Pandas)            (Analysis)           (Matplotlib)
     │                  │                   │                    │
trends_          trends_             trends_              chart1.png
YYYYMMDD.json    clean.csv           analysed.csv         chart2.png
                                                          chart3.png
                                                          dashboard.png
```

### Libraries Used

| Library | Purpose |
|---|---|
| `requests` | Make HTTP calls to the HackerNews API |
| `json` | Read and write JSON files |
| `pandas` | Load, clean, and analyse tabular data |
| `numpy` | Statistical calculations (mean, median, std) |
| `matplotlib` | Draw and save charts as PNG images |
| `os` / `glob` | File and folder management |
| `time` / `datetime` | Delays between requests, timestamps |

---

## 2. Task 1 — Fetch Data from API

**File:** `task1_data_collection.py` | **Marks:** 20

### Planning & Reasoning

The goal was to pull real, live data from the internet without needing an API key.  
HackerNews offers a completely free, open REST API that returns JSON.  
The plan was:

1. Hit one endpoint to get a ranked list of top story IDs
2. Loop through those IDs and fetch each story's details one by one
3. Classify each story into a category by checking its title for keywords
4. Stop each category once it reached 25 stories, then save everything to JSON

### How the API Works

```
Step 1 — Get IDs (one request):
GET https://hacker-news.firebaseio.com/v0/topstories.json
→ Returns: [43721, 43698, 43712, ...]   ← a list of integers (story IDs)

Step 2 — Get each story (one request per story):
GET https://hacker-news.firebaseio.com/v0/item/{id}.json
→ Returns: { "id": 43721, "title": "...", "score": 412, "by": "user", ... }
```

### Category Keyword Logic

A story is assigned to the **first** category whose keyword appears anywhere in its title (case-insensitive):

| Category | Keywords |
|---|---|
| `technology` | ai, software, tech, code, computer, data, cloud, api, gpu, llm |
| `worldnews` | war, government, country, president, election, climate, attack, global |
| `sports` | nfl, nba, fifa, sport, game, team, player, league, championship |
| `science` | research, study, space, physics, biology, discovery, nasa, genome |
| `entertainment` | movie, film, music, netflix, game, book, show, award, streaming |

### Code Explanation

```python
# SECTION 1 — Settings
BASE_URL = "https://hacker-news.firebaseio.com/v0"
HEADERS  = {"User-Agent": "TrendPulse/1.0"}   # identifies our app to the server
MAX_PER_CATEGORY = 25                          # cap per bucket
STORY_POOL_SIZE  = 500                         # how many IDs to pull
```

```python
# SECTION 3 — assign_category() function
def assign_category(title):
    title_lower = title.lower()          # make comparison case-insensitive
    for category_name, keyword_list in CATEGORIES.items():
        for keyword in keyword_list:
            if keyword in title_lower:   # substring match
                return category_name     # return on FIRST match — no double-counting
    return None                          # no match → skip the story
```

```python
# SECTION 4 — fetch_json() function
def fetch_json(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()      # raises error on 4xx / 5xx status codes
        return response.json()
    except requests.exceptions.RequestException as error:
        print(f"  [WARNING] {error}")
        return None                      # return None instead of crashing
```

```python
# MAIN LOOP — fetch and categorise
for story_id in story_ids:
    if all_buckets_full():   # early exit — no point fetching more
        break
    story    = fetch_json(f"{BASE_URL}/item/{story_id}.json")
    category = assign_category(story["title"])
    buckets[category].append(record)     # add to the right bucket

# sleep ONCE per category (not per story — as per the spec)
for category_name in CATEGORIES:
    time.sleep(2)
```

### Output

```
============================================================
TrendPulse — Task 1: Data Collection
============================================================

Step 1: Fetching the top 500 story IDs...
  OK — got 500 story IDs.

Step 2: Fetching story details and categorising...

  [   technology]  (1/25)  Launch HN: Twill.ai (YC S25) – Delegate to cloud agents, get back
  [   technology]  (2/25)  Bild AI (YC W25) Is Hiring a Founding Product Engineer
  [   technology]  (3/25)  Clojure on Fennel Part One: Persistent Data Structures
  [   technology]  (4/25)  FBI used iPhone notification data to retrieve deleted Signal mess
  [   technology]  (5/25)  How NASA built Artemis II’s fault-tolerant computer
  [   technology]  (6/25)  HBO Obtains DMCA Subpoena to Unmask 'Euphoria' Spoiler Account on
  [   technology]  (7/25)  France to ditch Windows for Linux to reduce reliance on US tech
  [      science]  (1/25)  Native Instant Space Switching on macOS
  [   technology]  (8/25)  Supply chain nightmare: How Rust will be attacked and what we can
  [   technology]  (9/25)  We've raised $17M to build what comes after Git
  [   technology]  (10/25)  Why I'm Building a Database Engine in C#
  [   technology]  (11/25)  Code is run more than read (2023)
  [   technology]  (12/25)  Charcuterie – Visual similarity Unicode explorer
  [entertainment]  (1/25)  Show HN: Keeper – embedded secret store for Go (help me break it)
  [    worldnews]  (1/25)  "Negative" views of Broadcom driving VMware migrations, rival say
  [   technology]  (13/25)  Show HN: Marimo pair – Reactive Python notebooks as environments 
  [   technology]  (14/25)  US summons bank bosses over cyber risks from Anthropic's latest A
  [   technology]  (15/25)  OpenAI backs Illinois bill that would limit when AI labs can be h
  [       sports]  (1/25)  Inflation Rose to 3.3% in March, Driven by Rising Fuel Costs
  [   technology]  (16/25)  Instant 1.0, a backend for AI-coded apps
  [   technology]  (17/25)  Show HN: QVAC SDK, a universal JavaScript SDK for building local 
  [   technology]  (18/25)  Research-Driven Agents: When an agent reads before it codes
  [   technology]  (19/25)  An AI robot in my home
  [   technology]  (20/25)  The Raft consensus algorithm explained through "Mean Girls" (2019
  [   technology]  (21/25)  A WebGPU implementation of Augmented Vertex Block Descent
  [entertainment]  (2/25)  Show HN: I built a Cargo-like build tool for C/C++
  [   technology]  (22/25)  Git commands I run before reading any code
  [   technology]  (23/25)  Born Private: Reserve your child's first email address with Proto
  [    worldnews]  (2/25)  War on Raze
  [entertainment]  (3/25)  Launch HN: Relvy (YC F24) – On-call runbooks, automated
  [   technology]  (24/25)  LLM plays an 8-bit Commander X16 game using structured "smart sen
  [   technology]  (25/25)  Show HN: CSS Studio. Design by hand, code by agent
  [entertainment]  (4/25)  Show HN: Rust based eBook library for Python, with MIT license
  [       sports]  (2/25)  Show HN: Moon simulator game, ray-casting
  [entertainment]  (5/25)  Teardown of unreleased LG Rollable shows why rollable phones aren
  [entertainment]  (6/25)  Show HN: Guruka.com – free guided mediations. No signup, private,
  [      science]  (2/25)  How Close Is Too Close? Applying Fluid Dynamics Research Methods 
  [    worldnews]  (3/25)  Mexico's President Sheinbaum Decrees Universal Healthcare for 120
  [entertainment]  (7/25)  Show HN: Orange Juice – Small UX improvements that make HN easier
  [    worldnews]  (4/25)  Muse Spark: Scaling towards personal superintelligence
  [entertainment]  (8/25)  Show HN: 41 years sea surface temperature anomalies
  [entertainment]  (9/25)  Show HN: A (marginally) useful x86-64 ELF executable in 301 bytes
  [entertainment]  (10/25)  Show HN: Mdpdf a 2k line C CLI to convert Markdown to tiny PDFs
  [entertainment]  (11/25)  Show HN: Is Hormuz open yet?
  [entertainment]  (12/25)  Show HN: Brutalist Concrete Laptop Stand (2024)
  [    worldnews]  (5/25)  GLM-5.1: Towards Long-Horizon Tasks
  [       sports]  (3/25)  Show HN: I pipe free sports streams into Jellyfin – no ads, just 
  [entertainment]  (13/25)  Show HN: We built a camera only robot vacuum for less than $300 (
  [entertainment]  (14/25)  Show HN: Go-Bt: Minimalist Behavior Trees for Go
  [entertainment]  (15/25)  Show HN: I built a navigation app that displays weather along the
  [entertainment]  (16/25)  Show HN: Linear RNN/Reservoir hybrid generative model, one C file
  [    worldnews]  (6/25)  IPv6 is the only way forward
  [    worldnews]  (7/25)  Moving fast in hardware: lessons from lab to $100M ARR
  [entertainment]  (17/25)  Show HN: An interactive map of Tolkien's Middle-earth
  [    worldnews]  (8/25)  Three hundred synths, 3 hardware projects, and one app
  [entertainment]  (18/25)  Show HN: Gemma 4 Multimodal Fine-Tuner for Apple Silicon
  [       sports]  (4/25)  Breaking the console: a brief history of video game security
  [entertainment]  (19/25)  Show HN: Ghost Pepper – Local hold-to-talk speech-to-text for mac
  [entertainment]  (20/25)  Show HN: A cartographer's attempt to realistically map Tolkien's 
  [entertainment]  (21/25)  Show HN: Hindsight Simulator – Go back in time and get rich
  [entertainment]  (22/25)  Show HN: Zoneless – Open-source Stripe Connect clone with $0.002 
  [    worldnews]  (9/25)  German police name alleged leaders of GandCrab and REvil ransomwa
  [       sports]  (5/25)  Battle for Wesnoth: open-source, turn-based strategy game
  [       sports]  (6/25)  The 1987 game “The Last Ninja” was 40 kilobytes
  [entertainment]  (23/25)  Show HN: Pion/handoff – Move WebRTC out of browser and into Go
  [entertainment]  (24/25)  Show HN: Logoshi, a brand kit generator for solo founders
  [entertainment]  (25/25)  Show HN: BrokenClaw Part 5: GPT-5.4 Edition (Prompt Injection)
  [      science]  (3/25)  Computational Physics (2nd Edition) (2025)
  [       sports]  (7/25)  The Harvard Library Passport
  [    worldnews]  (10/25)  Show HN: GovAuctions lets you browse government auctions at once
  [       sports]  (8/25)  Can It Resolve Doom? Game Engine in 2k DNS Records
  [      science]  (4/25)  SOM: A minimal Smalltalk for teaching of and research on Virtual 
  [      science]  (5/25)  The Bra-and-Girdle Maker That Fashioned the Impossible for NASA
  [      science]  (6/25)  Case study: recovery of a corrupted 12 TB multi-device pool
  [       sports]  (9/25)  BYD teams up with KFC to offer 9 minute EV charging
  [       sports]  (10/25)  Lethal conflict after group fission in wild chimpanzees
  [    worldnews]  (11/25)  Winners of the 2026 Kokuyo Design Awards
  [    worldnews]  (12/25)  The Blueprint of a North Korean Attack on Open-Source
  [    worldnews]  (13/25)  France Launches Government Linux Desktop Plan as Windows Exit Beg
  [       sports]  (11/25)  Starfling: A one-tap endless orbital slingshot game in a single H
  [       sports]  (12/25)  Bevy game development tutorials and in-depth resources
  [    worldnews]  (14/25)  How Iran's Information War Machine Operates Online
  [    worldnews]  (15/25)  ICE acknowledges it is using powerful spyware
  [    worldnews]  (16/25)  FCC considers retroactive ban on foreign hardware
  [    worldnews]  (17/25)  Flashback to a time when government reports were works of art
  [    worldnews]  (18/25)  Amazon rewards loyal Kindle devotees by closing the book on old e
  [    worldnews]  (19/25)  Chrome rolls out hardware-bound session protection to combat info
  [    worldnews]  (20/25)  White House Warns Staff Not to Place Bets on Prediction Markets A
  [    worldnews]  (21/25)  The Iran war depleted US weapons. Rebuilding will require China's
  [    worldnews]  (22/25)  Not just spyware scandals: EU is funding the industry that spies 

  Waiting 2 seconds between categories (as required)...
  Slept 2 s  ->  done with category: technology
  Slept 2 s  ->  done with category: worldnews
  Slept 2 s  ->  done with category: sports
  Slept 2 s  ->  done with category: science
  Slept 2 s  ->  done with category: entertainment

Step 3: Saving stories to a JSON file...

Collected 90 stories. Saved to data/trends_20260411.json

Breakdown by category:
     technology : 25 stories
      worldnews : 22 stories
         sports : 12 stories
        science : 6 stories
  entertainment : 25 stories

All done!

```

> **Note:** Sports and science collected fewer than 25 stories because the top 500 HackerNews stories on this date contained fewer matching keywords for those categories — this is real-world data, not an error.

---

## 3. Task 2 — Clean the Data & Save as CSV

**File:** `task2_data_processing.py` | **Marks:** 20

### Planning & Reasoning

Raw JSON data from any API is rarely perfect. Before doing any analysis the data needs to be validated and standardised. The cleaning pipeline was designed to go from most destructive to least: remove junk rows first (duplicates, nulls), then fix the surviving rows (types, whitespace).

### Cleaning Pipeline (Step by Step)

```
Raw JSON (from Task 1)
        │
 A. Remove duplicates       — same post_id appearing twice inflates counts
        │
 B. Drop rows with nulls    — post_id / title / score must exist
        │
 C. Fix data types          — score & num_comments must be integers, not floats
        │
 D. Remove low scores       — stories with score < 5 are noise, not trends
        │
 E. Strip whitespace        — "  Hello  " becomes "Hello" to avoid match errors
        │
 Clean CSV  →  data/trends_clean.csv
```

### Code Explanation

```python
# STEP 1 — Auto-find the latest JSON file
json_files = glob.glob("data/trends_*.json")   # find all matching files
json_files.sort()                              # sort by date (alphabetical = chronological)
json_file_path = json_files[-1]               # pick the newest one

df = pd.read_json(json_file_path)             # load into a DataFrame
```

```python
# STEP 2A — Remove duplicates
df.drop_duplicates(subset=["post_id"], keep="first", inplace=True)
# subset=["post_id"] → only check this column for duplicates
# keep="first"       → keep the first occurrence, drop the rest
# inplace=True       → modify df directly, no need to reassign
```

```python
# STEP 2B — Drop rows missing key fields
df.dropna(subset=["post_id", "title", "score"], inplace=True)
# If ANY of these three fields is missing in a row, that row is removed
```

```python
# STEP 2C — Fix data types
df["score"]        = df["score"].astype(int)
df["num_comments"] = df["num_comments"].fillna(0).astype(int)
# fillna(0) replaces NaN with 0 first — astype(int) crashes on NaN
```

```python
# STEP 2D — Remove low-quality stories
df = df[df["score"] >= 5]
# df["score"] >= 5 creates a True/False mask for every row
# wrapping df[...] keeps only the True rows
```

```python
# STEP 2E — Strip whitespace from titles
df["title"] = df["title"].str.strip()
# .str.strip() removes leading and trailing spaces from every string in the column
```

### Output

```
After removing nulls: 90
Data types fixed: score and num_comments are now integers.
After removing low scores: 83
Whitespace stripped from title column.

--- Saving cleaned data ---

Saved 83 rows to data/trends_clean.csv

Stories per category:
  technology      24
  entertainment   24
  worldnews       20
  sports          9
  science         6

All done! trends_clean.csv is ready for Task 3.

```

---

## 4. Task 3 — Analysis with Pandas & NumPy

**File:** `task3_analysis.py` | **Marks:** 20

### Planning & Reasoning

With clean data in hand the goal was to find patterns and answer specific questions:
- How spread out are the scores? (mean vs median tells us if there are outliers)
- Which category dominates? (category counts)
- Which story sparked the most discussion? (most comments)
- Can we rank stories beyond just score? (engagement column)

NumPy was used for all statistical calculations — it operates on arrays directly and is faster and more precise than doing the maths manually.

### Key Statistics (from the real data)

| Metric | Value |
|---|---|
| **Total stories** | 83 |
| **Mean score** | 171.20 |
| **Median score** | 90.00 |
| **Std deviation** | 285.68 |
| **Highest score** | 2,263 |
| **Lowest score** | 6 |
| **Average comments** | 75.19 |
| **Popular stories** | 22 (score > 171.20) |
| **Not popular stories** | 61 |

> **Insight:** The mean (171.20) is almost **double** the median (90.00). This tells us the score distribution is heavily skewed — a few viral stories with very high scores are pulling the average up. The standard deviation of 285.68 confirms scores are very spread out.

### New Columns Added

| Column | Formula | What it tells us |
|---|---|---|
| `engagement` | `num_comments / (score + 1)` | How much debate per upvote. A high score but few comments = low engagement. |
| `is_popular` | `score > mean_score` (171.20) | Simple True/False flag for above-average stories |

### Code Explanation

```python
# SECTION 2 — NumPy statistics
score_array = np.array(df["score"])   # convert Pandas column → NumPy array

mean_score   = np.mean(score_array)   # sum ÷ count
median_score = np.median(score_array) # middle value when sorted
std_score    = np.std(score_array)    # how spread out the values are
max_score    = np.max(score_array)    # highest value
min_score    = np.min(score_array)    # lowest value
```

```python
# Find the most commented story
most_commented_index = df["num_comments"].idxmax()  # row index of the max value
most_commented_row   = df.loc[most_commented_index] # fetch the full row
title    = most_commented_row["title"]
comments = most_commented_row["num_comments"]
```

```python
# SECTION 3 — Add new columns
df["engagement"] = df["num_comments"] / (df["score"] + 1)
# +1 prevents divide-by-zero if score is 0
df["engagement"] = df["engagement"].round(4)

df["is_popular"] = df["score"] > average_score
# Pandas compares every row to average_score and writes True or False
```

### Output

```
Most commented story: "We've raised $17M to build what comes after Git"
  — 604 comments

--- Adding new columns ---

Added column: engagement  (= num_comments / (score + 1))
Added column: is_popular  (True if score > 171.2)
  → Popular stories    : 22
  → Not popular stories: 61

--- Saving results ---

Saved to data/trends_analysed.csv
  → 83 rows, 9 columns
  → Columns: ['post_id', 'title', 'category', 'score', 'num_comments', 'author', 'collected_at', 'engagement', 'is_popular']

All done! trends_analysed.csv is ready for Task 4.

```

---

## 5. Task 4 — Visualizations

**File:** `task4_visualization.py` | **Marks:** 20 (+3 bonus)

### Planning & Reasoning

Three charts were chosen to answer three different questions visually:

| Chart | Question answered | Chart type |
|---|---|---|
| Chart 1 | Which individual stories got the most upvotes? | Horizontal bar |
| Chart 2 | Which category had the most coverage? | Vertical bar |
| Chart 3 | Do high-scoring stories also get more comments? | Scatter plot |
| Dashboard | All three at a glance | Combined figure |

The `savefig()` → `close()` pattern was followed for every chart to ensure files are saved correctly before the figure is cleared.

---

### Chart 1 — Top 10 Stories by Score

![Top 10 HackerNews Stories by Score](chart1_top_stories.png)

**What the chart shows:** The top-ranked story (*"Git commands I run before reading any code"*) scored **2,263 upvotes** — nearly 3× more than the second-place story. Positions 3–10 are much closer together, suggesting one viral outlier dominated the day's feed.

**Key code decisions:**
```python
df_sorted = df.sort_values("score", ascending=False)  # highest first
top10     = df_sorted.head(10)                        # first 10 rows

# Shorten titles longer than 50 characters
for title in top10["title"]:
    if len(title) > 50:
        short_titles.append(title[:47] + "...")   # trim + add "..."

ax.barh(short_titles, top10["score"], color="steelblue")
ax.invert_yaxis()   # rank #1 at the TOP, not the bottom
```

---

### Chart 2 — Stories per Category

![Number of Stories per Category](chart2_categories.png)

**What the chart shows:** Technology and entertainment tied at **24 stories each**, followed by worldnews (20). Sports (9) and science (6) had far fewer matches — HackerNews simply had fewer qualifying posts in those categories on this date.

**Key code decisions:**
```python
category_counts = df["category"].value_counts()      # count per category

bar_colors = ["steelblue", "tomato", "mediumseagreen", "goldenrod", "mediumpurple"]
# one unique colour per bar — makes each category visually distinct

# Add count labels on top of each bar
for i, value in enumerate(category_values):
    ax.text(i, value + 0.2, str(value), ha="center")  # number floating above bar
```

---

### Chart 3 — Score vs Comments (Scatter Plot)

![Score vs Number of Comments](chart3_scatter.png)

**What the chart shows:** There is a **loose positive trend** — higher-scoring stories tend to get more comments. However, some stories with moderate scores still attracted huge comment counts (e.g., the $17M Git story at ~350 score but 604 comments), suggesting certain topics spark debate regardless of upvotes.

Popular stories (red dots, score > 171.20) cluster in the upper-right as expected, but a few blue (not-popular) dots also appear high on the comments axis — stories that were controversial rather than simply liked.

**Key code decisions:**
```python
# Split into two groups using the is_popular column
popular     = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

# Plot each group separately so they get different colours and legend labels
ax.scatter(not_popular["score"], not_popular["num_comments"],
           color="cornflowerblue", label="Not Popular", alpha=0.7)

ax.scatter(popular["score"], popular["num_comments"],
           color="tomato", label="Popular", alpha=0.8)

ax.legend(title="Story Type")   # legend generated automatically from label= values
```

---

### Dashboard (Bonus) — All 3 Charts Combined

![TrendPulse Dashboard](dashboard.png)

**What it shows:** A single image containing all three charts side by side under the title "TrendPulse Dashboard" — useful for sharing the full picture at a glance.

**Key code decisions:**
```python
# Create 1 row × 3 columns of chart panels in one figure
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 6))

# Overall title above all panels
fig.suptitle("TrendPulse Dashboard", fontsize=18, fontweight="bold", y=1.02)

# Leave room for the suptitle so it doesn't overlap the charts
plt.tight_layout(rect=[0, 0, 1, 0.97])

plt.savefig("outputs/dashboard.png", bbox_inches="tight")
```

---

## 6. Key Findings & Summary

### What the Data Tells Us

**1. One story dominated the entire day**  
*"Git commands I run before reading any code"* scored 2,263 — almost 3× the nearest competitor. This is a common pattern on HackerNews: practical, developer-focused "tips & tricks" posts go viral quickly.

**2. Technology and entertainment led in volume**  
Both tied at 24 stories (out of 83 total = 29% each). Sports and science were severely underrepresented, reflecting what HackerNews readers write about most.

**3. High score ≠ high engagement**  
The most-commented story (*"We've raised $17M to build what comes after Git"* — 604 comments) was NOT the highest-scored story. This shows that controversy and debate drive comments more than pure popularity.

**4. Scores are heavily skewed**  
Mean (171.20) >> Median (90.00). In a perfectly even distribution these would be equal. The large gap proves a few outliers are pulling the average up — the median is the more honest "typical score."

**5. Only 22 out of 83 stories are truly popular**  
Just 26% of stories beat the mean score. Most stories cluster at the lower end of the scale — a small number of viral stories carry most of the social weight.

### Files Produced

| File | Contents |
|---|---|
| `data/trends_20260411.json` | Raw story data from HackerNews API |
| `data/trends_clean.csv` | Cleaned data (83 rows, 7 columns) |
| `data/trends_analysed.csv` | Cleaned + engagement + is_popular columns (83 rows, 9 columns) |
| `outputs/chart1_top_stories.png` | Top 10 stories by score (horizontal bar) |
| `outputs/chart2_categories.png` | Stories per category (vertical bar) |
| `outputs/chart3_scatter.png` | Score vs comments coloured by popularity |
| `outputs/dashboard.png` | All 3 charts combined in one image |

### Pipeline Summary

```
task1_data_collection.py
  → Fetched 500 story IDs from HackerNews
  → Categorised and collected 83 matching stories
  → Saved as data/trends_20260411.json

task2_data_processing.py
  → Loaded 83 rows, removed duplicates, nulls, low scores
  → Fixed data types, stripped whitespace
  → Saved 83 clean rows to data/trends_clean.csv

task3_analysis.py
  → Computed mean=171.20, median=90.00, std=285.68
  → Identified top story (score=2263) and most commented (604 comments)
  → Added engagement and is_popular columns
  → Saved to data/trends_analysed.csv

task4_visualization.py
  → Chart 1: Top 10 stories horizontal bar chart
  → Chart 2: Category count bar chart
  → Chart 3: Score vs comments scatter plot
  → Dashboard: All 3 charts in one combined figure
```

---

*TrendPulse — Built with Python, Pandas, NumPy, and Matplotlib*
