from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from app.repositories.usuario_repository import UsuarioRepository
from app.models.usuario import Usuario

# CONFIGURACIÓN DE SEGURIDAD
# IMPORTANTE: Usamos 'pbkdf2_sha256' para que coincida con UsuarioService
# y evitamos el error de la librería bcrypt.
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# Configuración JWT
SECRET_KEY = "tu_clave_secreta_super_segura_aqui"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 # 24 horas

class AuthService:

    @staticmethod
    def login(username, password):
        # 1. Buscar usuario en BD
        usuario = UsuarioRepository.obtener_por_username(username)
        
        if not usuario:
            return {'success': False, 'message': 'Usuario o contraseña incorrectos'}

        # 2. Verificar contraseña
        # verify() intentará usar pbkdf2_sha256. 
        # Gracias a 'deprecated="auto"', si tienes usuarios viejos con bcrypt, 
        # intentará leerlos, pero si bcrypt falla en tu PC, fallará el login de esos viejos.
        try:
            if not pwd_context.verify(password, usuario.password_hash):
                return {'success': False, 'message': 'Usuario o contraseña incorrectos'}
        except Exception as e:
            # Si falla la verificación (ej. por el error de bcrypt en usuarios viejos)
            print(f"Error verificando hash: {e}")
            return {'success': False, 'message': 'Error de seguridad. Contacte al admin.'}
            
        if not usuario.activo:
             return {'success': False, 'message': 'El usuario está desactivado'}

        # 3. Generar Token JWT
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = AuthService.crear_access_token(
            data={"sub": usuario.username, "rol": usuario.rol, "id": usuario.id},
            expires_delta=access_token_expires
        )

        return {
            'success': True,
            'message': 'Login exitoso',
            'token': access_token,
            'usuario': usuario.to_dict()
        }

    @staticmethod
    def registrar_usuario(nombre, username, password, rol):
        """Registro público o auxiliar"""
        if UsuarioRepository.obtener_por_username(username):
            return {'success': False, 'message': 'El nombre de usuario ya existe'}
            
        # Hashing consistente con el Panel de Admin
        password_hash = pwd_context.hash(password)
        
        nuevo_usuario = Usuario(nombre=nombre, username=username, password_hash=password_hash, rol=rol)
        UsuarioRepository.crear(nuevo_usuario)
        
        return {'success': True, 'message': 'Usuario registrado exitosamente'}

    @staticmethod
    def crear_access_token(data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def validar_token(token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return {'success': True, 'payload': payload}
        except Exception as e:
            return {'success': False, 'message': 'Token inválido o expirado'}