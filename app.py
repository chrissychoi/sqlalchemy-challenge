import numpy as np
from datetime import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# import os
# cwd=os.getcwd()
# print("current work directory is:{}".format(cwd))

engine = create_engine("sqlite:///Documents/GitHub/sqlalchemy-challenge/Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine,reflect = True)

session = Session(engine)

Station = Base.classes.station
Measurement = Base.classes.measurement

app = Flask(__name__)

# 1. list all routes available
@app.route("/")
def index():
    return (
        f"Welcome to weather stations API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/'input start date in the format of %y-%m-%d <br/>"
        f"/api/v1.0/'start date'/'end date of the same format'<br/>"
    )

# 2.Convert the query results to a dictionary using date as the key and prcp as the value.
#Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def prcp():
    results = session.query(Measurement.date,Measurement.prcp).all()
    session.close()

    date_prcp = []
    for date, prcp in results:
        date_prcp_dict = {}
        date_prcp_dict["date"] = date
        date_prcp_dict["prcp"] = prcp
        date_prcp.append({date:prcp})

    return jsonify(date_prcp)

#3.Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    session.close()

    stn_stn = list(np.ravel(results))

    return jsonify(stn_stn)

#4.Query the dates and temperature observations of the most active station for the last year of data.
#Return a JSON list of temperature observations (TOBS) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    
    results = session.query(Measurement.tobs).\
    filter(Measurement.station=='USC00519281', Measurement.date > '2016-08-22' ).all()
    session.close()

    most_active_last_year = list(np.ravel(results))
    return jsonify(most_active_last_year)


# #5.Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# #When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
# #When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
@app.route("/api/v1.0/<start_date>")
def calc_temp(start_date):


    startDate = dt.strptime(start_date,'%Y-%m-%d')
    temp_calc = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
    filter(Measurement.date >= startDate).filter(Measurement.date <= '2017-08-23').all()
    session.close()

    calc_results = []
    for TMIN, TAVG, TMAX in temp_calc:
        calc_dict = {}
        calc_dict['TMIN'] = TMIN
        calc_dict['TAVG'] = TAVG
        calc_dict['TMAX'] = TMAX
        calc_results.append(calc_dict)

    
    return jsonify(calc_results)

@app.route("/api/v1.0/<start_date>/<end_date>")
def calc_temps(start_date, end_date):
    
    startDate = dt.strptime(start_date,'%Y-%m-%d')
    endDate = dt.strptime(end_date,'%Y-%m-%d')

    temps_calc = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= startDate).filter(Measurement.date <= endDate).all()
    session.close()

    calc_results = []
    for TMIN, TAVG, TMAX in temps_calc:
        calc_dict = {}
        calc_dict['TMIN'] = TMIN
        calc_dict['TAVG'] = TAVG
        calc_dict['TMAX'] = TMAX
        calc_results.append(calc_dict)

    return jsonify(calc_results)
   
           
if __name__ == "__main__":
    app.run(debug=True)
