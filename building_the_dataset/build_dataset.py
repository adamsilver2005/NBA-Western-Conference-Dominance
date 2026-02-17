import pandas as pd
import numpy as np

raw_dataset = pd.read_csv("C:/Users/Ilike/OneDrive/Year 3/Personal Projects/Western Conference Dominance/data/nba_team_stats.csv")


# print(raw_dataset.shape)



#print(len(raw_dataset) / 30)

# years in the dataset, need 1996 to 2023 so need to add the +1
years = list(range(1997, 2023 + 1))


# print(years)

# seasons column 
seasons = []


for year in years:

    if year <= 2004:
        teams = 29

    else:
        teams = 30


    for i in range(teams):
        
        seasons.append(year)




updated_dataset = raw_dataset 


updated_dataset["Season"] = seasons

# print(updated_dataset)


# move season column to be the first column
seasons = updated_dataset.pop("Season")

updated_dataset.insert(0, "Season", seasons)



# add a conference column
team_to_conference = {
    # Eastern Conference Teams
    "Atlanta Hawks": "East",
    "Boston Celtics": "East",
    "Brooklyn Nets": "East",
    "Charlotte Hornets": "East",        # original 1988-2002
    "Charlotte Bobcats": "East",       # 2004–2014
    "Chicago Bulls": "East",
    "Cleveland Cavaliers": "East",
    "Detroit Pistons": "East",
    "Indiana Pacers": "East",
    "Miami Heat": "East",
    "Milwaukee Bucks": "East",
    "New Jersey Nets": "East",         # Nets before move
    "New York Knicks": "East",
    "Orlando Magic": "East",
    "Philadelphia 76ers": "East",
    "Toronto Raptors": "East",
    "Washington Bullets": "East",      
    "Washington Wizards": "East",

    # Western Conference Teams
    "Dallas Mavericks": "West",
    "Denver Nuggets": "West",
    "Golden State Warriors": "West",
    "Houston Rockets": "West",
    "LA Clippers": "West",
    "Los Angeles Clippers": "West",
    "Los Angeles Lakers": "West",
    "Memphis Grizzlies": "West",
    "Vancouver Grizzlies": "West",      # added
    "Minnesota Timberwolves": "West",
    "New Orleans Hornets": "West",
    "New Orleans/Oklahoma City Hornets": "West",
    "New Orleans Pelicans": "West",
    "Oklahoma City Thunder": "West",
    "Phoenix Suns": "West",
    "Portland Trail Blazers": "West",
    "Sacramento Kings": "West",
    "San Antonio Spurs": "West",
    "Seattle SuperSonics": "West",
    "Utah Jazz": "West",
    
    # sometimes used variants
    "LA Lakers": "West"
}

updated_dataset["Conference"] = updated_dataset["TEAM_NAME"].map(team_to_conference)

# check for missing mappings
missing = updated_dataset[updated_dataset["Conference"].isna()]["TEAM_NAME"].unique()

if len(missing) > 0:
    print(missing)


# move the new conference column to be the 2nd column (rught after the season column)
conference_column = updated_dataset.pop("Conference")
updated_dataset.insert(1, "Conference", conference_column)


# delete the Unnamed: 0 column
updated_dataset = updated_dataset.drop(columns=["Unnamed: 0"])  

# delete the TEAM_ID column
updated_dataset = updated_dataset.drop(columns=["TEAM_ID"])


updated_dataset.to_csv("updated_dataset.csv", index=False)

