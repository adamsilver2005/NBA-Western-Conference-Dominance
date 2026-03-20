# Filename: predictive_modeling.py
# Author: Adam Silver
# Date: 2026-03-17
# Description: Two predictive modeling approaches for NBA team win percentage.
#              Section A: Explain W_PCT from same-season stats (1996-97 to 2022-23 train, 2023-24 test)
#              Forecast W_PCT from previous season's stats (season N -> N+1), enhanced with rolling averages, 
#              YoY changes, and previous W_PCT

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


data = pd.read_csv(
    "C:/Users/Ilike/OneDrive/Year 3/Personal Projects/Western Conference Dominance"
    "/data/processed/updated_dataset.csv"
)

# fix LA Clippers naming issue
data["TEAM_NAME"] = data["TEAM_NAME"].replace("LA Clippers", "Los Angeles Clippers")



# features used in both sections
# PLUS_MINUS excluded — 0.97 correlation with W_PCT would be data leakage
FEATURES = [
    "PTS",
    "REB",
    "AST",
    "FG_PCT",
    "FG3_PCT",
    "TOV",
    "STL",
    "BLK",
]


# SECTION A: Explain W_PCT from same-season stats
# Goal: given a team's stats in a season, how well can the model explain
# their win percentage?
# Train: all seasons 1996-97 through 2022-23
# Test:  2023-24 season (held out entirely)

print("SECTION A: Explaining W_PCT from Same-Season Stats")


# split into train and test sets
train_a = data[data["Season"] != 2024]
test_a  = data[data["Season"] == 2024]

X_train_a = train_a[FEATURES]
y_train_a  = train_a["W_PCT"]
X_test_a   = test_a[FEATURES]
y_test_a   = test_a["W_PCT"]

# define the three models to compare
lr_a  = LinearRegression()
rf_a  = RandomForestRegressor(n_estimators=100, max_depth=4, random_state=42)
gb_a  = GradientBoostingRegressor(n_estimators=100, max_depth=3, learning_rate=0.05, random_state=42)

models_a = {
    "Linear Regression": lr_a,
    "Random Forest":     rf_a,
    "Gradient Boosting": gb_a,
}

# train each model, then calculate RMSE, R², and cross-validated R²
best_rmse_a  = float("inf")
best_model_a = None
best_name_a  = ""

for name, model in models_a.items():
    model.fit(X_train_a, y_train_a)
    preds = model.predict(X_test_a)

    rmse = np.sqrt(mean_squared_error(y_test_a, preds))
    r2   = r2_score(y_test_a, preds)

    
    cv_r2 = cross_val_score(model, X_train_a, y_train_a, cv=10, scoring="r2").mean()

    print(f"\n  {name}")
    print(f"    RMSE:        {rmse:.4f}")
    print(f"    R²:          {r2:.4f}")
    print(f"    CV R² (10k): {cv_r2:.4f}")

    # keep track of the best model by lowest RMSE
    if rmse < best_rmse_a:
        best_rmse_a  = rmse
        best_model_a = model
        best_name_a  = name

print(f"\n  Best model: {best_name_a}")

# retrain the best model on all historical data before predicting 2023-24
best_model_a.fit(X_train_a, y_train_a)

# print feature importances if the best model is a tree-based model
if hasattr(best_model_a, "feature_importances_"):
    importances = pd.Series(best_model_a.feature_importances_, index=FEATURES)
    print("\n  Feature Importances:")
    print(importances.sort_values(ascending=False).to_string())

# predict 2023-24 win percentages and compare to actual
preds_a = best_model_a.predict(X_test_a)

results_a = test_a[["TEAM_NAME", "Conference", "W_PCT"]].copy()
results_a["Predicted_W_PCT"] = preds_a.round(3)
results_a["Actual_W_PCT"]    = results_a["W_PCT"].round(3)
results_a = results_a.drop(columns="W_PCT")
results_a = results_a.sort_values("Predicted_W_PCT", ascending=False)

print("\n  Predicted vs Actual Win Percentage:")
print(results_a.to_string(index=False))






# SECTION B: Forecast W_PCT from previous season stats
# Goal: can historical team stats predict next season's win percentage?
# Uses three types of features to give the model more context about each
# team's trajectory rather than just a single season snapshot:
#
#   1. Last season's raw stats and W_PCT
#   2. 3 year rolling averages of each stat
#   3. Year over year change in each stat
#
# Train: all lagged season pairs up to 2021-22 → 2022-23
# Test:  2022-23 stats used to forecast 2023-24 W_PCT
# ═══════════════════════════════════════════════════════════════════════════════

print("SECTION B: Forecasting W_PCT from Previous Season Stats")

# sort by team and season so all rolling/lag operations are applied correctly
data_b = data.sort_values(["TEAM_NAME", "Season"]).copy()


# last season's W_PCT as a feature: 
# a strong prior teams that won a lot last year tend to win more this year
data_b["PREV_W_PCT"] = data_b.groupby("TEAM_NAME")["W_PCT"].shift(1)

# 3 year rolling averages for each stat:
# smooths out outlier seasons and captures sustained team quality
# min_periods=1 means teams with fewer than 3 seasons still get a value
for stat in FEATURES:
    data_b[f"{stat}_ROLL3"] = (
        data_b.groupby("TEAM_NAME")[stat]
        .transform(lambda x: x.shift(1).rolling(window=3, min_periods=1).mean())
    )

# year over year change in each stat
# captures whether a team is improving or declining heading into next season
for stat in FEATURES:
    data_b[f"{stat}_CHANGE"] = (
        data_b.groupby("TEAM_NAME")[stat]
        .transform(lambda x: x.shift(1).diff())
    )

# combine all three feature types into one list
FEATURES_B = (
    FEATURES                                  # last season's raw stats
    + ["PREV_W_PCT"]                          # last season's W_PCT
    + [f"{s}_ROLL3"  for s in FEATURES]       # 3 year rolling averages
    + [f"{s}_CHANGE" for s in FEATURES]       # year over year changes
)

# create the target: next season's W_PCT
data_b["NEXT_W_PCT"] = data_b.groupby("TEAM_NAME")["W_PCT"].shift(-1)

# drop rows with NaN in any feature or target column
# this removes each team's first 1-2 seasons (not enough history for rolling)
# and each team's final season (no next season to predict)
data_b = data_b.dropna(subset=FEATURES_B + ["NEXT_W_PCT"])

# 2022-23 rows pair with 2023-24 W_PCT, so use them as the test set
train_b = data_b[data_b["Season"] != 2023]
test_b  = data_b[data_b["Season"] == 2023]

X_train_b = train_b[FEATURES_B]
y_train_b  = train_b["NEXT_W_PCT"]
X_test_b   = test_b[FEATURES_B]
y_test_b   = test_b["NEXT_W_PCT"]

# define the three models to compare
lr_b  = LinearRegression()
rf_b  = RandomForestRegressor(n_estimators=100, max_depth=4, random_state=42)
gb_b  = GradientBoostingRegressor(n_estimators=100, max_depth=3, learning_rate=0.05, random_state=42)

models_b = {
    "Linear Regression": lr_b,
    "Random Forest":     rf_b,
    "Gradient Boosting": gb_b,
}

# train each model, then calculate RMSE, R², and cross-validated R²
best_rmse_b  = float("inf")
best_model_b = None
best_name_b  = ""

for name, model in models_b.items():
    model.fit(X_train_b, y_train_b)
    preds = model.predict(X_test_b)

    rmse  = np.sqrt(mean_squared_error(y_test_b, preds))
    r2    = r2_score(y_test_b, preds)

    # 10-fold CV on training data only
    cv_r2 = cross_val_score(model, X_train_b, y_train_b, cv=10, scoring="r2").mean()

    print(f"\n  {name}")
    print(f"    RMSE:        {rmse:.4f}")
    print(f"    R²:          {r2:.4f}")
    print(f"    CV R² (10k): {cv_r2:.4f}")

    if rmse < best_rmse_b:
        best_rmse_b  = rmse
        best_model_b = model
        best_name_b  = name

print(f"\n  Best model: {best_name_b}")

# retrain best model on all available lagged data before forecasting
best_model_b.fit(X_train_b, y_train_b)

# print feature importances if tree-based model won
# capped at top 10 since there are now 25 features total
if hasattr(best_model_b, "feature_importances_"):
    importances = pd.Series(best_model_b.feature_importances_, index=FEATURES_B)
    print("\n  Feature Importances (top 10):")
    print(importances.sort_values(ascending=False).head(10).to_string())

# forecast 2023-24 W_PCT using 2022-23 stats as input
preds_b = best_model_b.predict(X_test_b)

results_b = test_b[["TEAM_NAME", "Conference"]].copy()
results_b["Predicted_2324_W_PCT"] = preds_b.round(3)
results_b["Actual_2324_W_PCT"]    = y_test_b.values.round(3)
results_b = results_b.sort_values("Predicted_2324_W_PCT", ascending=False)

print("\n  Predicted vs Actual Win Percentage:")
print(results_b.to_string(index=False))




# Section B Visualization: Predicted vs Actual W_PCT 
# horizontal bar chart showing predicted vs actual for each team,
# colored by conference, sorted by actual W_PCT for easy comparison

# sort by actual W_PCT so the best teams appear at the top
results_b = results_b.sort_values("Actual_2324_W_PCT", ascending=True)

teams      = results_b["TEAM_NAME"].tolist()
predicted  = results_b["Predicted_2324_W_PCT"].tolist()
actual     = results_b["Actual_2324_W_PCT"].tolist()
conference = results_b["Conference"].tolist()

# y positions for each team
y = range(len(teams))

fig, ax = plt.subplots(figsize=(12, 11))

# draw a horizontal bar for each team showing predicted (lighter) and actual (darker)
# east teams are blue, west teams are red
for i, (pred, act, conf) in enumerate(zip(predicted, actual, conference)):
    if conf == "West":
        pred_color = "#f4a582"   # light red for predicted
        act_color  = "#d6604d"   # dark red for actual
    else:
        pred_color = "#92c5de"   # light blue for predicted
        act_color  = "#4393c3"   # dark blue for actual

    # draw predicted bar (lighter, slightly thinner)
    ax.barh(i + 0.2, pred, height=0.35, color=pred_color, alpha=0.9)

    # draw actual bar (darker, slightly lower)
    ax.barh(i - 0.2, act, height=0.35, color=act_color, alpha=0.9)

# team name labels on y axis
ax.set_yticks(list(y))
ax.set_yticklabels(teams, fontsize=9)

# labels and title
ax.set_xlabel("Win Percentage", fontsize=11)
ax.set_title(
    "Section B: Forecasted vs Actual 2023-24 Win Percentage\n(using 2022-23 stats as input)",
    fontsize=13, fontweight="bold", pad=15
)

# vertical line at 0.5 (winning record threshold)
ax.axvline(x=0.5, color="gray", linestyle="--", linewidth=0.8, alpha=0.7)
ax.text(0.502, len(teams) - 0.5, ".500 mark", fontsize=8, color="gray")

# x axis range
ax.set_xlim(0, 0.95)

# legend
west_pred_patch  = mpatches.Patch(color="#f4a582", label="West — Forecasted")
west_act_patch   = mpatches.Patch(color="#d6604d", label="West — Actual")
east_pred_patch  = mpatches.Patch(color="#92c5de", label="East — Forecasted")
east_act_patch   = mpatches.Patch(color="#4393c3", label="East — Actual")

ax.legend(
    handles=[west_act_patch, west_pred_patch, east_act_patch, east_pred_patch],
    loc="lower right", fontsize=9, framealpha=0.9
)

plt.tight_layout()
plt.savefig(
    "C:/Users/Ilike/OneDrive/Year 3/Personal Projects/Western Conference Dominance"
    "/images/section_b_predicted_vs_actual.png",
    dpi=150, bbox_inches="tight"
)
plt.show()
print("Section B visualization saved.")