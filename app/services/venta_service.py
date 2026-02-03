from datetime import datetime
from app.repositories.venta_repository import VentaRepository
from app.repositories.producto_repository import ProductoRepository
from app.repositories.caja_repository import CajaRepository
from app.models.venta import Venta

class VentaService:
    
    @staticmethod
    def realizar_venta(items_request, fk_cliente, fk_usuario, metodo_pago, monto_pago, referencia): # <--- Params nuevos
        # 1. Validar Caja (Igual que antes)
        caja = CajaRepository.obtener_abierta_por_usuario(fk_usuario)
        if not caja:
            raise Exception("No puedes vender porque no tienes una caja abierta.")

        total_venta = 0
        items_procesados = []

        # 2. Procesar Items y Stock (Igual que antes)
        for item in items_request:
            prod_id = item['producto_id']
            cantidad = item['cantidad']
            producto = ProductoRepository.obtener_por_id(prod_id)
            if not producto: raise Exception(f"Producto ID {prod_id} no encontrado")
            if producto.stock < cantidad: raise Exception(f"Stock insuficiente para '{producto.nombre}'")
            
            subtotal = producto.precio * cantidad
            total_venta += subtotal
            items_procesados.append({
                "producto_id": prod_id, "cantidad": cantidad, "precio": producto.precio, "subtotal": subtotal
            })
            ProductoRepository.actualizar_stock(prod_id, producto.stock - cantidad)

        # 3. Lógica de Pago (NUEVO)
        cambio = 0
        if metodo_pago == "Efectivo":
            if monto_pago < total_venta:
                raise Exception("El monto pagado es menor al total de la venta")
            cambio = monto_pago - total_venta
        else:
            # Para tarjeta y transferencia, el monto pagado es exacto al total
            monto_pago = total_venta 
            cambio = 0

        # 4. Crear Venta
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        nueva_venta = Venta(
            fecha=fecha_actual,
            total=total_venta,
            fk_cliente=fk_cliente,
            fk_usuario=fk_usuario,
            fk_caja=caja.id,
            metodo_pago=metodo_pago,
            monto_pago=monto_pago,   
            cambio=cambio,           
            referencia=referencia    
        )
        nueva_venta.items = items_procesados
        return VentaRepository.crear_venta(nueva_venta)

    @staticmethod
    def listar_ventas():
        return VentaRepository.listar()
        
    @staticmethod
    def obtener_venta(id):
        return VentaRepository.obtener_por_id(id)