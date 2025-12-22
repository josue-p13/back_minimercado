"""
Modelo Producto
RF10 - Control de inventario automático
RF11 - Alerta de stock bajo
"""

class Producto:
    def __init__(self, id=None, nombre=None, precio=None, stock=0, stock_minimo=5, fk_proveedor=None, activo=1):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.stock_minimo = stock_minimo
        self.fk_proveedor = fk_proveedor
        self.activo = activo
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'precio': self.precio,
            'stock': self.stock,
            'stock_minimo': self.stock_minimo,
            'fk_proveedor': self.fk_proveedor,
            'activo': self.activo,
            'alerta_stock': self.stock <= self.stock_minimo  # RF11
        }
