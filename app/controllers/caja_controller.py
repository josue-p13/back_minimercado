"""
Controlador de Caja
RF20, RF21 - Gestiona apertura y cierre de caja
"""
from app.services.caja_service import CajaService

class CajaController:
    
    @staticmethod
    def abrir_caja(monto_inicial, fk_usuario):
        """RF20 - Abre una caja"""
        try:
            caja = CajaService.abrir_caja(monto_inicial, fk_usuario)
            return {
                'success': True,
                'message': 'Caja abierta exitosamente',
                'caja': caja.to_dict()
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    @staticmethod
    def cerrar_caja(monto_final):
        """RF21 - Cierra la caja actual"""
        try:
            resultado = CajaService.cerrar_caja(monto_final)
            return {
                'success': True,
                'message': 'Caja cerrada exitosamente',
                'data': resultado
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    @staticmethod
    def obtener_caja_actual():
        """Obtiene la caja actualmente abierta"""
        try:
            caja = CajaService.obtener_caja_actual()
            if not caja:
                return {'success': False, 'message': 'No hay caja abierta'}
            
            return {
                'success': True,
                'caja': caja
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    @staticmethod
    def listar_cajas():
        """Lista todas las cajas"""
        try:
            cajas = CajaService.listar_cajas()
            return {
                'success': True,
                'cajas': cajas
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
