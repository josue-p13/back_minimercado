"""
Repositorio de Usuarios
Operaciones CRUD básicas
"""
from app.database.connection import get_connection
from app.models.usuario import Usuario

class UsuarioRepository:
    
    @staticmethod
    def crear(usuario):
        """Crea un nuevo usuario"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO usuario (nombre, username, password_hash, rol, activo)
            VALUES (?, ?, ?, ?, ?)
        ''', (usuario.nombre, usuario.username, usuario.password_hash, usuario.rol, usuario.activo))
        conn.commit()
        usuario.id = cursor.lastrowid
        conn.close()
        return usuario
    
    @staticmethod
    def obtener_por_id(id):
        """Obtiene un usuario por ID"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuario WHERE id = ?', (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Usuario(row[0], row[1], row[2], row[3], row[4], row[5])
        return None
    
    @staticmethod
    def obtener_por_username(username):
        """Obtiene un usuario por username"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuario WHERE username = ?', (username,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Usuario(row[0], row[1], row[2], row[3], row[4], row[5])
        return None
    
    @staticmethod
    def listar():
        """Lista todos los usuarios activos"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuario WHERE activo = 1')
        rows = cursor.fetchall()
        conn.close()
        return [Usuario(r[0], r[1], r[2], r[3], r[4], r[5]) for r in rows]
    
    @staticmethod
    def actualizar(usuario):
        """Actualiza un usuario"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE usuario SET nombre = ?, rol = ?, activo = ?
            WHERE id = ?
        ''', (usuario.nombre, usuario.rol, usuario.activo, usuario.id))
        conn.commit()
        conn.close()
    
    @staticmethod
    def eliminar(id):
        """Elimina (desactiva) un usuario"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE usuario SET activo = 0 WHERE id = ?', (id,))
        conn.commit()
        conn.close()
