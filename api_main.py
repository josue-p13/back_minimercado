"""
API REST con FastAPI para el Sistema de Gestión de Minimercado
"""
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from app.database.connection import init_db
from app.controllers.auth_controller import AuthController
from app.controllers.inventario_controller import InventarioController
from app.controllers.caja_controller import CajaController
from app.controllers.venta_controller import VentaController

# Inicializar base de datos
init_db()

# Crear aplicación FastAPI
app = FastAPI(
    title="Sistema de Gestión de Minimercado",
    description="API REST para gestión de inventario, ventas y caja",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============= MODELOS PYDANTIC =============

class LoginRequest(BaseModel):
    username: str
    password: str

class RegistrarUsuarioRequest(BaseModel):
    nombre: str
    username: str
    password: str
    rol: str

class ProductoCreate(BaseModel):
    nombre: str
    precio: float
    stock: int
    stock_minimo: int
    fk_proveedor: Optional[int] = None

class ProductoUpdate(BaseModel):
    nombre: str
    precio: float
    stock_minimo: int

class AgregarStockRequest(BaseModel):
    cantidad: int

class AbrirCajaRequest(BaseModel):
    monto_inicial: float
    fk_usuario: int

class CerrarCajaRequest(BaseModel):
    monto_final: float

class ItemVenta(BaseModel):
    producto_id: int
    cantidad: int

class VentaRequest(BaseModel):
    items: List[ItemVenta]
    fk_cliente: Optional[int] = None
    fk_usuario: int

# ============= ENDPOINTS DE AUTENTICACIÓN =============

@app.post("/api/auth/login")
def login(request: LoginRequest):
    """Iniciar sesión"""
    resultado = AuthController.login(request.username, request.password)
    if not resultado['success']:
        raise HTTPException(status_code=401, detail=resultado['message'])
    return resultado

@app.post("/api/auth/register")
def registrar_usuario(request: RegistrarUsuarioRequest):
    """Registrar un nuevo usuario"""
    resultado = AuthController.registrar_usuario(
        request.nombre,
        request.username,
        request.password,
        request.rol
    )
    if not resultado['success']:
        raise HTTPException(status_code=400, detail=resultado['message'])
    return resultado

@app.post("/api/auth/validate")
def validar_token(authorization: Optional[str] = Header(None)):
    """Validar token de autenticación"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Token no proporcionado")
    
    token = authorization.replace("Bearer ", "")
    resultado = AuthController.validar_token(token)
    if not resultado['success']:
        raise HTTPException(status_code=401, detail=resultado['message'])
    return resultado

# ============= ENDPOINTS DE INVENTARIO =============

@app.post("/api/inventario/productos")
def agregar_producto(producto: ProductoCreate):
    """Agregar un nuevo producto"""
    resultado = InventarioController.agregar_producto(
        producto.nombre,
        producto.precio,
        producto.stock,
        producto.stock_minimo,
        producto.fk_proveedor
    )
    if not resultado['success']:
        raise HTTPException(status_code=400, detail=resultado['message'])
    return resultado

@app.get("/api/inventario/productos")
def listar_productos():
    """Listar todos los productos"""
    resultado = InventarioController.listar_productos()
    if not resultado['success']:
        raise HTTPException(status_code=500, detail=resultado['message'])
    return resultado

@app.get("/api/inventario/productos/{id}")
def buscar_producto(id: int):
    """Buscar un producto por ID"""
    resultado = InventarioController.buscar_producto(id)
    if not resultado['success']:
        raise HTTPException(status_code=404, detail=resultado['message'])
    return resultado

@app.put("/api/inventario/productos/{id}")
def actualizar_producto(id: int, producto: ProductoUpdate):
    """Actualizar un producto"""
    resultado = InventarioController.actualizar_producto(
        id,
        producto.nombre,
        producto.precio,
        producto.stock_minimo
    )
    if not resultado['success']:
        raise HTTPException(status_code=400, detail=resultado['message'])
    return resultado

@app.post("/api/inventario/productos/{id}/stock")
def agregar_stock(id: int, request: AgregarStockRequest):
    """Agregar stock a un producto (RF10)"""
    resultado = InventarioController.agregar_stock(id, request.cantidad)
    if not resultado['success']:
        raise HTTPException(status_code=400, detail=resultado['message'])
    return resultado

@app.get("/api/inventario/alertas")
def obtener_alertas_stock():
    """Obtener productos con stock bajo (RF11)"""
    resultado = InventarioController.obtener_alertas_stock()
    if not resultado['success']:
        raise HTTPException(status_code=500, detail=resultado['message'])
    return resultado

# ============= ENDPOINTS DE CAJA =============

@app.post("/api/caja/abrir")
def abrir_caja(request: AbrirCajaRequest):
    """Abrir una caja (RF20)"""
    resultado = CajaController.abrir_caja(
        request.monto_inicial,
        request.fk_usuario
    )
    if not resultado['success']:
        raise HTTPException(status_code=400, detail=resultado['message'])
    return resultado

@app.post("/api/caja/cerrar")
def cerrar_caja(request: CerrarCajaRequest):
    """Cerrar la caja actual (RF21)"""
    resultado = CajaController.cerrar_caja(request.monto_final)
    if not resultado['success']:
        raise HTTPException(status_code=400, detail=resultado['message'])
    return resultado

@app.get("/api/caja/actual")
def obtener_caja_actual():
    """Obtener la caja actualmente abierta"""
    resultado = CajaController.obtener_caja_actual()
    if not resultado['success']:
        raise HTTPException(status_code=404, detail=resultado['message'])
    return resultado

@app.get("/api/caja")
def listar_cajas():
    """Listar todas las cajas"""
    resultado = CajaController.listar_cajas()
    if not resultado['success']:
        raise HTTPException(status_code=500, detail=resultado['message'])
    return resultado

# ============= ENDPOINTS DE VENTAS =============

@app.post("/api/ventas")
def realizar_venta(venta: VentaRequest):
    """Realizar una venta (RF14, RF15)"""
    items = [item.dict() for item in venta.items]
    resultado = VentaController.realizar_venta(
        items,
        venta.fk_cliente,
        venta.fk_usuario
    )
    if not resultado['success']:
        raise HTTPException(status_code=400, detail=resultado['message'])
    return resultado

@app.get("/api/ventas")
def listar_ventas():
    """Listar todas las ventas"""
    resultado = VentaController.listar_ventas()
    if not resultado['success']:
        raise HTTPException(status_code=500, detail=resultado['message'])
    return resultado

@app.get("/api/ventas/{id}")
def obtener_venta(id: int):
    """Obtener una venta con sus detalles"""
    resultado = VentaController.obtener_venta(id)
    if not resultado['success']:
        raise HTTPException(status_code=404, detail=resultado['message'])
    return resultado

# ============= ENDPOINT RAÍZ =============

@app.get("/")
def root():
    """Endpoint raíz"""
    return {
        "message": "Sistema de Gestión de Minimercado - API REST",
        "version": "1.0.0",
        "endpoints": {
            "auth": "/api/auth",
            "inventario": "/api/inventario",
            "caja": "/api/caja",
            "ventas": "/api/ventas",
            "docs": "/docs"
        }
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "ok", "message": "API funcionando correctamente"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
