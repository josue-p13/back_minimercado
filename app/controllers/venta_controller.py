from app.services.venta_service import VentaService

class VentaController:
    
    @staticmethod
    def realizar_venta(venta_request): # Recibimos el objeto Pydantic completo
        try:
            # Obtenemos usuario (usamos 1 temporalmente o la logica de token futura)
            usuario_id = venta_request.fk_usuario if venta_request.fk_usuario else 1
            
            venta = VentaService.realizar_venta(
                venta_request.items,
                venta_request.fk_cliente,
                usuario_id,
                venta_request.metodo_pago, # <---
                venta_request.monto_pago,  # <---
                venta_request.referencia   # <---
            )
            
            return {
                'success': True,
                'message': 'Venta registrada correctamente',
                'venta_id': venta.id,
                'total': venta.total,
                'cambio': venta.cambio
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