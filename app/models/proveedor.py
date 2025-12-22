"""
Modelo Proveedor
"""

class Proveedor:
    def __init__(self, id=None, nombre=None, telefono=None, direccion=None, activo=1):
        self.id = id
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion
        self.activo = activo
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'telefono': self.telefono,
            'direccion': self.direccion,
            'activo': self.activo
        }
