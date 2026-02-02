"""
Repositorio de Usuarios
Gestiona las operaciones CRUD para la entidad Usuario
"""
from app.database.connection import get_connection
from app.models.usuario import Usuario

class UsuarioRepository:
    
    @staticmethod
    def crear(usuario):
        """Crea un nuevo usuario en la base de datos"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO usuario (nombre, username, password_hash, rol, activo)
                VALUES (?, ?, ?, ?, ?)
            ''', (usuario.nombre, usuario.username, usuario.password_hash, usuario.rol, usuario.activo))
            conn.commit()
            usuario.id = cursor.lastrowid
            return usuario
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    @staticmethod
    def obtener_por_id(id):
        """Obtiene un usuario por ID"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuario WHERE id = ?', (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            # id, nombre, username, password_hash, rol, activo
            return Usuario(id=row[0], nombre=row[1], username=row[2], password_hash=row[3], rol=row[4], activo=row[5])
        return None

    @staticmethod
    def obtener_por_username(username):
        """Obtiene un usuario por Username (para validaciones)"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuario WHERE username = ? AND activo = 1', (username,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Usuario(id=row[0], nombre=row[1], username=row[2], password_hash=row[3], rol=row[4], activo=row[5])
        return None
    
    @staticmethod
    def listar():
        """Lista todos los usuarios activos"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuario WHERE activo = 1')
        rows = cursor.fetchall()
        conn.close()
        return [Usuario(id=r[0], nombre=r[1], username=r[2], password_hash=r[3], rol=r[4], activo=r[5]) for r in rows]
    
    @staticmethod
    def actualizar(usuario):
        """Actualiza la información de un usuario"""
        conn = get_connection()
        cursor = conn.cursor()
        
        # Si el hash es None, no actualizamos la contraseña
        if usuario.password_hash:
            query = '''
                UPDATE usuario SET nombre = ?, username = ?, password_hash = ?, rol = ?
                WHERE id = ?
            '''
            params = (usuario.nombre, usuario.username, usuario.password_hash, usuario.rol, usuario.id)
        else:
            query = '''
                UPDATE usuario SET nombre = ?, username = ?, rol = ?
                WHERE id = ?
            '''
            params = (usuario.nombre, usuario.username, usuario.rol, usuario.id)

        cursor.execute(query, params)
        conn.commit()
        conn.close()
    
    @staticmethod
    def eliminar(id):
        """Elimina (desactiva) un usuario (Soft Delete)"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE usuario SET activo = 0 WHERE id = ?', (id,))
        conn.commit()
        conn.close()