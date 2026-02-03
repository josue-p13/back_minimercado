from app.services.caja_service import CajaService

class CajaController:
    
    @staticmethod
    def abrir_caja(monto_inicial, fk_usuario):
        try:
            # Si fk_usuario viene 0 o null, asumimos 1 para pruebas (temporal)
            usuario_id = fk_usuario if fk_usuario else 1
            
            caja = CajaService.abrir_caja(monto_inicial, usuario_id)
            return {
                'success': True,
                'message': 'Caja abierta correctamente',
                'caja': caja.to_dict()
            }
        except Exception as e:
            return {'success': False, 'message': str(e)}

    @staticmethod
    def cerrar_caja(monto_final):
        try:
            # NOTA: En un sistema real, el usuario se saca del token de sesión.
            # Por ahora usaremos el usuario 1 o el que estemos usando para pruebas.
            usuario_id = 1 
            
            CajaService.cerrar_caja(monto_final, usuario_id)
            return {
                'success': True,
                'message': 'Caja cerrada correctamente'
            }
        except Exception as e:
            return {'success': False, 'message': str(e)}

    @staticmethod
    def obtener_caja_actual():
        try:
            usuario_id = 1 # Temporal para pruebas
            caja = CajaService.obtener_caja_actual(usuario_id)
            
            if caja:
                return {'success': True, 'abierta': True, 'caja': caja.to_dict()}
            else:
                return {'success': True, 'abierta': False, 'message': 'No hay caja abierta'}
                
        except Exception as e:
            return {'success': False, 'message': str(e)}

    @staticmethod
    def listar_cajas():
        try:
            cajas = CajaService.listar_cajas()
            return {'success': True, 'cajas': cajas}
        except Exception as e:
            return {'success': False, 'message': str(e)}