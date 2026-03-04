# Weather Data Logger 🌦️

A Flask-based web application that collects real-time weather data from the OpenWeatherMap API and stores it in a SQLite database. The application logs weather data periodically and displays historical data and temperature trends.

## Features
- Real-time weather data retrieval
- Automatic logging every 30 seconds
- Weather history tracking
- Temperature trend graph visualization
- Flask backend with SQLite database

## Tech Stack
- Python
- Flask
- SQLAlchemy
- SQLite
- HTML/CSS
- OpenWeatherMap API

## Project Structure
Weather_app/
│
├── app.py
├── requirements.txt
├── README.md
│
├── database/
│   └── weather.db
│
├── templates/
│   ├── index.html
│   ├── history.html
│   └── graph.html
│
└── static/
    ├── style.css
    └── graph.png

## How to Run

Install dependencies:

pip install -r requirements.txt

Run the application:

python app.py

Open browser:

http://127.0.0.1:5000