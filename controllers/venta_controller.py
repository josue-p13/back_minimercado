"""
Controlador de Ventas
RF14, RF15 - Gestiona el proceso de ventas
"""
from app.services.venta_service import VentaService

class VentaController:
    
    @staticmethod
    def realizar_venta(items, fk_cliente, fk_usuario):
        """
        Procesa una venta
        items: [{'producto_id': int, 'cantidad': int}, ...]
        """
        try:
            venta = VentaService.procesar_venta(items, fk_cliente, fk_usuario)
            return {
                'success': True,
                'message': 'Venta procesada exitosamente',
                'venta': venta.to_dict()
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    @staticmethod
    def obtener_venta(id_venta):
        """Obtiene una venta con sus detalles"""
        try:
            venta_completa = VentaService.obtener_venta_completa(id_venta)
            if not venta_completa:
                return {'success': False, 'message': 'Venta no encontrada'}
            
            return {
                'success': True,
                'data': venta_completa
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    @staticmethod
    def listar_ventas():
        """Lista todas las ventas"""
        try:
            ventas = VentaService.listar_ventas()
            return {
                'success': True,
                'ventas': ventas
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
