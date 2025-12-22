"""
Utilidad de autenticación
RNF1 - Hashing de contraseñas
RNF2 - Control de acceso basado en roles
"""
import hashlib
import secrets
import json
import base64
from datetime import datetime, timedelta

class AuthService:
    
    @staticmethod
    def hash_password(password):
        """RNF1 - Hashea una contraseña con SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def verify_password(password, password_hash):
        """Verifica una contraseña contra su hash"""
        return AuthService.hash_password(password) == password_hash
    
    @staticmethod
    def generate_token(usuario):
        """Genera un token simple (simulando JWT)"""
        payload = {
            'id': usuario.id,
            'username': usuario.username,
            'rol': usuario.rol,
            'exp': (datetime.now() + timedelta(hours=24)).isoformat()
        }
        token = base64.b64encode(json.dumps(payload).encode()).decode()
        return token
    
    @staticmethod
    def decode_token(token):
        """Decodifica un token"""
        try:
            payload = json.loads(base64.b64decode(token.encode()).decode())
            # Verificar expiración
            if datetime.fromisoformat(payload['exp']) < datetime.now():
                return None
            return payload
        except:
            return None
    
    @staticmethod
    def verificar_rol(rol_requerido, rol_usuario):
        """RNF2 - Verifica si un usuario tiene el rol requerido"""
        roles_jerarquia = {'Admin': 3, 'Cajero': 2, 'Auxiliar': 1}
        return roles_jerarquia.get(rol_usuario, 0) >= roles_jerarquia.get(rol_requerido, 0)
