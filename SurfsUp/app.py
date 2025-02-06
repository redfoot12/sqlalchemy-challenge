# Import the dependencies.
from flask import Flask, jsonify

import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

app = Flask(__name__)


#################################################
# Database Setup
#################################################

# connect to the database
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
# home route
@app.route("/")
def home():
    return(
        f"<center><h2>Welcome to the Hawaii Climate Analysis Local API!</h2></center>"
        f"<center><h3>Select from one of the available routes:</h3></center>"
        f"<center>/api/v1.0/precipitation</center>"
        f"<center>/api/v1.0/stations</center>"
        f"<center>/api/v1.0/tobs</center>"
        f"<center>/api/v1.0/start/end</center>"
        )

# /api/v1.0/precipitation route
@app.route("/api/v1.0/precipitation")
def precip():
    # return the previous year's precipitation as a json
    # Calculate the date one year from the last date in data set/
    previous_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    # Performs a query to retrieve the date and precipitation scores
     # Query the database (session is created and closed properly)
    with Session(engine) as session:
        results = session.query(Measurement.date, Measurement.prcp).\
            filter(Measurement.date >= previous_year).all()
    
    
    # dictionary with the date as the key and the precipitation (prcp) as the value
    precipitation = {date: prcp for date, prcp in results}
    
    # convert to a json
    return jsonify(precipitation)

 #################################################
# Flask Routes
##################################################
# /api/v1.0/stations route
@app.route("/api/v1.0/stations")
def stations():
    # Perform a query to retrieve the names of the stations
    with Session(engine) as session:
        results = session.query(Station.station).all()

    # shows a list of stations
    stationList = list(np.ravel(results))

    # convert to a json and display
    return jsonify(stationList)

# /api/v1.0/tobs route
@app.route("/api/v1.0/tobs")
def temperatures():
    # Calculate the date one year from the last date in data set
    previous_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Perform a query to retrieve the temperatures from the most active stastion from the past year
    with Session(engine) as session:
        results = session.query(Measurement.tobs).\
            filter(Measurement.station == "USC00519281").\
            filter(Measurement.date >= previous_year).all()

    # return the previous year temperatures
    temperatures_list = list(np.ravel(results))

    # convert to a json and display
    return jsonify(temperatures_list)

# /api/v1.0/start/end and /api/v1.0/start routes
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")

# Return min, avg, and max temperature stats for a given date range.
def dateStats(start=None, end=None):

    # select statement
    selection = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]

    with Session(engine) as session:
        if not end:

            start_date = dt.datetime.strptime(start, "%m%d%Y")

            results = session.query(*selection).filter(Measurement.date >= start_date).all()

            session.close()

            temperature_list = list(np.ravel(results))

            # return the list of temperatures
            return jsonify(temperature_list)
    
        else:

            start_date = dt.datetime.strptime(start, "%m%d%Y")
            end_date = dt.datetime.strptime(end, "%m%d%Y")


            results = session.query(*selection)\
                .filter(Measurement.date >= start_date)\
                .filter(Measurement.date <= end_date)\
                .all()

        # return the list of temperatures
        temperature_list = list(np.ravel(results))

        # convert to json
        return jsonify(temperature_list)

## app launcher
if __name__ == "__main__":
    app.run(debug=True)
   