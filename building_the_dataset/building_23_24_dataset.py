# Filename: building_23_24_dataset.py
# Author: Adam Silver
# Date: 2026-03-17
# Description: Cleans the 2023-24 season data and appends it to the
#              existing dataset so predictive_modeling.py can use it.

import pandas as pd

# load the existing processed dataset
data = pd.read_csv(
    "C:/Users/Ilike/OneDrive/Year 3/Personal Projects/Western Conference Dominance/data/processed/updated_dataset.csv"
)

# load the 2023-24 season data
new = pd.read_csv(
    "C:/Users/Ilike/OneDrive/Year 3/Personal Projects/Western Conference Dominance/data/raw/nba_2024_scraped_.csv"
)

# conference mapping — assign each team to East or West
conference_map = {
    "Atlanta Hawks": "East", "Boston Celtics": "East", "Brooklyn Nets": "East",
    "Charlotte Hornets": "East", "Chicago Bulls": "East", "Cleveland Cavaliers": "East",
    "Detroit Pistons": "East", "Indiana Pacers": "East", "Miami Heat": "East",
    "Milwaukee Bucks": "East", "New York Knicks": "East", "Orlando Magic": "East",
    "Philadelphia 76ers": "East", "Toronto Raptors": "East", "Washington Wizards": "East",
    "Dallas Mavericks": "West", "Denver Nuggets": "West", "Golden State Warriors": "West",
    "Houston Rockets": "West", "Los Angeles Clippers": "West", "Los Angeles Lakers": "West",
    "Memphis Grizzlies": "West", "Minnesota Timberwolves": "West", "New Orleans Pelicans": "West",
    "Oklahoma City Thunder": "West", "Phoenix Suns": "West", "Portland Trail Blazers": "West",
    "Sacramento Kings": "West", "San Antonio Spurs": "West", "Utah Jazz": "West",
}

# rename columns to match the existing dataset
new = new.rename(columns={
    "Team":  "TEAM_NAME",
    "FG":    "FGM",
    "3P":    "FG3M",
    "3PA":   "FG3A",
    "FT":    "FTM",
    "ORB":   "OREB",
    "DRB":   "DREB",
})

# add Season and Conference columns
new["Season"]     = 2024
new["Conference"] = new["TEAM_NAME"].map(conference_map)

# add any missing columns that exist in the main dataset, filled with None
# this covers rank columns, PLUS_MINUS, etc. that aren't in the 2023-24 source
# these columns are not used in modeling so None values are fine
for col in data.columns:
    if col not in new.columns:
        new[col] = None

# reorder columns to match the main dataset exactly
new = new[data.columns]

# append and save
combined = pd.concat([data, new], ignore_index=True)
combined.to_csv(
    "C:/Users/Ilike/OneDrive/Year 3/Personal Projects/Western Conference Dominance"
    "/data/processed/updated_dataset.csv",
    index=False
)

print(f"Done. Dataset now has {len(combined)} rows.")
print(f"Seasons: {sorted(combined['Season'].unique())}")