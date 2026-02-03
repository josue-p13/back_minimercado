from datetime import datetime
from app.repositories.caja_repository import CajaRepository
from app.models.caja import Caja

class CajaService:
    
    @staticmethod
    def abrir_caja(monto_inicial, fk_usuario):
        # 1. Verificar que no tenga ya una abierta
        caja_abierta = CajaRepository.obtener_abierta_por_usuario(fk_usuario)
        if caja_abierta:
            raise Exception("Ya tienes una caja abierta. Ciérrala antes de abrir una nueva.")
            
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        nueva_caja = Caja(fecha_apertura=fecha_actual, monto_inicial=monto_inicial, fk_usuario=fk_usuario)
        
        return CajaRepository.abrir(nueva_caja)

    @staticmethod
    def cerrar_caja(monto_final, fk_usuario):
        # 1. Buscar la caja que vamos a cerrar
        caja_abierta = CajaRepository.obtener_abierta_por_usuario(fk_usuario)
        if not caja_abierta:
            raise Exception("No hay ninguna caja abierta para cerrar.")
            
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        CajaRepository.cerrar(caja_abierta.id, fecha_actual, monto_final)
        return True

    @staticmethod
    def obtener_caja_actual(fk_usuario):
        return CajaRepository.obtener_abierta_por_usuario(fk_usuario)
        
    @staticmethod
    def listar_cajas():
        return [c.to_dict() for c in CajaRepository.listar_todas()]