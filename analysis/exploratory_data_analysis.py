# Filename: exploratory_data_analysis.py
# Author: Adam Silver
# Date: 2026-03-09
# Description: 



# import libraries

import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns 


data = pd.read_csv("C:/Users/Ilike/OneDrive/Year 3/Personal Projects/Western Conference Dominance"
                    "/data/processed/updated_dataset.csv")


print(data.head())
print(data.info())



# basic information about dataset (number of rows, number of columns, etc)


print("number of rows:", len(data))
print("number of columns:", len(data.columns))

print("\nColumns:")
print(data.columns)






# basic summary statistics: tells us averages across the league, ranges, and variability 
basic_stats = ["W_PCT", "PTS", "REB", "AST", "FG_PCT", "FG3_PCT", "PLUS_MINUS"]

print(data[basic_stats].describe())





# comparing conferences 

# stats we want to consider for now
important_stats = ["W_PCT", "PLUS_MINUS", "PTS", "REB", "AST"]


# just the conference plus the stats we want
subsetted_data = data[["Conference"] + important_stats]

# group by the conference
group_by_conference = subsetted_data.groupby("Conference")

# mean for each column 
conference_mean = group_by_conference.mean()

print(conference_mean)






# box plot of win percentage by conference 

plt.figure(figsize=(8,5))

sns.boxplot(data, x = "Conference", y = "W_PCT")
plt.title("Win Percentage by Conference")
plt.show()





# win percentage over time 
season_conf = data.groupby(["Season", "Conference"])["W_PCT"].mean().reset_index()


plt.figure(figsize=(12,6))

sns.lineplot(
    data = season_conf,
    x = "Season",
    y = "W_PCT", 
    hue = "Conference" # colour code by conference 
)

plt.xticks(rotation = 90)

plt.title("Average Conference Win Percentage Over Time")


plt.show()





# distribution of point differential

plt.figure(figsize=(8,5))

sns.histplot(
    data = data, 
    x = "PLUS_MINUS",
    hue = "Conference", 
    bins = 30,
    kde = True
)

plt.title("Point Differential Distribution")

plt.show()




# Correlation Analysis 
numeric_columns = data.select_dtypes(include = ["float64", "int64"])


correlation = numeric_columns.corr()

# do the heatmap 
plt.figure(figsize=(12,10))

sns.heatmap(
    correlation, 
    cmap = "coolwarm",
    center = 0
)

plt.title("Correlation Heatmap")

plt.show()

corr_with_wins = correlation["W_PCT"].sort_values(ascending=False)

print("\nCorrelation with Win Percentage:")
print(corr_with_wins)
