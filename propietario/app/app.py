from orator import Model
from database import db
from flask import abort
#orator.orm.collection.Collection object at 0x000001AA82700978
class Propietario(Model):

    def connect():
        Model.set_connection_resolver(db)
    __table__ = 'propietarios'
    
    def getall(): 
        try:
            return Propietario.all().serialize()
        except:
            return abort(404)

    def get(id):
        try:
            return Propietario.find(id).serialize()
        except:
            return abort(404)

    def buscar(param):
        try:
            return Propietario.where('nombres', 'like', '%{}%'.format(param)).get().serialize();
        except:
            return abort(404)

    def add(temp):
        propietario = Propietario()
        try:
            propietario.nombres = temp['nombres']
            propietario.apellidos = temp['apellidos']
            propietario.codigo = temp['codigo']
            propietario.save() #salta id cuando no puede agregar; falta validar requests
            return True
        except:
            return "No se pudo agregar elemento."

    def remove(id):
        propietario = Propietario.find(id)
        try:
            propietario.delete()
            return True
        except:
            return "No se pudo eliminar elemento."

    def update(id, temp):
        propietario = Propietario.find(id)
        try:
            propietario.nombres = temp['nombres']
            propietario.apellidos = temp['apellidos']
            propietario.codigo = temp['codigo']
            propietario.save()
            return True
        except:
            return "No se pudo actualizar elemento."

    def valid(temp):
        if 'ip' in temp and not isinstance(temp['nombres'], str):
            return False
        return True