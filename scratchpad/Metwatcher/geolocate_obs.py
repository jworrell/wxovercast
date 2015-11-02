import pyproj
import sqlite3
import time

OBS_LOCATION = "/Users/jworrell/Desktop/obs.txt"
DATA_LOCATION = "/Users/jworrell/Desktop/airports.db"

SELECT_SQL_NOBOX = """SELECT name, latitude_deg, longitude_deg FROM airports 
                      WHERE ident = ? """

SELECT_SQL = """SELECT name, latitude_deg, longitude_deg FROM airports 
                WHERE ident = ?
                AND latitude_deg < ? AND longitude_deg < ? 
                AND latitude_deg > ? AND longitude_deg > ? """

geod = pyproj.Geod(ellps="WGS84")

obs_list = []
results_list = []

with open(OBS_LOCATION) as obs_file:
    while True:
        obs_file.readline()
        ob = obs_file.readline()[:-1]
        obs_file.readline()
        
        if ob:
            obs_list.append(ob)
        else:
            break
            
start_work = time.time()

with sqlite3.connect(DATA_LOCATION) as airports_conn:
    results = airports_conn.execute(SELECT_SQL_NOBOX, ("KOFF",)).fetchone()
    koff, koff_lat, koff_long = results
    print koff, koff_lat, koff_long
    
    for ob in obs_list:
        ob_tokens = ob.split()
        
        if "TS" in ob or "LTG" in ob:
            #criterea = (ob_tokens[0], koff_lat+10, koff_long+10, koff_lat-10, koff_long-10)
            #results = airports_conn.execute(SELECT_SQL, criterea).fetchone()
            
            results = airports_conn.execute(SELECT_SQL_NOBOX, (ob_tokens[0],)).fetchone()
            
            if results:
                name, latitude_deg, longitude_deg = results
                dist = geod.inv(koff_long, koff_lat, longitude_deg, latitude_deg)[2]
                
                #if dist < 80467.2:
                results_list.append((dist,name,ob))

print "Done in ", time.time() - start_work, " got ", len(results_list), "obs."

results_list.sort()

for x in xrange(25):
    dist, name, ob = results_list[x]
    
    print round(0.000621371 * dist), name, ob
