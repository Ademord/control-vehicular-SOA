from orator import Model
from database import db
from flask import abort, jsonify
#orator.orm.collection.Collection object at 0x000001AA82700978
class Camara(Model):
    
    __table__ = 'camaras'

    def connect():
        Model.set_connection_resolver(db)
    
    def getall(): 
        try:
            return Camara.all().serialize()
        except:
            return abort(404)

    def get(id):
        try:
            return Camara.find(id).serialize()
        except:
            return abort(404)

    def buscar(param):
        try:
            return Camara.where('ip', 'like', '%{}%'.format(param)).get().serialize();
        except:
            return abort(404)

    def add(temp):
        camara = Camara()
        try:
            camara.ip = temp['ip']
            camara.lugar_id = temp['lugar_id']
            camara.estado = False
            camara.recolector = ""
            camara.save() #salta id cuando no puede agregar; falta validar requests
            return jsonify({'result': "Elemento agregado"}), 200
        except:
            return jsonify({'result': "No se pudo agregar elemento."}), 500

    def remove(id):
        try:
            Camara.find(id).delete()
            return jsonify({'result': "Elemento eliminado"}), 200
        except:
            return jsonify({'result': "No se pudo agregar elemento."}), 500

    def update(id, temp):
        camara = Camara.find(id)
        try:
            camara.ip = temp['ip']
            camara.lugar_id = temp['lugar_id']
            camara.estado = False
            camara.recolector = ""
            camara.save()
            return jsonify({'result': "Elemento actualizado"}), 200
        except:
            return jsonify({'result': "No se pudo agregar elemento."}), 500

    def valid(temp):
        if 'ip' in temp and not isinstance(temp['ip'], str):
            return False
        return True
