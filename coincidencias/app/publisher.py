import redis
import json

def publishInRedis(data):

    config = {
        'host': 'redis-15196.c1.eu-west-1-3.ec2.cloud.redislabs.com',
        'port': 15196,
        'db': 0,
    }

    r = redis.StrictRedis(**config)

    payload = {
        'event': 'PlateRegistered',
        'data': {
            'camara': data.camara,
            'lugar': data.lugar,
            'matricula': data.matricula,
            'propietario': data.propietario,
        }
    }

    r.publish('test-channel', json.dumps(payload))
