"""
Conexión a base de datos SQLite
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'minimercado.db')

def get_connection():
    """Obtiene una conexión a la base de datos"""
    return sqlite3.connect(DB_PATH)

def init_db():
    """Inicializa las tablas de la base de datos"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Tabla Usuario (RNF2 - Roles: Admin, Cajero, Auxiliar)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            rol TEXT NOT NULL CHECK(rol IN ('Admin', 'Cajero', 'Auxiliar')),
            activo INTEGER DEFAULT 1
        )
    ''')
    
    # Tabla Proveedor
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS proveedor (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT,
            direccion TEXT,
            activo INTEGER DEFAULT 1
        )
    ''')
    
    # Tabla Producto (RF10 - Control de inventario)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS producto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER DEFAULT 0,
            stock_minimo INTEGER DEFAULT 5,
            fk_proveedor INTEGER,
            codigo_barras TEXT,
            activo INTEGER DEFAULT 1,
            FOREIGN KEY (fk_proveedor) REFERENCES proveedor(id)
        )
    ''')
    
    # Tabla Cliente
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cliente (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT,
            email TEXT,
            activo INTEGER DEFAULT 1
        )
    ''')
    
    # Tabla Caja (RF20, RF21 - Control de apertura/cierre)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS caja (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha_apertura TEXT NOT NULL,
            fecha_cierre TEXT,
            monto_inicial REAL NOT NULL,
            monto_final REAL,
            fk_usuario INTEGER,
            estado TEXT DEFAULT 'Abierta' CHECK(estado IN ('Abierta', 'Cerrada')),
            FOREIGN KEY (fk_usuario) REFERENCES usuario(id)
        )
    ''')
    
    # Tabla Venta (RF14, RF15 - Procesar ventas)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS venta (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            total REAL NOT NULL,
            fk_cliente INTEGER,
            fk_usuario INTEGER,
            fk_caja INTEGER,
            FOREIGN KEY (fk_cliente) REFERENCES cliente(id),
            FOREIGN KEY (fk_usuario) REFERENCES usuario(id),
            FOREIGN KEY (fk_caja) REFERENCES caja(id)
        )
    ''')
    
    # Tabla DetalleVenta (RF14, RF15 - Detalle de productos en venta)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS detalle_venta (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fk_venta INTEGER,
            fk_producto INTEGER,
            cantidad INTEGER NOT NULL,
            precio_unitario REAL NOT NULL,
            subtotal REAL NOT NULL,
            FOREIGN KEY (fk_venta) REFERENCES venta(id),
            FOREIGN KEY (fk_producto) REFERENCES producto(id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Base de datos inicializada correctamente")