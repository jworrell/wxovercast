#import cPickle

import beanstalkc
import redis

def fetch_forever(host, port):
    beanstalk_conn = beanstalkc.Connection(host=host, port=port)
    redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0)
    
    while beanstalk_conn:
        job = beanstalk_conn.reserve()
        
        try: 
            redis_conn.publish("events", job.body)
        
        except Exception, e:
            print e
        
        finally:
            job.delete()