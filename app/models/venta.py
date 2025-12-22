"""
Modelos Venta y DetalleVenta
RF14, RF15 - Procesar ventas con múltiples productos
"""

class Venta:
    def __init__(self, id=None, fecha=None, total=None, fk_cliente=None, fk_usuario=None, fk_caja=None):
        self.id = id
        self.fecha = fecha
        self.total = total
        self.fk_cliente = fk_cliente
        self.fk_usuario = fk_usuario
        self.fk_caja = fk_caja
    
    def to_dict(self):
        return {
            'id': self.id,
            'fecha': self.fecha,
            'total': self.total,
            'fk_cliente': self.fk_cliente,
            'fk_usuario': self.fk_usuario,
            'fk_caja': self.fk_caja
        }

class DetalleVenta:
    def __init__(self, id=None, fk_venta=None, fk_producto=None, cantidad=None, precio_unitario=None, subtotal=None):
        self.id = id
        self.fk_venta = fk_venta
        self.fk_producto = fk_producto
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.subtotal = subtotal
    
    def to_dict(self):
        return {
            'id': self.id,
            'fk_venta': self.fk_venta,
            'fk_producto': self.fk_producto,
            'cantidad': self.cantidad,
            'precio_unitario': self.precio_unitario,
            'subtotal': self.subtotal
        }
