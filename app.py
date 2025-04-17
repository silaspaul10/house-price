from flask import Flask, request, render_template
import joblib
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import os

app = Flask(__name__)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/house_prices")
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Define Database Model
class HousePrice(db.Model):
    __tablename__ = "house_price"  # Explicitly define the table name
    id = db.Column(db.Integer, primary_key=True)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    housing_median_age = db.Column(db.Integer, nullable=False)
    total_rooms = db.Column(db.Integer, nullable=False)
    total_bedrooms = db.Column(db.Integer, nullable=False)
    population = db.Column(db.Integer, nullable=False)
    households = db.Column(db.Integer, nullable=False)
    median_income = db.Column(db.Float, nullable=False)
    predicted_price = db.Column(db.Float, nullable=False)

# Load model
model = joblib.load("House_price_prediction.pkl")

@app.route("/")
def home():
    return render_template("index.html", prediction=None)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Collect input values from form
        data = {
            "longitude": float(request.form["longitude"]),
            "latitude": float(request.form["latitude"]),
            "housing_median_age": float(request.form["housing_median_age"]),
            "total_rooms": float(request.form["total_rooms"]),
            "total_bedrooms": float(request.form["total_bedrooms"]),
            "population": float(request.form["population"]),
            "households": float(request.form["households"]),
            "median_income": float(request.form["median_income"])
        }

        # Convert data to DataFrame
        df = pd.DataFrame([data])  # Wrap dict in a list to match DataFrame format
        # Store in database
        prediction = float(model.predict(df)[0])  # Convert np.float64 to Python float

        new_entry = HousePrice(
            longitude=float(data["longitude"]),
            latitude=float(data["latitude"]),
            housing_median_age=int(float(data["housing_median_age"])),  # ✅ FIXED
            total_rooms=int(float(data["total_rooms"])),  # ✅ FIXED
            total_bedrooms=int(float(data["total_bedrooms"])),  # ✅ FIXED
            population=int(float(data["population"])),  # ✅ FIXED
            households=int(float(data["households"])),  # ✅ FIXED
            median_income=float(data["median_income"]),
            predicted_price=float(prediction)
        )


        db.session.add(new_entry)
        db.session.commit()



        return render_template("index.html", prediction=f"Predicted House Price: ${prediction:,.2f}")

    except Exception as e:
        return render_template("index.html", prediction=f"Error: {str(e)}")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5001)
