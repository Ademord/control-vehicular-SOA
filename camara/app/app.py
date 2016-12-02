from orator import Model
from database import db
from flask import abort
#orator.orm.collection.Collection object at 0x000001AA82700978
class Camara(Model):

    # def __init__(self):
    #     self.ip = ""
    #     self.lugar_id = ""
    #     self.estado = False
    #     self.recolector = ""

    def connect():
        Model.set_connection_resolver(db)
    __table__ = 'camaras'
    
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
        camara.ip = temp['ip']
        camara.lugar_id = temp['lugar_id']
        camara.estado = temp['estado']
        camara.recolector = temp['recolector']
        camara.save() #salta id cuando no puede agregar; falta validar requests
        return 200

    def remove(id):
        try:
            Camara.find(id).delete()
            return 200
        except:
            return "No se pudo eliminar elemento."

    def update(id, temp):
        camara = Camara.find(id)
        try:
            camara.ip = temp['ip']
            camara.lugar_id = temp['lugar_id']
            camara.estado = temp['estado']
            camara.recolector = temp['recolector']
            camara.save()
            return 200
        except:
            return "No se pudo actualizar elemento."

    def valid(temp):
        if 'ip' in temp and not isinstance(temp['ip'], str):
            return False
        # if 'lugar_id' in temp and not isinstance(temp['lugar_id'], str):
        #     return False
        return True
