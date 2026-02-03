class Producto:
    def __init__(self, id=None, nombre=None, precio=None, stock=None, stock_minimo=None, fk_proveedor=None, activo=1, codigo_barras=None):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.stock_minimo = stock_minimo
        self.fk_proveedor = fk_proveedor
        self.activo = activo
        self.codigo_barras = codigo_barras # <--- NUEVO

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'precio': self.precio,
            'stock': self.stock,
            'stock_minimo': self.stock_minimo,
            'fk_proveedor': self.fk_proveedor,
            'activo': self.activo,
            'codigo_barras': self.codigo_barras # <--- NUEVO
        }