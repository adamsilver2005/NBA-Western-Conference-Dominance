# NBA Western Conference Dominance Analysis 

This Project analyzes NBA team statistics from the 1996-97 season to the 2022-23 season.

The dataset used for this project was sourced from Kaggle: [Dataset on Kaggle] (https://www.kaggle.com/datasets/mamadoudiallo/nba-team-stats?resource=download)

This data set has been altered in the fact that I have added a column for the season (which was not included in the original dataset), and I have also added a column for the conference (which was not included in the original dataset). There are quite a few inconsistences with team names (since they have changed a bit throughout the years), and also the NBA expanded from 29 to 30 teams in 2005, so I used a dictionary for the team names to add the conference column. 

I used python to build the data set using the package "pandas".


Explanation of each column in the dataset:


| Column | Description |
|--------|-------------|
| Season | NBA season year (ex: 1996-97) |
| Conference | The team's conference (East or West) |
| TEAM_NAME | Name of the NBA team |
| GP | Games played in the season |
| W | Number of wins |
| L | Number of losses |
| W_PCT | Winning percentage (W / GP) |
| MIN | Total minutes played by the team |
| FGM | Field goals made |
| FGA | Field goals attempted |
| FG_PCT | Field goal percentage (FGM / FGA) |
| FG3M | Three-point field goals made |
| FG3A | Three-point field goals attempted |
| FG3_PCT | Three-point field goal percentage (FG3M / FG3A) |
| FTM | Free throws made |
| FTA | Free throws attempted |
| FT_PCT | Free throw percentage (FTM / FTA) |
| OREB | Offensive rebounds |
| DREB | Defensive rebounds |
| REB | Total rebounds (OREB + DREB) |
| AST | Assists |
| TOV | Turnovers |
| STL | Steals |
| BLK | Blocks |
| BLKA | Block attempts |
| PF | Personal fouls |
| PFD | Personal fouls drawn |
| PTS | Total points scored |
| PLUS_MINUS | Team's point differential (points scored minus points allowed) |
| GP_RANK | Rank of team in games played relative to other teams |
| W_RANK | Rank of team in wins relative to other teams |
| L_RANK | Rank of team in losses relative to other teams |
| W_PCT_RANK | Rank of team in winning percentage |
| MIN_RANK | Rank in total minutes played |
| FGM_RANK | Rank in field goals made |
| FGA_RANK | Rank in field goals attempted |
| FG_PCT_RANK | Rank in field goal percentage |
| FG3M_RANK | Rank in three-pointers made |
| FG3A_RANK | Rank in three-pointers attempted |
| FG3_PCT_RANK | Rank in three-point percentage |
| FTM_RANK | Rank in free throws made |
| FTA_RANK | Rank in free throws attempted |
| FT_PCT_RANK | Rank in free throw percentage |
| OREB_RANK | Rank in offensive rebounds |
| DREB_RANK | Rank in defensive rebounds |
| REB_RANK | Rank in total rebounds |
| AST_RANK | Rank in assists |
| TOV_RANK | Rank in turnovers |
| STL_RANK | Rank in steals
