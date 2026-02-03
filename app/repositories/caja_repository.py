from app.database.connection import get_connection
from app.models.caja import Caja

class CajaRepository:
    
    @staticmethod
    def abrir(caja):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO caja (fecha_apertura, monto_inicial, fk_usuario, estado)
                VALUES (?, ?, ?, 'Abierta')
            ''', (caja.fecha_apertura, caja.monto_inicial, caja.fk_usuario))
            conn.commit()
            caja.id = cursor.lastrowid
            return caja
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @staticmethod
    def cerrar(id, fecha_cierre, monto_final):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE caja 
                SET fecha_cierre = ?, monto_final = ?, estado = 'Cerrada'
                WHERE id = ?
            ''', (fecha_cierre, monto_final, id))
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def obtener_abierta_por_usuario(fk_usuario):
        """Busca si el usuario tiene una caja abierta actualmente"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM caja 
            WHERE fk_usuario = ? AND estado = 'Abierta'
            ORDER BY id DESC LIMIT 1
        ''', (fk_usuario,))
        row = cursor.fetchone()
        conn.close()
        if row:
            # Mapeo: id, fecha_apertura, fecha_cierre, monto_inicial, monto_final, fk_usuario, estado
            return Caja(id=row[0], fecha_apertura=row[1], fecha_cierre=row[2], 
                       monto_inicial=row[3], monto_final=row[4], 
                       fk_usuario=row[5], estado=row[6])
        return None

    @staticmethod
    def listar_todas():
        """Para historial de cajas (Admin)"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM caja ORDER BY id DESC')
        rows = cursor.fetchall()
        conn.close()
        return [Caja(id=r[0], fecha_apertura=r[1], fecha_cierre=r[2], 
                     monto_inicial=r[3], monto_final=r[4], 
                     fk_usuario=r[5], estado=r[6]) for r in rows]