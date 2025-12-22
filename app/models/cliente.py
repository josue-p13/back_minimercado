"""
Modelo Cliente
"""

class Cliente:
    def __init__(self, id=None, nombre=None, telefono=None, email=None, activo=1):
        self.id = id
        self.nombre = nombre
        self.telefono = telefono
        self.email = email
        self.activo = activo
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'telefono': self.telefono,
            'email': self.email,
            'activo': self.activo
        }
