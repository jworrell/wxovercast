import uuid

class LocationNotFound(Exception):
    pass

class TimeNotFound(Exception):
    pass

class WxEvent():
    def __init__(self, location, time, message, airport_id=None):
        self.uuid = str(uuid.uuid1())
        self.location = location
        self.time = time
        self.message = message
        self.airport_id = airport_id
        