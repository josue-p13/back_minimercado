"""
Servicio de Inventario
RF10 - Actualización automática de inventario
RF11 - Alertas de stock bajo
"""
from app.repositories.producto_repository import ProductoRepository
from app.models.producto import Producto

class InventarioService:
    
    @staticmethod
    def agregar_producto(nombre, precio, stock, stock_minimo, fk_proveedor):
        """Agrega un nuevo producto al inventario"""
        if precio < 0:
            raise Exception("El precio no puede ser negativo")
        if stock < 0:
            raise Exception("El stock no puede ser negativo")
        
        producto = Producto(
            nombre=nombre,
            precio=precio,
            stock=stock,
            stock_minimo=stock_minimo,
            fk_proveedor=fk_proveedor
        )
        return ProductoRepository.crear(producto)
    
    @staticmethod
    def actualizar_producto(id, nombre, precio, stock_minimo):
        """Actualiza la información de un producto"""
        producto = ProductoRepository.obtener_por_id(id)
        if not producto:
            raise Exception("Producto no encontrado")
        
        producto.nombre = nombre
        producto.precio = precio
        producto.stock_minimo = stock_minimo
        ProductoRepository.actualizar(producto)
        return producto
    
    @staticmethod
    def agregar_stock(id_producto, cantidad):
        """RF10 - Agrega stock a un producto (por compra/recepción)"""
        producto = ProductoRepository.obtener_por_id(id_producto)
        if not producto:
            raise Exception("Producto no encontrado")
        
        if cantidad <= 0:
            raise Exception("La cantidad debe ser mayor a 0")
        
        ProductoRepository.actualizar_stock(id_producto, cantidad)
        producto_actualizado = ProductoRepository.obtener_por_id(id_producto)
        return producto_actualizado
    
    @staticmethod
    def obtener_alertas_stock():
        """RF11 - Obtiene productos con stock bajo"""
        productos = ProductoRepository.obtener_productos_bajo_stock()
        return [p.to_dict() for p in productos]
    
    @staticmethod
    def listar_productos():
        """Lista todos los productos"""
        productos = ProductoRepository.listar()
        return [p.to_dict() for p in productos]
    
    @staticmethod
    def buscar_producto(id):
        """Busca un producto por ID"""
        producto = ProductoRepository.obtener_por_id(id)
        if producto:
            return producto.to_dict()
        return None
