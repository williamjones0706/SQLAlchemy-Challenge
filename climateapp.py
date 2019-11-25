import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipdef():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precip data"""
    # Query precip data
    precip_data = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= '2016-08-23').\
    order_by(Measurement.date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of precip_list
    precip_list = []
    for date, prcp in precip_data:
        precip_dict = {}
        precip_dict["Date"] = date
        precip_dict["Precipitation"] = prcp
        precip_list.append(precip_dict)

    return jsonify(precip_list)


@app.route("/api/v1.0/tobs")
def tobsdef():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of temp data"""
    # Query temp data
    station_temp_12months = session.query(Measurement.date,Measurement.station,Measurement.tobs).\
             filter(Measurement.date >= '2016-08-23').\
             filter(Measurement.station == 'USC00519281').order_by(Measurement.date.desc()).all()

    session.close()

    # Create a dictionary from the row data and append to a list of precip_list
    temp_list = []
    for date, stations, tobs in station_temp_12months:
        temp_dict = {}
        temp_dict["Date"] = date
        temp_dict["Station"] = station
        temp_dict["Tobs"] = tobs
        temp_list.append(temp_dict)

    return jsonify(temp_list)


@app.route("/api/v1.0/stations")
def stationdef():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of station data"""
    # Query temp data
    stations_data= session.query(Station.station)

    session.close()

    # Create a dictionary from the row data and append to a list of precip_list
    station_names = list(np.ravel(stations_data))

    return jsonify(station_names)


@app.route("/api/v1.0/<start>")
def startdatedef():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of temp min max avg data"""
    # Query temp data
    start_date = input("Enter the trip start date in 'YYYY-MM-DD' format: ")
    
    start_date_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of precip_list
    start_list = []
    for min, avg, max in start_date_data:
        temp_start_dict = {}
        temp_start_dict["Min"] = start_date_data [0]
        temp_start_dict["Avg"] = start_date_data [1]
        temp_start_dict["Max"] = start_date_data [2]
        start_list.append(temp_start_dict)

    return jsonify(start_list)


@app.route("/api/v1.0/<start>/<end>")
def startenddatedef():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of temp min max avg data"""
    # Query temp data
    start_date = input("Enter the trip start date in 'YYYY-MM-DD' format: ")
    end_date = input("Enter the trip start date in 'YYYY-MM-DD' format: ")

    startend_date_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of precip_list
    startend_list = []
    for min, avg, max in start_date_data:
        temp_startend_dict = {}
        temp_startend_dict["Min"] = start_enddate_data [0]
        temp_startend_dict["Avg"] = start_enddate_data [1]
        temp_startend_dict["Max"] = start_enddate_data [2]
        start_list.append(temp_startend_dict)

    return jsonify(startend_list)


if __name__ == '__main__':
    app.run(debug=True)
