"""
Servicio de Usuarios
Lógica de negocio para usuarios
"""
from app.repositories.usuario_repository import UsuarioRepository
from app.models.usuario import Usuario
# CAMBIO: Usamos passlib que ya lo tienes en requirements.txt
from passlib.context import CryptContext

# Configuración básica de hashing (seguramente tienes algo similar en tu AuthController)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UsuarioService:
    
    @staticmethod
    def agregar_usuario(nombre, username, password, rol):
        if UsuarioRepository.obtener_por_username(username):
            raise Exception("El nombre de usuario ya existe")
            
        # CAMBIO: Usamos pwd_context.hash en lugar de generate_password_hash
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
            # CAMBIO: Usamos pwd_context.hash
            usuario_actual.password_hash = pwd_context.hash(password)
        else:
            usuario_actual.password_hash = None
            
        UsuarioRepository.actualizar(usuario_actual)
        return usuario_actual
    
    @staticmethod
    def eliminar_usuario(id):
        if not UsuarioRepository.obtener_por_id(id):
            raise Exception("Usuario no encontrado")
        UsuarioRepository.eliminar(id)