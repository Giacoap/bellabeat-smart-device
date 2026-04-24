# Bellabeat Smart Device Analysis: Trends Informing a Wellness Marketing Strategy

**Google Data Analytics Professional Certificate — Capstone Case Study**
**Author:** Giacomo | **Date:** April 2026 | **Tools:** Python, SQL (sqlite3), pandas, matplotlib, seaborn

---

## Introduction & Business Context

Bellabeat is a high-tech wellness company that designs smart products for women. Founded in 2013 by Urška Sršen and Sando Mur, the company develops wearables and an accompanying app that track activity, sleep, stress, and reproductive health. Bellabeat's product line includes the Leaf tracker, the Time wellness watch, the Spring hydration bottle, and the Bellabeat App — the central hub that connects all devices and delivers personalized health insights.

Despite strong growth since its founding, Bellabeat has identified an opportunity to expand its presence in the global smart device market. Urška Sršen believes that analyzing fitness data from third-party smart devices can reveal behavioral patterns in how people actually use wellness technology — insights that can sharpen Bellabeat's marketing strategy and product positioning.

This analysis uses publicly available FitBit tracker data to answer three strategic questions:

1. What trends exist in smart device usage?
2. How could these trends apply to Bellabeat customers?
3. How could these trends influence Bellabeat's marketing strategy?

The findings and recommendations in this report are focused on the **Bellabeat App** — the product that connects the entire Bellabeat ecosystem and serves as the primary touchpoint for user engagement across all devices.

---

## Ask — Business Task & Stakeholders

### Business Task

Analyze FitBit fitness tracker data to identify trends in smart device usage and determine how those trends can inform Bellabeat's marketing strategy for the Bellabeat App.

### Guiding Questions

1. What trends exist in how users engage with smart fitness devices?
2. How could these behavioral patterns apply to Bellabeat's customer base?
3. What marketing opportunities do these trends suggest for the Bellabeat App?

### Stakeholders

| Stakeholder | Role | Interest in this analysis |
|---|---|---|
| Urška Sršen | Co-founder & CCO | Wants data-backed insights to guide marketing strategy and product development |
| Sando Mur | Co-founder & Mathematician | Interested in the analytical approach and business implications |
| Bellabeat Marketing Analytics Team | Peers | Will use findings to design campaigns and app features |

---

## Prepare — Data Sources & Credibility

### Data Source

This analysis uses the **FitBit Fitness Tracker Data** dataset, made available by Möbius on Kaggle under a CC0 Public Domain license. The dataset contains personal fitness tracker data from 33 Fitbit users who consented to share their minute-level data on physical activity, heart rate, and sleep monitoring.

| Attribute | Detail |
|---|---|
| Source | Möbius via Kaggle |
| License | CC0 Public Domain |
| Period | April 12 – May 12, 2016 (31 days) |
| Users | 33 participants (24 with sleep data, 8 with weight data) |
| Files used | dailyActivity_merged.csv, hourlySteps_merged.csv, sleepDay_merged.csv, weightLogInfo_merged.csv |

### Data Structure

Four files were used in this analysis:

- **dailyActivity_merged.csv** — daily totals per user: steps, distance, active minutes by intensity, calories (940 rows, 33 users)
- **hourlySteps_merged.csv** — step count per hour per user (22,099 rows, 33 users)
- **sleepDay_merged.csv** — total minutes asleep and time in bed per sleep session (413 rows, 24 users)
- **weightLogInfo_merged.csv** — weight, BMI, and logging method (67 rows, 8 users)

### Credibility Assessment (ROCCC)

| Criterion | Assessment |
|---|---|
| **Reliable** | ⚠️ Small sample — only 33 users. Results are directional, not statistically representative |
| **Original** | Third-party data collected via a survey on Amazon Mechanical Turk, not by Bellabeat |
| **Comprehensive** | Limited — no demographic data; gender, age, and location are unknown |
| **Current** | ⚠️ Data from 2016 — nearly 10 years old. Wearable usage patterns have evolved significantly |
| **Cited** | Properly attributed to Möbius under CC0 license |

### Acknowledged Limitations

These limitations are documented transparently, as the course requires:

- **Sample size:** 33 users is too small to generalize with statistical confidence
- **No demographics:** It is unknown whether participants are women — a critical gap given Bellabeat's target audience
- **Date range:** 31 days is insufficient to capture seasonal variation in activity or sleep
- **Self-selection bias:** Participants opted in, likely skewing toward more health-conscious users
- **Data age:** 2016 behavior may not reflect how users engage with modern wearables

Despite these limitations, the dataset surfaces behavioral patterns consistent with broader wellness research and is sufficient to generate directional marketing recommendations.

---

## Process — Data Cleaning & Transformation

### Tools

This analysis uses a **Python + SQL hybrid approach**:

- **Python (pandas)** — data loading, cleaning, date parsing, and feature engineering
- **SQL (sqlite3)** — all analytical aggregations and cross-table queries
- **matplotlib / seaborn** — data visualization

Using SQL for the analysis layer demonstrates reproducibility and allows the queries to be ported to any SQL environment (PostgreSQL, BigQuery, etc.) without modification.

### Cleaning Steps

| Dataset | Issue | Action |
|---|---|---|
| sleepDay | 3 duplicate rows | Removed — exact duplicates across all columns |
| dailyActivity | 77 days with 0 steps | Flagged as `non_wear_day = True`; excluded from activity averages |
| weightLogInfo | 65/67 null values in `Fat` column | Column dropped — insufficient data for analysis |
| All files | Date columns stored as strings | Parsed to datetime using pandas |

**Total rows after cleaning:**

| Table | Raw | Clean |
|---|---|---|
| daily_activity | 940 | 940 (77 flagged, not removed) |
| hourly_steps | 22,099 | 22,099 |
| sleep_day | 413 | 410 |
| weight_log | 67 | 67 (Fat column dropped) |

### Feature Engineering

New columns derived from the raw data:

| Column | Source | Description |
|---|---|---|
| `non_wear_day` | `TotalSteps == 0` | Boolean flag for days the device was not worn |
| `total_active_min` | Sum of Very + Fairly + Lightly active minutes | Total non-sedentary minutes |
| `sedentary_pct` | `SedentaryMinutes / total daily minutes` | Share of day spent sedentary |
| `meets_step_goal` | `TotalSteps >= 10000` | Boolean flag vs. WHO recommendation |
| `sleep_efficiency` | `TotalMinutesAsleep / TotalTimeInBed * 100` | Percentage of time in bed actually spent asleep |
| `hours_asleep` | `TotalMinutesAsleep / 60` | Sleep duration in hours |
| `hour` | `ActivityHour` | Hour of day extracted for temporal analysis |
| `day_of_week` / `dow_num` | `ActivityDate` | Day name and number for weekly pattern analysis |
| `log_type` | `IsManualReport` | Whether weight was logged manually or automatically |

### Database

All cleaned tables were stored in a local SQLite database (`bellabeat.db`) to enable SQL-based analysis across all four datasets, including joins between daily activity and sleep data.

---

## Analyze — Key Findings

All aggregations in this section were performed using SQL queries against the `bellabeat.db` SQLite database.

### Finding 1: Most Users Fall Short of Basic Activity Targets

The average user logged 8,319 steps per day — below the widely cited WHO recommendation of 10,000 steps. Only **35.1% of tracked days** met the 10,000-step goal. When users are segmented by their average daily steps, nearly half (48.5%) fall into sedentary or low-active categories:

| Segment | Avg Steps | Users | Share |
|---|---|---|---|
| Sedentary | < 5,000 | 7 | 21.2% |
| Low Active | 5,000–7,500 | 9 | 27.3% |
| Somewhat Active | 7,500–10,000 | 10 | 30.3% |
| Active | 10,000+ | 7 | 21.2% |

This suggests that the majority of smart device users are not meeting basic health movement targets — even though they are actively wearing and using a fitness tracker.

### Finding 2: Sedentary Time Dominates the Day

On average, users spent **955 minutes (nearly 16 hours) sedentary per day** — representing 78.2% of their tracked time. Active minutes break down as follows:

- Very Active: 23 min/day
- Fairly Active: 15 min/day
- Lightly Active: 210 min/day

Even among users who met their step goal, sedentary time remained high. Long periods of inactivity are a recognized health risk independent of total daily step count.

### Finding 3: Activity Peaks on Tuesday and Saturday — Dips on Sunday

Weekly patterns show that Tuesday and Saturday are the most active days by average steps (8,949 and 8,947 respectively), while Sunday is consistently the least active (7,627 steps) and the most sedentary. This suggests users are motivated to be active mid-week and on Saturday mornings, but disengage on Sundays.

### Finding 4: More Than Half of Users Are Sleep-Deprived

Among the 24 users with sleep data, the average nightly sleep was **6.99 hours** — barely at the lower bound of the recommended 7–9 hours. More significantly, **54% of users averaged less than 7 hours of sleep per night**:

| Segment | Users |
|---|---|
| Insufficient (< 6 hrs) | 8 (33%) |
| Below recommended (6–7 hrs) | 5 (21%) |
| Recommended (7–9 hrs) | 10 (42%) |
| Over 9 hrs | 1 (4%) |

Average sleep efficiency was 91.6%, meaning users spent approximately 46 minutes in bed each night without sleeping — a potential signal of poor sleep quality or inconsistent bedtime routines.

### Finding 5: Activity and Sleep Are Related

A JOIN between daily activity and sleep records shows that users who are more physically active tend to sleep closer to the recommended 7-hour threshold, while the most sedentary users also tend to have the shortest or least efficient sleep. This directional relationship — though not statistically confirmable at this sample size — is consistent with established sleep research and relevant for Bellabeat's wellness positioning.

### Finding 6: Activity Concentrates Between 8 AM and 7 PM

Hourly step data shows that nearly all movement occurs between 8 AM and 7 PM, with notable peaks around **12 PM (lunch)** and **5–6 PM (after work)**. Early morning (before 7 AM) and late evening (after 8 PM) are almost completely inactive — periods where a wellness app could add the most behavioral value through timely prompts and goal reminders.

---

## Share — Visualizations & Insights

All visualizations were produced in Python using matplotlib and seaborn, with a consistent color palette: teal for positive/active metrics, coral for negative/sedentary metrics, purple for sleep, and gold for intermediate states.

---

**Figure 1 — User Activity Segments**
Bar chart segmenting 33 users by average daily steps. Nearly half fall in the sedentary or low-active range — a key audience for Bellabeat's motivational features.

---

**Figure 2 — Daily Step Goal Achievement**
Donut chart showing that 64.9% of tracked days fall below the 10,000-step goal. Reinforces Finding 1 with a visually immediate message.

---

**Figure 3 — Steps and Sedentary Time by Day of Week**
Dual-axis chart combining average steps (bars) and sedentary minutes (line) by day. Tuesday and Saturday peak in activity; Sunday dips in both dimensions.

---

**Figure 4 — Daily Time Distribution**
Pie chart showing how the average day is divided across activity levels. The 78% sedentary slice is the chart's dominant message and the most compelling finding for marketing purposes.

---

**Figure 5 — Sleep Duration Distribution**
Histogram of average nightly sleep per user, with reference lines for the recommended 7–9 hours and the group mean (6.99 hrs). Visually shows the cluster of users below the 7-hour threshold.

---

**Figure 6 — Daily Steps vs. Sleep Duration**
Scatter plot per user, with color encoding sedentary minutes. Shows the directional relationship between higher activity, lower sedentary time, and sleep duration closer to the recommended range.

---

**Figure 7 — Hourly Steps Heatmap**
Heatmap of average steps by hour and day of week. Clearly shows the activity windows (8 AM–7 PM) and the dead zones (early morning, late evening) where app engagement could have the highest impact.

---

## Act — Recommendations

Based on the analysis of FitBit tracker data, three marketing recommendations are proposed for the **Bellabeat App**.

---

**Recommendation 1: Position the App as a Sedentary Behavior Coach**

The most consistent finding across the dataset is not a lack of exercise — it is an excess of sedentary time. Users average nearly 16 hours of inactivity per day, even when they are wearing a fitness tracker. This is a behavioral gap that a wellness app is uniquely positioned to address.

*Recommended action:* Market the Bellabeat App around the concept of **breaking sedentary patterns**, not just hitting step counts. Campaigns should emphasize smart inactivity alerts — personalized reminders to move during prolonged sitting periods, timed to the user's schedule. This differentiates Bellabeat from step-counting wearables and speaks to a real, data-confirmed problem. Messaging could anchor on the insight: *"Most fitness trackers tell you how much you moved. Bellabeat tells you when to move."*

---

**Recommendation 2: Make Sleep a Primary Feature, Not a Secondary Metric**

Over half of tracked users average less than 7 hours of sleep per night. Sleep deprivation is a recognized driver of poor physical health, impaired cognitive function, and increased stress — all areas within Bellabeat's wellness positioning. Yet most fitness app marketing focuses on activity metrics rather than sleep.

*Recommended action:* Elevate sleep tracking as a **hero feature** in the Bellabeat App's marketing. Campaigns should communicate that consistent, quality sleep is foundational to the wellness outcomes users care about — energy, mood, and physical performance. In-app features should include a personalized sleep score, bedtime reminders keyed to the user's typical schedule, and weekly sleep trend reports. The data shows users already track sleep inconsistently (only 24 of 33 users have sleep records) — reducing friction in sleep logging is itself a product and marketing opportunity.

---

**Recommendation 3: Design Engagement Campaigns Around Peak Activity Windows**

The hourly heatmap reveals that user activity concentrates in two windows: **midday (12 PM)** and **late afternoon (5–6 PM)**. Early mornings and evenings are nearly inactive. Sunday is consistently the weakest day of the week.

*Recommended action:* Time app notifications, challenges, and content delivery to align with these natural engagement windows. Midday push notifications ("You're halfway through your day — here's where you stand") and end-of-workday movement prompts have the highest probability of reaching users when they are already in a behavioral mindset to act. Additionally, a **Sunday reset feature** — a weekly summary delivered Sunday morning with goals for the coming week — could address the Sunday disengagement pattern and prime users for a stronger Monday start.

---

*This case study was completed as part of the Google Data Analytics Professional Certificate. FitBit data provided by Möbius via Kaggle under CC0 public domain license.*
