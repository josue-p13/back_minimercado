"""
Pruebas unitarias para VentaRepository
Utiliza unittest, pytest y mocking
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
import pytest
from app.repositories.venta_repository import VentaRepository
from app.models.venta import Venta, DetalleVenta


class TestVentaRepository(unittest.TestCase):
    """Suite de pruebas para VentaRepository"""

    def setUp(self):
        """Configuración inicial para cada test"""
        self.venta_data = {
            'id': 1,
            'fecha': '2025-12-25 10:00:00',
            'total': 100.0,
            'fk_cliente': 1,
            'fk_usuario': 1,
            'fk_caja': 1
        }
        self.detalle_data = {
            'id': 1,
            'fk_venta': 1,
            'fk_producto': 1,
            'cantidad': 2,
            'precio_unitario': 10.5,
            'subtotal': 21.0
        }

    def tearDown(self):
        """Limpieza después de cada test"""
        pass

    @patch('app.repositories.venta_repository.get_connection')
    def test_crear(self, mock_get_connection):
        """Test: Crear una nueva venta"""
        # Arrange
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn
        mock_cursor.lastrowid = 1

        venta = Venta(fecha='2025-12-25 10:00:00', total=100.0, fk_cliente=1, fk_usuario=1, fk_caja=1)

        # Act
        resultado = VentaRepository.crear(venta)

        # Assert
        mock_get_connection.assert_called_once()
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with('''
            INSERT INTO venta (fecha, total, fk_cliente, fk_usuario, fk_caja)
            VALUES (?, ?, ?, ?, ?)
        ''', ('2025-12-25 10:00:00', 100.0, 1, 1, 1))
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertEqual(resultado.id, 1)
        self.assertEqual(resultado, venta)

    @patch('app.repositories.venta_repository.get_connection')
    def test_crear_detalle(self, mock_get_connection):
        """Test: Crear un detalle de venta"""
        # Arrange
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn
        mock_cursor.lastrowid = 1

        detalle = DetalleVenta(fk_venta=1, fk_producto=1, cantidad=2, precio_unitario=10.5, subtotal=21.0)

        # Act
        resultado = VentaRepository.crear_detalle(detalle)

        # Assert
        mock_get_connection.assert_called_once()
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with('''
            INSERT INTO detalle_venta (fk_venta, fk_producto, cantidad, precio_unitario, subtotal)
            VALUES (?, ?, ?, ?, ?)
        ''', (1, 1, 2, 10.5, 21.0))
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertEqual(resultado.id, 1)
        self.assertEqual(resultado, detalle)

    @patch('app.repositories.venta_repository.get_connection')
    def test_obtener_por_id_existe(self, mock_get_connection):
        """Test: Obtener venta por ID cuando existe"""
        # Arrange
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn
        mock_cursor.fetchone.return_value = (1, '2025-12-25 10:00:00', 100.0, 1, 1, 1)

        # Act
        resultado = VentaRepository.obtener_por_id(1)

        # Assert
        mock_get_connection.assert_called_once()
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with('SELECT * FROM venta WHERE id = ?', (1,))
        mock_conn.close.assert_called_once()
        self.assertIsInstance(resultado, Venta)
        self.assertEqual(resultado.id, 1)
        self.assertEqual(resultado.total, 100.0)

    @patch('app.repositories.venta_repository.get_connection')
    def test_obtener_por_id_no_existe(self, mock_get_connection):
        """Test: Obtener venta por ID cuando no existe"""
        # Arrange
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn
        mock_cursor.fetchone.return_value = None

        # Act
        resultado = VentaRepository.obtener_por_id(999)

        # Assert
        mock_get_connection.assert_called_once()
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with('SELECT * FROM venta WHERE id = ?', (999,))
        mock_conn.close.assert_called_once()
        self.assertIsNone(resultado)

    @patch('app.repositories.venta_repository.get_connection')
    def test_obtener_detalles(self, mock_get_connection):
        """Test: Obtener detalles de una venta"""
        # Arrange
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn
        mock_cursor.fetchall.return_value = [
            (1, 1, 1, 2, 10.5, 21.0),
            (2, 1, 2, 1, 20.0, 20.0)
        ]

        # Act
        resultado = VentaRepository.obtener_detalles(1)

        # Assert
        mock_get_connection.assert_called_once()
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with('SELECT * FROM detalle_venta WHERE fk_venta = ?', (1,))
        mock_conn.close.assert_called_once()
        self.assertEqual(len(resultado), 2)
        self.assertIsInstance(resultado[0], DetalleVenta)
        self.assertEqual(resultado[0].id, 1)
        self.assertEqual(resultado[1].id, 2)

    @patch('app.repositories.venta_repository.get_connection')
    def test_listar(self, mock_get_connection):
        """Test: Listar todas las ventas"""
        # Arrange
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn
        mock_cursor.fetchall.return_value = [
            (1, '2025-12-25 10:00:00', 100.0, 1, 1, 1),
            (2, '2025-12-25 11:00:00', 50.0, 2, 1, 1)
        ]

        # Act
        resultado = VentaRepository.listar()

        # Assert
        mock_get_connection.assert_called_once()
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with('SELECT * FROM venta ORDER BY fecha DESC')
        mock_conn.close.assert_called_once()
        self.assertEqual(len(resultado), 2)
        self.assertIsInstance(resultado[0], Venta)
        self.assertEqual(resultado[0].id, 1)
        self.assertEqual(resultado[1].id, 2)


if __name__ == '__main__':
    unittest.main()