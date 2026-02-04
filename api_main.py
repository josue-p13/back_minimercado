from fastapi import FastAPI, HTTPException, Header, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional, List

# Importaciones de tu app
from app.database.connection import init_db
from app.controllers.auth_controller import AuthController
from app.controllers.inventario_controller import InventarioController
from app.controllers.caja_controller import CajaController
from app.controllers.venta_controller import VentaController
from app.controllers.proveedor_controller import ProveedorController
from app.controllers.cliente_controller import ClienteController
from app.controllers.usuario_controller import UsuarioController

# Inicializar base de datos
init_db()

app = FastAPI(
    title="Sistema de Gestión de Minimercado",
    description="API REST para gestión de inventario, ventas, caja y proveedores",
    version="1.0.0"
)

# Archivos estáticos y Templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

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

# --- Modelos Gestión de Usuarios ---
class UsuarioCreateRequest(BaseModel):
    nombre: str
    username: str
    password: str
    rol: str

class UsuarioUpdateRequest(BaseModel):
    nombre: str
    username: str
    password: Optional[str] = None # Opcional
    rol: str

# --- Modelos Producto (INCLUYE CÓDIGO DE BARRAS) ---
class ProductoCreate(BaseModel):
    nombre: str
    precio: float
    stock: int
    stock_minimo: int
    fk_proveedor: Optional[int] = None
    codigo_barras: Optional[str] = None # <--- Nuevo

class ProductoUpdate(BaseModel):
    nombre: str
    precio: float
    stock: int
    stock_minimo: int
    fk_proveedor: Optional[int] = None
    codigo_barras: Optional[str] = None # <--- Nuevo

class AgregarStockRequest(BaseModel):
    cantidad: int

# --- Modelos Proveedor ---
class ProveedorCreate(BaseModel):
    nombre: str
    telefono: Optional[str] = None
    direccion: Optional[str] = None

class ProveedorUpdate(BaseModel):
    nombre: str
    telefono: Optional[str] = None
    direccion: Optional[str] = None

# --- Modelos Caja ---
class AbrirCajaRequest(BaseModel):
    monto_inicial: float
    fk_usuario: int

class CerrarCajaRequest(BaseModel):
    monto_final: float

# --- Modelos Venta (INCLUYE PAGOS) ---
class ItemVenta(BaseModel):
    producto_id: int
    cantidad: int

class VentaRequest(BaseModel):
    items: List[ItemVenta]
    fk_cliente: Optional[int] = None
    fk_usuario: int
    metodo_pago: str
    monto_pago: float
    referencia: Optional[str] = None    

# --- Modelos Cliente ---
class ClienteCreate(BaseModel):
    nombre: str
    telefono: Optional[str] = None
    email: Optional[str] = None

class ClienteUpdate(BaseModel):
    nombre: str
    telefono: Optional[str] = None
    email: Optional[str] = None


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
        request.nombre, request.username, request.password, request.rol
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

# ============= ENDPOINTS DE GESTIÓN DE USUARIOS (ADMIN) =============

@app.get("/api/usuarios")
def listar_usuarios():
    resultado = UsuarioController.listar_usuarios()
    if not resultado['success']: raise HTTPException(status_code=500, detail=resultado['message'])
    return resultado

@app.post("/api/usuarios")
def crear_usuario_admin(usuario: UsuarioCreateRequest):
    resultado = UsuarioController.agregar_usuario(
        usuario.nombre, usuario.username, usuario.password, usuario.rol
    )
    if not resultado['success']: raise HTTPException(status_code=400, detail=resultado['message'])
    return resultado

@app.get("/api/usuarios/{id}")
def buscar_usuario(id: int):
    resultado = UsuarioController.buscar_usuario(id)
    if not resultado['success']: raise HTTPException(status_code=404, detail=resultado['message'])
    return resultado

@app.put("/api/usuarios/{id}")
def actualizar_usuario(id: int, usuario: UsuarioUpdateRequest):
    resultado = UsuarioController.actualizar_usuario(
        id, usuario.nombre, usuario.username, usuario.password, usuario.rol
    )
    if not resultado['success']: raise HTTPException(status_code=400, detail=resultado['message'])
    return resultado

@app.delete("/api/usuarios/{id}")
def eliminar_usuario(id: int):
    resultado = UsuarioController.eliminar_usuario(id)
    if not resultado['success']: raise HTTPException(status_code=400, detail=resultado['message'])
    return resultado

# ============= ENDPOINTS DE INVENTARIO =============

@app.post("/api/inventario/productos")
def agregar_producto(producto: ProductoCreate):
    # Pasamos el nuevo campo codigo_barras
    resultado = InventarioController.agregar_producto(
        producto.nombre, producto.precio, producto.stock, 
        producto.stock_minimo, producto.fk_proveedor, 
        producto.codigo_barras
    )
    if not resultado['success']: raise HTTPException(status_code=400, detail=resultado['message'])
    return resultado

@app.get("/api/inventario/productos")
def listar_productos():
    resultado = InventarioController.listar_productos()
    if not resultado['success']: raise HTTPException(status_code=500, detail=resultado['message'])
    return resultado

@app.get("/api/inventario/productos/{id}")
def buscar_producto(id: int):
    resultado = InventarioController.buscar_producto(id)
    if not resultado['success']: raise HTTPException(status_code=404, detail=resultado['message'])
    return resultado

@app.put("/api/inventario/productos/{id}")
def actualizar_producto(id: int, producto: ProductoUpdate):
    # Pasamos el nuevo campo codigo_barras y el stock para edición completa
    resultado = InventarioController.actualizar_producto(
        id, producto.nombre, producto.precio, producto.stock, 
        producto.stock_minimo, producto.fk_proveedor, 
        producto.codigo_barras
    )
    if not resultado['success']: raise HTTPException(status_code=400, detail=resultado['message'])
    return resultado

@app.delete("/api/inventario/productos/{id}")
def eliminar_producto(id: int):
    resultado = InventarioController.eliminar_producto(id)
    if not resultado['success']: raise HTTPException(status_code=400, detail=resultado['message'])
    return resultado

@app.post("/api/inventario/productos/{id}/stock")
def agregar_stock(id: int, request: AgregarStockRequest):
    resultado = InventarioController.agregar_stock(id, request.cantidad)
    if not resultado['success']: raise HTTPException(status_code=400, detail=resultado['message'])
    return resultado

@app.get("/api/inventario/alertas")
def obtener_alertas_stock():
    resultado = InventarioController.obtener_alertas_stock()
    if not resultado['success']: raise HTTPException(status_code=500, detail=resultado['message'])
    return resultado

# ============= ENDPOINTS DE PROVEEDORES =============

@app.post("/api/proveedores")
def agregar_proveedor(proveedor: ProveedorCreate):
    resultado = ProveedorController.agregar_proveedor(
        proveedor.nombre, proveedor.telefono, proveedor.direccion
    )
    if not resultado['success']: raise HTTPException(status_code=400, detail=resultado['message'])
    return resultado

@app.get("/api/proveedores")
def listar_proveedores():
    resultado = ProveedorController.listar_proveedores()
    if not resultado['success']: raise HTTPException(status_code=500, detail=resultado['message'])
    return resultado

@app.get("/api/proveedores/{id}")
def buscar_proveedor(id: int):
    resultado = ProveedorController.buscar_proveedor(id)
    if not resultado['success']: raise HTTPException(status_code=404, detail=resultado['message'])
    return resultado

@app.put("/api/proveedores/{id}")
def actualizar_proveedor(id: int, proveedor: ProveedorUpdate):
    resultado = ProveedorController.actualizar_proveedor(
        id, proveedor.nombre, proveedor.telefono, proveedor.direccion
    )
    if not resultado['success']: raise HTTPException(status_code=400, detail=resultado['message'])
    return resultado

@app.delete("/api/proveedores/{id}")
def eliminar_proveedor(id: int):
    resultado = ProveedorController.eliminar_proveedor(id)
    if not resultado['success']: raise HTTPException(status_code=404, detail=resultado['message'])
    return resultado

# ============= ENDPOINTS DE CAJA =============

@app.post("/api/caja/abrir")
def abrir_caja(request: AbrirCajaRequest):
    resultado = CajaController.abrir_caja(request.monto_inicial, request.fk_usuario)
    if not resultado['success']: raise HTTPException(status_code=400, detail=resultado['message'])
    return resultado

@app.post("/api/caja/cerrar")
def cerrar_caja(request: CerrarCajaRequest):
    resultado = CajaController.cerrar_caja(request.monto_final)
    if not resultado['success']: raise HTTPException(status_code=400, detail=resultado['message'])
    return resultado

@app.get("/api/caja/actual")
def obtener_caja_actual():
    resultado = CajaController.obtener_caja_actual()
    if not resultado['success']: raise HTTPException(status_code=404, detail=resultado['message'])
    return resultado

@app.get("/api/caja")
def listar_cajas():
    resultado = CajaController.listar_cajas()
    if not resultado['success']: raise HTTPException(status_code=500, detail=resultado['message'])
    return resultado

# ============= ENDPOINTS DE VENTAS =============

@app.post("/api/ventas")
def realizar_venta(venta: VentaRequest):
    # Pasamos el objeto completo 'venta' para manejar los pagos
    resultado = VentaController.realizar_venta(venta)
    if not resultado['success']: raise HTTPException(status_code=400, detail=resultado['message'])
    return resultado

@app.get("/api/ventas")
def listar_ventas():
    resultado = VentaController.listar_ventas()
    if not resultado['success']: raise HTTPException(status_code=500, detail=resultado['message'])
    return resultado

@app.get("/api/ventas/{id}")
def obtener_venta(id: int):
    resultado = VentaController.obtener_venta(id)
    if not resultado['success']: raise HTTPException(status_code=404, detail=resultado['message'])
    return resultado

# ============= ENDPOINTS DE CLIENTES =============

@app.post("/api/clientes")
def agregar_cliente(cliente: ClienteCreate):
    resultado = ClienteController.agregar_cliente(cliente.nombre, cliente.telefono, cliente.email)
    if not resultado['success']: raise HTTPException(status_code=400, detail=resultado['message'])
    return resultado

@app.get("/api/clientes")
def listar_clientes():
    resultado = ClienteController.listar_clientes()
    if not resultado['success']: raise HTTPException(status_code=500, detail=resultado['message'])
    return resultado

@app.get("/api/clientes/{id}")
def buscar_cliente(id: int):
    resultado = ClienteController.buscar_cliente(id)
    if not resultado['success']: raise HTTPException(status_code=404, detail=resultado['message'])
    return resultado

@app.put("/api/clientes/{id}")
def actualizar_cliente(id: int, cliente: ClienteUpdate):
    resultado = ClienteController.actualizar_cliente(id, cliente.nombre, cliente.telefono, cliente.email)
    if not resultado['success']: raise HTTPException(status_code=400, detail=resultado['message'])
    return resultado

@app.delete("/api/clientes/{id}")
def eliminar_cliente(id: int):
    resultado = ClienteController.eliminar_cliente(id)
    if not resultado['success']: raise HTTPException(status_code=400, detail=resultado['message'])
    return resultado

# ============= PÁGINAS HTML =============

@app.get("/", response_class=HTMLResponse)
def root():
    """Pantalla de Bienvenida"""
    return """
    <html>
        <head>
            <title>Sistema Minimercado</title>
            <style>
                body { font-family: sans-serif; text-align: center; margin-top: 50px; background-color: #f4f4f4; }
                h1 { color: #333; }
                .btn { display: inline-block; padding: 10px 20px; margin: 10px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; }
                .btn:hover { background: #0056b3; }
            </style>
        </head>
        <body>
            <h1>Sistema de Gestión de Minimercado</h1>
            <p>API REST v1</p>
            <br>
            <a href="/login" class="btn">Iniciar Sesión</a>
            <a href="/docs" class="btn" style="background:#28a745">Documentación API</a>
        </body>
    </html>
    """

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login/login.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("login/register.html", {"request": request})

@app.get("/admin", response_class=HTMLResponse)
def admin_page(request: Request):
    return templates.TemplateResponse("roles/admin.html", {"request": request})

@app.get("/caja", response_class=HTMLResponse)
def caja_page(request: Request):
    return templates.TemplateResponse("roles/cajero.html", {"request": request})

@app.get("/auxiliar", response_class=HTMLResponse)
def auxiliar_page(request: Request):
    return templates.TemplateResponse("roles/auxiliar.html", {"request": request})

# MÓDULOS DE ADMINISTRACIÓN
@app.get("/admin/usuarios", response_class=HTMLResponse)
async def usuarios_page(request: Request):
    # Ruta corregida: usuarios/admin_usuarios.html
    return templates.TemplateResponse("usuarios/admin_usuarios.html", {"request": request})

@app.get("/admin/clientes", response_class=HTMLResponse)
async def clientes_page(request: Request):
    return templates.TemplateResponse("clientes/clientes.html", {"request": request})

@app.get("/admin/proveedores", response_class=HTMLResponse)
async def proveedores_page(request: Request):
    return templates.TemplateResponse("proveedores/proveedores.html", {"request": request})

@app.get("/admin/productos", response_class=HTMLResponse)
async def productos_page(request: Request):
    return templates.TemplateResponse("productos/productos.html", {"request": request})

@app.get("/admin/ventas", response_class=HTMLResponse)
async def historial_page(request: Request):
    return templates.TemplateResponse("ventas/historial.html", {"request": request})

# MÓDULO DE VENTAS (POS)
@app.get("/ventas/nuevo", response_class=HTMLResponse)
async def pos_page(request: Request):
    return templates.TemplateResponse("ventas/pos.html", {"request": request})

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API funcionando correctamente"}

if __name__ == "__main__":
    import uvicorn
    # Imprimimos accesos rápidos en consola
    print("----------------------------------------------------------------")
    print("🚀 SERVIDOR INICIADO")
    print("📄 Swagger Docs: http://localhost:8000/docs")
    print("🔑 Login:        http://localhost:8000/login")
    print("----------------------------------------------------------------")
    uvicorn.run(app, host="localhost", port=8000)