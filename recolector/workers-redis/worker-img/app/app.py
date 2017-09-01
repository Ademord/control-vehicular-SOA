import cv2
import os
from datetime import datetime
import json
from redis import Redis
import uuid

def main():
    print(os.environ.get('TARGET_SERVICE', 'http://reconocedor'))
    print(os.environ.get('TARGET'))

    # IMAGE RECOGNITION
    image = cv2.imread(os.environ.get('TARGET'), 0)
    # data = {
    #     'ip': 'unset',
    #     'frame': frame.tolist(),
    #     'timestamp': str(datetime.now())
    # }
    # redis_conn.rpush('reconocer', json.dumps(data))
    array_dtype = str(image.dtype)
    l, w = image.shape
    string_image = image.ravel().tostring()
    # Generate a key
    key = uuid.uuid4()
    item = '{5}#{0}|{1}#{2}#{3}#{4}|{6}'.format(datetime.now(), array_dtype, l, w, 1, "", key)
    # Push the data
    redis_conn = Redis(host='redis')
    redis_conn.set(key, string_image)
    redis_conn.rpush('reconocer', item)
    redis_conn.rpush('test', item)
    redis_conn.rpush('recolector_requests', "{}:{}".format('kill', os.environ.get('HOSTNAME')))

if __name__ == '__main__':
    main()
