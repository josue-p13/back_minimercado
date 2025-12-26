"""
Pruebas unitarias para ProveedorRepository
Utiliza unittest, pytest y mocking
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
import pytest
from app.repositories.proveedor_repository import ProveedorRepository
from app.models.proveedor import Proveedor


class TestProveedorRepository(unittest.TestCase):
    """Suite de pruebas para ProveedorRepository"""

    def setUp(self):
        """Configuración inicial para cada test"""
        self.proveedor_data = {
            'id': 1,
            'nombre': 'Distribuidora Los Andes',
            'telefono': '0991234567',
            'direccion': 'Av. Principal 123',
            'activo': 1
        }

    def tearDown(self):
        """Limpieza después de cada test"""
        pass

    @patch('app.repositories.proveedor_repository.get_connection')
    def test_crear(self, mock_get_connection):
        """Test: Crear un nuevo proveedor"""
        # Arrange
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn
        mock_cursor.lastrowid = 1

        proveedor = Proveedor(nombre='Distribuidora Los Andes', telefono='0991234567', direccion='Av. Principal 123')

        # Act
        resultado = ProveedorRepository.crear(proveedor)

        # Assert
        mock_get_connection.assert_called_once()
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with('''
            INSERT INTO proveedor (nombre, telefono, direccion, activo)
            VALUES (?, ?, ?, ?)
        ''', ('Distribuidora Los Andes', '0991234567', 'Av. Principal 123', 1))
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertEqual(resultado.id, 1)
        self.assertEqual(resultado, proveedor)

    @patch('app.repositories.proveedor_repository.get_connection')
    def test_obtener_por_id_existe(self, mock_get_connection):
        """Test: Obtener proveedor por ID cuando existe"""
        # Arrange
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn
        mock_cursor.fetchone.return_value = (1, 'Distribuidora Los Andes', '0991234567', 'Av. Principal 123', 1)

        # Act
        resultado = ProveedorRepository.obtener_por_id(1)

        # Assert
        mock_get_connection.assert_called_once()
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with('SELECT * FROM proveedor WHERE id = ?', (1,))
        mock_conn.close.assert_called_once()
        self.assertIsInstance(resultado, Proveedor)
        self.assertEqual(resultado.id, 1)
        self.assertEqual(resultado.nombre, 'Distribuidora Los Andes')

    @patch('app.repositories.proveedor_repository.get_connection')
    def test_obtener_por_id_no_existe(self, mock_get_connection):
        """Test: Obtener proveedor por ID cuando no existe"""
        # Arrange
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn
        mock_cursor.fetchone.return_value = None

        # Act
        resultado = ProveedorRepository.obtener_por_id(999)

        # Assert
        mock_get_connection.assert_called_once()
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with('SELECT * FROM proveedor WHERE id = ?', (999,))
        mock_conn.close.assert_called_once()
        self.assertIsNone(resultado)

    @patch('app.repositories.proveedor_repository.get_connection')
    def test_listar(self, mock_get_connection):
        """Test: Listar todos los proveedores activos"""
        # Arrange
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn
        mock_cursor.fetchall.return_value = [
            (1, 'Distribuidora A', '099111', 'Dir A', 1),
            (2, 'Distribuidora B', '099222', 'Dir B', 1)
        ]

        # Act
        resultado = ProveedorRepository.listar()

        # Assert
        mock_get_connection.assert_called_once()
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with('SELECT * FROM proveedor WHERE activo = 1')
        mock_conn.close.assert_called_once()
        self.assertEqual(len(resultado), 2)
        self.assertIsInstance(resultado[0], Proveedor)
        self.assertEqual(resultado[0].id, 1)
        self.assertEqual(resultado[1].id, 2)

    @patch('app.repositories.proveedor_repository.get_connection')
    def test_actualizar(self, mock_get_connection):
        """Test: Actualizar un proveedor"""
        # Arrange
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn
        
        proveedor = Proveedor(id=1, nombre='Nuevo Nombre', telefono='099888', direccion='Nueva Dir', activo=1)

        # Act
        ProveedorRepository.actualizar(proveedor)

        # Assert
        mock_get_connection.assert_called_once()
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with('''
            UPDATE proveedor SET nombre = ?, telefono = ?, direccion = ?
            WHERE id = ?
        ''', ('Nuevo Nombre', '099888', 'Nueva Dir', 1))
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('app.repositories.proveedor_repository.get_connection')
    def test_eliminar(self, mock_get_connection):
        """Test: Eliminar (desactivar) un proveedor"""
        # Arrange
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn

        # Act
        ProveedorRepository.eliminar(1)

        # Assert
        mock_get_connection.assert_called_once()
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with('UPDATE proveedor SET activo = 0 WHERE id = ?', (1,))
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()