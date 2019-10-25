import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
engine = create_engine("sqlite:///C:\Rutgers\Homework\Sqlalchemy-challenge\Resources\hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)
app = Flask(__name__)

maxdate = (session.query(Measurement.date)
           .order_by(Measurement.date.desc()).first())
maxdate = list(np.ravel(maxdate))[0]

maxdate2 = dt.datetime.strptime(maxdate, "%Y-%m-%d")
maxdate2 = maxdate2.timetuple()

year = maxdate2[0]-1
month = maxdate2[1]
day = maxdate2[2]
last12m = dt.date(year, month, day)

start_date = dt.date(2017,7,20)
end_date= dt.date(2017,7,30)

def calc_temps(start_date, end_date):
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()


@app.route("/")
def hawaii():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return a list of all passenger names"""
    # Query all 
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()
    all_prcps = []
    for date, prcp in results:
        measurement_dict = {}
        measurement_dict["date"] = date
        measurement_dict["prcp"] = prcp
        all_prcps.append(measurement_dict)
    return jsonify(all_prcps)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query all passengers
    results = session.query(Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    session.close()
  
    all_stations = []
    for name, latitude, longitude, elevation in results:
        station_dict = {}
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        all_stations.append(station_dict)
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
 
   session = Session(engine)
   #Query all tobs
   tobs_results = session.query(Measurement.station, Measurement.tobs).filter(Measurement.date.between('2016-08-01', '2017-08-01')).all()
   tobs_list=[]
   for tobs in tobs_results:
       tobs_dict = {}
       tobs_dict["station"] = tobs[0]
       tobs_dict["tobs"] = float(tobs[1])
       tobs_list.append(tobs_dict)
   return jsonify(tobs_list)

@app.route('/api/v1.0/<start>')
def start(start):
    session = Session(engine)
    results=(session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs))
    .filter(Measurement.date>=start_date).all())
    trvl=list(np.ravel(results))   
    return jsonify(trvl) 

@app.route('/api/v1.0/<start>/<end>')
def start_end(start, end):
        session = Session(engine)
        results1=(session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs))
       .filter(Measurement.date>=start_date).filter(Measurement.date<=end_date).all())
        return jsonify(results1)

   
    

if __name__ == '__main__':
    app.run(debug=True)    
