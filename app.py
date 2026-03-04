from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import requests
from datetime import datetime
import os
import matplotlib.pyplot as plt

app = Flask(__name__)

# ----------------------------
# DATABASE CONFIGURATION
# ----------------------------

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database', 'weather.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ----------------------------
# API KEY (Replace if needed)
# ----------------------------

API_KEY = "cecbf9c638755ca0f64e43358af6786c"

# ----------------------------
# DATABASE MODEL
# ----------------------------

class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    pressure = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Create database
with app.app_context():
    db.create_all()

# ----------------------------
# FETCH WEATHER FUNCTION
# ----------------------------

def fetch_weather():
    city = "Bangalore"

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        print("API Response:", data)

        if response.status_code != 200:
            print("Error:", data.get("message"))
            return None, None, None

        temp = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']

        # Save to database
        new_entry = Weather(
            temperature=temp,
            humidity=humidity,
            pressure=pressure
        )
        db.session.add(new_entry)
        db.session.commit()

        return temp, humidity, pressure

    except Exception as e:
        print("Exception:", e)
        return None, None, None


# ----------------------------
# ROUTES
# ----------------------------

@app.route("/")
def home():
    temp, humidity, pressure = fetch_weather()
    return render_template("index.html",
                           temp=temp,
                           humidity=humidity,
                           pressure=pressure)


@app.route("/history")
def history():
    records = Weather.query.order_by(Weather.timestamp.desc()).all()
    return render_template("history.html", records=records)

@app.route("/graph")
def graph():

    records = Weather.query.order_by(Weather.timestamp).all()

    temps = [r.temperature for r in records]
    times = [r.timestamp for r in records]

    plt.figure(figsize=(8,4))
    plt.plot(times, temps)
    plt.xlabel("Time")
    plt.ylabel("Temperature")
    plt.title("Temperature Trend")

    graph_path = os.path.join("static","graph.png")
    plt.savefig(graph_path)
    plt.close()

    return render_template("graph.html")
# ----------------------------
# RUN APP
# ----------------------------

if __name__ == "__main__":
    app.run(debug=True)