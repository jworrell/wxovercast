import csv
import gzip
import pyproj
import StringIO
import sqlite3
import urllib2

METERS_IN_MILE = 1609.34

def get_gzip_local_obs():
    return open("/Users/jworrell/Desktop/metars.cache.csv.gz")

def get_gzip_nws_obs():
    OBS_LOCATION = "http://aviationweather.gov/adds/dataserver_current/current/metars.cache.csv.gz"

    gz_reader = urllib2.urlopen(OBS_LOCATION)
    
    print gz_reader.info()
    
    gz_data = gz_reader.read()
    return StringIO.StringIO(gz_data)

def main():
    geod = pyproj.Geod(ellps="WGS84")
    select_statement = "SELECT name, latitude_deg, longitude_deg FROM airports WHERE ident = ?"
    airports_conn = sqlite3.connect("/Users/jworrell/Desktop/airports.db")
    results = airports_conn.execute(select_statement, ("KOFF",)).fetchone()
    koff, koff_lat, koff_long = results
    
    print "Looking at %s" %koff
        
    #gz_file = get_gzip_local_obs()
    gz_file = get_gzip_nws_obs()
    
    with gzip.GzipFile(fileobj=gz_file) as raw_reader:
        csv_reader = csv.reader(raw_reader)
        found_header = False
        for ob in csv_reader:
            if len(ob) == 1:
                continue
            elif not found_header:
                found_header = True
                continue
            
            metar = ob[0]
            ob_lat = ob[3]
            ob_long = ob[4]
            
            try:
                dist = geod.inv(koff_long, koff_lat, ob_long, ob_lat)[2] / METERS_IN_MILE
                
                if (dist < 1000) and ("LGT" in metar or "TS" in metar) and ("TSNO" not in metar):
                    print str(round(dist)).ljust(10), metar
            
            except:
                pass
            
if __name__ == "__main__":
    main()
