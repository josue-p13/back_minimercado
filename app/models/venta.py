class Venta:
    def __init__(self, id=None, fecha=None, total=None, fk_cliente=None, fk_usuario=None, fk_caja=None, 
                 items=None, metodo_pago=None, monto_pago=0, cambio=0, referencia=None): # <--- NUEVOS ARGUMENTOS
        self.id = id
        self.fecha = fecha
        self.total = total
        self.fk_cliente = fk_cliente
        self.fk_usuario = fk_usuario
        self.fk_caja = fk_caja
        self.items = items if items else []
        
        # Campos nuevos
        self.metodo_pago = metodo_pago
        self.monto_pago = monto_pago
        self.cambio = cambio
        self.referencia = referencia

    def to_dict(self):
        return {
            'id': self.id,
            'fecha': self.fecha,
            'total': self.total,
            'fk_cliente': self.fk_cliente,
            'fk_usuario': self.fk_usuario,
            'metodo_pago': self.metodo_pago, # <--- NUEVO
            'monto_pago': self.monto_pago,   # <--- NUEVO
            'cambio': self.cambio,           # <--- NUEVO
            'referencia': self.referencia,   # <--- NUEVO
            'items': self.items
        }