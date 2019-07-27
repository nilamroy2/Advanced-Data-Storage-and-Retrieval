import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func


import datetime as dt
import numpy as np
import pandas as pd
from flask import Flask, jsonify

# Create an engine for database
engine = create_engine('sqlite:///Resources/hawaii.sqlite')
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

#make references to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

#create a session
session = Session(engine)
#make an app instance
app = Flask(__name__)
#index route
@app.route('/')
def index():
    return(
        f"<bold>Welcome to the Hawaiian Climate API!<br/><br/></bold>"
        f" Available Routes:<br/>"
        f" /api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations</br>"
        f"/api/v1.0/tobs</br>"
        f"api/v1.0/'startdate as 2017-8-23'</br>"
        f"/api/v1.0/'startdate as 2017-8-23'/'enddate as 2017-9-7'<br>"
    )
@app.route('/api/v1.0/precipitation')
def precipitation():
    first_date =  dt.date(2017,8, 23) - dt.timedelta(days=365)
    year_ago_prcp = session.query(Measurement.date, Measurement.prcp).\
                        filter(Measurement.date > first_date).\
                        order_by(Measurement.date).all()
#convert the query results to a dict using date as the key and prcp as the value
 
    #prep_dict = dict(year_ago_prcp)
    prcp_dict = {}
    for rain in year_ago_prcp:
     prcp_dict[str(rain.date)] = rain.prcp
     #return the json representation of the dict
    return jsonify(prcp_dict)

    
# list of station
@app.route('/api/v1.0/stations')
def stations():
#get a list of all the stations
    station_list = session.query(Station.station).all()
#convert list of tuples into normal list
    station_rav = list(np.ravel(station_list))
    return jsonify(station_rav)


#temperature observations for the last 12 months
@app.route('/api/v1.0/tobs')
def temp_obs():
    first_date = dt.date(2017,8, 23) - dt.timedelta(days=365)
#find the one previous year temperature
    temp_prev=session.query(Measurement.date,Measurement.tobs).\
               filter(Measurement.date >first_date).all()
#convert the tuple to list
    temp_rav=list(np.ravel(temp_prev))
#return json representation of list
    return jsonify(temp_rav)

# find the min,max,avarage temperature


@app.route('/api/v1.0/<start>')
@app.route('/api/v1.0/<start>/<end>')
def temperature(start=None,end=None):
#when given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive'''
    if end != None:
        temp_start_end = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
                         filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    
#When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.  
    else:
        temp_start_end = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
                          filter (Measurement.date >= start).all()
    #convert list of tuple into normal list
    temp_start_end_rav = list(np.ravel(temp_start_end))
    return jsonify(temp_start_end_rav)

if __name__ == '__main__':
    app.run(debug=True)