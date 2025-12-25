"""
Pruebas unitarias para CajaController
Utiliza unittest, pytest y mocking
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
import pytest
from app.controllers.caja_controller import CajaController
from app.models.caja import Caja


class TestCajaController(unittest.TestCase):
    """Suite de pruebas para CajaController"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.monto_inicial = 500.00
        self.monto_final = 1500.00
        self.fk_usuario = 1
        
    def tearDown(self):
        """Limpieza después de cada test"""
        pass

    # ==================== TESTS PARA ABRIR CAJA ====================
    
    @patch('app.controllers.caja_controller.CajaService')
    def test_abrir_caja_exitoso(self, mock_caja_service):
        """Test: Apertura exitosa de caja"""
        # Arrange
        mock_caja = Mock()
        mock_caja.id = 1
        mock_caja.monto_inicial = self.monto_inicial
        mock_caja.fk_usuario = self.fk_usuario
        mock_caja.to_dict.return_value = {
            'id': 1,
            'monto_inicial': self.monto_inicial,
            'fk_usuario': self.fk_usuario,
            'activa': True
        }
        
        mock_caja_service.abrir_caja.return_value = mock_caja
        
        # Act
        resultado = CajaController.abrir_caja(self.monto_inicial, self.fk_usuario)
        
        # Assert
        self.assertTrue(resultado['success'])
        self.assertEqual(resultado['message'], 'Caja abierta exitosamente')
        self.assertIn('caja', resultado)
        self.assertEqual(resultado['caja']['monto_inicial'], self.monto_inicial)
        mock_caja_service.abrir_caja.assert_called_once_with(self.monto_inicial, self.fk_usuario)
    
    @patch('app.controllers.caja_controller.CajaService')
    def test_abrir_caja_con_error(self, mock_caja_service):
        """Test: Error al abrir caja"""
        # Arrange
        mock_caja_service.abrir_caja.side_effect = Exception("Ya existe una caja abierta")
        
        # Act
        resultado = CajaController.abrir_caja(self.monto_inicial, self.fk_usuario)
        
        # Assert
        self.assertFalse(resultado['success'])
        self.assertEqual(resultado['message'], "Ya existe una caja abierta")
        mock_caja_service.abrir_caja.assert_called_once()
    
    @patch('app.controllers.caja_controller.CajaService')
    def test_abrir_caja_monto_cero(self, mock_caja_service):
        """Test: Apertura de caja con monto inicial cero"""
        # Arrange
        mock_caja = Mock()
        mock_caja.to_dict.return_value = {'id': 1, 'monto_inicial': 0}
        mock_caja_service.abrir_caja.return_value = mock_caja
        
        # Act
        resultado = CajaController.abrir_caja(0, self.fk_usuario)
        
        # Assert
        self.assertTrue(resultado['success'])
        mock_caja_service.abrir_caja.assert_called_once_with(0, self.fk_usuario)
    
    @patch('app.controllers.caja_controller.CajaService')
    def test_abrir_caja_monto_negativo(self, mock_caja_service):
        """Test: Error al intentar abrir caja con monto negativo"""
        # Arrange
        mock_caja_service.abrir_caja.side_effect = Exception("Monto inicial no puede ser negativo")
        
        # Act
        resultado = CajaController.abrir_caja(-100, self.fk_usuario)
        
        # Assert
        self.assertFalse(resultado['success'])
        self.assertIn("negativo", resultado['message'])

    # ==================== TESTS PARA CERRAR CAJA ====================
    
    @patch('app.controllers.caja_controller.CajaService')
    def test_cerrar_caja_exitoso(self, mock_caja_service):
        """Test: Cierre exitoso de caja"""
        # Arrange
        mock_resultado = {
            'caja_id': 1,
            'monto_inicial': self.monto_inicial,
            'monto_final': self.monto_final,
            'diferencia': self.monto_final - self.monto_inicial
        }
        mock_caja_service.cerrar_caja.return_value = mock_resultado
        
        # Act
        resultado = CajaController.cerrar_caja(self.monto_final)
        
        # Assert
        self.assertTrue(resultado['success'])
        self.assertEqual(resultado['message'], 'Caja cerrada exitosamente')
        self.assertIn('data', resultado)
        self.assertEqual(resultado['data']['monto_final'], self.monto_final)
        mock_caja_service.cerrar_caja.assert_called_once_with(self.monto_final)
    
    @patch('app.controllers.caja_controller.CajaService')
    def test_cerrar_caja_sin_caja_abierta(self, mock_caja_service):
        """Test: Error al intentar cerrar cuando no hay caja abierta"""
        # Arrange
        mock_caja_service.cerrar_caja.side_effect = Exception("No hay caja abierta")
        
        # Act
        resultado = CajaController.cerrar_caja(self.monto_final)
        
        # Assert
        self.assertFalse(resultado['success'])
        self.assertEqual(resultado['message'], "No hay caja abierta")
    
    @patch('app.controllers.caja_controller.CajaService')
    def test_cerrar_caja_con_diferencia_positiva(self, mock_caja_service):
        """Test: Cierre de caja con ganancia"""
        # Arrange
        mock_resultado = {
            'diferencia': 1000.00,
            'monto_inicial': 500.00,
            'monto_final': 1500.00
        }
        mock_caja_service.cerrar_caja.return_value = mock_resultado
        
        # Act
        resultado = CajaController.cerrar_caja(1500.00)
        
        # Assert
        self.assertTrue(resultado['success'])
        self.assertGreater(resultado['data']['diferencia'], 0)
    
    @patch('app.controllers.caja_controller.CajaService')
    def test_cerrar_caja_con_diferencia_negativa(self, mock_caja_service):
        """Test: Cierre de caja con pérdida"""
        # Arrange
        mock_resultado = {
            'diferencia': -200.00,
            'monto_inicial': 500.00,
            'monto_final': 300.00
        }
        mock_caja_service.cerrar_caja.return_value = mock_resultado
        
        # Act
        resultado = CajaController.cerrar_caja(300.00)
        
        # Assert
        self.assertTrue(resultado['success'])
        self.assertLess(resultado['data']['diferencia'], 0)

    # ==================== TESTS PARA OBTENER CAJA ACTUAL ====================
    
    @patch('app.controllers.caja_controller.CajaService')
    def test_obtener_caja_actual_exitoso(self, mock_caja_service):
        """Test: Obtención exitosa de caja actual"""
        # Arrange
        mock_caja = {
            'id': 1,
            'monto_inicial': 500.00,
            'activa': True
        }
        mock_caja_service.obtener_caja_actual.return_value = mock_caja
        
        # Act
        resultado = CajaController.obtener_caja_actual()
        
        # Assert
        self.assertTrue(resultado['success'])
        self.assertIn('caja', resultado)
        self.assertEqual(resultado['caja']['id'], 1)
        mock_caja_service.obtener_caja_actual.assert_called_once()
    
    @patch('app.controllers.caja_controller.CajaService')
    def test_obtener_caja_actual_sin_caja(self, mock_caja_service):
        """Test: No hay caja abierta actualmente"""
        # Arrange
        mock_caja_service.obtener_caja_actual.return_value = None
        
        # Act
        resultado = CajaController.obtener_caja_actual()
        
        # Assert
        self.assertFalse(resultado['success'])
        self.assertEqual(resultado['message'], 'No hay caja abierta')
    
    @patch('app.controllers.caja_controller.CajaService')
    def test_obtener_caja_actual_con_error(self, mock_caja_service):
        """Test: Error al obtener caja actual"""
        # Arrange
        mock_caja_service.obtener_caja_actual.side_effect = Exception("Error de base de datos")
        
        # Act
        resultado = CajaController.obtener_caja_actual()
        
        # Assert
        self.assertFalse(resultado['success'])
        self.assertIn("Error", resultado['message'])

    # ==================== TESTS PARA LISTAR CAJAS ====================
    
    @patch('app.controllers.caja_controller.CajaService')
    def test_listar_cajas_exitoso(self, mock_caja_service):
        """Test: Listado exitoso de cajas"""
        # Arrange
        mock_cajas = [
            {'id': 1, 'monto_inicial': 500.00, 'activa': False},
            {'id': 2, 'monto_inicial': 600.00, 'activa': True}
        ]
        mock_caja_service.listar_cajas.return_value = mock_cajas
        
        # Act
        resultado = CajaController.listar_cajas()
        
        # Assert
        self.assertTrue(resultado['success'])
        self.assertIn('cajas', resultado)
        self.assertEqual(len(resultado['cajas']), 2)
        mock_caja_service.listar_cajas.assert_called_once()
    
    @patch('app.controllers.caja_controller.CajaService')
    def test_listar_cajas_vacio(self, mock_caja_service):
        """Test: Listado cuando no hay cajas"""
        # Arrange
        mock_caja_service.listar_cajas.return_value = []
        
        # Act
        resultado = CajaController.listar_cajas()
        
        # Assert
        self.assertTrue(resultado['success'])
        self.assertEqual(len(resultado['cajas']), 0)
    
    @patch('app.controllers.caja_controller.CajaService')
    def test_listar_cajas_con_error(self, mock_caja_service):
        """Test: Error al listar cajas"""
        # Arrange
        mock_caja_service.listar_cajas.side_effect = Exception("Error de conexión")
        
        # Act
        resultado = CajaController.listar_cajas()
        
        # Assert
        self.assertFalse(resultado['success'])
        self.assertIn("conexión", resultado['message'])


# ==================== TESTS CON PYTEST ====================

@pytest.fixture
def mock_caja():
    """Fixture: Caja de prueba"""
    caja = Mock()
    caja.id = 1
    caja.monto_inicial = 500.00
    caja.monto_final = None
    caja.activa = True
    caja.to_dict.return_value = {
        'id': 1,
        'monto_inicial': 500.00,
        'activa': True
    }
    return caja


def test_abrir_caja_con_pytest(mock_caja):
    """Test con pytest: Apertura de caja"""
    with patch('app.controllers.caja_controller.CajaService') as mock_service:
        mock_service.abrir_caja.return_value = mock_caja
        
        resultado = CajaController.abrir_caja(500.00, 1)
        
        assert resultado['success'] is True
        assert resultado['message'] == 'Caja abierta exitosamente'
        assert 'caja' in resultado


def test_ciclo_completo_caja():
    """Test con pytest: Ciclo completo de apertura y cierre"""
    with patch('app.controllers.caja_controller.CajaService') as mock_service:
        # Abrir caja
        mock_caja = Mock()
        mock_caja.to_dict.return_value = {'id': 1, 'monto_inicial': 500.00}
        mock_service.abrir_caja.return_value = mock_caja
        
        resultado_abrir = CajaController.abrir_caja(500.00, 1)
        assert resultado_abrir['success'] is True
        
        # Cerrar caja
        mock_service.cerrar_caja.return_value = {
            'monto_inicial': 500.00,
            'monto_final': 1500.00,
            'diferencia': 1000.00
        }
        
        resultado_cerrar = CajaController.cerrar_caja(1500.00)
        assert resultado_cerrar['success'] is True
        assert resultado_cerrar['data']['diferencia'] == 1000.00


@pytest.mark.parametrize("monto_inicial,esperado", [
    (0, True),
    (100, True),
    (1000, True),
    (5000.50, True)
])
def test_abrir_caja_diferentes_montos(monto_inicial, esperado):
    """Test con pytest: Probar diferentes montos iniciales"""
    with patch('app.controllers.caja_controller.CajaService') as mock_service:
        mock_caja = Mock()
        mock_caja.to_dict.return_value = {'monto_inicial': monto_inicial}
        mock_service.abrir_caja.return_value = mock_caja
        
        resultado = CajaController.abrir_caja(monto_inicial, 1)
        
        assert resultado['success'] == esperado


if __name__ == '__main__':
    # Ejecutar tests con unittest
    unittest.main()
