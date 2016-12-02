from orator import Model
from database import db
#orator.orm.collection.Collection object at 0x000001AA82700978
class Coincidencia(Model):
    def connect():
        Model.set_connection_resolver(db)
    __table__ = 'coincidencias'
    
    def getall(): 
        return Coincidencia.all().serialize()

    def get(id):
        coincidencia = Coincidencia.find(id)
        try:
            return coincidencia.serialize()
        except:
            return coincidencia

    def add(temp):
        coincidencia = Coincidencia()
        try:
            coincidencia.camara = temp['camara']
            coincidencia.lugar = temp['lugar']
            coincidencia.filename = temp['filename']
            coincidencia.placa = temp['plate'] #cambiar
            coincidencia.mime = temp['mime']
            coincidencia.miembro = temp['miembro']
            coincidencia.mismatch = temp['mismatch']
            coincidencia.save() #salta id cuando no puede agregar; falta validar requests
            return True
        except:
            return "No se pudo agregar elemento."

    def remove(id):
        coincidencia = Coincidencia.find(id)
        try:
            coincidencia.delete()
            return True
        except:
            return "No se pudo eliminar elemento."

    def update(id, temp):
        coincidencia = Coincidencia.find(id)
        try:
            coincidencia.camara = temp['camara']
            coincidencia.lugar = temp['lugar']
            coincidencia.filename = temp['filename']
            coincidencia.placa = temp['placa'] #cambiar
            coincidencia.mime = temp['mime']
            coincidencia.miembro = temp['miembro']
            coincidencia.mismatch = temp['mismatch']
            coincidencia.save()
            return True
        except:
            return "No se pudo actualizar elemento."

    def valid(temp):
        if 'ip' in temp and not isinstance(temp['plate'], str): #cambiar
            return False
        return True