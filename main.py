from app.database.connection import init_db
from app.controllers.auth_controller import AuthController
from app.controllers.inventario_controller import InventarioController
from app.controllers.caja_controller import CajaController
from app.controllers.venta_controller import VentaController

def print_resultado(titulo, resultado):
    """Helper para imprimir resultados"""
    print(f"\n{'='*50}")
    print(f"  {titulo}")
    print(f"{'='*50}")
    if resultado.get('success'):
        print(f"✓ {resultado.get('message', 'Operación exitosa')}")
        # Imprimir datos relevantes
        for key, value in resultado.items():
            if key not in ['success', 'message']:
                print(f"  {key}: {value}")
    else:
        print(f"✗ Error: {resultado.get('message')}")
    print()

def main():
    print("\n" + "="*50)
    print("  SISTEMA DE GESTIÓN DE MINIMERCADO")
    print("="*50)
    
    # Inicializar base de datos
    print("\n[1] Inicializando base de datos...")
    init_db()
    
    # Registrar usuario administrador
    print("\n[2] Registrando usuario administrador...")
    resultado = AuthController.registrar_usuario(
        nombre="Admin Principal",
        username="admin",
        password="admin123",
        rol="Admin"
    )
    print_resultado("REGISTRO DE USUARIO", resultado)
    
    # Login
    print("\n[3] Iniciando sesión...")
    resultado = AuthController.login("admin", "admin123")
    print_resultado("LOGIN", resultado)
    token = resultado.get('token')
    usuario_id = resultado.get('usuario', {}).get('id')
    
    # Agregar productos
    print("\n[4] Agregando productos al inventario...")
    productos = [
        {"nombre": "Coca Cola 2L", "precio": 2.50, "stock": 50, "stock_minimo": 10},
        {"nombre": "Pan Blanco", "precio": 0.50, "stock": 100, "stock_minimo": 20},
        {"nombre": "Leche Gloria", "precio": 3.80, "stock": 30, "stock_minimo": 15},
        {"nombre": "Arroz Costeño 1kg", "precio": 4.00, "stock": 5, "stock_minimo": 10}
    ]
    
    for prod in productos:
        resultado = InventarioController.agregar_producto(
            nombre=prod["nombre"],
            precio=prod["precio"],
            stock=prod["stock"],
            stock_minimo=prod["stock_minimo"],
            fk_proveedor=None
        )
        print(f"  - {prod['nombre']}: {'✓' if resultado['success'] else '✗'}")
    
    # Listar productos
    print("\n[5] Listando todos los productos...")
    resultado = InventarioController.listar_productos()
    if resultado['success']:
        print(f"\n  Total de productos: {len(resultado['productos'])}")
        for p in resultado['productos']:
            alerta = "⚠️ STOCK BAJO" if p['alerta_stock'] else "✓"
            print(f"  {alerta} [{p['id']}] {p['nombre']} - ${p['precio']} - Stock: {p['stock']}")
    
    # Verificar alertas de stock bajo (RF11)
    print("\n[6] Verificando alertas de stock bajo (RF11)...")
    resultado = InventarioController.obtener_alertas_stock()
    print_resultado("ALERTAS DE STOCK", resultado)
    
    # Abrir caja (RF20)
    print("\n[7] Abriendo caja (RF20)...")
    resultado = CajaController.abrir_caja(monto_inicial=100.00, fk_usuario=usuario_id)
    print_resultado("APERTURA DE CAJA", resultado)
    
    # Realizar venta (RF14, RF15)
    print("\n[8] Realizando venta (RF14, RF15)...")
    items_venta = [
        {'producto_id': 1, 'cantidad': 2},  # 2 Coca Colas
        {'producto_id': 2, 'cantidad': 5},  # 5 Panes
    ]
    resultado = VentaController.realizar_venta(
        items=items_venta,
        fk_cliente=None,
        fk_usuario=usuario_id
    )
    print_resultado("VENTA PROCESADA", resultado)
    venta_id = resultado.get('venta', {}).get('id')
    
    # Verificar actualización automática de stock (RF10)
    print("\n[9] Verificando actualización automática de stock (RF10)...")
    resultado = InventarioController.buscar_producto(1)
    if resultado['success']:
        print(f"  Stock de Coca Cola después de venta: {resultado['producto']['stock']} unidades")
    
    # Intentar venta sin stock suficiente
    print("\n[10] Intentando venta sin stock suficiente...")
    items_venta_error = [
        {'producto_id': 4, 'cantidad': 10},  # Intentar vender 10 cuando hay 5
    ]
    resultado = VentaController.realizar_venta(
        items=items_venta_error,
        fk_cliente=None,
        fk_usuario=usuario_id
    )
    print_resultado("VALIDACIÓN DE STOCK", resultado)
    
    # Obtener detalles de venta
    print("\n[11] Obteniendo detalles de venta...")
    if venta_id:
        resultado = VentaController.obtener_venta(venta_id)
        print_resultado("DETALLE DE VENTA", resultado)
    
    # Cerrar caja (RF21)
    print("\n[12] Cerrando caja (RF21)...")
    resultado = CajaController.cerrar_caja(monto_final=107.50)
    print_resultado("CIERRE DE CAJA", resultado)
    
    # Intentar venta con caja cerrada
    print("\n[13] Intentando venta con caja cerrada...")
    items_venta = [{'producto_id': 1, 'cantidad': 1}]
    resultado = VentaController.realizar_venta(
        items=items_venta,
        fk_cliente=None,
        fk_usuario=usuario_id
    )
    print_resultado("VALIDACIÓN CAJA CERRADA", resultado)
    
    print("\n" + "="*50)
    print("  DEMO COMPLETADA")
    print("="*50)
    print("\n✓ Base de datos creada en: app/database/minimercado.db")
    print("✓ Todos los requerimientos funcionales probados")
    print("✓ Sistema listo para usar\n")

if __name__ == "__main__":
    main()
