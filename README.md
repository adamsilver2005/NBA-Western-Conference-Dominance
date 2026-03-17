# NBA Western Conference Dominance Analysis

Python | pandas | NumPy | Data Analysis | Machine Learning | Sports Analytics

## Table of Contents

- [Project Goal](#project-goal)
- [Dataset](#dataset)
- [Project Structure](#project-structure)
- [Dataset Columns](#dataset-columns)
- [Exploratory Data Analysis](#exploratory-data-analysis)
- [How to Run the Project](#how-to-run-the-project)
- [Hypothesis Testing](#hypothesis-testing)
- [Predictive Modeling](#predictive-modeling)
- [Final Conclusion](#final-conclusion)


## Project Goal

For years, NBA fans and analysts have argued that the Western Conference has historically been stronger than the Eastern Conference. This project investigates that claim by analyzing team statistics from the 1996-97 season to the 2022-23 season and comparing performance metrics between conferences. 

The analysis will include:

- Exploratory Data Analysis (EDA)
- Statistical comparisons between conferences
- Visualization of these comparisons over the multiple seasons
- Predictive modeling of team success


## Dataset

The dataset used for this project was sourced from Kaggle: 
(https://www.kaggle.com/datasets/mamadoudiallo/nba-team-stats?resource=download)

The original dataset did not include a **Season** or a **Conference** column, so these were added during data preprocessing. 

Other preprocessing steps included: 

- Creating a **Season** column
- Assigning each team to its **Conference** using a dictionary of team-conference mappings
- Handling inconsistencies in team names due to franchise name changes
- Accounting for the NBA expansion from **29 to 30 teams in 2005**

The dataset was preprocessed using **Python and pandas**



## Project Structure

```
nba-western-conference-analysis/

data/
    raw/                # original Kaggle dataset
        nba_team_stats.csv
    processed/          # cleaned dataset used for analysis
        updated_dataset.csv

analysis/
    exploratory_data_analysis.py             
    hypothesis_testing.py
    predictive_modeling.py

scripts/
    build_dataset.py    # script used to clean and prepare dataset

images/
    # visualizations created during analysis

README.md
.gitignore
```

## Dataset Columns:

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



## Exploratory Data Analysis

Exploratory data analysis was performed to understand the distribution of team statistics and compare performance between conferences.

The key questions that were explored include:

- Do Western Conference teams have higher average win percentages?
- How has conference performance changed over time?
- Which statistics are most strongly associated with winning?

Several visualizations were created to investigate these questions.


### Win Percentage by Conference

![Win Percentage Boxplot](images/win_pct_boxplot.png)

These boxplots compare the distribution of team win percentages between the Eastern and Western Conferences. We can see that there is a small discrepancy between the boxplots, where the Western Conference teams tend to have slightly higher median win percentage, as well as higher Q1 and Q3 values.


### Average Statistics by Conference

The table below shows the average values of several key performance metrics for teams in each conference across all seasons in the dataset.

| Conference | W_PCT | PLUS_MINUS | PTS | REB | AST |
|------------|------|-----------|------|------|------|
| East | 0.483 | -0.496 | 99.70 | 42.35 | 21.95 |
| West | 0.517 | 0.490 | 102.16 | 42.85 | 22.61 |

These averages suggest that Western Conference teams tend to have slightly higher win percentages, score more points per game, and have a positive average point differential compared to Eastern Conference teams.

This initial comparison provides evidence that Western Conference teams may perform slightly better on average, motivating further statistical testing in later sections of the analysis.



### Average Conference Win Percentage Over Time

![Win Percentage Over Time](images/win_pct_trend_over_time.png)


This visualization shows the average team win percentage for the Eastern and Western Conferences for each NBA season in the dataset. Across most seasons, the Western Conference maintains a higher average win percentage than the Eastern Conference, suggesting stronger overall team performance in the West. The gap is particularly noticeable during the early 2000s and mid-2010s, where Western teams consistently outperform Eastern teams.

In more recent seasons, the difference between conferences appears to narrow, indicating that the competitive balance between the two conferences may be becoming more even. In the early 2020's, the Eastern Conference has overtaken the Western Conference in win percentage, potentially suggesting that we are seeing a shift in dominance in conferences. 



### Point Differential Distribution by Conference

![Point Differential Distribution](images/point_differential_distribution.png)

This histogram compares the distribution of team point differentials (PLUS_MINUS) between the Eastern and Western Conferences. Point differential measures the average margin by which a team outscores its opponents and is often considered one of the strongest indicators of overall team strength.

The distribution for Western Conference teams is slightly shifted to the right compared to the Eastern Conference, indicating that Western teams tend to have slightly higher average point differentials. This suggests that, across seasons, Western Conference teams have generally outscored their opponents by larger margins than Eastern Conference teams.




### Correlation Heatmap of Team Statistics

![Correlation Heatmap](images/correlation_heatmap.png)

This heatmap visualizes the correlation between all numerical variables in the dataset. Correlation values range from -1 to 1, where values closer to 1 indicate strong positive relationships, values closer to -1 indicate strong negative relationships, and values near 0 indicate weak or no linear relationship.

Several strong relationships appear in the dataset. As expected, wins (W) and win percentage (W_PCT) show a near-perfect positive correlation. Additionally, point differential (PLUS_MINUS) has a strong positive correlation with both wins and win percentage, indicating that teams that outscore their opponents by larger margins tend to win more games.

Other offensive statistics such as points scored (PTS), assists (AST), and field goal metrics also show moderate positive correlations with winning performance.

These relationships provide insight into which team statistics are most strongly associated with success and help motivate the use of predictive models in the next stage of the analysis.



### Top Correlations with Winning

To better understand which team statistics are associated with success, correlations with win percentage (W_PCT) were examined.

The strongest positive correlations with winning include:

| Statistic | Correlation with W_PCT |
|----------|------------------------|
| PLUS_MINUS | 0.97 |
| FG_PCT | 0.56 |
| FG3_PCT | 0.46 |
| AST | 0.31 |
| DREB | 0.30 |
| PTS | 0.27 |

Among these variables, point differential (PLUS_MINUS) shows the strongest relationship with winning. This indicates that teams that outscore opponents by larger margins tend to achieve higher win percentages. Shooting efficiency metrics such as field goal percentage (FG_PCT) and three-point percentage (FG3_PCT) also show strong positive relationships with winning, suggesting that offensive efficiency is an important factor in team success. Additionally, statistics like assists and defensive rebounds show moderate correlations with winning, highlighting the importance of ball movement and defensive performance. Finally, Turnovers (TOV) show a negative correlation with win percentage, indicating that teams committing fewer turnovers tend to perform better.




### Scatter Plot of Point Differential vs Win Percentage 

![Scatter Plot of Point Differential vs Win Percentage](images/plus_minus_vs_win_pct.png)

This scatter plot shows the relationship between team point differential (PLUS_MINUS) and win percentage (W_PCT) across NBA teams. Each point represents a team-season, with colors distinguishing teams from the Eastern and Western Conferences. The visualization reveals a strong positive relationship between point differential and win percentage. Teams that outscore their opponents by larger margins tend  to have higher win percentages. This relationship appears consisten across both conferences, indicating that point differential is a strong indicator of team performance. While both conferences follow the same overall trend, Western Conference teams appear slightly more concentrated in the higher point differential and win percentage range (top right) in several seasons, supporting the hypothesis that the Western Conference has historically been stronger.



## Hypothesis Testing

I conducted hypothesis tests to determine whether Western Conference teams outperform Eastern Conference teams. 
The null hypothesis was there is no difference in statistic being tested between conferences. 
The alternative hypothesis is that there is a difference in the statistic that we are testing between conferences.

**Win Percentage (W_PCT):**  
- T-test results: t = 3.12, p = 0.0001  
- Conclusion: Western teams have a statistically higher average win percentage than Eastern teams.

**Point Differential (PLUS_MINUS):**  
- T-test results: t = 3.06, p = 0.001
- Conclusion: Western teams outscore opponents by larger margins, supporting the claim of Western dominance.

Other metrics like assists, rebounds, and shooting efficiency were also tested, and all of them showed significant differences in favor of Western Conference dominance. 



## Predictive Modeling 

Two modeling approaches were implemented, each answering a distinct question.
Three models were evaluated in both sections: **Linear Regression**,
**Random Forest**, and **Gradient Boosting**.

> **Note:** PLUS_MINUS was excluded from all models as a feature. Its 0.97
> correlation with W_PCT would constitute data leakage — the model would
> effectively be predicting the target using a near-perfect proxy of itself.

---

### Section A — Explaining W_PCT from Same-Season Stats

**Question:** Given a team's stats in a season, how well can we explain their win percentage?

**Approach:**
- Features: PTS, REB, AST, FG_PCT, FG3_PCT, TOV, STL, BLK
- Training data: all seasons from 1996-97 to 2022-23
- Test data: 2023-24 season (held out entirely)
- Evaluation: RMSE, R², and 10-fold cross-validated R²

| Model | RMSE | R² | CV R² (10-fold) |
|---|---|---|---|
| Linear Regression | 0.0755 | 0.7798 | 0.6313 |
| Random Forest | 0.1464 | 0.1711 | 0.3842 |
| Gradient Boosting | 0.1182 | 0.4594 | 0.4971 |

**Best model: Linear Regression**

Linear Regression outperformed both tree-based models across all three metrics.
This is expected given the small dataset size of ~800 rows — simpler models
tend to generalize better when data is limited, and the relationships between
team stats and win percentage are largely linear in nature.

The model explains 78% of the variance in win percentage (R² = 0.78) from just
8 team statistics, with an average prediction error of 7.5 percentage points.
The cross-validated R² of 0.63 confirms the model generalizes well to unseen seasons.

**2023-24 Predicted vs Actual Win Percentage:**

| Team | Conference | Predicted W_PCT | Actual W_PCT |
|---|---|---|---|
| Denver Nuggets | West | 0.742 | 0.695 |
| Boston Celtics | East | 0.740 | 0.780 |
| New Orleans Pelicans | West | 0.724 | 0.598 |
| Oklahoma City Thunder | West | 0.720 | 0.695 |
| Minnesota Timberwolves | West | 0.676 | 0.683 |
| Los Angeles Clippers | West | 0.670 | 0.622 |
| Phoenix Suns | West | 0.633 | 0.598 |
| Los Angeles Lakers | West | 0.630 | 0.573 |
| Chicago Bulls | East | 0.611 | 0.476 |
| Indiana Pacers | East | 0.605 | 0.573 |
| Milwaukee Bucks | East | 0.589 | 0.598 |
| Golden State Warriors | West | 0.584 | 0.561 |
| New York Knicks | East | 0.581 | 0.610 |
| Philadelphia 76ers | East | 0.577 | 0.573 |
| Cleveland Cavaliers | East | 0.568 | 0.585 |
| Sacramento Kings | West | 0.554 | 0.561 |
| Houston Rockets | West | 0.538 | 0.500 |
| Dallas Mavericks | West | 0.531 | 0.610 |
| Miami Heat | East | 0.519 | 0.561 |
| Orlando Magic | East | 0.517 | 0.573 |
| Brooklyn Nets | East | 0.466 | 0.390 |
| Atlanta Hawks | East | 0.457 | 0.439 |
| Toronto Raptors | East | 0.448 | 0.305 |
| San Antonio Spurs | West | 0.375 | 0.268 |
| Utah Jazz | West | 0.367 | 0.378 |
| Washington Wizards | East | 0.362 | 0.183 |
| Charlotte Hornets | East | 0.352 | 0.256 |
| Detroit Pistons | East | 0.342 | 0.171 |
| Memphis Grizzlies | West | 0.292 | 0.329 |
| Portland Trail Blazers | West | 0.264 | 0.256 |

Most predictions are within 5-10 percentage points of actual. Notable misses
include New Orleans (predicted 0.724, actual 0.598) and Chicago (predicted
0.611, actual 0.476), both of whom underperformed their raw statistics.
Dallas Mavericks was the biggest positive outlier — predicted 0.531 but
achieved 0.610, suggesting they overperformed their counting stats, largely
driven by Luka Dončić's playoff-caliber play throughout the regular season.

---

### Section B — Forecasting W_PCT from Previous Season Stats

**Question:** Can last season's team stats predict next season's win percentage?

**Approach:**
- Features: same as Section A (PTS, REB, AST, FG_PCT, FG3_PCT, TOV, STL, BLK)
- Target: next season's W_PCT (season N stats → season N+1 W_PCT)
- Training data: all lagged season pairs up to 2021-22 → 2022-23
- Test data: 2022-23 stats used to predict 2023-24 W_PCT
- Evaluation: RMSE, R², and 10-fold cross-validated R²

| Model | RMSE | R² | CV R² (10-fold) |
|---|---|---|---|
| Linear Regression | 0.1566 | 0.0512 | 0.2150 |
| Random Forest | 0.1626 | -0.0221 | 0.1378 |
| Gradient Boosting | 0.1602 | 0.0074 | 0.1388 |

**Best model: Linear Regression**

All three models struggled significantly in Section B, with R² values close to
zero. Linear Regression again performed best but only explains about 5% of the
variance in next season's win percentage — barely better than simply predicting
the league average for every team.

This is an expected and meaningful finding. Raw team statistics from one season
are poor predictors of the following season because so much changes between
seasons — roster moves, injuries, player development, and coaching adjustments
all play a significant role that counting stats alone cannot capture. The average
prediction error nearly doubles compared to Section A (0.1566 vs 0.0755),
reflecting how much harder genuine forecasting is compared to explanation.

**2023-24 Forecasted vs Actual Win Percentage** *(using 2022-23 stats as input)*:

| Team | Conference | Forecasted W_PCT | Actual W_PCT |
|---|---|---|---|
| Denver Nuggets | West | 0.608 | 0.695 |
| Memphis Grizzlies | West | 0.606 | 0.329 |
| Chicago Bulls | East | 0.581 | 0.476 |
| Milwaukee Bucks | East | 0.558 | 0.598 |
| Toronto Raptors | East | 0.541 | 0.305 |
| Washington Wizards | East | 0.539 | 0.183 |
| New Orleans Pelicans | West | 0.538 | 0.598 |
| Brooklyn Nets | East | 0.537 | 0.390 |
| Atlanta Hawks | East | 0.535 | 0.439 |
| Philadelphia 76ers | East | 0.534 | 0.573 |
| Cleveland Cavaliers | East | 0.532 | 0.585 |
| Minnesota Timberwolves | West | 0.526 | 0.683 |
| Boston Celtics | East | 0.523 | 0.780 |
| Phoenix Suns | West | 0.518 | 0.598 |
| Los Angeles Clippers | West | 0.516 | 0.622 |
| New York Knicks | East | 0.514 | 0.610 |
| Los Angeles Lakers | West | 0.506 | 0.573 |
| Sacramento Kings | West | 0.488 | 0.561 |
| Oklahoma City Thunder | West | 0.477 | 0.695 |
| Orlando Magic | East | 0.460 | 0.573 |
| Charlotte Hornets | East | 0.458 | 0.256 |
| Golden State Warriors | West | 0.458 | 0.561 |
| Utah Jazz | West | 0.451 | 0.378 |
| Houston Rockets | West | 0.431 | 0.500 |
| Indiana Pacers | East | 0.431 | 0.573 |
| Portland Trail Blazers | West | 0.404 | 0.256 |
| San Antonio Spurs | West | 0.396 | 0.268 |
| Miami Heat | East | 0.393 | 0.561 |
| Dallas Mavericks | West | 0.392 | 0.610 |
| Detroit Pistons | East | 0.356 | 0.171 |

The forecasts are noticeably clustered between 0.35 and 0.61, failing to
predict either strong or weak teams accurately. The largest misses highlight
exactly why season-to-season forecasting is difficult — Memphis was predicted
at 0.606 but collapsed to 0.329 following Ja Morant's suspension, while Boston
was predicted at 0.523 but jumped to 0.780 in a breakout season. Oklahoma City
was predicted at 0.477 but reached 0.695 as a young roster took a significant
leap. These outcomes were driven by factors completely invisible to a model
built on the previous season's counting stats.

## How to Run the Project

Clone the repository:

```
git clone https://github.com/YOUR_USERNAME/nba-western-conference-analysis.git
```

Install dependencies:

```
pip install -r requirements.txt
```

Run the exploratory data analysis:

```
python analysis/eda.py
```


## Tools and Libraries

- Python
- pandas
- NumPy
- matplotlib
- seaborn
- scikit-learn
