"""
Pruebas unitarias para ProductoRepository
Utiliza unittest, pytest y mocking
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
import pytest
from app.repositories.producto_repository import ProductoRepository
from app.models.producto import Producto


class TestProductoRepository(unittest.TestCase):
    """Suite de pruebas para ProductoRepository"""

    def setUp(self):
        """Configuración inicial para cada test"""
        self.producto_data = {
            'id': 1,
            'nombre': 'Producto Test',
            'precio': 10.5,
            'stock': 100,
            'stock_minimo': 10,
            'fk_proveedor': 1,
            'activo': 1
        }

    def tearDown(self):
        """Limpieza después de cada test"""
        pass

    @patch('app.repositories.producto_repository.get_connection')
    def test_crear(self, mock_get_connection):
        """Test: Crear un nuevo producto"""
        # Arrange
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn
        mock_cursor.lastrowid = 1

        producto = Producto(nombre='Producto Test', precio=10.5, stock=100, stock_minimo=10, fk_proveedor=1, activo=1)

        # Act
        resultado = ProductoRepository.crear(producto)

        # Assert
        mock_get_connection.assert_called_once()
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with('''
            INSERT INTO producto (nombre, precio, stock, stock_minimo, fk_proveedor, activo)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', ('Producto Test', 10.5, 100, 10, 1, 1))
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertEqual(resultado.id, 1)
        self.assertEqual(resultado, producto)

    @patch('app.repositories.producto_repository.get_connection')
    def test_obtener_por_id_existe(self, mock_get_connection):
        """Test: Obtener producto por ID cuando existe"""
        # Arrange
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn
        mock_cursor.fetchone.return_value = (1, 'Producto Test', 10.5, 100, 10, 1, 1)

        # Act
        resultado = ProductoRepository.obtener_por_id(1)

        # Assert
        mock_get_connection.assert_called_once()
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with('SELECT * FROM producto WHERE id = ?', (1,))
        mock_conn.close.assert_called_once()
        self.assertIsInstance(resultado, Producto)
        self.assertEqual(resultado.id, 1)
        self.assertEqual(resultado.nombre, 'Producto Test')

    @patch('app.repositories.producto_repository.get_connection')
    def test_obtener_por_id_no_existe(self, mock_get_connection):
        """Test: Obtener producto por ID cuando no existe"""
        # Arrange
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn
        mock_cursor.fetchone.return_value = None

        # Act
        resultado = ProductoRepository.obtener_por_id(999)

        # Assert
        mock_get_connection.assert_called_once()
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with('SELECT * FROM producto WHERE id = ?', (999,))
        mock_conn.close.assert_called_once()
        self.assertIsNone(resultado)

    @patch('app.repositories.producto_repository.get_connection')
    def test_listar(self, mock_get_connection):
        """Test: Listar productos activos"""
        # Arrange
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn
        mock_cursor.fetchall.return_value = [
            (1, 'Producto 1', 10.5, 100, 10, 1, 1),
            (2, 'Producto 2', 20.0, 50, 5, 2, 1)
        ]

        # Act
        resultado = ProductoRepository.listar()

        # Assert
        mock_get_connection.assert_called_once()
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with('SELECT * FROM producto WHERE activo = 1')
        mock_conn.close.assert_called_once()
        self.assertEqual(len(resultado), 2)
        self.assertIsInstance(resultado[0], Producto)
        self.assertEqual(resultado[0].id, 1)
        self.assertEqual(resultado[1].id, 2)

    @patch('app.repositories.producto_repository.get_connection')
    def test_actualizar(self, mock_get_connection):
        """Test: Actualizar un producto"""
        # Arrange
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn

        producto = Producto(id=1, nombre='Producto Actualizado', precio=15.0, stock=80, stock_minimo=8, fk_proveedor=1)

        # Act
        ProductoRepository.actualizar(producto)

        # Assert
        mock_get_connection.assert_called_once()
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with('''
            UPDATE producto SET nombre = ?, precio = ?, stock = ?, stock_minimo = ?, fk_proveedor = ?
            WHERE id = ?
        ''', ('Producto Actualizado', 15.0, 80, 8, 1, 1))
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('app.repositories.producto_repository.get_connection')
    def test_actualizar_stock(self, mock_get_connection):
        """Test: Actualizar stock de un producto"""
        # Arrange
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn

        # Act
        ProductoRepository.actualizar_stock(1, -5)

        # Assert
        mock_get_connection.assert_called_once()
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with('UPDATE producto SET stock = stock + ? WHERE id = ?', (-5, 1))
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('app.repositories.producto_repository.get_connection')
    def test_obtener_productos_bajo_stock(self, mock_get_connection):
        """Test: Obtener productos con stock bajo"""
        # Arrange
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn
        mock_cursor.fetchall.return_value = [
            (1, 'Producto Bajo Stock', 5.0, 5, 10, 1, 1)
        ]

        # Act
        resultado = ProductoRepository.obtener_productos_bajo_stock()

        # Assert
        mock_get_connection.assert_called_once()
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with('SELECT * FROM producto WHERE stock <= stock_minimo AND activo = 1')
        mock_conn.close.assert_called_once()
        self.assertEqual(len(resultado), 1)
        self.assertIsInstance(resultado[0], Producto)
        self.assertEqual(resultado[0].id, 1)

    @patch('app.repositories.producto_repository.get_connection')
    def test_eliminar(self, mock_get_connection):
        """Test: Eliminar (desactivar) un producto"""
        # Arrange
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn

        # Act
        ProductoRepository.eliminar(1)

        # Assert
        mock_get_connection.assert_called_once()
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with('UPDATE producto SET activo = 0 WHERE id = ?', (1,))
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()