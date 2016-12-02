from orator import Model
from database import db
#orator.orm.collection.Collection object at 0x000001AA82700978
class Propietario(Model):

    def connect():
        Model.set_connection_resolver(db)
    __table__ = 'propietarios'
    
    def getall(): 
        return Propietario.all().serialize()

    def get(id):
        propietario = Propietario.find(id)
        try:
            return propietario.serialize()
        except:
            return propietario

    def add(temp):
        propietario = Propietario()
        try:
            propietario.nombres = temp['numero']
            propietario.apellidos = temp['apellidos']
            propietario.cod_administrativo = temp['cod_administrativo']
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
            propietario.cod_administrativo = temp['cod_administrativo']
            propietario.save()
            return True
        except:
            return "No se pudo actualizar elemento."

    def valid(temp):
        if 'ip' in temp and not isinstance(temp['nombres'], str):
            return False
        return True