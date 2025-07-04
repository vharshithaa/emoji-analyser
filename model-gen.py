import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# Step 1: Create dummy build data
data = {
    "developer": ["dev1", "dev2", "dev3", "dev4", "dev1", "dev2", "dev3", "dev4", "dev5", "dev1"],
    "time": ["10:00", "14:15", "09:30", "22:00", "13:00", "16:20", "11:45", "19:30", "20:20", "12:30"],
    "files_changed": [5, 20, 3, 18, 10, 7, 12, 30, 2, 8],
    "test_status": ["Success", "Failure", "Success", "Failure", "Success", "Success", "Failure", "Failure", "Success", "Success"],
    "predicted": ["Success", "Failure", "Success", "Failure", "Success", "Success", "Failure", "Failure", "Success", "Success"]
}

df = pd.DataFrame(data)

# Step 2: Convert categorical values to numeric for model
df['test_status_bin'] = df['test_status'].map({'Success': 0, 'Failure': 1})
df['predicted_bin'] = df['predicted'].map({'Success': 0, 'Failure': 1})

# Step 3: Use only relevant features for training
X = df[['files_changed', 'test_status_bin']]
y = df['predicted_bin']

# Step 4: Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Step 5: Save model to file
joblib.dump(model, 'cicd_model.pkl')

print("✅ Model trained and saved as cicd_model.pkl")