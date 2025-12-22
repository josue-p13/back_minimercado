"""
Controlador de Inventario
RF10, RF11 - Gestiona el inventario de productos
"""
from app.services.inventario_service import InventarioService

class InventarioController:
    
    @staticmethod
    def agregar_producto(nombre, precio, stock, stock_minimo, fk_proveedor):
        """Agrega un nuevo producto"""
        try:
            producto = InventarioService.agregar_producto(nombre, precio, stock, stock_minimo, fk_proveedor)
            return {
                'success': True,
                'message': 'Producto agregado exitosamente',
                'producto': producto.to_dict()
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    @staticmethod
    def actualizar_producto(id, nombre, precio, stock_minimo):
        """Actualiza un producto"""
        try:
            producto = InventarioService.actualizar_producto(id, nombre, precio, stock_minimo)
            return {
                'success': True,
                'message': 'Producto actualizado exitosamente',
                'producto': producto.to_dict()
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    @staticmethod
    def agregar_stock(id_producto, cantidad):
        """RF10 - Agrega stock a un producto"""
        try:
            producto = InventarioService.agregar_stock(id_producto, cantidad)
            return {
                'success': True,
                'message': f'Stock agregado. Nuevo stock: {producto.stock}',
                'producto': producto.to_dict()
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    @staticmethod
    def obtener_alertas_stock():
        """RF11 - Obtiene productos con stock bajo"""
        try:
            productos = InventarioService.obtener_alertas_stock()
            return {
                'success': True,
                'alertas': productos,
                'total': len(productos)
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    @staticmethod
    def listar_productos():
        """Lista todos los productos"""
        try:
            productos = InventarioService.listar_productos()
            return {
                'success': True,
                'productos': productos
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    @staticmethod
    def buscar_producto(id):
        """Busca un producto por ID"""
        try:
            producto = InventarioService.buscar_producto(id)
            if not producto:
                return {'success': False, 'message': 'Producto no encontrado'}
            
            return {
                'success': True,
                'producto': producto
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
