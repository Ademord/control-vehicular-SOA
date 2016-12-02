from orator import Model
from database import db
#orator.orm.collection.Collection object at 0x000001AA82700978
class Camara(Model):

    def connect():
        Model.set_connection_resolver(db)
    __table__ = 'camaras'
    
    def getall(): 
        return Camara.all().serialize()

    def get(id):
        camara = Camara.find(id)
        try:
            return camara.serialize()
        except:
            return camara

    def add(temp):
        camara = Camara()
        try:
            camara.nombre = temp['ip']
            camara.lugar_id = temp['lugar_id']
            camara.save() #salta id cuando no puede agregar; falta validar requests
            return True
        except:
            return "No se pudo agregar elemento."

    def remove(id):
        camara = Camara.find(id)
        try:
            camara.delete()
            return True
        except:
            return "No se pudo eliminar elemento."

    def update(id, temp):
        camara = Camara.find(id)
        try:
            camara.nombre = temp['ip']
            camara.lugar_id = temp['lugar_id']
            camara.save()
            return True
        except:
            return "No se pudo actualizar elemento."

    def valid(temp):
        if 'ip' in temp and not isinstance(temp['ip'], str):
            return False
        # if 'lugar_id' in temp and not isinstance(temp['lugar_id'], str):
        #     return False
        return True