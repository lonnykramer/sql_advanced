# 1. import dependencies

import numpy as numpy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///./hawaii.sqlite")



# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
Base.classes.keys()
print('Base.classes.keys()')

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


#################################################
# Flask Setup
#################################################
# 2. Create an app, being sure to pass __name__
app = Flask(__name__)


# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    # this only prints to the terminal below, not the website
    return (
            "Welcome to my Hawaii Weather (aka: homework assignmentfor unit 10) Home page! <br/><br/>"
        
    #################################################
    # Flask Routes
    #################################################
            f"Available Routes:<br/><br/>"
            f"/api/v1.0/precipitation <br/>"
            f"/api/v1.0/stations <br/>"
            f"/api/v1.0/tobs <br/>"
            f"/api/v1.0/(start_date as 'yyyy-mm-dd') <br/>"
            f"/api/v1.0/(start_date as 'yyyy-mm-dd')/(end_date as 'yyyy-mm-dd') <br/>"
            )


#### PRECIPITATION ####

# 4. Define what to do when a user hits the /precip route
@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for 'Precipitation' page...")
    # this only prints to the terminal below, not the website
        
    # create our session (link) from python to the db
    session = Session(engine)
    #return "Welcome to the Hawaii 'Precipitation' page!"    

    """Return a list of all the Dates and Precip Amounts"""
    
    # get last year date and query Measurement table
    query_date = dt.date(2017,8,23) - dt.timedelta(days=366)
    twelve_months_precip = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > query_date).order_by(Measurement.date).all()
    
    session.close()

    # create a dictionary for precipitation data
    date_precip = []
    for date, prcp in twelve_months_precip:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        date_precip.append(precip_dict)


    return jsonify(date_precip)

#### STATIONS ####

# 5. Define what to do when a user hits the /stations route
@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'Stations' page...")
    # this only prints to the terminal below, not the website
    #return "Welcome to the Hawaii 'Stations' page!" 
    session = Session(engine)

    # Query all stations - as example
    results = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    
    
    session.close()


    return jsonify(results)

#### TOBS ####

# 6. Define what to do when a user hits the /tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'TOBs' page...")
    # this only prints to the terminal below, not the website 

    # create our session (link) from python to the db
    session = Session(engine)

    """Return a list of all the Dates and Tobs Amounts"""

    # Calculate the date 1 year ago from the last data point in the database
    # 2016 was a leap year
    # get last year date and query Measurement table
    query_date = dt.date(2017,8,23) - dt.timedelta(days=366)
    twelve_months_tobs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > query_date).order_by(Measurement.date).all()
    
    session.close()

    # create a dictionary for precipitation data
    date_tobs = []
    for date, tobs in twelve_months_tobs:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        date_tobs.append(tobs_dict)

      
    return jsonify(date_tobs)
    

#### START DATE ####

# 7. Define what to do when a user hits the /<start> route
@app.route("/api/v1.0/<start>")
def start_tobs(start):
    """Fetch the start_date that start matches the path variable supplied by the user, or a 404 if not."""
    print("Server received request for 'Start Date' page...")
    # create our session (link) from python to the db
    session = Session(engine)

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
           filter(Measurement.date >= start).all()
    
    session.close()
    
    tcalc_collect = []
    for a,b,c in results:
       temp_d = {}
       temp_d["minimum_temp"] = a
       temp_d["average_temp"] = b
       temp_d["maximum_temp"] = c
       tcalc_collect.append(temp_d)
    return jsonify(tcalc_collect)
    
    
    
#### END DATE ####

# 8. Define what to do when a user hits the /<start>/<end> route
@app.route("/api/v1.0/<start>/<end>")
def end(start, end):
    """Fetch the end_date that end matches the path variable supplied by the user, or a 404 if not."""
    print("Server received request for 'End Date' page...")


    # create our session (link) from python to the db
    session = Session(engine)

# This function called `calc_temps` will accept start date and end date in the format '%Y-%m-%d' 
# and return the minimum, average, and maximum temperatures for that range of dates
    

 
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
   
    session.close()
   
   
    tcalc_collect = []
    for a,b,c in results:
       temp_d = {}
       temp_d["minimum_temp"] = a
       temp_d["average_temp"] = b
       temp_d["maximum_temp"] = c
       tcalc_collect.append(temp_d)
    return jsonify(tcalc_collect)
    


if __name__ == "__main__":
    app.run(debug=True)