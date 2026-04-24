# =============================================================================
# Bellabeat Smart Device Analysis
# Google Data Analytics Professional Certificate — Capstone Case Study
#
# Business Question: What trends in smart device usage can inform
#                    Bellabeat's marketing strategy?
#
# Author : Giacomo
# Date   : April 2026
# Tools  : Python 3.12 | pandas | sqlite3 | matplotlib | seaborn
# Data   : FitBit Fitness Tracker Data (Möbius, Kaggle)
#          https://www.kaggle.com/datasets/arashnic/fitbit
#          License: CC0 Public Domain
# =============================================================================

import os
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

# -----------------------------------------------------------------------------
# CONFIGURATION
# -----------------------------------------------------------------------------
# If running in Jupyter Notebook or Google Colab, uncomment the next line:
# %matplotlib inline

# --- PATH SETUP ---
# Option A (recommended): set BASE to your folder containing the CSV files.
#   The script will create 'processed/' and 'charts/' subfolders there.
# Option B: leave BASE = None and the script uses relative paths (data/raw/).
#   Use Option B only if your notebook is in the project root folder.

BASE = r'C:\Users\giaco\Downloads\Data fitbit\mturkfitbit_export_4.12.16-5.12.16\Fitabase Data 4.12.16-5.12.16'

if BASE:
    DATA_DIR   = BASE + '\\'
    OUTPUT_DIR = BASE + '\\processed\\'
    CHARTS_DIR = BASE + '\\charts\\'
else:
    DATA_DIR   = 'data/raw/'
    OUTPUT_DIR = 'data/processed/'
    CHARTS_DIR = 'charts/'

DB_PATH = OUTPUT_DIR + 'bellabeat.db'

for folder in [OUTPUT_DIR, CHARTS_DIR]:
    os.makedirs(folder, exist_ok=True)

print(f"DATA_DIR   : {DATA_DIR}")
print(f"OUTPUT_DIR : {OUTPUT_DIR}")
print(f"CHARTS_DIR : {CHARTS_DIR}")
print(f"Files found: {[f for f in os.listdir(DATA_DIR) if f.endswith('.csv')]}")

TEAL   = '#00B4A6'
CORAL  = '#FF6B6B'
PURPLE = '#7B5EA7'
GOLD   = '#F4A300'

plt.rcParams.update({
    'font.family'      : 'DejaVu Sans',
    'axes.spines.top'  : False,
    'axes.spines.right': False,
    'axes.grid'        : True,
    'axes.grid.axis'   : 'y',
    'grid.alpha'       : 0.3,
})

def save_chart(name):
    """Save chart to CHARTS_DIR and display inline in notebook."""
    plt.tight_layout()
    plt.savefig(f'{CHARTS_DIR}{name}.png', dpi=120, bbox_inches='tight')
    plt.show()
    plt.close()
    print(f'  Saved: {name}.png')


# =============================================================================
# PHASE 1 — PREPARE
# Load and validate the raw data
# =============================================================================

print("=" * 60)
print("PHASE 1 — PREPARE")
print("=" * 60)

daily  = pd.read_csv(DATA_DIR + 'dailyActivity_merged.csv')
hourly = pd.read_csv(DATA_DIR + 'hourlySteps_merged.csv')
sleep  = pd.read_csv(DATA_DIR + 'sleepDay_merged.csv')
weight = pd.read_csv(DATA_DIR + 'weightLogInfo_merged.csv')

print(f"daily_activity : {daily.shape}  | {daily['Id'].nunique()} users")
print(f"hourly_steps   : {hourly.shape} | {hourly['Id'].nunique()} users")
print(f"sleep_day      : {sleep.shape}  | {sleep['Id'].nunique()} users")
print(f"weight_log     : {weight.shape} | {weight['Id'].nunique()} users")

# Schema check
print("\n--- daily_activity columns ---")
print(daily.columns.tolist())

# Null check
print("\n--- Null counts ---")
for name, df in [('daily', daily), ('hourly', hourly),
                 ('sleep', sleep), ('weight', weight)]:
    nulls = df.isnull().sum().sum()
    print(f"  {name}: {nulls} total nulls")

# Duplicate check
print("\n--- Duplicate rows ---")
for name, df in [('daily', daily), ('hourly', hourly),
                 ('sleep', sleep), ('weight', weight)]:
    dups = df.duplicated().sum()
    print(f"  {name}: {dups} duplicates")


# =============================================================================
# PHASE 2 — PROCESS
# Clean data, engineer features, and load into SQLite
# =============================================================================

print("\n" + "=" * 60)
print("PHASE 2 — PROCESS")
print("=" * 60)

# --- Parse dates ---
# Use explicit format to avoid pandas inference warnings
daily['ActivityDate']  = pd.to_datetime(daily['ActivityDate'],  format='mixed')
hourly['ActivityHour'] = pd.to_datetime(hourly['ActivityHour'], format='mixed')
sleep['SleepDay']      = pd.to_datetime(sleep['SleepDay'],      format='mixed')
weight['Date']         = pd.to_datetime(weight['Date'],         format='mixed')

# --- Sleep: remove 3 exact duplicates ---
before = len(sleep)
sleep = sleep.drop_duplicates()
print(f"Sleep duplicates removed: {before - len(sleep)}")

# --- Weight: drop Fat column (65/67 nulls — unusable) ---
weight = weight.drop(columns=['Fat'])
print("Dropped 'Fat' column from weight_log (97% null)")

# --- Daily: flag zero-step days (device not worn) ---
# Kept in dataset but excluded from activity aggregations
daily['non_wear_day'] = daily['TotalSteps'] == 0
print(f"Non-wear days flagged: {daily['non_wear_day'].sum()} of {len(daily)}")

# --- Feature engineering: daily_activity ---
daily['day_of_week']     = daily['ActivityDate'].dt.strftime('%a')
daily['dow_num']         = daily['ActivityDate'].dt.dayofweek   # 0 = Monday
daily['week_num']        = daily['ActivityDate'].dt.isocalendar().week.astype(int)
daily['is_weekend']      = daily['dow_num'].isin([5, 6])
daily['total_active_min'] = (
    daily['VeryActiveMinutes'] +
    daily['FairlyActiveMinutes'] +
    daily['LightlyActiveMinutes']
)
daily['sedentary_pct']   = (
    daily['SedentaryMinutes'] /
    (daily['SedentaryMinutes'] + daily['total_active_min']) * 100
).round(1)
# WHO recommendation threshold
daily['meets_step_goal'] = daily['TotalSteps'] >= 10000

# --- Feature engineering: sleep_day ---
sleep['sleep_efficiency'] = (
    sleep['TotalMinutesAsleep'] / sleep['TotalTimeInBed'] * 100
).round(1)
sleep['hours_asleep'] = (sleep['TotalMinutesAsleep'] / 60).round(2)
sleep['date']         = sleep['SleepDay'].dt.date

# --- Feature engineering: hourly_steps ---
hourly['hour']     = hourly['ActivityHour'].dt.hour
hourly['date']     = hourly['ActivityHour'].dt.date
hourly['day_name'] = hourly['ActivityHour'].dt.strftime('%a')

# --- Feature engineering: weight_log ---
weight['log_type'] = weight['IsManualReport'].map(
    {True: 'Manual', False: 'Automatic'}
)

print("\nDatasets after cleaning:")
print(f"  daily_activity : {len(daily):,} rows")
print(f"  hourly_steps   : {len(hourly):,} rows")
print(f"  sleep_day      : {len(sleep):,} rows")
print(f"  weight_log     : {len(weight):,} rows")

# --- Load into SQLite database ---
conn = sqlite3.connect(DB_PATH)
daily.to_sql('daily_activity', conn, if_exists='replace', index=False)
hourly.to_sql('hourly_steps',  conn, if_exists='replace', index=False)
sleep.to_sql('sleep_day',      conn, if_exists='replace', index=False)
weight.to_sql('weight_log',    conn, if_exists='replace', index=False)
print(f"\nSaved to SQLite: {DB_PATH}")
print("Tables: daily_activity, hourly_steps, sleep_day, weight_log")


# =============================================================================
# PHASE 3 — ANALYZE
# SQL queries for all key findings
# =============================================================================

print("\n" + "=" * 60)
print("PHASE 3 — ANALYZE (SQL)")
print("=" * 60)

# --- Q1: Overall activity averages (excluding non-wear days) ---
q1 = pd.read_sql('''
    SELECT
        ROUND(AVG(TotalSteps), 0)           AS avg_steps,
        ROUND(AVG(Calories), 0)             AS avg_calories,
        ROUND(AVG(VeryActiveMinutes), 1)    AS avg_very_active_min,
        ROUND(AVG(FairlyActiveMinutes), 1)  AS avg_fairly_active_min,
        ROUND(AVG(LightlyActiveMinutes), 1) AS avg_lightly_active_min,
        ROUND(AVG(SedentaryMinutes), 1)     AS avg_sedentary_min,
        ROUND(AVG(sedentary_pct), 1)        AS avg_sedentary_pct
    FROM daily_activity
    WHERE non_wear_day = 0
''', conn)
print("\n--- Q1: Activity averages ---")
print(q1.to_string(index=False))

# --- Q2: Step goal achievement ---
q2 = pd.read_sql('''
    SELECT
        meets_step_goal,
        COUNT(*) AS days,
        ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 1) AS pct
    FROM daily_activity
    WHERE non_wear_day = 0
    GROUP BY meets_step_goal
''', conn)
print("\n--- Q2: Step goal achievement ---")
print(q2.to_string(index=False))

# --- Q3: User activity segments ---
q3 = pd.read_sql('''
    SELECT
        CASE
            WHEN avg_steps < 5000  THEN '1. Sedentary (<5K steps)'
            WHEN avg_steps < 7500  THEN '2. Low Active (5K-7.5K)'
            WHEN avg_steps < 10000 THEN '3. Somewhat Active (7.5K-10K)'
            ELSE                        '4. Active (10K+)'
        END AS segment,
        COUNT(*) AS users,
        ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 1) AS pct_users
    FROM (
        SELECT Id, AVG(TotalSteps) AS avg_steps
        FROM daily_activity
        WHERE non_wear_day = 0
        GROUP BY Id
    )
    GROUP BY segment
    ORDER BY segment
''', conn)
print("\n--- Q3: User segments ---")
print(q3.to_string(index=False))

# --- Q4: Activity by day of week ---
q4 = pd.read_sql('''
    SELECT
        day_of_week,
        dow_num,
        ROUND(AVG(TotalSteps), 0)        AS avg_steps,
        ROUND(AVG(total_active_min), 1)  AS avg_active_min,
        ROUND(AVG(SedentaryMinutes), 1)  AS avg_sedentary_min
    FROM daily_activity
    WHERE non_wear_day = 0
    GROUP BY day_of_week, dow_num
    ORDER BY dow_num
''', conn)
print("\n--- Q4: Activity by day of week ---")
print(q4.to_string(index=False))

# --- Q5: Sleep summary ---
q5 = pd.read_sql('''
    SELECT
        ROUND(AVG(hours_asleep), 2)        AS avg_hours_asleep,
        ROUND(AVG(TotalTimeInBed)/60.0, 2) AS avg_hours_in_bed,
        ROUND(AVG(sleep_efficiency), 1)    AS avg_sleep_efficiency_pct,
        COUNT(DISTINCT Id)                 AS users_tracked
    FROM sleep_day
''', conn)
print("\n--- Q5: Sleep summary ---")
print(q5.to_string(index=False))

# --- Q6: Sleep quality segments ---
q6 = pd.read_sql('''
    SELECT
        CASE
            WHEN avg_hrs < 6 THEN '1. Insufficient (<6 hrs)'
            WHEN avg_hrs < 7 THEN '2. Below recommended (6-7 hrs)'
            WHEN avg_hrs < 9 THEN '3. Recommended (7-9 hrs)'
            ELSE                  '4. Over 9 hrs'
        END AS sleep_segment,
        COUNT(*) AS users
    FROM (
        SELECT Id, AVG(hours_asleep) AS avg_hrs
        FROM sleep_day
        GROUP BY Id
    )
    GROUP BY sleep_segment
    ORDER BY sleep_segment
''', conn)
print("\n--- Q6: Sleep segments ---")
print(q6.to_string(index=False))

# --- Q7: Activity vs. sleep (joined) ---
q7 = pd.read_sql('''
    SELECT
        d.Id,
        AVG(d.TotalSteps)        AS avg_steps,
        AVG(s.hours_asleep)      AS avg_sleep_hrs,
        AVG(d.SedentaryMinutes)  AS avg_sedentary_min
    FROM daily_activity d
    JOIN sleep_day s
        ON d.Id = s.Id
        AND DATE(d.ActivityDate) = DATE(s.SleepDay)
    WHERE d.non_wear_day = 0
    GROUP BY d.Id
''', conn)
print("\n--- Q7: Per-user activity vs. sleep (joined) ---")
print(q7.describe().round(1).to_string())

# --- Q8: Hourly steps by hour and day ---
q8 = pd.read_sql('''
    SELECT
        hour,
        day_name,
        CAST(strftime('%w', date) AS INTEGER) AS dow_num,
        AVG(StepTotal) AS avg_steps
    FROM hourly_steps
    GROUP BY hour, day_name, dow_num
    ORDER BY dow_num, hour
''', conn)
print("\n--- Q8: Hourly steps aggregated ---")
print(f"  Rows: {len(q8)} (7 days x 24 hours)")


# =============================================================================
# PHASE 4 — SHARE
# Generate and export all visualizations
# =============================================================================

print("\n" + "=" * 60)
print("PHASE 4 — SHARE")
print("=" * 60)

# --- Figure 1: User activity segments ---
seg = pd.read_sql('''
    SELECT
        CASE
            WHEN avg_steps < 5000  THEN 'Sedentary\n(<5K)'
            WHEN avg_steps < 7500  THEN 'Low Active\n(5K-7.5K)'
            WHEN avg_steps < 10000 THEN 'Somewhat Active\n(7.5K-10K)'
            ELSE                        'Active\n(10K+)'
        END AS segment,
        COUNT(*) AS users
    FROM (SELECT Id, AVG(TotalSteps) AS avg_steps
          FROM daily_activity WHERE non_wear_day = 0 GROUP BY Id)
    GROUP BY segment ORDER BY MIN(avg_steps)
''', conn)

fig, ax = plt.subplots(figsize=(9, 5))
colors = [CORAL, GOLD, TEAL, PURPLE]
bars = ax.bar(seg['segment'], seg['users'], color=colors, alpha=0.9, width=0.5)
for bar, val in zip(bars, seg['users']):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
            f'{val} users\n({val/33*100:.0f}%)',
            ha='center', fontsize=11, fontweight='bold')
ax.set_ylabel('Number of Users', fontsize=12)
ax.set_title('User Activity Segments\nBased on Average Daily Steps',
             fontsize=15, fontweight='bold')
ax.set_ylim(0, 14)
save_chart('01_activity_segments')

# --- Figure 2: Step goal achievement (donut) ---
goal = pd.read_sql('''
    SELECT meets_step_goal, COUNT(*) AS days
    FROM daily_activity WHERE non_wear_day = 0
    GROUP BY meets_step_goal
''', conn)

fig, ax = plt.subplots(figsize=(6, 6))
wedges, texts, autotexts = ax.pie(
    goal['days'],
    labels=['Below 10K\nsteps', 'Meets 10K\ngoal'],
    colors=[CORAL, TEAL],
    autopct='%1.1f%%', startangle=90,
    wedgeprops={'width': 0.55, 'edgecolor': 'white', 'linewidth': 2},
    textprops={'fontsize': 12}
)
for at in autotexts:
    at.set_fontsize(13); at.set_fontweight('bold'); at.set_color('white')
ax.set_title('Daily Step Goal Achievement\n(WHO recommendation: 10,000 steps)',
             fontsize=14, fontweight='bold', pad=20)
ax.text(0, 0, f'{goal["days"].sum()}\ndays',
        ha='center', va='center', fontsize=13, fontweight='bold', color='#333')
save_chart('02_step_goal')

# --- Figure 3: Activity by day of week (dual axis) ---
dow = q4.copy()
fig, ax1 = plt.subplots(figsize=(10, 5))
ax2 = ax1.twinx()
ax1.bar(dow['day_of_week'], dow['avg_steps'],
        color=TEAL, alpha=0.8, width=0.5, label='Avg Steps')
ax2.plot(dow['day_of_week'], dow['avg_sedentary_min'],
         color=CORAL, marker='o', linewidth=2.5, markersize=8,
         label='Avg Sedentary Min')
ax1.set_ylabel('Average Steps', fontsize=12, color=TEAL)
ax2.set_ylabel('Avg Sedentary Minutes', fontsize=12, color=CORAL)
ax1.tick_params(axis='y', labelcolor=TEAL)
ax2.tick_params(axis='y', labelcolor=CORAL)
ax1.set_title('Steps and Sedentary Time by Day of Week',
              fontsize=15, fontweight='bold')
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, fontsize=11, loc='lower right')
ax2.grid(False)
save_chart('03_activity_by_dow')

# --- Figure 4: Daily time distribution (pie) ---
time_dist = pd.read_sql('''
    SELECT
        ROUND(AVG(VeryActiveMinutes), 1)    AS very_active,
        ROUND(AVG(FairlyActiveMinutes), 1)  AS fairly_active,
        ROUND(AVG(LightlyActiveMinutes), 1) AS lightly_active,
        ROUND(AVG(SedentaryMinutes), 1)     AS sedentary
    FROM daily_activity WHERE non_wear_day = 0
''', conn)

labels_t = ['Sedentary\n(~16 hrs)', 'Lightly Active\n(~3.5 hrs)',
            'Fairly Active\n(~15 min)', 'Very Active\n(~23 min)']
values_t = [
    time_dist['sedentary'].values[0],
    time_dist['lightly_active'].values[0],
    time_dist['fairly_active'].values[0],
    time_dist['very_active'].values[0]
]

fig, ax = plt.subplots(figsize=(8, 6))
wedges, texts, autotexts = ax.pie(
    values_t, labels=labels_t,
    colors=[CORAL, GOLD, TEAL, PURPLE],
    autopct=lambda p: f'{p:.1f}%\n({p*1440/100:.0f} min)',
    startangle=90,
    wedgeprops={'edgecolor': 'white', 'linewidth': 2},
    textprops={'fontsize': 10}
)
for at in autotexts:
    at.set_fontsize(9); at.set_color('white'); at.set_fontweight('bold')
ax.set_title('Average Daily Time Distribution\n(minutes per activity level)',
             fontsize=14, fontweight='bold', pad=15)
save_chart('04_time_distribution')

# --- Figure 5: Sleep duration distribution ---
sleep_dist = pd.read_sql('''
    SELECT Id, AVG(hours_asleep) AS avg_hrs
    FROM sleep_day GROUP BY Id
''', conn)

fig, ax = plt.subplots(figsize=(9, 5))
ax.hist(sleep_dist['avg_hrs'], bins=10, color=PURPLE, alpha=0.85, edgecolor='white')
ax.axvline(7, color=TEAL, linewidth=2.5, linestyle='--', label='Min recommended (7 hrs)')
ax.axvline(9, color=TEAL, linewidth=2.5, linestyle=':',  label='Max recommended (9 hrs)')
ax.axvline(sleep_dist['avg_hrs'].mean(), color=CORAL, linewidth=2.5,
           label=f'Mean: {sleep_dist["avg_hrs"].mean():.1f} hrs')
ax.set_xlabel('Average Hours Asleep', fontsize=12)
ax.set_ylabel('Number of Users', fontsize=12)
ax.set_title('Distribution of Average Sleep Duration\n(24 users tracked)',
             fontsize=14, fontweight='bold')
ax.legend(fontsize=11)
save_chart('05_sleep_distribution')

# --- Figure 6: Steps vs. sleep scatter ---
fig, ax = plt.subplots(figsize=(9, 5))
scatter = ax.scatter(
    q7['avg_steps'], q7['avg_sleep_hrs'],
    c=q7['avg_sedentary_min'], cmap='RdYlGn_r',
    s=120, alpha=0.85, edgecolors='white', linewidth=1
)
cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label('Avg Sedentary Minutes', fontsize=10)
ax.axhline(7, color=PURPLE, linewidth=1.5, linestyle='--',
           alpha=0.6, label='7 hrs sleep')
ax.axvline(10000, color=TEAL, linewidth=1.5, linestyle='--',
           alpha=0.6, label='10K steps')
ax.set_xlabel('Average Daily Steps', fontsize=12)
ax.set_ylabel('Average Hours Asleep', fontsize=12)
ax.set_title('Daily Steps vs. Sleep Duration\n(color = sedentary minutes per user)',
             fontsize=14, fontweight='bold')
ax.legend(fontsize=10)
save_chart('06_steps_vs_sleep')

# --- Figure 7: Hourly steps heatmap ---
dow_order = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
pivot = q8.pivot_table(
    index='day_name', columns='hour', values='avg_steps'
).reindex(dow_order)

fig, ax = plt.subplots(figsize=(14, 5))
sns.heatmap(pivot, cmap='YlOrRd', ax=ax, linewidths=0.3,
            cbar_kws={'label': 'Avg Steps'}, fmt='.0f')
ax.set_xlabel('Hour of Day', fontsize=12)
ax.set_ylabel('')
ax.set_title('Average Steps by Hour and Day of Week',
             fontsize=14, fontweight='bold')
save_chart('07_hourly_heatmap')

conn.close()
print("\nAnalysis complete.")
