from orator import Model
from database import db
#orator.orm.collection.Collection object at 0x000001AA82700978
class Lugar(Model):

    def connect():
        Model.set_connection_resolver(db)
    __table__ = 'lugares'
    
    def getall(): 
        return Lugar.all().serialize()

    def get(id):
        lugar = Lugar.find(id)
        try:
            return lugar.serialize()
        except:
            return lugar

    def add(temp):
        lugar = Lugar()
        try:
            lugar.nombre = temp['nombre']
            lugar.save() #salta id cuando no puede agregar; falta validar requests
            return True
        except:
            return "No se pudo agregar elemento."

    def remove(id):
        lugar = Lugar.find(id)
        try:
            lugar.delete()
            return True
        except:
            return "No se pudo eliminar elemento."

    def update(id, temp):
        lugar = Lugar.find(id)
        try:
            lugar.nombre = temp['nombre']
            lugar.save()
            return True
        except:
            return "No se pudo actualizar elemento."

    def valid(temp):
        if 'nombre' in temp and not isinstance(temp['nombre'], str):
            return False
        return True