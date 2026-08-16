"""
train_model.py
Trains a salary prediction model from employee_salary.csv
Run this once (and again anytime the CSV changes) to (re)generate salary_model.pkl
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

# 1. Load dataset
df = pd.read_csv("employee_salary.csv")

# 2. Features (X) and target (y)
#    We use Experience_Years, Education_Level, Job_Role, City.
#    Skills is a free-text multi-value column, so we skip it here to keep
#    things simple and reliable for a first version.
FEATURES = ["Experience_Years", "Education_Level", "Job_Role", "City"]
TARGET = "Monthly_Salary"

X = df[FEATURES]
y = df[TARGET]

categorical_features = ["Education_Level", "Job_Role", "City"]

# 3. Preprocessing: one-hot encode the categorical columns,
#    leave Experience_Years as-is (passthrough)
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
    ],
    remainder="passthrough"
)

# 4. Full pipeline: preprocessing + model
model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("regressor", LinearRegression())
])

# 5. Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 6. Train
model.fit(X_train, y_train)

# 7. Evaluate
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Absolute Error: {mae:.2f}")
print(f"R2 Score: {r2:.2f}")

# 8. Save the trained model
joblib.dump(model, "salary_model.pkl")

# 9. Save the dropdown option lists so the frontend/backend
#    always show valid choices (built from the actual CSV values)
joblib.dump(sorted(df["Education_Level"].unique().tolist()), "education_levels.pkl")
joblib.dump(sorted(df["Job_Role"].unique().tolist()), "job_roles.pkl")
joblib.dump(sorted(df["City"].unique().tolist()), "cities.pkl")

print("\nModel trained and saved as salary_model.pkl")
print("Dropdown option files saved: education_levels.pkl, job_roles.pkl, cities.pkl")