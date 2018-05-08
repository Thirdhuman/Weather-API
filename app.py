# # Step 4 - Climate App

# Now that you have completed your initial analysis, design a Flask api based on the queries that you have just developed.
# Use FLASK to create your routes.

# Routes
# /api/v1.0/precipitation

# Query for the dates and temperature observations from the last year.
# Convert the query results to a Dictionary using date as the key and tobs as the value.
# Return the json representation of your dictionary.
# /api/v1.0/stations

# Return a json list of stations from the dataset.
# /api/v1.0/tobs

# Return a json list of Temperature Observations (tobs) for the previous year
# /api/v1.0/<start> and /api/v1.0/<start>/<end>

# Return a json list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
#################################################

# dependencies 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, desc
from sqlalchemy.sql import label
import datetime as dt
import numpy as np
import pandas as pd
from flask import Flask, jsonify
# Database Setup
#################################################
engine = create_engine("sqlite:///./Resources/hawaii.sqlite", echo=False)
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurements
Station = Base.classes.stations
session = Session(engine)
#################################################
# Flask
app = Flask(__name__)
#################################################
@app.route("/")
def welcome():
    """Select Routine."""
    return (
        "Hawaii Weather Data<br/><br/>"
        "Pick from the available routes below:<br/><br/>"
        "Precipiation from 2016-08-23 to 2017-08-23.<br/>"
        "/api/v1.0/precipitation<br/><br/>"
        "list of all Hawaii weather stations.<br/>"
        "/api/v1.0/stations<br/><br/>"
        "The Temperature Observations (tobs) from 2016-08-23 to 2017-08-23.<br/>"
        "/api/v1.0/tobs<br/><br/>"
        "Type in a single date to see the min, max, and avg temperature since that date.<br/>"
        "/api/v1.0/temp/<start><br/><br/>"
        "Type a date range to see the min, max, and avg temperature for that range.<br/>"
        "/api/v1.0/temp/<start>/<end><br/>"
    )
#################################################
# Return precipitation.
@app.route("/api/v1.0/precipitation")
def precipitation():
    """ Return a list of measurement date and prcp information from the last year """
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').order_by(Measurement.date)
    precipitation_values = []
    for p in results:
        prcp_dict = {}
        prcp_dict["date"] = p.date
        prcp_dict["prcp"] = p.prcp
        precipitation_values.append(prcp_dict)
    return jsonify(precipitation_values)
#################################################
# Return a json list of stations.
@app.route("/api/v1.0/stations")
def stations():
    """Return list of all station names"""
    results = session.query(Station.name).all()
    station_names = list(np.ravel(results))
    return jsonify(station_names)
#################################################
# Return list (tobs) for the prev year
@app.route("/api/v1.0/tobs")
def tobs():
    """Return list of all temperature observations for the previous year"""
    results = session.query(Measurement.tobs).all()
    tobs_values = list(np.ravel(results))
    return jsonify(tobs_values)
#################################################
# json list min temperature,  avg temperature, and max 
@app.route("/api/v1.0/<start>")
def temperatures_start(start):
    """ with start only, calculate TMIN, TAVG, and TMAX for all dates greater than 
        and equal to the start date. 
    """
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    temperatures_start = list(np.ravel(results))
    return jsonify(temperatures_start)
#################################################
# from start and the end date, calculate the TMIN, TAVG, and TMAX 
@app.route("/api/v1.0/<start>/<end>")
def temperatures_start_end(start, end):
    """ given the start and the end date, calculate the TMIN, TAVG, TMAX for dates between the start and end date inclusive.
    """
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    temperatures_start_end = list(np.ravel(results))
    return jsonify(temperatures_start_end)
#################################################
if __name__ == "__main__":
    app.run(debug=False)