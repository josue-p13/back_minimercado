"""
Modelo Usuario
RNF2 - Control de acceso basado en roles
"""

class Usuario:
    def __init__(self, id=None, nombre=None, username=None, password_hash=None, rol=None, activo=1):
        self.id = id
        self.nombre = nombre
        self.username = username
        self.password_hash = password_hash
        self.rol = rol  # Admin, Cajero, Auxiliar
        self.activo = activo
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'username': self.username,
            'rol': self.rol,
            'activo': self.activo
        }
