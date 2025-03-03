import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

print("Arguments received:", sys.argv)  # Debugging: Print the arguments received

# Load the dataset
try:
    data = pd.read_csv("private/framingham.csv")
    print("Dataset loaded successfully")  # Debugging
except Exception as e:
    print("Error loading dataset:", e)
    sys.exit(1)

# Fill missing values
data.fillna(data.median(), inplace=True)

# Rename the gender column to match the original feature name during training
data.rename(columns={"gender": "male"}, inplace=True)

# Split the data into features (X) and target (y)
X = data.drop("TenYearCHD", axis=1)  # 'TenYearCHD' is the target column
y = data["TenYearCHD"]

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train a Random Forest Classifier
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)
print("Model trained successfully")  # Debugging

# Save the feature names in the correct order
feature_names = X.columns.tolist()
with open("private/feature_names.txt", "w") as f:
    f.write("\n".join(feature_names))

# Evaluate the model (optional, for debugging)
accuracy = accuracy_score(y_test, model.predict(X_test))
print(f"Model Accuracy: {accuracy * 100:.2f}%")  # Debugging

# Get user input from Node.js
try:
    input_data = [float(arg) for arg in sys.argv[1:]]  # Convert arguments to floats
    print("Input data received:", input_data)  # Debugging
except Exception as e:
    print("Error receiving input data:", e)
    sys.exit(1)

# Load the feature names in the correct order
try:
    with open("private/feature_names.txt", "r") as f:
        feature_names = f.read().splitlines()
except Exception as e:
    print("Error loading feature names:", e)
    sys.exit(1)

# Add missing features with default values
default_values = {
    "education": 1,
    "currentSmoker": 1 if input_data[2] > 0 else 0,
    "BPMeds": 0,
    "prevalentStroke": 0,
    "prevalentHyp": 0,
    "diaBP": 80,
    "heartRate": 70,
    "glucose": 90,
}

# Combine user input with default values
try:
    full_input = pd.DataFrame(
        np.array([
            input_data[0],  # age
            input_data[1],  # gender (renamed to male)
            default_values["education"],
            default_values["currentSmoker"],
            input_data[2],  # cigsPerDay
            default_values["BPMeds"],
            default_values["prevalentStroke"],
            default_values["prevalentHyp"],
            input_data[3],  # sysBP
            input_data[4],  # totChol
            input_data[5],  # diabetes
            input_data[6],  # BMI
            default_values["diaBP"],
            default_values["heartRate"],
            default_values["glucose"],
        ]).reshape(1, -1),
        columns=feature_names  # Use the feature names loaded from the file
    )
    print("Full input prepared:", full_input)  # Debugging
except Exception as e:
    print("Error preparing input data:", e)
    sys.exit(1)

try:
    prediction = model.predict(full_input)
    print("Prediction:", prediction[0])  # Debugging
    print(prediction[0])  # Output the prediction (0 = Low Risk, 1 = High Risk)
except Exception as e:
    print("Error making prediction:", e)
    sys.exit(1)

