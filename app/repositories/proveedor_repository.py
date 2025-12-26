"""
Repositorio de Proveedores
Gestiona las operaciones CRUD para la entidad Proveedor
"""
from app.database.connection import get_connection
from app.models.proveedor import Proveedor

class ProveedorRepository:
    
    @staticmethod
    def crear(proveedor):
        """Crea un nuevo proveedor"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO proveedor (nombre, telefono, direccion, activo)
            VALUES (?, ?, ?, ?)
        ''', (proveedor.nombre, proveedor.telefono, proveedor.direccion, proveedor.activo))
        conn.commit()
        proveedor.id = cursor.lastrowid
        conn.close()
        return proveedor
    
    @staticmethod
    def obtener_por_id(id):
        """Obtiene un proveedor por ID"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM proveedor WHERE id = ?', (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            # Mapeo según orden en tabla: id, nombre, telefono, direccion, activo
            return Proveedor(id=row[0], nombre=row[1], telefono=row[2], direccion=row[3], activo=row[4])
        return None
    
    @staticmethod
    def listar():
        """Lista todos los proveedores activos"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM proveedor WHERE activo = 1')
        rows = cursor.fetchall()
        conn.close()
        return [Proveedor(id=r[0], nombre=r[1], telefono=r[2], direccion=r[3], activo=r[4]) for r in rows]
    
    @staticmethod
    def actualizar(proveedor):
        """Actualiza la información de un proveedor"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE proveedor SET nombre = ?, telefono = ?, direccion = ?
            WHERE id = ?
        ''', (proveedor.nombre, proveedor.telefono, proveedor.direccion, proveedor.id))
        conn.commit()
        conn.close()
    
    @staticmethod
    def eliminar(id):
        """Elimina (desactiva) un proveedor"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE proveedor SET activo = 0 WHERE id = ?', (id,))
        conn.commit()
        conn.close()