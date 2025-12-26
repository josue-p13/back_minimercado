"""
Pruebas unitarias para CajaService
Utiliza unittest, pytest y mocking
Probando: apertura y cierre de caja, validaciones
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
import pytest
from app.services.caja_service import CajaService
from app.models.caja import Caja


class TestCajaService(unittest.TestCase):
    """Suite de pruebas para CajaService"""

    def setUp(self):
        """Configuración inicial para cada test"""
        self.monto_inicial = 100.00
        self.fk_usuario = 1
        self.caja_abierta = Mock()
        self.caja_abierta.id = 1
        self.caja_abierta.monto_inicial = 100.00

    def tearDown(self):
        """Limpieza después de cada test"""
        pass

    # ==================== TESTS PARA ABRIR CAJA ====================

    @patch('app.services.caja_service.CajaRepository')
    def test_abrir_caja_exitoso(self, mock_repo):
        """Test: Apertura exitosa de caja"""
        # Arrange
        mock_repo.obtener_caja_abierta.return_value = None
        mock_caja = Mock()
        mock_caja.id = 1
        mock_repo.crear.return_value = mock_caja

        # Act
        resultado = CajaService.abrir_caja(self.monto_inicial, self.fk_usuario)

        # Assert
        mock_repo.obtener_caja_abierta.assert_called_once()
        mock_repo.crear.assert_called_once()
        self.assertEqual(resultado, mock_caja)

    @patch('app.services.caja_service.CajaRepository')
    def test_abrir_caja_ya_existe_abierta(self, mock_repo):
        """Test: No se puede abrir caja si ya existe una abierta"""
        # Arrange
        mock_repo.obtener_caja_abierta.return_value = self.caja_abierta

        # Act & Assert
        with self.assertRaises(Exception) as context:
            CajaService.abrir_caja(self.monto_inicial, self.fk_usuario)
        
        self.assertIn("Ya existe una caja abierta", str(context.exception))

    @patch('app.services.caja_service.CajaRepository')
    def test_abrir_caja_monto_negativo(self, mock_repo):
        """Test: No se puede abrir caja con monto inicial negativo"""
        # Arrange
        mock_repo.obtener_caja_abierta.return_value = None

        # Act & Assert
        with self.assertRaises(Exception) as context:
            CajaService.abrir_caja(-50, self.fk_usuario)
        
        self.assertIn("no puede ser negativo", str(context.exception))

    @patch('app.services.caja_service.CajaRepository')
    def test_abrir_caja_monto_cero(self, mock_repo):
        """Test: Se puede abrir caja con monto inicial de 0"""
        # Arrange
        mock_repo.obtener_caja_abierta.return_value = None
        mock_caja = Mock()
        mock_caja.id = 1
        mock_repo.crear.return_value = mock_caja

        # Act
        resultado = CajaService.abrir_caja(0, self.fk_usuario)

        # Assert
        self.assertIsNotNone(resultado)
        mock_repo.crear.assert_called_once()

    @patch('app.services.caja_service.CajaRepository')
    def test_abrir_caja_monto_grande(self, mock_repo):
        """Test: Se puede abrir caja con monto grande"""
        # Arrange
        monto_grande = 10000.50
        mock_repo.obtener_caja_abierta.return_value = None
        mock_caja = Mock()
        mock_caja.id = 1
        mock_repo.crear.return_value = mock_caja

        # Act
        resultado = CajaService.abrir_caja(monto_grande, self.fk_usuario)

        # Assert
        self.assertIsNotNone(resultado)

    # ==================== TESTS PARA CERRAR CAJA ====================

    @patch('app.services.caja_service.CajaRepository')
    def test_cerrar_caja_exitoso(self, mock_repo):
        """Test: Cierre exitoso de caja"""
        # Arrange
        monto_final = 150.00
        mock_repo.obtener_caja_abierta.return_value = self.caja_abierta

        # Act
        resultado = CajaService.cerrar_caja(monto_final)

        # Assert
        mock_repo.cerrar_caja.assert_called_once()
        self.assertEqual(resultado['monto_inicial'], 100.00)
        self.assertEqual(resultado['monto_final'], 150.00)
        self.assertEqual(resultado['diferencia'], 50.00)

    @patch('app.services.caja_service.CajaRepository')
    def test_cerrar_caja_diferencia_negativa(self, mock_repo):
        """Test: Cierre de caja con diferencia negativa"""
        # Arrange
        monto_final = 80.00
        mock_repo.obtener_caja_abierta.return_value = self.caja_abierta

        # Act
        resultado = CajaService.cerrar_caja(monto_final)

        # Assert
        self.assertEqual(resultado['diferencia'], -20.00)

    @patch('app.services.caja_service.CajaRepository')
    def test_cerrar_caja_sin_caja_abierta(self, mock_repo):
        """Test: No se puede cerrar caja si no hay abierta"""
        # Arrange
        mock_repo.obtener_caja_abierta.return_value = None

        # Act & Assert
        with self.assertRaises(Exception) as context:
            CajaService.cerrar_caja(150.00)
        
        self.assertIn("No hay caja abierta", str(context.exception))

    @patch('app.services.caja_service.CajaRepository')
    def test_cerrar_caja_monto_negativo(self, mock_repo):
        """Test: No se puede cerrar caja con monto negativo"""
        # Arrange
        mock_repo.obtener_caja_abierta.return_value = self.caja_abierta

        # Act & Assert
        with self.assertRaises(Exception) as context:
            CajaService.cerrar_caja(-50)
        
        self.assertIn("no puede ser negativo", str(context.exception))

    @patch('app.services.caja_service.CajaRepository')
    def test_cerrar_caja_monto_cero(self, mock_repo):
        """Test: Se puede cerrar caja con monto de 0"""
        # Arrange
        mock_repo.obtener_caja_abierta.return_value = self.caja_abierta

        # Act
        resultado = CajaService.cerrar_caja(0)

        # Assert
        self.assertEqual(resultado['monto_final'], 0)
        self.assertEqual(resultado['diferencia'], -100.00)

    # ==================== TESTS PARA OBTENER CAJA ACTUAL ====================

    @patch('app.services.caja_service.CajaRepository')
    def test_obtener_caja_actual_existe(self, mock_repo):
        """Test: Obtiene la caja actual cuando existe"""
        # Arrange
        mock_caja = Mock()
        mock_caja.to_dict.return_value = {'id': 1, 'estado': 'Abierta'}
        mock_repo.obtener_caja_abierta.return_value = mock_caja

        # Act
        resultado = CajaService.obtener_caja_actual()

        # Assert
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado['id'], 1)

    @patch('app.services.caja_service.CajaRepository')
    def test_obtener_caja_actual_no_existe(self, mock_repo):
        """Test: Retorna None cuando no hay caja abierta"""
        # Arrange
        mock_repo.obtener_caja_abierta.return_value = None

        # Act
        resultado = CajaService.obtener_caja_actual()

        # Assert
        self.assertIsNone(resultado)

    # ==================== TESTS PARA LISTAR CAJAS ====================

    @patch('app.services.caja_service.CajaRepository')
    def test_listar_cajas_exitoso(self, mock_repo):
        """Test: Lista todas las cajas"""
        # Arrange
        mock_caja1 = Mock()
        mock_caja1.to_dict.return_value = {'id': 1, 'estado': 'Cerrada'}
        mock_caja2 = Mock()
        mock_caja2.to_dict.return_value = {'id': 2, 'estado': 'Cerrada'}
        mock_repo.listar.return_value = [mock_caja1, mock_caja2]

        # Act
        resultado = CajaService.listar_cajas()

        # Assert
        self.assertEqual(len(resultado), 2)
        self.assertEqual(resultado[0]['id'], 1)
        self.assertEqual(resultado[1]['id'], 2)

    @patch('app.services.caja_service.CajaRepository')
    def test_listar_cajas_vacio(self, mock_repo):
        """Test: Lista cajas cuando no hay ninguna"""
        # Arrange
        mock_repo.listar.return_value = []

        # Act
        resultado = CajaService.listar_cajas()

        # Assert
        self.assertEqual(len(resultado), 0)
        self.assertEqual(resultado, [])

    @patch('app.services.caja_service.CajaRepository')
    def test_listar_cajas_multiples(self, mock_repo):
        """Test: Lista múltiples cajas"""
        # Arrange
        cajas_mock = []
        for i in range(5):
            mock_caja = Mock()
            mock_caja.to_dict.return_value = {'id': i + 1, 'estado': 'Cerrada'}
            cajas_mock.append(mock_caja)
        mock_repo.listar.return_value = cajas_mock

        # Act
        resultado = CajaService.listar_cajas()

        # Assert
        self.assertEqual(len(resultado), 5)


if __name__ == '__main__':
    unittest.main()
