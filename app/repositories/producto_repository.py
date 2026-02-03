"""
Repositorio de Productos
"""
from app.database.connection import get_connection
from app.models.producto import Producto

class ProductoRepository:
    
    @staticmethod
    def crear(producto):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO producto (nombre, precio, stock, stock_minimo, fk_proveedor, activo)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (producto.nombre, producto.precio, producto.stock, producto.stock_minimo, producto.fk_proveedor, producto.activo))
            conn.commit()
            producto.id = cursor.lastrowid
            return producto
        finally:
            conn.close()

    @staticmethod
    def listar():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM producto WHERE activo = 1')
        rows = cursor.fetchall()
        conn.close()
        return [Producto(id=r[0], nombre=r[1], precio=r[2], stock=r[3], stock_minimo=r[4], fk_proveedor=r[5], activo=r[6]) for r in rows]

    @staticmethod
    def obtener_por_id(id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM producto WHERE id = ?', (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Producto(id=row[0], nombre=row[1], precio=row[2], stock=row[3], stock_minimo=row[4], fk_proveedor=row[5], activo=row[6])
        return None

    # 👇 ESTA ES LA FUNCIÓN CLAVE QUE SEGURAMENTE TE FALTA 👇
    @staticmethod
    def actualizar_stock(id, nuevo_stock):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('UPDATE producto SET stock = ? WHERE id = ?', (nuevo_stock, id))
            conn.commit()
        finally:
            conn.close()
    # 👆 -------------------------------------------------- 👆

    @staticmethod
    def actualizar(producto):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE producto SET nombre = ?, precio = ?, stock_minimo = ?
                WHERE id = ?
            ''', (producto.nombre, producto.precio, producto.stock_minimo, producto.id))
            conn.commit()
        finally:
            conn.close()