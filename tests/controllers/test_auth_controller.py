"""
Pruebas unitarias para AuthController
Utiliza unittest, pytest y mocking
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
import pytest
from app.controllers.auth_controller import AuthController
from app.models.usuario import Usuario


class TestAuthController(unittest.TestCase):
    """Suite de pruebas para AuthController"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.username = "test_user"
        self.password = "test_password"
        self.nombre = "Test User"
        self.rol = "Admin"
        
    def tearDown(self):
        """Limpieza después de cada test"""
        pass

    # ==================== TESTS PARA LOGIN ====================
    
    @patch('app.controllers.auth_controller.UsuarioRepository')
    @patch('app.controllers.auth_controller.AuthService')
    def test_login_exitoso(self, mock_auth_service, mock_usuario_repo):
        """Test: Login exitoso con credenciales válidas"""
        # Arrange
        mock_usuario = Mock()
        mock_usuario.activo = True
        mock_usuario.password_hash = "hashed_password"
        mock_usuario.to_dict.return_value = {
            'id': 1,
            'nombre': self.nombre,
            'username': self.username,
            'rol': self.rol
        }
        
        mock_usuario_repo.obtener_por_username.return_value = mock_usuario
        mock_auth_service.verify_password.return_value = True
        mock_auth_service.generate_token.return_value = "test_token_123"
        
        # Act
        resultado = AuthController.login(self.username, self.password)
        
        # Assert
        self.assertTrue(resultado['success'])
        self.assertEqual(resultado['token'], "test_token_123")
        self.assertIn('usuario', resultado)
        mock_usuario_repo.obtener_por_username.assert_called_once_with(self.username)
        mock_auth_service.verify_password.assert_called_once()
        mock_auth_service.generate_token.assert_called_once_with(mock_usuario)
    
    @patch('app.controllers.auth_controller.UsuarioRepository')
    def test_login_usuario_no_encontrado(self, mock_usuario_repo):
        """Test: Login falla cuando el usuario no existe"""
        # Arrange
        mock_usuario_repo.obtener_por_username.return_value = None
        
        # Act
        resultado = AuthController.login(self.username, self.password)
        
        # Assert
        self.assertFalse(resultado['success'])
        self.assertEqual(resultado['message'], 'Usuario no encontrado')
        mock_usuario_repo.obtener_por_username.assert_called_once_with(self.username)
    
    @patch('app.controllers.auth_controller.UsuarioRepository')
    def test_login_usuario_desactivado(self, mock_usuario_repo):
        """Test: Login falla cuando el usuario está desactivado"""
        # Arrange
        mock_usuario = Mock()
        mock_usuario.activo = False
        mock_usuario_repo.obtener_por_username.return_value = mock_usuario
        
        # Act
        resultado = AuthController.login(self.username, self.password)
        
        # Assert
        self.assertFalse(resultado['success'])
        self.assertEqual(resultado['message'], 'Usuario desactivado')
    
    @patch('app.controllers.auth_controller.UsuarioRepository')
    @patch('app.controllers.auth_controller.AuthService')
    def test_login_contraseña_incorrecta(self, mock_auth_service, mock_usuario_repo):
        """Test: Login falla con contraseña incorrecta"""
        # Arrange
        mock_usuario = Mock()
        mock_usuario.activo = True
        mock_usuario.password_hash = "hashed_password"
        
        mock_usuario_repo.obtener_por_username.return_value = mock_usuario
        mock_auth_service.verify_password.return_value = False
        
        # Act
        resultado = AuthController.login(self.username, self.password)
        
        # Assert
        self.assertFalse(resultado['success'])
        self.assertEqual(resultado['message'], 'Contraseña incorrecta')
        mock_auth_service.verify_password.assert_called_once()

    # ==================== TESTS PARA REGISTRO ====================
    
    @patch('app.controllers.auth_controller.UsuarioRepository')
    @patch('app.controllers.auth_controller.AuthService')
    def test_registrar_usuario_exitoso(self, mock_auth_service, mock_usuario_repo):
        """Test: Registro exitoso de nuevo usuario"""
        # Arrange
        mock_usuario_repo.obtener_por_username.return_value = None
        mock_auth_service.hash_password.return_value = "hashed_password"
        
        mock_usuario_creado = Mock()
        mock_usuario_creado.to_dict.return_value = {
            'id': 1,
            'nombre': self.nombre,
            'username': self.username,
            'rol': self.rol
        }
        mock_usuario_repo.crear.return_value = mock_usuario_creado
        
        # Act
        resultado = AuthController.registrar_usuario(
            self.nombre, self.username, self.password, self.rol
        )
        
        # Assert
        self.assertTrue(resultado['success'])
        self.assertEqual(resultado['message'], 'Usuario creado exitosamente')
        self.assertIn('usuario', resultado)
        mock_usuario_repo.obtener_por_username.assert_called_once_with(self.username)
        mock_auth_service.hash_password.assert_called_once_with(self.password)
        mock_usuario_repo.crear.assert_called_once()
    
    @patch('app.controllers.auth_controller.UsuarioRepository')
    def test_registrar_usuario_existente(self, mock_usuario_repo):
        """Test: Falla al intentar registrar username existente"""
        # Arrange
        mock_usuario_existente = Mock()
        mock_usuario_repo.obtener_por_username.return_value = mock_usuario_existente
        
        # Act
        resultado = AuthController.registrar_usuario(
            self.nombre, self.username, self.password, self.rol
        )
        
        # Assert
        self.assertFalse(resultado['success'])
        self.assertEqual(resultado['message'], 'El username ya existe')
        mock_usuario_repo.obtener_por_username.assert_called_once()
    
    @patch('app.controllers.auth_controller.UsuarioRepository')
    def test_registrar_usuario_rol_invalido(self, mock_usuario_repo):
        """Test: Falla con rol inválido"""
        # Arrange - Mock para evitar acceso a BD
        mock_usuario_repo.obtener_por_username.return_value = None
        
        # Act
        resultado = AuthController.registrar_usuario(
            self.nombre, self.username, self.password, "RolInvalido"
        )
        
        # Assert
        self.assertFalse(resultado['success'])
        self.assertEqual(resultado['message'], 'Rol inválido')

    # ==================== TESTS PARA VALIDACIÓN DE TOKEN ====================
    
    @patch('app.controllers.auth_controller.AuthService')
    def test_validar_token_exitoso(self, mock_auth_service):
        """Test: Validación exitosa de token válido"""
        # Arrange
        mock_payload = {
            'usuario_id': 1,
            'username': self.username,
            'rol': self.rol
        }
        mock_auth_service.decode_token.return_value = mock_payload
        
        # Act
        resultado = AuthController.validar_token("valid_token")
        
        # Assert
        self.assertTrue(resultado['success'])
        self.assertEqual(resultado['usuario'], mock_payload)
        mock_auth_service.decode_token.assert_called_once_with("valid_token")
    
    @patch('app.controllers.auth_controller.AuthService')
    def test_validar_token_invalido(self, mock_auth_service):
        """Test: Validación falla con token inválido"""
        # Arrange
        mock_auth_service.decode_token.return_value = None
        
        # Act
        resultado = AuthController.validar_token("invalid_token")
        
        # Assert
        self.assertFalse(resultado['success'])
        self.assertEqual(resultado['message'], 'Token inválido o expirado')
    
    @patch('app.controllers.auth_controller.AuthService')
    def test_validar_token_vacio(self, mock_auth_service):
        """Test: Validación falla con token vacío"""
        # Arrange
        mock_auth_service.decode_token.return_value = None
        
        # Act
        resultado = AuthController.validar_token("")
        
        # Assert
        self.assertFalse(resultado['success'])

    # ==================== TESTS PARA VERIFICAR PERMISOS ====================
    
    @patch('app.controllers.auth_controller.AuthService')
    def test_verificar_permiso_exitoso(self, mock_auth_service):
        """Test: Verificación exitosa de permisos"""
        # Arrange
        mock_payload = {'rol': 'Admin'}
        mock_auth_service.decode_token.return_value = mock_payload
        mock_auth_service.verificar_rol.return_value = True
        
        # Act
        resultado = AuthController.verificar_permiso("valid_token", "Admin")
        
        # Assert
        self.assertTrue(resultado)
        mock_auth_service.decode_token.assert_called_once_with("valid_token")
        mock_auth_service.verificar_rol.assert_called_once_with("Admin", "Admin")
    
    @patch('app.controllers.auth_controller.AuthService')
    def test_verificar_permiso_token_invalido(self, mock_auth_service):
        """Test: Verificación falla con token inválido"""
        # Arrange
        mock_auth_service.decode_token.return_value = None
        
        # Act
        resultado = AuthController.verificar_permiso("invalid_token", "Admin")
        
        # Assert
        self.assertFalse(resultado)
    
    @patch('app.controllers.auth_controller.AuthService')
    def test_verificar_permiso_rol_insuficiente(self, mock_auth_service):
        """Test: Verificación falla con rol insuficiente"""
        # Arrange
        mock_payload = {'rol': 'Cajero'}
        mock_auth_service.decode_token.return_value = mock_payload
        mock_auth_service.verificar_rol.return_value = False
        
        # Act
        resultado = AuthController.verificar_permiso("valid_token", "Admin")
        
        # Assert
        self.assertFalse(resultado)


# ==================== TESTS CON PYTEST ====================

@pytest.fixture
def mock_usuario():
    """Fixture: Usuario de prueba"""
    usuario = Mock()
    usuario.id = 1
    usuario.nombre = "Test User"
    usuario.username = "testuser"
    usuario.rol = "Admin"
    usuario.activo = True
    usuario.password_hash = "hashed_password"
    usuario.to_dict.return_value = {
        'id': 1,
        'nombre': "Test User",
        'username': "testuser",
        'rol': "Admin"
    }
    return usuario


def test_login_con_pytest(mock_usuario):
    """Test con pytest: Login exitoso"""
    with patch('app.controllers.auth_controller.UsuarioRepository') as mock_repo, \
         patch('app.controllers.auth_controller.AuthService') as mock_service:
        
        mock_repo.obtener_por_username.return_value = mock_usuario
        mock_service.verify_password.return_value = True
        mock_service.generate_token.return_value = "token_pytest"
        
        resultado = AuthController.login("testuser", "password")
        
        assert resultado['success'] is True
        assert resultado['token'] == "token_pytest"
        assert 'usuario' in resultado


def test_registro_usuario_con_validaciones():
    """Test con pytest: Validaciones en registro"""
    with patch('app.controllers.auth_controller.UsuarioRepository') as mock_repo:
        # Test 1: Username existente
        mock_repo.obtener_por_username.return_value = Mock()
        resultado = AuthController.registrar_usuario("Nombre", "user", "pass", "Admin")
        assert resultado['success'] is False
        assert "ya existe" in resultado['message']
        
        # Test 2: Rol inválido
        mock_repo.obtener_por_username.return_value = None
        resultado = AuthController.registrar_usuario("Nombre", "user", "pass", "InvalidRole")
        assert resultado['success'] is False
        assert "inválido" in resultado['message'].lower()


if __name__ == '__main__':
    # Ejecutar tests con unittest
    unittest.main()
