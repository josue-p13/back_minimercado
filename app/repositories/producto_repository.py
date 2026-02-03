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
            # AGREGAMOS codigo_barras al INSERT
            cursor.execute('''
                INSERT INTO producto (nombre, precio, stock, stock_minimo, fk_proveedor, activo, codigo_barras)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (producto.nombre, producto.precio, producto.stock, producto.stock_minimo, producto.fk_proveedor, producto.activo, producto.codigo_barras))
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
        # Mapeamos row[7] que es la nueva columna
        return [Producto(id=r[0], nombre=r[1], precio=r[2], stock=r[3], stock_minimo=r[4], fk_proveedor=r[5], activo=r[6], codigo_barras=r[7] if len(r)>7 else None) for r in rows]

    @staticmethod
    def obtener_por_id(id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM producto WHERE id = ?', (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
             # Mapeamos row[7]
            return Producto(id=row[0], nombre=row[1], precio=row[2], stock=row[3], stock_minimo=row[4], fk_proveedor=row[5], activo=row[6], codigo_barras=row[7] if len(row)>7 else None)
        return None

    @staticmethod
    def actualizar(producto):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            # AGREGAMOS codigo_barras al UPDATE
            cursor.execute('''
                UPDATE producto 
                SET nombre = ?, precio = ?, stock = ?, stock_minimo = ?, fk_proveedor = ?, codigo_barras = ?
                WHERE id = ?
            ''', (producto.nombre, producto.precio, producto.stock, producto.stock_minimo, producto.fk_proveedor, producto.codigo_barras, producto.id))
            conn.commit()
        finally:
            conn.close()
    @staticmethod
    def actualizar_stock(id, nuevo_stock):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('UPDATE producto SET stock = ? WHERE id = ?', (nuevo_stock, id))
            conn.commit()
        finally:
            conn.close()
    @staticmethod
    def eliminar(id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            # Soft delete: cambiamos activo a 0
            cursor.execute('UPDATE producto SET activo = 0 WHERE id = ?', (id,))
            conn.commit()
        finally:
            conn.close()