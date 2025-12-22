"""
Servicio de Ventas
RF14, RF15 - Procesar ventas con validación de stock
RF10 - Actualización automática de inventario
"""
from datetime import datetime
from app.models.venta import Venta, DetalleVenta
from app.repositories.venta_repository import VentaRepository
from app.repositories.producto_repository import ProductoRepository
from app.repositories.caja_repository import CajaRepository

class VentaService:
    
    @staticmethod
    def procesar_venta(items, fk_cliente, fk_usuario):
        """
        RF14, RF15 - Procesa una venta con múltiples productos
        items: [{'producto_id': int, 'cantidad': int}, ...]
        """
        # Validar que hay caja abierta
        caja = CajaRepository.obtener_caja_abierta()
        if not caja:
            raise Exception("No hay caja abierta. Abrir caja antes de realizar ventas")
        
        # Validar stock de todos los productos antes de procesar
        for item in items:
            producto = ProductoRepository.obtener_por_id(item['producto_id'])
            if not producto:
                raise Exception(f"Producto {item['producto_id']} no existe")
            if producto.stock < item['cantidad']:
                raise Exception(f"Stock insuficiente para {producto.nombre}. Disponible: {producto.stock}")
        
        # Calcular total
        total = 0
        detalles_info = []
        for item in items:
            producto = ProductoRepository.obtener_por_id(item['producto_id'])
            subtotal = producto.precio * item['cantidad']
            total += subtotal
            detalles_info.append({
                'producto': producto,
                'cantidad': item['cantidad'],
                'subtotal': subtotal
            })
        
        # Crear venta
        venta = Venta(
            fecha=datetime.now().isoformat(),
            total=total,
            fk_cliente=fk_cliente,
            fk_usuario=fk_usuario,
            fk_caja=caja.id
        )
        venta = VentaRepository.crear(venta)
        
        # Crear detalles y actualizar stock (RF10)
        for info in detalles_info:
            detalle = DetalleVenta(
                fk_venta=venta.id,
                fk_producto=info['producto'].id,
                cantidad=info['cantidad'],
                precio_unitario=info['producto'].precio,
                subtotal=info['subtotal']
            )
            VentaRepository.crear_detalle(detalle)
            
            # RF10 - Actualizar stock automáticamente
            ProductoRepository.actualizar_stock(info['producto'].id, -info['cantidad'])
        
        return venta
    
    @staticmethod
    def obtener_venta_completa(id_venta):
        """Obtiene una venta con sus detalles"""
        venta = VentaRepository.obtener_por_id(id_venta)
        if not venta:
            return None
        
        detalles = VentaRepository.obtener_detalles(id_venta)
        return {
            'venta': venta.to_dict(),
            'detalles': [d.to_dict() for d in detalles]
        }
    
    @staticmethod
    def listar_ventas():
        """Lista todas las ventas"""
        ventas = VentaRepository.listar()
        return [v.to_dict() for v in ventas]
