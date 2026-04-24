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
