import re

import wxovercast.database as wx_db

from wxovercast.lib.metar.Metar import Metar, ParserError
from wxovercast.data.event import WxEvent, LocationNotFound, TimeNotFound

LOCATION_QUERY = "SELECT location FROM airports WHERE airport_id = %s"

SPACE_REGEX = re.compile(r"\W+")
SAO_REGEX = re.compile(r"[A-Z]{3} (SA|SP) [0-9]{4}")

def parse_metar(body, connection=None):
    if connection is None:
        engine = wx_db.engine
        connection = engine.connect()

    m = Metar(body)

    if m.time is None:
        raise TimeNotFound() 
    
    if m.station_id is None:
        raise LocationNotFound()
        
    location = connection.execute(LOCATION_QUERY, m.station_id).fetchone()
    
    if location is None:
        raise LocationNotFound()
   
    return WxEvent(location[0], m.time, body, m.station_id)

def parse_metars(metars, prepend=None):
    engine = wx_db.engine
    events = []
    
    with engine.connect() as connection:
        for metar in metars:
            metar = SPACE_REGEX.sub(" ", metar).strip()
            
            if not metar:
                continue
            
            if prepend:
                metar = prepend + " " + metar
            
            try:
                new_metar = parse_metar(metar, connection)
                if new_metar:
                    events.append(new_metar)
    
            except ParserError:
                pass
    
            except LocationNotFound:
                pass
            
            except TimeNotFound:
                pass
    
            except Exception, e:
                print type(e), str(e)
    
    return events

def parse_wxwire_metar_message(message):
    return parse_metars(message.split("\x1e"))

def parse_wmo_metar_message(header, message):
    events = []
    
    inner_header, _, actual_message = [s.strip() for s in message.partition("\n")]
    
    # We have a SAO Surface Aviation Observation report. Message. Ignore it.
    if SAO_REGEX.match(inner_header):
        return events
        
    elif inner_header in ["METAR", "SPECI"]:
        message = actual_message
        prepend = inner_header
        
    elif len(inner_header) == 6 and inner_header.startswith("MTR"):
        message = actual_message
        prepend = None
        
    else:
        prepend = None
    
    events = parse_metars(message.split("="), prepend)
    
    return events
