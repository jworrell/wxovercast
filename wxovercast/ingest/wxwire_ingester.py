import cPickle
import logging
import os
import re
import socket
import uuid

import beanstalkc

from sqlalchemy.exc import IntegrityError

import wxovercast.data.metar as metar
import wxovercast.data.wmo_message as wmo_message
import wxovercast.database as database
import wxovercast.settings as settings

INSERT_QUERY = """
INSERT INTO events (event_id, time, location, location_hash, raw_text, airport_id) 
VALUES (%s, %s, %s, MD5(%s), %s, %s)
"""

START_MESSAGE = chr(1)
END_MESSAGE = chr(3)
WMO_HEADER = re.compile(r"[A-Z]{4}[0-9]{2} [A-Z]{4} [0-9]{6}")
D_WMO_HEADER = re.compile("D\x02([A-Z]{4}[0-9]{2} [A-Z]{4} [0-9]{6})")

logging.basicConfig(filename=settings.LOGS['error'],level=logging.DEBUG)

wxwire_settings = settings.get("wxwire")
log_file = os.path.join(settings.LOG_PATH, "failed_wxwire_messages.log")

db_engine = database.engine

beanstalk = beanstalkc.Connection(host='localhost', port=11300)

def handle_message(raw_message):
    split_message = raw_message.split("\r\r\n",3)
    
    try:
        if split_message[0] == "" and split_message[1] == "000 " and WMO_HEADER.match(split_message[2]):
            events = wmo_message.route_message(split_message[2], "\n".join(split_message[3:]))

        elif D_WMO_HEADER.match(split_message[1]):
            events = wmo_message.route_message(split_message[1][2:], "\n".join(split_message[2:]))

        elif split_message[0].startswith("0010") or split_message[0].startswith("1000"):
            #METAR
            events = metar.parse_wxwire_metar_message("\n".join(split_message[1:]))

        elif split_message[0].startswith("0120") or split_message[0].startswith("0140") or split_message[0].startswith("0160"):
            #TAF
            if "TAF" not in raw_message:
                print "Thought this was a TAF :(: ", split_message[:3]
                
            events = []
            
        elif split_message[0].startswith("0050"):
            #PIREP
            if not ("UA"  in raw_message or "UUA" in raw_message):
                print "Thought this was a PIREP :(: ", split_message[:3]
            
            events = []

        else:
            #print "Don't know what this is: ", split_message[:3]
            events = []
            
        if events:
            with db_engine.connect() as connection:
                for evt in events:
                    try:
                        connection.execute(INSERT_QUERY, evt.uuid, evt.time, evt.location, evt.location, evt.message, evt.airport_id)
                        beanstalk.put(cPickle.dumps(evt))

                    except IntegrityError:
                        # We tried to insert a duplicate event, which we don't care about
                        pass

                    except Exception, e:
                        print "insert failed: ", type(e),  e
        
    except Exception, e:
        print "Failed to ingest WxWire message: " + str(e)
        logging.exception("Failed to ingest WxWire message: " + str(e))
    

def read_forever():
    need_data = True
    in_message = False
    
    data_in = ""
    buff = ""
    
    sock = socket.create_connection((wxwire_settings['host'], wxwire_settings['port']))
    
    sock.recv(4096)
    
    connect_string = "log\\%s\\%s\n" %(wxwire_settings['username'], wxwire_settings['password'])
    sock.sendall(connect_string)
    
    while True:
        #print (data_in[:50],buff[:50], in_message)
        
        # If we're in the middle of a message or have no data, get more data
        if need_data:
            data_in = sock.recv(4096)
            need_data = False
        
            if not data_in:
                import datetime
                print "Lost connection at: "
                print datetime.datetime.now()
                break
        
            buff += data_in
        
        # If we're not in the middle of a message, look for one. 
        if not in_message:
            start_pos = buff.find(START_MESSAGE)
            
            if start_pos == -1:
                need_data = True
                continue
            
            in_message = True
            buff = buff[start_pos+1:]
        
        # If we are in the middle of a message, look for the end  
        if in_message:
            end_pos = buff.find(END_MESSAGE)
            
            if end_pos == -1:
                need_data = True
                continue
            
            in_message = False
            
            handle_message(buff[:end_pos])

            buff = buff[end_pos+1:]
