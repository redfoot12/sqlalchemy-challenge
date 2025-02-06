## sqlalchemy-challenge
Creating initial repository for the Module 10 Challenge

Overview
This project analyzes historical climate data using SQLAlchemy, Pandas, Matplotlib, and Flask. It includes a Jupyter Notebook for data exploration and a Flask API for querying weather data.
Project Files
upyter Notebook (climate.ipynb)
Queries precipitation & temperature data from SQLite using SQLAlchemy
Plots precipitation trends over the last year
Analyzes temperature observations from the most active station
Generates summary statistics
Flask API (app.py)
Creates an API with the following routes:

/api/v1.0/precipitation → Returns precipitation data
/api/v1.0/stations → Lists available weather stations
/api/v1.0/tobs → Temperature observations
/api/v1.0/<start> and /api/v1.0/<start>/<end> → Temperature stats for given dates
