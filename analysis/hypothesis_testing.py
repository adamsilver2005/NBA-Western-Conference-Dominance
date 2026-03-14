# Filename: hypothesis_testing.py
# Author: Adam Silver
# Date: 2026-03-13
# Description: 

from scipy.stats import ttest_ind
import pandas as pd


data = pd.read_csv("C:/Users/Ilike/OneDrive/Year 3/Personal Projects/Western Conference Dominance"
                    "/data/processed/updated_dataset.csv")



# two sample t test based on win percentage
west_wins = data[data["Conference"] == "West"]["W_PCT"]
east_wins = data[data["Conference"] == "East"]["W_PCT"]


t_stat, p_value = ttest_ind(west_wins, east_wins, alternative='greater')


print(f"T-statistic W_PCT: {t_stat:.5f}, P-value W_PCT: {p_value:.5f}")



# two sample t test based on plus minus

west_plus_minus = data[data["Conference"] == "West"]["PLUS_MINUS"]
east_plus_minus = data[data["Conference"] == "East"]["PLUS_MINUS"]


t_stat, p_value = ttest_ind(west_plus_minus, east_plus_minus, alternative='greater')


print(f"T-statistic PLUS_MINUS: {t_stat:.5f}, P-value PLUS_MINUS: {p_value:.5f}")





# two sample t test based on points 

west_points = data[data["Conference"] == "West"]["PTS"]
east_points = data[data["Conference"] == "East"]["PTS"]


t_stat, p_value = ttest_ind(west_points, east_points, alternative='greater')


print(f"T-statistic PTS: {t_stat:.5f}, P-value PTS: {p_value:.6f}")





# two sample t test based on assists

west_assists = data[data["Conference"] == "West"]["AST"]
east_assists = data[data["Conference"] == "East"]["AST"]


t_stat, p_value = ttest_ind(west_points, east_points, alternative='greater')


print(f"T-statistic AST: {t_stat:.5f}, P-value AST: {p_value:.6f}")





# two sample t test based on rebounds 

west_rebounds = data[data["Conference"] == "West"]["REB"]
east_rebounds = data[data["Conference"] == "East"]["REB"]


t_stat, p_value = ttest_ind(west_points, east_points, alternative='greater')


print(f"T-statistic REB: {t_stat:.5f}, P-value REB: {p_value:.6f}")







# two sample t test based on field goal percentage 

west_field_goal_pct = data[data["Conference"] == "West"]["FG_PCT"]
east_field_goal_pct = data[data["Conference"] == "East"]["FG_PCT"]


t_stat, p_value = ttest_ind(west_field_goal_pct, east_field_goal_pct, alternative='greater')


print(f"T-statistic FG_PCT: {t_stat:.5f}, P-value FG_PCT: {p_value:.10f}")


