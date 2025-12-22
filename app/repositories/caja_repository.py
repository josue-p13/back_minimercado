"""
Repositorio de Caja
RF20, RF21 - Control de caja
"""
from app.database.connection import get_connection
from app.models.caja import Caja

class CajaRepository:
    
    @staticmethod
    def crear(caja):
        """Crea una nueva apertura de caja"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO caja (fecha_apertura, monto_inicial, fk_usuario, estado)
            VALUES (?, ?, ?, ?)
        ''', (caja.fecha_apertura, caja.monto_inicial, caja.fk_usuario, caja.estado))
        conn.commit()
        caja.id = cursor.lastrowid
        conn.close()
        return caja
    
    @staticmethod
    def obtener_por_id(id):
        """Obtiene una caja por ID"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM caja WHERE id = ?', (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Caja(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
        return None
    
    @staticmethod
    def obtener_caja_abierta():
        """Obtiene la caja actualmente abierta"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM caja WHERE estado = 'Abierta' ORDER BY fecha_apertura DESC LIMIT 1")
        row = cursor.fetchone()
        conn.close()
        if row:
            return Caja(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
        return None
    
    @staticmethod
    def cerrar_caja(id, fecha_cierre, monto_final):
        """RF21 - Cierra una caja"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE caja SET fecha_cierre = ?, monto_final = ?, estado = 'Cerrada'
            WHERE id = ?
        ''', (fecha_cierre, monto_final, id))
        conn.commit()
        conn.close()
    
    @staticmethod
    def listar():
        """Lista todas las cajas"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM caja ORDER BY fecha_apertura DESC')
        rows = cursor.fetchall()
        conn.close()
        return [Caja(r[0], r[1], r[2], r[3], r[4], r[5], r[6]) for r in rows]
