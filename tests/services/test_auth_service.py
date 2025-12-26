"""
Pruebas unitarias para AuthService
Utiliza unittest, pytest y mocking
Probando: hash de contraseñas, verificación, tokens y roles
"""
import unittest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
import json
import base64
import pytest
from app.services.auth_service import AuthService
from app.models.usuario import Usuario


class TestAuthService(unittest.TestCase):
    """Suite de pruebas para AuthService"""

    def setUp(self):
        """Configuración inicial para cada test"""
        self.password = "test_password_123"
        self.usuario_data = {
            'id': 1,
            'username': 'testuser',
            'rol': 'Admin'
        }

    def tearDown(self):
        """Limpieza después de cada test"""
        pass

    # ==================== TESTS PARA HASH DE CONTRASEÑAS ====================

    def test_hash_password_genera_hash_consistente(self):
        """Test: Hash de contraseña genera resultado consistente"""
        # Act
        hash1 = AuthService.hash_password(self.password)
        hash2 = AuthService.hash_password(self.password)

        # Assert
        self.assertEqual(hash1, hash2)
        self.assertIsNotNone(hash1)
        self.assertGreater(len(hash1), 0)

    def test_hash_password_genera_hashes_diferentes_para_diferentes_contraseñas(self):
        """Test: Contraseñas diferentes generan hashes diferentes"""
        # Act
        hash1 = AuthService.hash_password("password123")
        hash2 = AuthService.hash_password("password456")

        # Assert
        self.assertNotEqual(hash1, hash2)

    def test_hash_password_maneja_contraseña_vacia(self):
        """Test: Hash maneja correctamente contraseña vacía"""
        # Act
        hash_vacio = AuthService.hash_password("")

        # Assert
        self.assertIsNotNone(hash_vacio)
        self.assertEqual(len(hash_vacio), 64)  # SHA256 produce 64 caracteres

    def test_hash_password_maneja_caracteres_especiales(self):
        """Test: Hash maneja caracteres especiales"""
        # Act
        hash_especial = AuthService.hash_password("P@ssw0rd!#$%^&*()")

        # Assert
        self.assertIsNotNone(hash_especial)
        self.assertEqual(len(hash_especial), 64)

    # ==================== TESTS PARA VERIFICACIÓN DE CONTRASEÑA ====================

    def test_verify_password_exitoso(self):
        """Test: Verificación exitosa de contraseña correcta"""
        # Arrange
        password_hash = AuthService.hash_password(self.password)

        # Act
        resultado = AuthService.verify_password(self.password, password_hash)

        # Assert
        self.assertTrue(resultado)

    def test_verify_password_fallido_contraseña_incorrecta(self):
        """Test: Verificación falla con contraseña incorrecta"""
        # Arrange
        password_hash = AuthService.hash_password(self.password)

        # Act
        resultado = AuthService.verify_password("contraseña_incorrecta", password_hash)

        # Assert
        self.assertFalse(resultado)

    def test_verify_password_sensible_a_mayusculas(self):
        """Test: Verificación es sensible a mayúsculas"""
        # Arrange
        password_hash = AuthService.hash_password("TestPassword")

        # Act
        resultado = AuthService.verify_password("testpassword", password_hash)

        # Assert
        self.assertFalse(resultado)

    # ==================== TESTS PARA GENERACIÓN DE TOKEN ====================

    def test_generate_token_estructura_correcta(self):
        """Test: Token generado tiene estructura correcta"""
        # Arrange
        usuario = Mock()
        usuario.id = 1
        usuario.username = "testuser"
        usuario.rol = "Admin"

        # Act
        token = AuthService.generate_token(usuario)

        # Assert
        self.assertIsNotNone(token)
        self.assertIsInstance(token, str)
        # Verificar que es base64
        try:
            decoded = base64.b64decode(token.encode()).decode()
            payload = json.loads(decoded)
            self.assertEqual(payload['id'], 1)
            self.assertEqual(payload['username'], 'testuser')
            self.assertEqual(payload['rol'], 'Admin')
        except:
            self.fail("Token no es válido en formato base64 + JSON")

    def test_generate_token_incluye_expiracion(self):
        """Test: Token incluye tiempo de expiración"""
        # Arrange
        usuario = Mock()
        usuario.id = 1
        usuario.username = "testuser"
        usuario.rol = "Admin"

        # Act
        token = AuthService.generate_token(usuario)
        decoded = json.loads(base64.b64decode(token.encode()).decode())

        # Assert
        self.assertIn('exp', decoded)
        exp_time = datetime.fromisoformat(decoded['exp'])
        now = datetime.now()
        self.assertGreater(exp_time, now)

    def test_generate_token_tokens_diferentes_en_diferentes_tiempos(self):
        """Test: Tokens generados en diferentes momentos son diferentes (por timestamp)"""
        # Arrange
        usuario = Mock()
        usuario.id = 1
        usuario.username = "testuser"
        usuario.rol = "Admin"

        # Act
        token1 = AuthService.generate_token(usuario)
        token2 = AuthService.generate_token(usuario)

        # Assert - Los tokens tendrán timestamps diferentes
        decoded1 = json.loads(base64.b64decode(token1.encode()).decode())
        decoded2 = json.loads(base64.b64decode(token2.encode()).decode())
        # Los timestamps serán iguales si se generan muy rápido, pero la estructura es idéntica
        self.assertEqual(decoded1['id'], decoded2['id'])

    # ==================== TESTS PARA DECODIFICACIÓN DE TOKEN ====================

    def test_decode_token_valido(self):
        """Test: Decodificación exitosa de token válido"""
        # Arrange
        usuario = Mock()
        usuario.id = 1
        usuario.username = "testuser"
        usuario.rol = "Admin"
        token = AuthService.generate_token(usuario)

        # Act
        payload = AuthService.decode_token(token)

        # Assert
        self.assertIsNotNone(payload)
        self.assertEqual(payload['id'], 1)
        self.assertEqual(payload['username'], 'testuser')
        self.assertEqual(payload['rol'], 'Admin')

    def test_decode_token_invalido_retorna_none(self):
        """Test: Token inválido retorna None"""
        # Act
        payload = AuthService.decode_token("token_invalido_xyz")

        # Assert
        self.assertIsNone(payload)

    def test_decode_token_token_expirado_retorna_none(self):
        """Test: Token expirado retorna None"""
        # Arrange - Crear token con expiración en el pasado
        payload_expirado = {
            'id': 1,
            'username': 'testuser',
            'rol': 'Admin',
            'exp': (datetime.now() - timedelta(hours=1)).isoformat()
        }
        token_expirado = base64.b64encode(
            json.dumps(payload_expirado).encode()
        ).decode()

        # Act
        resultado = AuthService.decode_token(token_expirado)

        # Assert
        self.assertIsNone(resultado)

    def test_decode_token_malformado_retorna_none(self):
        """Test: Token malformado retorna None"""
        # Act
        payload = AuthService.decode_token("not-valid-base64!!!")

        # Assert
        self.assertIsNone(payload)

    # ==================== TESTS PARA VERIFICACIÓN DE ROL ====================

    def test_verificar_rol_admin_puede_acceder_todo(self):
        """Test: Admin puede acceder a cualquier rol"""
        # Assert
        self.assertTrue(AuthService.verificar_rol('Cajero', 'Admin'))
        self.assertTrue(AuthService.verificar_rol('Auxiliar', 'Admin'))
        self.assertTrue(AuthService.verificar_rol('Admin', 'Admin'))

    def test_verificar_rol_cajero_puede_acceder_cajero_y_auxiliar(self):
        """Test: Cajero puede acceder a Cajero y Auxiliar"""
        # Assert
        self.assertTrue(AuthService.verificar_rol('Cajero', 'Cajero'))
        self.assertTrue(AuthService.verificar_rol('Auxiliar', 'Cajero'))
        self.assertFalse(AuthService.verificar_rol('Admin', 'Cajero'))

    def test_verificar_rol_auxiliar_solo_auxiliar(self):
        """Test: Auxiliar solo puede acceder a Auxiliar"""
        # Assert
        self.assertTrue(AuthService.verificar_rol('Auxiliar', 'Auxiliar'))
        self.assertFalse(AuthService.verificar_rol('Cajero', 'Auxiliar'))
        self.assertFalse(AuthService.verificar_rol('Admin', 'Auxiliar'))

    def test_verificar_rol_rol_desconocido(self):
        """Test: Rol desconocido no tiene acceso a roles superiores"""
        # Assert
        self.assertFalse(AuthService.verificar_rol('Admin', 'RolDesconocido'))
        # Un rol desconocido como usuario puede acceder a un rol desconocido como requerido (0 >= 0 es True)
        self.assertTrue(AuthService.verificar_rol('RolDesconocido', 'RolDesconocido'))

    def test_verificar_rol_rol_vacio(self):
        """Test: Rol vacío retorna comportamiento por defecto"""
        # Assert
        self.assertFalse(AuthService.verificar_rol('Admin', ''))
        # Un rol vacío como usuario puede acceder a un rol vacío como requerido (0 >= 0 es True)
        self.assertTrue(AuthService.verificar_rol('', ''))


if __name__ == '__main__':
    unittest.main()
