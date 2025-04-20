import json
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import joblib
import os


script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "labeled_scheduling_dataset.json")
with open(file_path) as f:
    data = json.load(f)


# Extract features
def extract_features(entry):
    processes = entry["processes"]
    arrivals = [p[0] for p in processes]
    bursts = [p[1] for p in processes]
    prios = [p[2] for p in processes]
    tq = entry["time_quantum"]

    return {
        "num_processes": len(processes),
        "avg_arrival": np.mean(arrivals),
        "std_arrival": np.std(arrivals),
        "avg_burst": np.mean(bursts),
        "std_burst": np.std(bursts),
        "max_burst": np.max(bursts),
        "min_burst": np.min(bursts),
        "avg_priority": np.mean(prios),
        "std_priority": np.std(prios),
        "max_priority": np.max(prios),
        "min_priority": np.min(prios),
        "arrival_span": max(arrivals) - min(arrivals),
        "time_quantum": tq,
        "best_algo": entry["best_algo"]
    }

# Convert all to DataFrame
df = pd.DataFrame([extract_features(entry) for entry in data])

# Encode target
algo_map = {"FCFS": 0, "SJF": 1, "RR": 2, "Priority": 3}
df["label"] = df["best_algo"].map(algo_map)

X = df.drop(["best_algo", "label"], axis=1)
y = df["label"]

# Train/Test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Evaluate
y_pred = clf.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"✅ Accuracy: {acc * 100:.2f}%\n")

print("📊 Classification Report:\n", classification_report(y_test, y_pred, target_names=algo_map.keys()))



model_path = os.path.join(script_dir, "best_algo_predictor_model.pkl")

# Save the trained model
joblib.dump(clf, model_path)
print("🎉 Model saved as best_algo_model.pkl")


# # Confusion Matrix
# plt.figure(figsize=(6, 4))
# sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, cmap="Blues", fmt="d", 
#             xticklabels=algo_map.keys(), yticklabels=algo_map.keys())
# plt.xlabel("Predicted")
# plt.ylabel("Actual")
# plt.title("🧠 Confusion Matrix: Best Scheduling Algorithm Prediction")
# plt.tight_layout()
# plt.show()
