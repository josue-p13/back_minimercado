from datetime import datetime
from app.repositories.venta_repository import VentaRepository
from app.repositories.producto_repository import ProductoRepository
from app.repositories.caja_repository import CajaRepository
from app.models.venta import Venta

class VentaService:
    
    @staticmethod
    def realizar_venta(items_request, fk_cliente, fk_usuario):
        # 1. Validar que la CAJA esté abierta
        caja = CajaRepository.obtener_abierta_por_usuario(fk_usuario)
        if not caja:
            raise Exception("No puedes vender porque no tienes una caja abierta.")

        total_venta = 0
        items_procesados = []

        # 2. Procesar cada item
        for item in items_request:
            prod_id = item['producto_id']
            cantidad = item['cantidad']
            
            producto = ProductoRepository.obtener_por_id(prod_id)
            if not producto:
                raise Exception(f"Producto ID {prod_id} no encontrado")
            
            # Validación de Stock
            if producto.stock < cantidad:
                raise Exception(f"Stock insuficiente para '{producto.nombre}'. Disponible: {producto.stock}")
            
            subtotal = producto.precio * cantidad
            total_venta += subtotal
            
            items_procesados.append({
                "producto_id": prod_id,
                "cantidad": cantidad,
                "precio": producto.precio,
                "subtotal": subtotal
            })

            # 3. Descontar Stock inmediatamente
            nuevo_stock = producto.stock - cantidad
            # 👇 AQUÍ SE LLAMA A LA FUNCIÓN DEL REPOSITORIO
            ProductoRepository.actualizar_stock(prod_id, nuevo_stock)

        # 4. Crear Objeto Venta
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        nueva_venta = Venta(
            fecha=fecha_actual,
            total=total_venta,
            fk_cliente=fk_cliente,
            fk_usuario=fk_usuario,
            fk_caja=caja.id
        )
        nueva_venta.items = items_procesados

        return VentaRepository.crear_venta(nueva_venta)

    @staticmethod
    def listar_ventas():
        return VentaRepository.listar()
        
    @staticmethod
    def obtener_venta(id):
        return VentaRepository.obtener_por_id(id)