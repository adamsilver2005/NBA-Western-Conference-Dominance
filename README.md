# NBA Western Conference Dominance Analysis 

This Project analyzes NBA team statistics from the 1996-97 season to the 2022-23 season.

The dataset used for this project was sourced from Kaggle: [Dataset on Kaggle] (https://www.kaggle.com/datasets/mamadoudiallo/nba-team-stats?resource=download)

This data set has been altered in the fact that I have added a column for the season (which was not included in the original dataset), and I have also added a column for the conference (which was not included in the original dataset). There are quite a few inconsistences with team names (since they have changed a bit throughout the years), and also the NBA expanded from 29 to 30 teams in 2005, so I used a dictionary for the team names to add the conference column. 

I used python to build the data set using the package "pandas".