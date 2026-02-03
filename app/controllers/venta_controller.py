from app.services.venta_service import VentaService

class VentaController:
    
    @staticmethod
    def realizar_venta(items, fk_cliente, fk_usuario):
        try:
            # Si fk_usuario viene vacio, usamos 1 temporalmente
            usuario_id = fk_usuario if fk_usuario else 1
            
            venta = VentaService.realizar_venta(items, fk_cliente, usuario_id)
            
            return {
                'success': True,
                'message': 'Venta registrada correctamente',
                'venta_id': venta.id,
                'total': venta.total
            }
        except Exception as e:
            return {'success': False, 'message': str(e)}

    @staticmethod
    def listar_ventas():
        try:
            ventas = VentaService.listar_ventas()
            return {'success': True, 'ventas': ventas}
        except Exception as e:
            return {'success': False, 'message': str(e)}

    @staticmethod
    def obtener_venta(id):
        try:
            venta = VentaService.obtener_venta(id)
            if venta:
                return {'success': True, 'venta': venta}
            else:
                return {'success': False, 'message': 'Venta no encontrada'}
        except Exception as e:
            return {'success': False, 'message': str(e)}