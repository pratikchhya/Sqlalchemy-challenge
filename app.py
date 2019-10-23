import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc

from flask import Flask, jsonify
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)
# Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def Hawaii():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipitaion with date"""
    # Query all precipitaion
    prcp_data= session.query(Measurement.date, Measurement.prcp).all()
    print(prcp_data)

    session.close()

    # Convert list of tuples into normal list
    # Prcption = list(np.ravel(prcp_data))

    all_data = []
    for date, prcp in prcp_data:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_data.append(prcp_dict)

    return jsonify(all_data)
    
@app.route("/api/v1.0/stations")
def stations():

   # Query all stations
   station_results = session.query(Station.station).all()

   # Convert list of tuples into normal list
   station_list = list(np.ravel(station_results))
   return jsonify(station_list)


@app.route("/api/v1.0/<start>")
def start(start):
    results = (session.query(*data).filter(Measurement.station==Station.station)).filter(Measurement.date>=start_date).group_by(Station.name).order_by(func.sum(Measurement.prcp).desc()).all()
    print(results)
session.close()
temps = list(np.ravel(results))
return jsonify(temps)


@app.route("/api/v1.0/<start>/<end>")
def startend(start,end):
    result = (session.query(*data)).filter(Measurement.station==Station.station).filter(Measurement.date>=start_date).\
         filter(Measurement.date<=end_date).group_by(Station.name).order_by(func.sum(Measurement.prcp).desc()).all()
    print(result)

session.close()
temp = list(np.ravel(result))
return jsonify(temp)






    if __name__ == '__main__':
        app.run(debug=True)
