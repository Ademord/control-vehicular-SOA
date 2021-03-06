from orator import Model
from database import db
from flask import abort
import uuid
import re
import json
import requests
import cv2
import numpy as NP
from redis import Redis
import publisher
import psycopg2
import logging

#orator.orm.collection.Collection object at 0x000001AA82700978
class Coincidencia(Model):
    def connect():
        Model.set_connection_resolver(db)
    __table__ = 'coincidencias'

    def get_external(url):
        r = requests.get(url.strip())
        return r.json()

    def getall():
            return Coincidencia.all().serialize()

    def get(id):
        try:
            return Coincidencia.find(id).serialize()
        except:
            return abort(404)

    def raw(query):
        try:
            conn = psycopg2.connect(
                "host='homestead' port=5432 dbname='homestead' user='homestead' host='homestead' password='secret'")
        except:
            print("I am unable to connect to the database")
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        cur.close()

    def getCountByPlace():
        return db.select('SELECT lugar, count(*) FROM coincidencias GROUP BY lugar;') 
    
    def getCountKnownByPlace():
        return db.select("SELECT l.nombre, coalesce(count(c.id),0) \
            FROM (SELECT DISTINCT lugar as nombre FROM coincidencias) l \
            LEFT OUTER JOIN ( \
            SELECT * FROM coincidencias WHERE propietario != 'Desconocido' ) c \
            ON l.nombre = c.lugar GROUP BY l.nombre;") 
    
    def getCountUnknownByPlace():
        return db.select("SELECT l.nombre, coalesce(count(c.id),0) \
            FROM (SELECT DISTINCT lugar as nombre FROM coincidencias) l \
            LEFT OUTER JOIN ( \
            SELECT * FROM coincidencias WHERE propietario = 'Desconocido' ) c \
            ON l.nombre = c.lugar GROUP BY l.nombre;") 
    
    def getCountKnown():
        return db.select("SELECT count(*) FROM coincidencias as c WHERE c.propietario = 'Desconocido';") 
    
    def getCountUnknown():
        return db.select("SELECT count(*) FROM coincidencias as c WHERE c.propietario != 'Desconocido';")   
    
    def getDateCountKnown():
        return db.select("SELECT d.date, count(se.id) FROM ( \
            select to_char(date_trunc('day', (current_date - offs)), 'YYYY-MM-DD') \
            AS date \
            FROM generate_series(0, 14, 1) \
            AS offs \
            ) d \
            LEFT OUTER JOIN (SELECT * FROM coincidencias as c WHERE c.propietario != 'Desconocido') se \
            ON (d.date=to_char(date_trunc('day', se.created_at), 'YYYY-MM-DD'))  \
            GROUP BY d.date \
            ORDER BY d.date asc;")

    def getDateCountUnknown():
        return db.select("SELECT d.date, count(se.id) FROM ( \
            select to_char(date_trunc('day', (current_date - offs)), 'YYYY-MM-DD') \
            AS date \
            FROM generate_series(0, 14, 1) \
            AS offs \
            ) d \
            LEFT OUTER JOIN (SELECT * FROM coincidencias as c WHERE c.propietario = 'Desconocido') se \
            ON (d.date=to_char(date_trunc('day', se.created_at), 'YYYY-MM-DD'))  \
            GROUP BY d.date \
            ORDER BY d.date asc;")

    def buscar(param):
        try:
            return Coincidencia.where('matricula', 'like', '%{}%'.format(param)).get().serialize()
        except:
            return abort(404)

    def decode_frame(self, item, key):
        array_dtype, l, w, k = item.split('|')[1].split('#')
        image = self.redis_client.get(key)
        image = NP.fromstring(image, dtype=array_dtype).reshape(int(l), int(w), int(k))
        return image

    def add(data):
        coincidencia = Coincidencia()
        # IP
        print(data['ip'])
        coincidencia.camara = data['ip']

        # LUGAR
        if coincidencia.camara != 'unset':
            lugar_id = Coincidencia.get_external('http://camaras/search/{}'.format(data['ip']))[0]['lugar_id']
            lugar = Coincidencia.get_external('http://lugares/{}'.format(lugar_id))
            coincidencia.lugar = lugar['nombre']
        else:
            coincidencia.lugar = 'EntradaVirtual'
            coincidencia.camara = 'IPVirtual'


        # MATRICULA
        coincidencia.matricula = data['plate']
        pattern = re.compile(r"^\d{3,4}[A-Z]{3}$",re.I)
        mismatch = True
        if pattern.search(coincidencia.matricula): mismatch = False
        coincidencia.mismatch = mismatch

        # PROPIETARIO
        coincidencia.propietario = "Desconocido" #se asume que es desconocido
        if not mismatch:
            id_propietario = Coincidencia.get_external('http://matriculas/search/{}'.format(coincidencia.matricula))
            if len(id_propietario):
                id_propietario = id_propietario[0]['propietario_id']
                propietario = Coincidencia.get_external('http://propietarios/{}'.format(id_propietario))
                coincidencia.propietario = propietario['nombres'] + propietario['apellidos']

        # CUADRO
        filename = str(uuid.uuid4()) + ".png"
        coincidencia.filename = filename
        coincidencia.mime = "image/png"

        item = data['item']
        print(type(item))
        redis_client = Redis(host='redis')
        key = item.split('|')[2]

        array_dtype, l, w, k = item.split('|')[1].split('#')
        image = redis_client.get(key)
        image = NP.fromstring(image, dtype=array_dtype).reshape(int(l), int(w), int(k))
        logging.info(type(image))
        cv2.imwrite('/media/frames/' + filename, image)

        coincidencia.save() #salta id cuando no puede agregar; falta validar requests
        del data
        del image
        redis_client.delete(key)
        publisher.publishInRedis(coincidencia)
        return 200

    def remove(id):
        try:
            Coincidencia.find(id).delete()
            return 200
        except:
            return "No se pudo eliminar elemento."

    def valid(temp):
        if 'ip' in temp and not isinstance(temp['plate'], str): #cambiar
            return False
        return True
