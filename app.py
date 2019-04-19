import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Flask Setup
app = Flask(__name__)

@app.route("/")
def home():
    # Home page
    # List all routes that are available
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

# Flask Routes
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Convert the query results to a Dictionary using date as the key and prcp as the value.
    # Return the JSON representation of your dictionary.
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    year_from_last_date = dt.date(2017, 8,23) - dt.timedelta(days=364)

    # Perform a query to retrieve the date and precipitation scores sorted by date
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date>=year_from_last_date).order_by(Measurement.date).all()

    results_dict = []
    for date, prcp in results:
        entry_dict = {}
        entry_dict["date"] = date
        entry_dict["prcp"] = prcp
        results_dict.append(entry_dict)

    return jsonify(results_dict)

@app.route("/api/v1.0/stations")
def stations():
    # Return a JSON list of stations from the dataset.
    results = session.query(Station.station, Station.name).all()
    results_dict = []
    for station, name in results:
        entry_dict = {}
        entry_dict["station"] = station
        entry_dict["name"] = name
        results_dict.append(entry_dict)
    return jsonify(results_dict)

@app.route("/api/v1.0/tobs")
def tobs():
    # Query for the dates and temperature observations from a year from the last data point.
    # Return a JSON list of Temperature Observations (tobs) for the previous year.
    year_from_last_date = dt.date(2017, 8,23) - dt.timedelta(days=364)

    # Perform a query to retrieve the date and precipitation scores sorted by date
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date>=year_from_last_date).order_by(Measurement.date).all()

    results_dict = []
    for date, tobs in results:
        entry_dict = {}
        entry_dict["date"] = date
        entry_dict["tobs"] = tobs
        results_dict.append(entry_dict)

    return jsonify(results_dict)

@app.route("/api/v1.0/<start>")
def start():
    # Return a JSON list of the minimum temperature, the average temperature, 
    # and the max temperature for a given start or start-end range.
    # When given the start only, calculate TMIN, TAVG, and TMAX for 
    # all dates greater than and equal to the start date.
    return "start"

@app.route("/api/v1.0/<start>/<end>")
def start_end():
    # Return a JSON list of the minimum temperature, the average temperature, 
    # and the max temperature for a given start or start-end range.
    # When given the start and the end date, calculate the TMIN, TAVG, and TMAX for 
    # dates between the start and end date inclusive.
    return "start end"

if __name__ == "__main__":
    app.run(debug=True)
