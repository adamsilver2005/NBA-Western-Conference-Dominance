# Filename: build_dataset.py
# Author: Adam Silver
# Date: 2026-02-22
# Description: Cleans and prepares the original Kaggle dataset, adds Season
#              and Conference columns, and saves the processed dataset.


import pandas as pd


raw_dataset = pd.read_csv("C:/Users/Ilike/OneDrive/Year 3/Personal Projects/Western Conference Dominance/data/raw/nba_team_stats.csv")


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


# updated_dataset.to_csv("updated_dataset.csv", index=False)






# webscrapping the 2023-2024 win and losses for each team for the predictive model to compare

# get the website 

url = "https://www.basketball-reference.com/leagues/NBA_2024.html"

tables = pd.read_html(url)



# print out all of the tables first few rows to see whic one we need

for i, table in enumerate(tables):
    print(i)
    print(table.head())



# we need the first and second table 
team_stats_2024 = tables[4]

# check to make sure
print("check:", team_stats_2024)




# Remove repeated header rows
team_stats_2024 = team_stats_2024[team_stats_2024["Team"] != "Team"]

# Rename columns to match my dataset
team_stats_2024 = team_stats_2024.rename(columns={
    "TRB": "REB",
    "FG%": "FG_PCT",
    "3P%": "FG3_PCT"
})

# Reset index
team_stats_2024 = team_stats_2024.reset_index(drop=True)






# get the actual standings for the season

# East + West tables
east = tables[0]
west = tables[1]

# Fix column names
east.columns = ["Team", "W", "L", "W_PCT", "GB", "PS_G", "PA_G", "SRS"]
west.columns = ["Team", "W", "L", "W_PCT", "GB", "PS_G", "PA_G", "SRS"]

# Remove header rows inside table
east = east[east["Team"] != "Team"]
west = west[west["Team"] != "Team"]

# Combine
standings = pd.concat([east, west], ignore_index=True)

# Convert numeric columns
standings["W"] = pd.to_numeric(standings["W"])
standings["L"] = pd.to_numeric(standings["L"])
standings["W_PCT"] = pd.to_numeric(standings["W_PCT"])


# some teams include a * for playoff teams which we don't care about
team_stats_2024["Team"] = team_stats_2024["Team"].str.replace("*", "", regex=False)
standings["Team"] = standings["Team"].str.replace("*", "", regex=False)


team_stats_2024 = team_stats_2024.merge(
    standings[["Team", "W", "L", "W_PCT"]],
    on="Team"
)




# make sure it worked
print("team stats 2024:", team_stats_2024.head())

print("team stats 2024 tail:", team_stats_2024.tail())




features = [
    "PTS",
    "REB",
    "AST",
    "FG_PCT",
    "FG3_PCT",
    "TOV",
    "STL",
    "BLK"
]


print(team_stats_2024.columns)
print(features)


# export to csv 
team_stats_2024.to_csv("C:/Users/Ilike/OneDrive/Year 3/Personal Projects/Western Conference Dominance/data/raw/nba_2024_scraped_.csv", index=False)


