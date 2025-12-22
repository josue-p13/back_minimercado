"""
Repositorio de Productos
RF10 - Actualización automática de inventario
"""
from app.database.connection import get_connection
from app.models.producto import Producto

class ProductoRepository:
    
    @staticmethod
    def crear(producto):
        """Crea un nuevo producto"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO producto (nombre, precio, stock, stock_minimo, fk_proveedor, activo)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (producto.nombre, producto.precio, producto.stock, producto.stock_minimo, producto.fk_proveedor, producto.activo))
        conn.commit()
        producto.id = cursor.lastrowid
        conn.close()
        return producto
    
    @staticmethod
    def obtener_por_id(id):
        """Obtiene un producto por ID"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM producto WHERE id = ?', (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Producto(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
        return None
    
    @staticmethod
    def listar():
        """Lista todos los productos activos"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM producto WHERE activo = 1')
        rows = cursor.fetchall()
        conn.close()
        return [Producto(r[0], r[1], r[2], r[3], r[4], r[5], r[6]) for r in rows]
    
    @staticmethod
    def actualizar(producto):
        """Actualiza un producto"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE producto SET nombre = ?, precio = ?, stock = ?, stock_minimo = ?, fk_proveedor = ?
            WHERE id = ?
        ''', (producto.nombre, producto.precio, producto.stock, producto.stock_minimo, producto.fk_proveedor, producto.id))
        conn.commit()
        conn.close()
    
    @staticmethod
    def actualizar_stock(id, cantidad):
        """RF10 - Actualiza el stock de un producto"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE producto SET stock = stock + ? WHERE id = ?', (cantidad, id))
        conn.commit()
        conn.close()
    
    @staticmethod
    def obtener_productos_bajo_stock():
        """RF11 - Obtiene productos con stock bajo"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM producto WHERE stock <= stock_minimo AND activo = 1')
        rows = cursor.fetchall()
        conn.close()
        return [Producto(r[0], r[1], r[2], r[3], r[4], r[5], r[6]) for r in rows]
    
    @staticmethod
    def eliminar(id):
        """Elimina (desactiva) un producto"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE producto SET activo = 0 WHERE id = ?', (id,))
        conn.commit()
        conn.close()
