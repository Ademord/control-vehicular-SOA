from orator import Model
from database import db
from flask import abort
import uuid
import re
import json
import requests
import cv2
import numpy as np

#orator.orm.collection.Collection object at 0x000001AA82700978
class Coincidencia(Model):
    def connect():
        Model.set_connection_resolver(db)
    __table__ = 'coincidencias'

    def get_external(url):
        r = requests.get(url.strip())
        return r.json()

    def getall(): 
        try:
            return Coincidencia.all().serialize()
        except:
            return abort(404)

    def get(id):
        try:
            return Coincidencia.find(id).serialize()
        except:
            return abort(404)

    def buscar(param):
        try:
            return Coincidencia.where('matricula', 'like', '%{}%'.format(param)).get().serialize();
        except:
            return abort(404)

    def add(data):
        coincidencia = Coincidencia()
        # IP
        coincidencia.camara = data['ip']
        # LUGAR
        lugar_id = Coincidencia.get_external('http://camaras/search/{}'.format(data['ip']))[0]['lugar_id']
        lugar = Coincidencia.get_external('http://lugares/{}'.format(lugar_id))
        coincidencia.lugar = lugar['nombre']
        # MATRICULA
        coincidencia.matricula = data['plate']
        pattern = re.compile(r"^\d{1,4}[A-Z]{3}$",re.I)
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
        cv2.imwrite('/usr/src/data/' + filename, np.array(data['frame'])); 
        del data['frame']

        coincidencia.save() #salta id cuando no puede agregar; falta validar requests
        return True

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
