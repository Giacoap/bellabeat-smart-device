# Cyclistic Bike-Share Analysis

**Google Data Analytics Professional Certificate — Capstone Case Study**

> How do annual members and casual riders use Cyclistic bikes differently?

---

## Overview

This project analyzes 12 months of real bike-share trip data (April 2025 – March 2026) from Divvy Bikes in Chicago to identify behavioral differences between casual riders and annual members. The goal is to inform a marketing strategy aimed at converting casual riders into annual members.

This analysis was completed as the capstone project for the [Google Data Analytics Professional Certificate](https://grow.google/certificates/data-analytics/). Unlike the course's suggested dataset (2019–2020), this project uses the most recent data available to ensure findings reflect current rider behavior.

---

## Key Findings

| Finding | Members | Casual Riders |
|---|---|---|
| Primary use case | Commuting | Leisure / recreation |
| Peak days | Tue – Thu | Saturday – Sunday |
| Peak hours | 8 AM and 5 PM (bimodal) | 3 – 5 PM (gradual curve) |
| Median ride duration | 8.7 min | 11.8 min (+36%) |
| Weekend share of rides | 23.4% | 37.7% |
| Summer share of annual rides | ~33% | ~42% |

**Top 3 recommendations:**
1. Launch a weekend-focused membership tier to lower the conversion barrier for leisure riders
2. Concentrate conversion campaigns in summer, when casual ridership peaks
3. Deploy targeted activation at high-casual stations (lakefront, parks, tourist areas)

---

## Repository Structure

```
cyclistic-bike-share/
│
├── data/
│   ├── raw/                  # Monthly CSV files (not included — see Data section)
│   └── processed/            # Cleaned dataset (cyclistic_clean.parquet)
│
├── charts/                   # All exported visualizations (PNG)
│   ├── 01_rides_by_type.png
│   ├── 02_rides_by_dow.png
│   ├── 03_avg_duration_dow.png
│   ├── 04_rides_by_hour.png
│   ├── 05_monthly_trend.png
│   ├── 06_ride_length_boxplot.png
│   ├── 07_rides_by_season.png
│   └── 08_bike_type.png
│
├── analysis.py               # Full analysis script (Prepare → Share)
├── writeup.md                # Case study write-up (Ask → Act)
└── README.md
```

---

## Data

**Source:** [Divvy Trip Data](https://divvy-tripdata.s3.amazonaws.com/index.html), provided by Motivate International Inc.  
**License:** [Divvy Data License Agreement](https://divvybikes.com/data-license-agreement)  
**Period:** April 2025 – March 2026 (12 monthly CSV files)  
**Raw size:** ~1 GB, 5,242,349 trips  
**After cleaning:** 5,103,110 trips (2.66% removed)

The raw CSV files are not included in this repository due to size. To reproduce the analysis, download the monthly files from the link above and place them in `data/raw/`.

---

## How to Reproduce

### Requirements

```
python >= 3.10
pandas
matplotlib
seaborn
pyarrow
```

Install dependencies:

```bash
pip install pandas matplotlib seaborn pyarrow
```

### Run the analysis

```bash
git clone https://github.com/your-username/cyclistic-bike-share.git
cd cyclistic-bike-share

# Download and place CSV files in data/raw/ (see Data section above)
# Bellabeat Smart Device Analysis

**Google Data Analytics Professional Certificate — Capstone Case Study**

> What trends in smart device usage can inform Bellabeat's marketing strategy?

---

## Overview

This project analyzes FitBit fitness tracker data to identify behavioral trends in how people use wellness devices — and translates those trends into actionable marketing recommendations for the **Bellabeat App**.

The analysis uses a **Python + SQL hybrid approach**: pandas for data cleaning and feature engineering, SQLite for all analytical queries, and matplotlib/seaborn for visualizations. This demonstrates proficiency in both Python-based data analysis and structured query language within a single reproducible workflow.

This case study was completed as the capstone project for the [Google Data Analytics Professional Certificate](https://grow.google/certificates/data-analytics/).

---

## Key Findings

| Finding | Metric |
|---|---|
| Average daily steps | 8,319 (below the 10,000-step WHO recommendation) |
| Days meeting step goal | 35.1% |
| Average sedentary time | 955 min/day (~16 hours, 78% of tracked time) |
| Users sleeping < 7 hrs | 54% (below recommended 7–9 hrs) |
| Average sleep duration | 6.99 hrs/night |
| Most active days | Tuesday and Saturday |
| Least active day | Sunday |
| Peak activity hours | 12 PM and 5–6 PM |

**Top 3 recommendations for the Bellabeat App:**
1. Position the app as a **sedentary behavior coach** — smart inactivity alerts, not just step counters
2. Elevate **sleep tracking** as a hero feature, not a secondary metric
3. Time notifications and campaigns to **peak activity windows** (midday and late afternoon)

---

## Repository Structure

```
bellabeat-smart-device/
│
├── data/
│   ├── raw/                        # Source CSV files (not included — see Data section)
│   │   ├── dailyActivity_merged.csv
│   │   ├── hourlySteps_merged.csv
│   │   ├── sleepDay_merged.csv
│   │   └── weightLogInfo_merged.csv
│   └── processed/
│       └── bellabeat.db            # SQLite database with cleaned tables
│
├── charts/                         # All exported visualizations (PNG)
│   ├── 01_activity_segments.png
│   ├── 02_step_goal.png
│   ├── 03_activity_by_dow.png
│   ├── 04_time_distribution.png
│   ├── 05_sleep_distribution.png
│   ├── 06_steps_vs_sleep.png
│   └── 07_hourly_heatmap.png
│
├── analysis.py                     # Full analysis script (Prepare → Share)
├── writeup.md                      # Case study write-up (Ask → Act)
└── README.md
```

---

## Data

**Source:** [FitBit Fitness Tracker Data](https://www.kaggle.com/datasets/arashnic/fitbit) by Möbius on Kaggle  
**License:** CC0 Public Domain  
**Period:** April 12 – May 12, 2016 (31 days)  
**Participants:** 33 users (24 with sleep data, 8 with weight data)

The raw CSV files are not included in this repository. Download them from Kaggle and place them in `data/raw/` before running the script.

### Acknowledged Limitations

This dataset has known limitations documented transparently in the write-up:
- Small sample (33 users) — not statistically representative
- No demographic data — gender and age unknown
- 2016 data — wearable behavior has evolved significantly
- 31-day window — insufficient to capture seasonal patterns

---

## How to Reproduce

### Requirements

```
python >= 3.10
pandas
matplotlib
seaborn
numpy
```

Install dependencies:

```bash
pip install pandas matplotlib seaborn numpy
```

`sqlite3` is included in Python's standard library — no additional installation needed.

### Run the analysis

```bash
git clone https://github.com/your-username/bellabeat-smart-device.git
cd bellabeat-smart-device

# Download CSV files from Kaggle and place them in data/raw/

python analysis.py
```

The script will:
1. Load and validate the 4 source CSV files
2. Clean the data and engineer features
3. Load all tables into a local SQLite database (`data/processed/bellabeat.db`)
4. Run SQL queries for all key findings
5. Generate and export 7 visualizations to `charts/`

### Running in Jupyter Notebook

Uncomment `%matplotlib inline` at the top of the script — charts will render inline in addition to being saved to disk.

---

## Methodology

This analysis follows the **Google Data Analytics six-phase process**:

| Phase | Description |
|---|---|
| **Ask** | Defined business task, guiding questions, and stakeholders |
| **Prepare** | Evaluated data credibility (ROCCC), documented limitations |
| **Process** | Cleaned data in Python, loaded into SQLite for reproducible querying |
| **Analyze** | Ran SQL queries for activity, sleep, and behavioral pattern analysis |
| **Share** | Generated 7 visualizations communicating key findings |
| **Act** | Formulated 3 actionable recommendations for the Bellabeat App |

Full documentation in [`writeup.md`](writeup.md).

---

## Tools

| Tool | Use |
|---|---|
| Python 3.12 | Primary analysis language |
| pandas | Data loading, cleaning, and feature engineering |
| sqlite3 | SQL-based analytical queries (standard library) |
| matplotlib | Chart generation |
| seaborn | Statistical visualizations (heatmap, scatter) |
| numpy | Numerical support |

---

## Author

**Giacomo**  
Google Data Analytics Professional Certificate — April 2026  
[LinkedIn](#) · [Portfolio](#)
