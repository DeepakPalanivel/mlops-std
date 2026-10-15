import pickle
from flask import Flask, render_template, request

app = Flask(__name__)
with open("model.pkl", "rb") as f:
    saved = pickle.load(f)
model = saved["model"]
MODEL_VERSION = saved["version"]

@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    if request.method == "POST":
        try:
            hours = float(request.form["study_hours"])
            attendance = float(request.form["attendance"])
            marks = float(request.form["internal_marks"])
        except (ValueError, KeyError):
            return "Please enter valid numeric values.", 400
        if not 0 <= hours <= 24:
            return "Study hours must be between 0 and 24.", 400
        if not 0 <= attendance <= 100:
            return "Attendance must be between 0 and 100.", 400
        if not 0 <= marks <= 50:
            return "Internal marks must be between 0 and 50.", 400
        result = model.predict([[hours, attendance, marks]])[0]
        prediction = "Pass" if result == 1 else "Fail"
    return render_template("index.html", prediction=prediction, version=MODEL_VERSION)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
