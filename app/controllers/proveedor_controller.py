"""
Controlador de Proveedores
Gestiona las peticiones relacionadas con proveedores
"""
from app.services.proveedor_service import ProveedorService

class ProveedorController:
    
    @staticmethod
    def agregar_proveedor(nombre, telefono, direccion):
        """Agrega un nuevo proveedor"""
        try:
            proveedor = ProveedorService.agregar_proveedor(nombre, telefono, direccion)
            return {
                'success': True,
                'message': 'Proveedor agregado exitosamente',
                'proveedor': proveedor.to_dict()
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    @staticmethod
    def actualizar_proveedor(id, nombre, telefono, direccion):
        """Actualiza un proveedor"""
        try:
            proveedor = ProveedorService.actualizar_proveedor(id, nombre, telefono, direccion)
            return {
                'success': True,
                'message': 'Proveedor actualizado exitosamente',
                'proveedor': proveedor.to_dict()
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    @staticmethod
    def eliminar_proveedor(id):
        """Elimina (desactiva) un proveedor"""
        try:
            ProveedorService.eliminar_proveedor(id)
            return {
                'success': True,
                'message': 'Proveedor eliminado exitosamente'
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
            
    @staticmethod
    def listar_proveedores():
        """Lista todos los proveedores"""
        try:
            proveedores = ProveedorService.listar_proveedores()
            return {
                'success': True,
                'proveedores': proveedores
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    @staticmethod
    def buscar_proveedor(id):
        """Busca un proveedor por ID"""
        try:
            proveedor = ProveedorService.buscar_proveedor(id)
            if not proveedor:
                return {'success': False, 'message': 'Proveedor no encontrado'}
            
            return {
                'success': True,
                'proveedor': proveedor
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }