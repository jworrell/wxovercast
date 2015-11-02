import csv
import gzip
import StringIO
import urllib2

METAR_URL = "http://aviationweather.gov/adds/dataserver_current/current/metars.cache.csv.gz"

METAR_FIELDS = ['raw_text',
                'station_id', 
                'observation_time', 
                'latitude', 
                'longitude', 
                'temp_c', 
                'dewpoint_c', 
                'wind_dir_degrees', 
                'wind_speed_kt', 
                'wind_gust_kt', 
                'visibility_statute_mi', 
                'altim_in_hg', 
                'sea_level_pressure_mb', 
                'corrected', 
                'auto', 
                'auto_station', 
                'maintenance_indicator_on', 
                'no_signal', 
                'lightning_sensor_off', 
                'freezing_rain_sensor_off', 
                'present_weather_sensor_off', 
                'wx_string', 
                'sky_cover', 
                'cloud_base_ft_agl', 
                'sky_cover', 
                'cloud_base_ft_agl', 
                'sky_cover', 
                'cloud_base_ft_agl', 
                'sky_cover', 
                'cloud_base_ft_agl', 
                'flight_category', 
                'three_hr_pressure_tendency_mb', 
                'maxT_c', 
                'minT_c', 
                'maxT24hr_c', 
                'minT24hr_c', 
                'precip_in', 
                'pcp3hr_in', 
                'pcp6hr_in', 
                'pcp24hr_in', 
                'snow_in', 
                'vert_vis_ft', 
                'metar_type', 
                'elevation_m']

class HeadRequest(urllib2.Request):
    def get_method(self):
        return 'HEAD'

class SensibleWxEvent(object):
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        
        self.max_wind = None
        self.raw = None
    
class MetwatchCriterea(object):
    def __init__(self, test):
        self.test = test
        
    def testEvent(self, evt):
        return self.test(evt)
    
def fetch_metars(last_modified=None):
    '''
    request = urllib2.Request(METAR_URL)
    
    if last_modified:
        request.add_header("if-Modified-Since", last_modified)
    
    result = urllib2.urlopen(request)
    '''
    
    result = open("dummy_metars.csv.gz")
    result_reader = StringIO.StringIO(result.read())
    gzip_reader = gzip.GzipFile(fileobj=result_reader)
    csv_reader = csv.DictReader(gzip_reader, METAR_FIELDS)
    
    for _ in xrange(6):
        csv_reader.next()
    
    metars = []
    for metar in csv_reader:
        try:
            event = SensibleWxEvent(float(metar["latitude"]), float(metar["longitude"]))
        except:
            continue
        
        try:
            gust = float(metar['wind_gust_kt'])
        except:
            gust = 0
            
        try:
            sustained = float(metar['wind_speed_kt'])
        except:
            sustained = 0;
        
        event.max_wind = gust if gust > sustained else sustained
        event.raw = metar["raw_text"]
    
        metars.append(event)
    
    return metars
    
if __name__ == "__main__":
    """
    request = HeadRequest(METAR_URL)
    result = urllib2.urlopen(request)
    last_modified = result.headers["Last-Modified"]
    """
    
    criterea = [MetwatchCriterea(lambda evt:evt.max_wind >= 35),]
    
    events = fetch_metars()
    
    for event in events:
        for crt in criterea:
            if crt.testEvent(event):
                print event.max_wind, event.raw
