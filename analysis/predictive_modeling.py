# Filename: predictive_modeling.py
# Author: Adam Silver
# Date: 2026-03-17
# Description: Two predictive modeling approaches for NBA team win percentage.
#              Section A: Explain W_PCT from same-season stats (1996-97 to 2022-23 train, 2023-24 test)
#              Section B: Forecast W_PCT from previous season's stats (season N -> N+1)

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score
import numpy as np
import pandas as pd


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


# SECTION A — Explain W_PCT from same-season stats
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


# SECTION B — Forecast W_PCT from previous season stats
# Goal: can last season's stats predict next season's win percentage?
# Approach: use season N stats to predict season N+1 W_PCT
# Train: all lagged season pairs up to 2021-22 → 2022-23
# Test:  2022-23 stats used to forecast 2023-24 W_PCT

print("SECTION B: Forecasting W_PCT from Previous Season Stats")


# sort by team and season so the shift(-1) correctly pairs each season
# with the following season for the same team
data_b = data.sort_values(["TEAM_NAME", "Season"]).copy()

# for each team, create a new column containing next season's W_PCT as the target
data_b["NEXT_W_PCT"] = data_b.groupby("TEAM_NAME")["W_PCT"].shift(-1)

# remove rows where there is no following season (each team's last season)
data_b = data_b.dropna(subset=["NEXT_W_PCT"])

# 2022-23 rows pair with 2023-24 W_PCT, so use them as the test set
train_b = data_b[data_b["Season"] != 2023]
test_b  = data_b[data_b["Season"] == 2023]

X_train_b = train_b[FEATURES]
y_train_b  = train_b["NEXT_W_PCT"]
X_test_b   = test_b[FEATURES]
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

    rmse = np.sqrt(mean_squared_error(y_test_b, preds))
    r2   = r2_score(y_test_b, preds)

    # 10-fold CV gives a more reliable estimate of generalization on ~800 rows
    cv_r2 = cross_val_score(model, X_train_b, y_train_b, cv=10, scoring="r2").mean()

    print(f"\n  {name}")
    print(f"    RMSE:        {rmse:.4f}")
    print(f"    R²:          {r2:.4f}")
    print(f"    CV R² (10k): {cv_r2:.4f}")

    # keep track of the best model by lowest RMSE
    if rmse < best_rmse_b:
        best_rmse_b  = rmse
        best_model_b = model
        best_name_b  = name

print(f"\n  Best model: {best_name_b}")

# retrain the best model on all lagged data before making the final forecast
best_model_b.fit(X_train_b, y_train_b)

# print feature importances if the best model is a tree-based model
if hasattr(best_model_b, "feature_importances_"):
    importances = pd.Series(best_model_b.feature_importances_, index=FEATURES)
    print("\n  Feature Importances:")
    print(importances.sort_values(ascending=False).to_string())

# forecast 2023-24 win percentages using 2022-23 stats as input
preds_b = best_model_b.predict(X_test_b)

results_b = test_b[["TEAM_NAME", "Conference"]].copy()
results_b["Predicted_2324_W_PCT"] = preds_b.round(3)
results_b["Actual_2324_W_PCT"]    = y_test_b.values.round(3)
results_b = results_b.sort_values("Predicted_2324_W_PCT", ascending=False)

print("\n  Predicted vs Actual Win Percentage:")
print(results_b.to_string(index=False))

