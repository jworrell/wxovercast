import cPickle
import redis

redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0)
redis_sub = redis_conn.pubsub()
redis_sub.subscribe("events")

for event in redis_sub.listen():
    try:
        event = cPickle.loads(event["data"])
        print event.message
    except: 
        print "failed to unpickle ", event