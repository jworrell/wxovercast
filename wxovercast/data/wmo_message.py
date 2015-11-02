import re

import wxovercast.data.metar

message_handlers = ((re.compile(r"SA"), wxovercast.data.metar.parse_wmo_metar_message),
                    (re.compile(r"SP"), wxovercast.data.metar.parse_wmo_metar_message),
                    )

def route_message(header, message):
    ''' 
    Routes a WMO message to the correct class to handle it
    '''
    
    for pattern, handler in message_handlers:
        if pattern.match(header):
            return handler(header, message)

    return []