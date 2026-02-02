from app.database.connection import get_connection
from app.models.cliente import Cliente

class ClienteRepository:
    
    @staticmethod
    def crear(cliente):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO cliente (nombre, telefono, email, activo)
                VALUES (?, ?, ?, ?)
            ''', (cliente.nombre, cliente.telefono, cliente.email, cliente.activo))
            conn.commit()
            cliente.id = cursor.lastrowid
            return cliente
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @staticmethod
    def listar():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM cliente WHERE activo = 1')
        rows = cursor.fetchall()
        conn.close()
        return [Cliente(id=r[0], nombre=r[1], telefono=r[2], email=r[3], activo=r[4]) for r in rows]

    @staticmethod
    def obtener_por_id(id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM cliente WHERE id = ?', (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Cliente(id=row[0], nombre=row[1], telefono=row[2], email=row[3], activo=row[4])
        return None

    @staticmethod
    def actualizar(cliente):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE cliente SET nombre = ?, telefono = ?, email = ?
                WHERE id = ?
            ''', (cliente.nombre, cliente.telefono, cliente.email, cliente.id))
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def eliminar(id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('UPDATE cliente SET activo = 0 WHERE id = ?', (id,))
            conn.commit()
        finally:
            conn.close()