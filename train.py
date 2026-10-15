import pickle
from sklearn.tree import DecisionTreeClassifier

# Change to "2.0" and commit to demonstrate automatic deployment.
MODEL_VERSION = "1.0"

# Demo data: study hours/day, attendance %, internal marks out of 50
X = [
    [1, 40, 10], [2, 50, 15], [2, 60, 20], [3, 65, 25],
    [4, 70, 30], [5, 75, 35], [6, 80, 40], [7, 90, 45],
    [8, 95, 48], [1, 80, 12], [2, 90, 18], [3, 50, 10],
    [4, 60, 20], [5, 85, 25], [6, 60, 30], [7, 70, 35],
    [8, 80, 45], [3, 90, 40],
]
# 0 = Fail, 1 = Pass
y = [0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1]

model = DecisionTreeClassifier(max_depth=3, random_state=42)
model.fit(X, y)
with open("model.pkl", "wb") as f:
    pickle.dump({"model": model, "version": MODEL_VERSION}, f)
print(f"Student result model version {MODEL_VERSION} trained and saved.")
