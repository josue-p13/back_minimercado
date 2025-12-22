"""
Servicio de Caja
RF20, RF21 - Control de apertura y cierre de caja
"""
from datetime import datetime
from app.models.caja import Caja
from app.repositories.caja_repository import CajaRepository

class CajaService:
    
    @staticmethod
    def abrir_caja(monto_inicial, fk_usuario):
        """RF20 - Abre una nueva caja"""
        # Verificar que no hay caja abierta
        caja_abierta = CajaRepository.obtener_caja_abierta()
        if caja_abierta:
            raise Exception("Ya existe una caja abierta. Cerrar la caja actual antes de abrir una nueva")
        
        if monto_inicial < 0:
            raise Exception("El monto inicial no puede ser negativo")
        
        caja = Caja(
            fecha_apertura=datetime.now().isoformat(),
            monto_inicial=monto_inicial,
            fk_usuario=fk_usuario,
            estado='Abierta'
        )
        return CajaRepository.crear(caja)
    
    @staticmethod
    def cerrar_caja(monto_final):
        """RF21 - Cierra la caja actual"""
        caja = CajaRepository.obtener_caja_abierta()
        if not caja:
            raise Exception("No hay caja abierta para cerrar")
        
        if monto_final < 0:
            raise Exception("El monto final no puede ser negativo")
        
        CajaRepository.cerrar_caja(
            caja.id,
            datetime.now().isoformat(),
            monto_final
        )
        
        # Calcular diferencia
        diferencia = monto_final - caja.monto_inicial
        return {
            'id': caja.id,
            'monto_inicial': caja.monto_inicial,
            'monto_final': monto_final,
            'diferencia': diferencia
        }
    
    @staticmethod
    def obtener_caja_actual():
        """Obtiene la caja actualmente abierta"""
        caja = CajaRepository.obtener_caja_abierta()
        if caja:
            return caja.to_dict()
        return None
    
    @staticmethod
    def listar_cajas():
        """Lista todas las cajas"""
        cajas = CajaRepository.listar()
        return [c.to_dict() for c in cajas]
