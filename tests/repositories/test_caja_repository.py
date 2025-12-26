"""
Pruebas unitarias para CajaRepository
Utiliza unittest, pytest y mocking
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
import pytest
from app.repositories.caja_repository import CajaRepository
from app.models.caja import Caja


class TestCajaRepository(unittest.TestCase):
    """Suite de pruebas para CajaRepository"""

    def setUp(self):
        """Configuración inicial para cada test"""
        self.caja_data = {
            'id': 1,
            'fecha_apertura': '2025-12-25',
            'fecha_cierre': None,
            'monto_inicial': 100.0,
            'monto_final': None,
            'fk_usuario': 1,
            'estado': 'Abierta'
        }

    def tearDown(self):
        """Limpieza después de cada test"""
        pass

    @patch('app.repositories.caja_repository.get_connection')
    def test_crear(self, mock_get_connection):
        """Test: Crear una nueva caja"""
        # Arrange
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn
        mock_cursor.lastrowid = 1

        caja = Caja(fecha_apertura='2025-12-25', monto_inicial=100.0, fk_usuario=1, estado='Abierta')

        # Act
        resultado = CajaRepository.crear(caja)

        # Assert
        mock_get_connection.assert_called_once()
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with('''
            INSERT INTO caja (fecha_apertura, monto_inicial, fk_usuario, estado)
            VALUES (?, ?, ?, ?)
        ''', ('2025-12-25', 100.0, 1, 'Abierta'))
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertEqual(resultado.id, 1)
        self.assertEqual(resultado, caja)

    @patch('app.repositories.caja_repository.get_connection')
    def test_obtener_por_id_existe(self, mock_get_connection):
        """Test: Obtener caja por ID cuando existe"""
        # Arrange
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn
        mock_cursor.fetchone.return_value = (1, '2025-12-25', None, 100.0, None, 1, 'Abierta')

        # Act
        resultado = CajaRepository.obtener_por_id(1)

        # Assert
        mock_get_connection.assert_called_once()
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with('SELECT * FROM caja WHERE id = ?', (1,))
        mock_conn.close.assert_called_once()
        self.assertIsInstance(resultado, Caja)
        self.assertEqual(resultado.id, 1)
        self.assertEqual(resultado.fecha_apertura, '2025-12-25')

    @patch('app.repositories.caja_repository.get_connection')
    def test_obtener_por_id_no_existe(self, mock_get_connection):
        """Test: Obtener caja por ID cuando no existe"""
        # Arrange
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn
        mock_cursor.fetchone.return_value = None

        # Act
        resultado = CajaRepository.obtener_por_id(999)

        # Assert
        mock_get_connection.assert_called_once()
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with('SELECT * FROM caja WHERE id = ?', (999,))
        mock_conn.close.assert_called_once()
        self.assertIsNone(resultado)

    @patch('app.repositories.caja_repository.get_connection')
    def test_obtener_caja_abierta_existe(self, mock_get_connection):
        """Test: Obtener caja abierta cuando existe"""
        # Arrange
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn
        mock_cursor.fetchone.return_value = (1, '2025-12-25', None, 100.0, None, 1, 'Abierta')

        # Act
        resultado = CajaRepository.obtener_caja_abierta()

        # Assert
        mock_get_connection.assert_called_once()
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with("SELECT * FROM caja WHERE estado = 'Abierta' ORDER BY fecha_apertura DESC LIMIT 1")
        mock_conn.close.assert_called_once()
        self.assertIsInstance(resultado, Caja)
        self.assertEqual(resultado.estado, 'Abierta')

    @patch('app.repositories.caja_repository.get_connection')
    def test_obtener_caja_abierta_no_existe(self, mock_get_connection):
        """Test: Obtener caja abierta cuando no existe"""
        # Arrange
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn
        mock_cursor.fetchone.return_value = None

        # Act
        resultado = CajaRepository.obtener_caja_abierta()

        # Assert
        mock_get_connection.assert_called_once()
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with("SELECT * FROM caja WHERE estado = 'Abierta' ORDER BY fecha_apertura DESC LIMIT 1")
        mock_conn.close.assert_called_once()
        self.assertIsNone(resultado)

    @patch('app.repositories.caja_repository.get_connection')
    def test_cerrar_caja(self, mock_get_connection):
        """Test: Cerrar una caja"""
        # Arrange
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn

        # Act
        CajaRepository.cerrar_caja(1, '2025-12-25 18:00:00', 150.0)

        # Assert
        mock_get_connection.assert_called_once()
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with('''
            UPDATE caja SET fecha_cierre = ?, monto_final = ?, estado = 'Cerrada'
            WHERE id = ?
        ''', ('2025-12-25 18:00:00', 150.0, 1))
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('app.repositories.caja_repository.get_connection')
    def test_listar(self, mock_get_connection):
        """Test: Listar todas las cajas"""
        # Arrange
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn
        mock_cursor.fetchall.return_value = [
            (1, '2025-12-25', None, 100.0, None, 1, 'Abierta'),
            (2, '2025-12-24', '2025-12-24 18:00:00', 100.0, 150.0, 1, 'Cerrada')
        ]

        # Act
        resultado = CajaRepository.listar()

        # Assert
        mock_get_connection.assert_called_once()
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with('SELECT * FROM caja ORDER BY fecha_apertura DESC')
        mock_conn.close.assert_called_once()
        self.assertEqual(len(resultado), 2)
        self.assertIsInstance(resultado[0], Caja)
        self.assertEqual(resultado[0].id, 1)
        self.assertEqual(resultado[1].id, 2)


if __name__ == '__main__':
    unittest.main()