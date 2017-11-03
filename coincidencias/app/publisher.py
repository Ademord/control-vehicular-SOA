import redis
import json

def publishInRedis(data):

    config = {
        'host': 'redis',
        'port': 6379,
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
