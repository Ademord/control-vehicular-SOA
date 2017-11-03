#!/usr/bin/env python
# coding=utf-8
import threading
import os
import pykube, yaml
import requests
import uuid
import rediswq
import time
import logging
from math import sqrt
from redis import Redis


# decorator to thread functions
def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper

class KubernetesConnectError(BaseException): pass

class Minikube():
    def __init__(self, data_path='data', config_file='k8s_config', prefix='k8s_'):
        self.data_path = data_path
        self.config_file = config_file
        self.files_prefix = prefix
        # Connect to API
        self.directory = os.path.abspath(os.path.join(os.path.dirname(__file__), self.data_path))
        k8s_config_file = os.path.abspath(os.path.join(self.directory, self.config_file))
        self.api = pykube.HTTPClient(pykube.KubeConfig.from_file(k8s_config_file))
        # Get all templates
        self.files = [os.path.join(self.directory, filename) for filename in os.listdir(self.directory)
                      if filename.startswith(self.files_prefix) and filename.endswith('.yaml')]

    def deploy(self, obj):
        if obj['kind'] == 'Deployment':
            logging.info('Starting Deployment... ' + obj['metadata']['name'])
            pykube.Deployment(self.api, obj).create()
        elif obj['kind'] == 'Service':
            logging.info('Starting Service... ' + obj['metadata']['name'])
            pykube.Service(self.api, obj).create()
        elif obj['kind'] == 'Pod':
            logging.info('Starting Pod... ' + obj['metadata']['name'] + '(' + obj['spec']['containers'][0]['image'] + ')')
            pykube.Pod(self.api, obj).create()

    def load_template(self, file):
        with open(file, 'r') as stream:
            try:
                return yaml.load(stream)  # type: dictionary
            except yaml.YAMLError as exc:
                logging.info(exc)

    def deploy_templates(self, image, name, env=None):
        # Loop files that must be deployed
        for file in self.files:
            # 1. Try to load the file
            obj = self.load_template(file)
            # Adjust template variables
            obj['spec']['containers'][0]['image'] = image
            obj['metadata']['name'] = name
            if env: obj['spec']['containers'][0]['env'].append(env)
            # 2. Deploy Templates
            self.deploy(obj)

    def delete_pod(self, name):
        obj = {
            'apiVersion': 'v1',
            'kind': 'Pod',
            'metadata': {
                'name': name,
                'namespace': 'default'
            }
        }
        logging.info('Deleting...{}'.format(name))
        pykube.Pod(self.api, obj).delete()

def Fibo(n):
    return ((1+sqrt(5))**n-(1-sqrt(5))**n)/(2**n*sqrt(5))

class RedisConnectError(BaseException): pass

class Listener():
    def __init__(self, redis_endpoint, work_queue):
        self.redis_endpoint = redis_endpoint
        self.work_queue = work_queue
        self.redis_client = None
        self.minikube = None
        self.q = None
        self.bind_redis()
        self.bind_minikube()

    @threaded
    def destroy_recolector(self, name):
        self.minikube.delete_pod(name)

    @threaded
    def create_recolector(self, mimetype, target_data):
        image = 'ademord/recolector-' + mimetype
        name = 'recolector-' + str(uuid.uuid4())[:8]
        env = {'name': 'TARGET', 'value': target_data}
        self.minikube.deploy_templates(image=image, name=name, env=env)

    def bind_redis(self):
        for retry_n in range(20):
            try:
                self.redis_client = Redis(host=self.redis_endpoint)
                self.redis_client.delete('test_conn')
                logging.info('Connected to Redis!')
            except:
                logging.warning(
                    'Failed to connect to Redis. Retrying to connect in {} seconds...'.format(Fibo(retry_n)))
                time.sleep(Fibo(retry_n))
                continue
            break
        else:
            raise RedisConnectError()

        self.q = rediswq.RedisWQ(name=self.work_queue, host=self.redis_endpoint)
        logging.info('Worker with sessionID: ' + self.q.sessionID())
        logging.info('Initial queue state: empty=' + str(self.q.empty()))

    def bind_minikube(self):
        for retry_n in range(20):
            try:
                self.minikube = Minikube()
                logging.info('Minikube API connected!')
            except:
                logging.info('Failed to connect to Minikube. Retrying to connect in 15 seconds...')
                time.sleep(Fibo(retry_n))
                continue
            break
        else:
            raise KubernetesConnectError()

    def get_external(self, url):
        r = requests.get(url.strip())
        return r.json()

    def is_deployed(self, ip):
        estado = True
        try:
            estado = self.get_external('http://camaras/search/{}'.format(ip))[0]['estado']
        except:
            return True
        return estado  # False => undeployed

    def start(self):
        while True:
            # time.sleep(5)
            if not self.q.empty():
                item = self.q.lease(lease_secs=10, block=True, timeout=2)
                if item is not None:
                    item = item.decode('utf-8')
                    # syntax: img:filename | kill:container-name
                    mimetype, args = item.split(':')

                    if mimetype == 'kill':
                        self.destroy_recolector(args)
                    elif mimetype == 'ip' and not self.is_deployed(args) or mimetype != 'ip':
                        self.create_recolector(mimetype, args)
                    self.q.complete(item.encode('utf-8'))
            # else: logging.info('Waiting for work')

def main():
    logging.getLogger().setLevel(logging.INFO)
    redis_endpoint = os.environ.get('REDIS_SERVICE_HOST', 'redis')
    container_name = os.environ.get('HOSTNAME')
    work_queue = 'recolector_requests'
    Listener(redis_endpoint=redis_endpoint, work_queue=work_queue).start()

if __name__ == '__main__':
    main()