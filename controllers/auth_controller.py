"""
Controlador de Autenticación
Gestiona login, registro y validación de tokens
"""
from app.services.auth_service import AuthService
from app.repositories.usuario_repository import UsuarioRepository
from app.models.usuario import Usuario

class AuthController:
    
    @staticmethod
    def login(username, password):
        """Inicia sesión y devuelve un token"""
        usuario = UsuarioRepository.obtener_por_username(username)
        
        if not usuario:
            return {'success': False, 'message': 'Usuario no encontrado'}
        
        if not usuario.activo:
            return {'success': False, 'message': 'Usuario desactivado'}
        
        if not AuthService.verify_password(password, usuario.password_hash):
            return {'success': False, 'message': 'Contraseña incorrecta'}
        
        token = AuthService.generate_token(usuario)
        return {
            'success': True,
            'token': token,
            'usuario': usuario.to_dict()
        }
    
    @staticmethod
    def registrar_usuario(nombre, username, password, rol):
        """Registra un nuevo usuario (solo Admin puede hacer esto)"""
        # Verificar si el username ya existe
        usuario_existente = UsuarioRepository.obtener_por_username(username)
        if usuario_existente:
            return {'success': False, 'message': 'El username ya existe'}
        
        # Validar rol
        if rol not in ['Admin', 'Cajero', 'Auxiliar']:
            return {'success': False, 'message': 'Rol inválido'}
        
        # Crear usuario
        password_hash = AuthService.hash_password(password)
        usuario = Usuario(
            nombre=nombre,
            username=username,
            password_hash=password_hash,
            rol=rol
        )
        usuario = UsuarioRepository.crear(usuario)
        
        return {
            'success': True,
            'message': 'Usuario creado exitosamente',
            'usuario': usuario.to_dict()
        }
    
    @staticmethod
    def validar_token(token):
        """Valida un token y devuelve la información del usuario"""
        payload = AuthService.decode_token(token)
        if not payload:
            return {'success': False, 'message': 'Token inválido o expirado'}
        
        return {'success': True, 'usuario': payload}
    
    @staticmethod
    def verificar_permiso(token, rol_requerido):
        """Verifica si un usuario tiene permisos suficientes"""
        payload = AuthService.decode_token(token)
        if not payload:
            return False
        
        return AuthService.verificar_rol(rol_requerido, payload['rol'])
