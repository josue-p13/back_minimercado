"""
Repositorio de Ventas
RF14, RF15 - Procesar ventas
"""
from app.database.connection import get_connection
from app.models.venta import Venta, DetalleVenta

class VentaRepository:
    
    @staticmethod
    def crear(venta):
        """Crea una nueva venta"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO venta (fecha, total, fk_cliente, fk_usuario, fk_caja)
            VALUES (?, ?, ?, ?, ?)
        ''', (venta.fecha, venta.total, venta.fk_cliente, venta.fk_usuario, venta.fk_caja))
        conn.commit()
        venta.id = cursor.lastrowid
        conn.close()
        return venta
    
    @staticmethod
    def crear_detalle(detalle):
        """Crea un detalle de venta"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO detalle_venta (fk_venta, fk_producto, cantidad, precio_unitario, subtotal)
            VALUES (?, ?, ?, ?, ?)
        ''', (detalle.fk_venta, detalle.fk_producto, detalle.cantidad, detalle.precio_unitario, detalle.subtotal))
        conn.commit()
        detalle.id = cursor.lastrowid
        conn.close()
        return detalle
    
    @staticmethod
    def obtener_por_id(id):
        """Obtiene una venta por ID"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM venta WHERE id = ?', (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Venta(row[0], row[1], row[2], row[3], row[4], row[5])
        return None
    
    @staticmethod
    def obtener_detalles(id_venta):
        """Obtiene los detalles de una venta"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM detalle_venta WHERE fk_venta = ?', (id_venta,))
        rows = cursor.fetchall()
        conn.close()
        return [DetalleVenta(r[0], r[1], r[2], r[3], r[4], r[5]) for r in rows]
    
    @staticmethod
    def listar():
        """Lista todas las ventas"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM venta ORDER BY fecha DESC')
        rows = cursor.fetchall()
        conn.close()
        return [Venta(r[0], r[1], r[2], r[3], r[4], r[5]) for r in rows]
