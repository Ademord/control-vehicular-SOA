#!/usr/bin/env python

import time
import rediswq

host="redis"
# Uncomment next two lines if you do not have Kube-DNS working.
# import os
# host = os.getenv("REDIS_SERVICE_HOST")
def status()
    # PRIO 3
    # in case this is an IP, query homestead database for camera status
    # else return UNDEPLOYED
    return None
def deploy()
    # PRIO 1
    # PYKUBE or TOBIs code here to talk to minikube API
    return None
def newRecolectorYAML(itemstr):
    # PRIO 2
    # yaml = load base yaml from template file() 
    # if itemstr == IP: set yaml.env.IP = itemstr
        # this full process should be tested somehow, even if its a camera that has no car plate infront of it 
    # else because itemstr == media : set yaml.env.media = itemstr   
    # reconocedor uses different methods to process an image or a video 
        # to process an image, use processImage method
        # to process a video, use processVideo method
        # to differentiate across these we will use the mimetype
    # coincidencias requires an IP to save the bundle
    # => to be able to support media recognition on coincidencias
        # modifiy coincidencias code 
            # if the ip was set to 'unset'
                # dont verify that the ip exists
                # don't look up a place name, use 'unset' or the ip's name

q = rediswq.RedisWQ(name="ip", host="redis")
print("Worker with sessionID: " +  q.sessionID())
print("Initial queue state: empty=" + str(q.empty()))
while True:
    if not q.empty():
      item = q.lease(lease_secs=10, block=True, timeout=2) 
      if item is not None:
        itemstr = item.decode("utf=8")
        print("Working on " + itemstr)
        time.sleep(10) # Put your actual work here instead of sleep.
        if status(itemstr) == 'UNDEPLOYED':
            deploy(newRecolectorYAML(itemstr))


        q.complete(item)
      else:
        print("Waiting for work")
    print("Queue empty, exiting")
