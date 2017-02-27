from orator import Model
from database import db
from flask import abort, jsonify

#orator.orm.collection.Collection object at 0x000001AA82700978
class Lugar(Model):

    def connect():
        Model.set_connection_resolver(db)
    __table__ = 'lugares'
    
    def getall(): 
            return Lugar.all().serialize()

    def get(id):
        try:
            return Lugar.find(id).serialize()
        except:
            return abort(404)

    def buscar(param):
        try:
            return Lugar.where('nombre', 'like', '%{}%'.format(param)).get().serialize();
        except:
            return abort(404)

    def add(temp):
        lugar = Lugar()
        try:
            lugar.nombre = temp['nombre']
            lugar.save() #salta id cuando no puede agregar; falta validar requests
            return jsonify({'result': "Elemento agregado"}), 200
        except:
            return jsonify({'result': "No se pudo agregar elemento."}), 500

    def remove(id):
        try:
            Lugar.find(id).delete()
            return jsonify({'result': "Elemento eliminado"}), 200
        except:
            return jsonify({'result': "No se pudo agregar elemento."}), 500

    def update(id, temp):
        lugar = Lugar.find(id)
        try:
            lugar.nombre = temp['nombre']
            lugar.save()
            return jsonify({'result': "Elemento actualizado"}), 200
        except:
            return jsonify({'result': "No se pudo agregar elemento."}), 500

    def valid(temp):
        if 'nombre' in temp and not isinstance(temp['nombre'], str):
            return False
        return True