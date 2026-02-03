"""
Servicio de Usuarios
Lógica de negocio para usuarios
"""
from app.repositories.usuario_repository import UsuarioRepository
from app.models.usuario import Usuario
from passlib.context import CryptContext

# CAMBIO IMPORTANTE: Usamos 'pbkdf2_sha256' que no da conflictos de versión
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

class UsuarioService:
    
    @staticmethod
    def agregar_usuario(nombre, username, password, rol):
        if UsuarioRepository.obtener_por_username(username):
            raise Exception("El nombre de usuario ya existe")
            
        # Hashing seguro sin errores de bcrypt
        password_hash = pwd_context.hash(password)
        
        nuevo_usuario = Usuario(nombre=nombre, username=username, password_hash=password_hash, rol=rol)
        return UsuarioRepository.crear(nuevo_usuario)
    
    @staticmethod
    def listar_usuarios():
        usuarios = UsuarioRepository.listar()
        return [u.to_dict() for u in usuarios]
    
    @staticmethod
    def buscar_usuario(id):
        usuario = UsuarioRepository.obtener_por_id(id)
        return usuario.to_dict() if usuario else None
    
    @staticmethod
    def actualizar_usuario(id, nombre, username, password, rol):
        usuario_actual = UsuarioRepository.obtener_por_id(id)
        if not usuario_actual:
            raise Exception("Usuario no encontrado")
            
        if usuario_actual.username != username:
            if UsuarioRepository.obtener_por_username(username):
                raise Exception("El nombre de usuario ya está en uso")
        
        usuario_actual.nombre = nombre
        usuario_actual.username = username
        usuario_actual.rol = rol
        
        # Solo actualizamos password si se envía uno nuevo
        if password:
            usuario_actual.password_hash = pwd_context.hash(password)
            
        # Nota: Si el usuario_actual.password_hash es None, el repositorio sabrá qué hacer
        # (asegúrate que tu repositorio maneje el caso de no actualizar pass si no cambia)
        
        UsuarioRepository.actualizar(usuario_actual)
        return usuario_actual
    
    @staticmethod
    def eliminar_usuario(id):
        if not UsuarioRepository.obtener_por_id(id):
            raise Exception("Usuario no encontrado")
        UsuarioRepository.eliminar(id)