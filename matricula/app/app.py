from orator import Model
from database import db
from flask import abort

#orator.orm.collection.Collection object at 0x000001AA82700978
class Matricula(Model):

    def connect():
        Model.set_connection_resolver(db)
    __table__ = 'matriculas'
    
    def getall(): 
        try:
            return Matricula.all().serialize()
        except:
            return abort(404)

    def get(id):
        try:
            return Matricula.find(id).serialize()
        except:
            return abort(404)

    def buscar(param):
        try:
            return Matricula.where('numero', 'like', '%{}%'.format(param)).get().serialize();
        except:
            return abort(404)

    def add(temp):
        matricula = Matricula()
        try:
            matricula.numero = temp['numero']
            matricula.propietario_id = temp['propietario_id']
            matricula.save() #salta id cuando no puede agregar; falta validar requests
            return True
        except:
            return "No se pudo agregar elemento."

    def remove(id):
        matricula = Matricula.find(id)
        try:
            matricula.delete()
            return True
        except:
            return "No se pudo eliminar elemento."

    def update(id, temp):
        matricula = Matricula.find(id)
        try:
            matricula.numero = temp['numero']
            matricula.propietario_id = temp['propietario_id']
            matricula.save()
            return True
        except:
            return "No se pudo actualizar elemento."

    def valid(temp):
        if 'ip' in temp and not isinstance(temp['numero'], str):
            return False
        # if 'lugar_id' in temp and not isinstance(temp['lugar_id'], str):
        #     return False
        return True