# import statements

import numpy as np
import pandas as pd
import datetime as datetime
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify

# taken from day 3 activity 10
engine = create_engine("sqlite:///hawaii.sqlite")


Base = automap_base()

Base.prepare(engine, reflect=True)
Station = Base.classes.station
Measurement = Base.classes.measurement
session = Session(engine)

app = Flask(__name__)

# Create the main route that shows you all of the others
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return results that have a date a a corresponding percipitation value"""
    date = session.query(func.max(Measurement.date)).first()
    year_ago =(datetime.datetime.strptime(date[0], '%Y-%m-%d') - datetime.timedelta(days=365)).strftime('%Y-%m-%d')
    prcp_one_year = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date.between(year_ago,date[0])).all()
    
    # Convert list of tuples into a dict
    precipitation_dict = dict(prcp_one_year)

    return jsonify(precipitation_dict=precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all Stations"""
    # Query all passengers
    station_list= session.query(Measurement.station).group_by(Measurement.station).all()
  

    return jsonify(station_list=station_list)
@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of measurements from most active station over the past year"""
    # Query all passengers
    date = session.query(func.max(Measurement.date)).first()
    year_ago =(datetime.datetime.strptime(date[0], '%Y-%m-%d') - datetime.timedelta(days=365)).strftime('%Y-%m-%d')
    temp_one_year = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date.between(year_ago,date[0])).all()
    return jsonify(temp_one_year=temp_one_year)

@app.route("/api/v1.0/<start>")
def start(start=None):
    """Returns minimum, maximum, and average temp after a start ramge"""
    summary = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
    
    return jsonify(summary = summary)
@app.route("/api/v1.0/<start>/<end>")
def startend(start=None, end=None):
    """Returns minimum, maximum, and average temp between a date range"""
    summary_both = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    return jsonify(summary_both = summary_both)


if __name__ == '__main__':
    app.run()