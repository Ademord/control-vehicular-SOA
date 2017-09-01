import cv2
import os
from datetime import datetime
import numpy as NP
import time
from redis import Redis
import uuid

tic = time.clock()

def main():
    #################### Setting up the file ################
    vidcap = cv2.VideoCapture(os.environ.get('TARGET'))
    success, image = vidcap.read(1)  # must read the first frames

    ##################### Setting up parameters ################
    est_tot_frames = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)  # cuadros totales
    n = 14                                                 # intervalo k de cuadros a incluir
    desired_frames = NP.arange(1, est_tot_frames, n)       # cuadros deseados

    #################### Initiate Process ####################
    redis_conn = Redis(host='redis')
    print('cuadros deseados', len(desired_frames), ": " , desired_frames)
    for i in desired_frames:
        vidcap.set(1, i-1)
        success, image = vidcap.read(1)
        if success:
            # Save data about the frame
            array_dtype = str(image.dtype)
            l, w, k = image.shape
            image = image.ravel().tostring()
            # Generate a key
            key = uuid.uuid4()
            item = '{5}#{0}|{1}#{2}#{3}#{4}|{6}'.format(datetime.now(), array_dtype, l, w, k, "", key)
            # Push the data
            redis_conn.set(key, image)
            redis_conn.rpush('reconocer', item)

    vidcap.release()
    toc = time.clock()
    # Get total execution time
    redis_conn.rpush('recolector_times', toc - tic)
    # Kill this process
    redis_conn.rpush('recolector_requests', "{}:{}".format('kill', os.environ.get('HOSTNAME')))


if __name__ == '__main__':
    main()
    # middle = desired_frames[len(desired_frames)//2]
# rs = []
# data = {
#     'ip': 'unset',
#     'frame': image,
#     'specs': key,
#     'timestamp': str(datetime.now())
# }
# rs.append(json.dumps(data))
# # if (i-1) % (n*10) == 0:
# if i == middle:
#     redis_conn.rpush('reconocer', *rs)
#     rs = []
# if rs:
#     redis_conn.rpush('reconocer', *rs)
