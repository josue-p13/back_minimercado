"""
Pruebas unitarias para UsuarioRepository
Utiliza unittest, pytest y mocking
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
import pytest
from app.repositories.usuario_repository import UsuarioRepository
from app.models.usuario import Usuario


class TestUsuarioRepository(unittest.TestCase):
    """Suite de pruebas para UsuarioRepository"""

    def setUp(self):
        """Configuración inicial para cada test"""
        self.usuario_data = {
            'id': 1,
            'nombre': 'Usuario Test',
            'username': 'testuser',
            'password_hash': 'hashed_password',
            'rol': 'Admin',
            'activo': 1
        }

    def tearDown(self):
        """Limpieza después de cada test"""
        pass

    @patch('app.repositories.usuario_repository.get_connection')
    def test_crear(self, mock_get_connection):
        """Test: Crear un nuevo usuario"""
        # Arrange
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn
        mock_cursor.lastrowid = 1

        usuario = Usuario(nombre='Usuario Test', username='testuser', password_hash='hashed_password', rol='Admin', activo=1)

        # Act
        resultado = UsuarioRepository.crear(usuario)

        # Assert
        mock_get_connection.assert_called_once()
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with('''
            INSERT INTO usuario (nombre, username, password_hash, rol, activo)
            VALUES (?, ?, ?, ?, ?)
        ''', ('Usuario Test', 'testuser', 'hashed_password', 'Admin', 1))
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertEqual(resultado.id, 1)
        self.assertEqual(resultado, usuario)

    @patch('app.repositories.usuario_repository.get_connection')
    def test_obtener_por_id_existe(self, mock_get_connection):
        """Test: Obtener usuario por ID cuando existe"""
        # Arrange
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn
        mock_cursor.fetchone.return_value = (1, 'Usuario Test', 'testuser', 'hashed_password', 'Admin', 1)

        # Act
        resultado = UsuarioRepository.obtener_por_id(1)

        # Assert
        mock_get_connection.assert_called_once()
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with('SELECT * FROM usuario WHERE id = ?', (1,))
        mock_conn.close.assert_called_once()
        self.assertIsInstance(resultado, Usuario)
        self.assertEqual(resultado.id, 1)
        self.assertEqual(resultado.nombre, 'Usuario Test')

    @patch('app.repositories.usuario_repository.get_connection')
    def test_obtener_por_id_no_existe(self, mock_get_connection):
        """Test: Obtener usuario por ID cuando no existe"""
        # Arrange
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn
        mock_cursor.fetchone.return_value = None

        # Act
        resultado = UsuarioRepository.obtener_por_id(999)

        # Assert
        mock_get_connection.assert_called_once()
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with('SELECT * FROM usuario WHERE id = ?', (999,))
        mock_conn.close.assert_called_once()
        self.assertIsNone(resultado)

    @patch('app.repositories.usuario_repository.get_connection')
    def test_obtener_por_username_existe(self, mock_get_connection):
        """Test: Obtener usuario por username cuando existe"""
        # Arrange
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn
        mock_cursor.fetchone.return_value = (1, 'Usuario Test', 'testuser', 'hashed_password', 'Admin', 1)

        # Act
        resultado = UsuarioRepository.obtener_por_username('testuser')

        # Assert
        mock_get_connection.assert_called_once()
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with('SELECT * FROM usuario WHERE username = ?', ('testuser',))
        mock_conn.close.assert_called_once()
        self.assertIsInstance(resultado, Usuario)
        self.assertEqual(resultado.username, 'testuser')

    @patch('app.repositories.usuario_repository.get_connection')
    def test_obtener_por_username_no_existe(self, mock_get_connection):
        """Test: Obtener usuario por username cuando no existe"""
        # Arrange
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn
        mock_cursor.fetchone.return_value = None

        # Act
        resultado = UsuarioRepository.obtener_por_username('nonexistent')

        # Assert
        mock_get_connection.assert_called_once()
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with('SELECT * FROM usuario WHERE username = ?', ('nonexistent',))
        mock_conn.close.assert_called_once()
        self.assertIsNone(resultado)

    @patch('app.repositories.usuario_repository.get_connection')
    def test_listar(self, mock_get_connection):
        """Test: Listar usuarios activos"""
        # Arrange
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn
        mock_cursor.fetchall.return_value = [
            (1, 'Usuario 1', 'user1', 'hash1', 'Admin', 1),
            (2, 'Usuario 2', 'user2', 'hash2', 'Cajero', 1)
        ]

        # Act
        resultado = UsuarioRepository.listar()

        # Assert
        mock_get_connection.assert_called_once()
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with('SELECT * FROM usuario WHERE activo = 1')
        mock_conn.close.assert_called_once()
        self.assertEqual(len(resultado), 2)
        self.assertIsInstance(resultado[0], Usuario)
        self.assertEqual(resultado[0].id, 1)
        self.assertEqual(resultado[1].id, 2)

    @patch('app.repositories.usuario_repository.get_connection')
    def test_actualizar(self, mock_get_connection):
        """Test: Actualizar un usuario"""
        # Arrange
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn

        usuario = Usuario(id=1, nombre='Usuario Actualizado', rol='Cajero', activo=1)

        # Act
        UsuarioRepository.actualizar(usuario)

        # Assert
        mock_get_connection.assert_called_once()
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with('''
            UPDATE usuario SET nombre = ?, rol = ?, activo = ?
            WHERE id = ?
        ''', ('Usuario Actualizado', 'Cajero', 1, 1))
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('app.repositories.usuario_repository.get_connection')
    def test_eliminar(self, mock_get_connection):
        """Test: Eliminar (desactivar) un usuario"""
        # Arrange
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn

        # Act
        UsuarioRepository.eliminar(1)

        # Assert
        mock_get_connection.assert_called_once()
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with('UPDATE usuario SET activo = 0 WHERE id = ?', (1,))
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()