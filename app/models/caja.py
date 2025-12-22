"""
Modelo Caja
RF20, RF21 - Control de apertura y cierre de caja
"""

class Caja:
    def __init__(self, id=None, fecha_apertura=None, fecha_cierre=None, monto_inicial=None, monto_final=None, fk_usuario=None, estado='Abierta'):
        self.id = id
        self.fecha_apertura = fecha_apertura
        self.fecha_cierre = fecha_cierre
        self.monto_inicial = monto_inicial
        self.monto_final = monto_final
        self.fk_usuario = fk_usuario
        self.estado = estado
    
    def to_dict(self):
        return {
            'id': self.id,
            'fecha_apertura': self.fecha_apertura,
            'fecha_cierre': self.fecha_cierre,
            'monto_inicial': self.monto_inicial,
            'monto_final': self.monto_final,
            'fk_usuario': self.fk_usuario,
            'estado': self.estado
        }
