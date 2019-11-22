from flask import Flask, render_template, request
import pusher

app = Flask(__name__)

channels_client = pusher.Pusher(
  app_id='865352',
  key='2929f012f8448e1e7297',
  secret='3718786561642f32bace',
  cluster='us2',
  ssl=True
)
################################################################
import mysql.connector as mariadb

mariadb_connection = mariadb.connect(user='root', password='1234', host='10.20.0.167', database='AirlineStat')
cursor = mariadb_connection.cursor()

cursor.execute("Select AVG(CARRIER_DELAY+WEATHER_DELAY+NAS_DELAY+SECURITY_DELAY+LATE_AIRCRAFT_DELAY ) from flight;")
query1 = cursor.fetchone()
query1 = query1[0]
print(query1)

cursor.execute("Select COUNT(CANCELLED) from flight where CANCELLED=1 and DISTANCE>1000;")
query2 = cursor.fetchone()
query2 = query2[0]
print(query2)

cursor.execute("Select COUNT(CANCELLED) from flight where CANCELLED=1 and DISTANCE<=1000;")
query3 = cursor.fetchone()
query3 = query3[0]
print(query3)

cursor.execute("Select Airport_Desc, COUNT(CANCELLED) "
               "from flight, airport where flight.origin_airport_code = airport.airport_code and CANCELLED =1 group by airport_desc;")
query4 = cursor.fetchall()

cursor.execute("Select SUM(CARRIER_DELAY) as carrier_delay, SUM(WEATHER_DELAY) as weather_delay,sum(NAS_DELAY) as nas_delay, "
               "sum(SECURITY_DELAY) as security_delay,sum(LATE_AIRCRAFT_DELAY) as late_craft_delay From flight;")
query5 = cursor.fetchall()

cursor.execute("Select count(CARRIER_DELAY) as carrier_delay from flight where CARRIER_DELAY >0;")
query6 = cursor.fetchone()
query6 = query6[0]
print(query6)

cursor.execute("Select count(WEATHER_DELAY) as weather_delay from flight where WEATHER_DELAY >0;")
query7 = cursor.fetchone()
query7 = query7[0]
print(query7)

cursor.execute("select count(NAS_DELAY) as nas_delay from flight where NAS_DELAY>0;")
query8 = cursor.fetchone()
query8 = query8[0]
print(query8)

cursor.execute("select count(SECURITY_DELAY) as security_delay from flight where SECURITY_DELAY>0;")
query9 = cursor.fetchone()
query9 = query9[0]
print(query9)

cursor.execute("select count(LATE_AIRCRAFT_DELAY) as late_aircraft_delay from flight where LATE_AIRCRAFT_DELAY>0;")
query10 = cursor.fetchone()
query10 = query10[0]
print(query10)

#######################################################################

@app.route('/')
def dashboard():
    # Display website
    #len = Length of list and then ports over
    return render_template('dashboard.html', query1 = query1, query2 = query2, query3 = query3, len = len(query4), query4 = query4, len1 = len(query5),
                           query5 = query5, query6 = query6, query7 = query7, query8 = query8, query9 = query9, query10 = query10)

if __name__ == '__main__':
   app.run(debug=False)