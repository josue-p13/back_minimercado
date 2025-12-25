"""
Pruebas unitarias para VentaController
Utiliza unittest, pytest y mocking
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
import pytest
from app.controllers.venta_controller import VentaController
from app.models.venta import Venta


class TestVentaController(unittest.TestCase):
    """Suite de pruebas para VentaController"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.venta_id = 1
        self.fk_cliente = 1
        self.fk_usuario = 1
        self.items = [
            {'producto_id': 1, 'cantidad': 2},
            {'producto_id': 2, 'cantidad': 3}
        ]
        
    def tearDown(self):
        """Limpieza después de cada test"""
        pass

    # ==================== TESTS PARA REALIZAR VENTA ====================
    
    @patch('app.controllers.venta_controller.VentaService')
    def test_realizar_venta_exitosa(self, mock_venta_service):
        """Test: RF14 - Procesar venta exitosamente"""
        # Arrange
        mock_venta = Mock()
        mock_venta.id = self.venta_id
        mock_venta.total = 125.50
        mock_venta.to_dict.return_value = {
            'id': self.venta_id,
            'total': 125.50,
            'fk_cliente': self.fk_cliente,
            'fk_usuario': self.fk_usuario,
            'items': self.items
        }
        
        mock_venta_service.procesar_venta.return_value = mock_venta
        
        # Act
        resultado = VentaController.realizar_venta(
            self.items, self.fk_cliente, self.fk_usuario
        )
        
        # Assert
        self.assertTrue(resultado['success'])
        self.assertEqual(resultado['message'], 'Venta procesada exitosamente')
        self.assertIn('venta', resultado)
        self.assertEqual(resultado['venta']['total'], 125.50)
        mock_venta_service.procesar_venta.assert_called_once_with(
            self.items, self.fk_cliente, self.fk_usuario
        )
    
    @patch('app.controllers.venta_controller.VentaService')
    def test_realizar_venta_sin_items(self, mock_venta_service):
        """Test: Error al procesar venta sin items"""
        # Arrange
        mock_venta_service.procesar_venta.side_effect = Exception("La venta debe tener al menos un item")
        
        # Act
        resultado = VentaController.realizar_venta([], self.fk_cliente, self.fk_usuario)
        
        # Assert
        self.assertFalse(resultado['success'])
        self.assertIn("item", resultado['message'])
    
    @patch('app.controllers.venta_controller.VentaService')
    def test_realizar_venta_stock_insuficiente(self, mock_venta_service):
        """Test: Error por stock insuficiente"""
        # Arrange
        mock_venta_service.procesar_venta.side_effect = Exception("Stock insuficiente para producto ID 1")
        
        # Act
        resultado = VentaController.realizar_venta(
            self.items, self.fk_cliente, self.fk_usuario
        )
        
        # Assert
        self.assertFalse(resultado['success'])
        self.assertIn("Stock insuficiente", resultado['message'])
    
    @patch('app.controllers.venta_controller.VentaService')
    def test_realizar_venta_producto_no_existe(self, mock_venta_service):
        """Test: Error cuando producto no existe"""
        # Arrange
        mock_venta_service.procesar_venta.side_effect = Exception("Producto no encontrado")
        
        # Act
        resultado = VentaController.realizar_venta(
            [{'producto_id': 999, 'cantidad': 1}],
            self.fk_cliente, self.fk_usuario
        )
        
        # Assert
        self.assertFalse(resultado['success'])
        self.assertIn("no encontrado", resultado['message'])
    
    @patch('app.controllers.venta_controller.VentaService')
    def test_realizar_venta_sin_caja_abierta(self, mock_venta_service):
        """Test: Error al procesar venta sin caja abierta"""
        # Arrange
        mock_venta_service.procesar_venta.side_effect = Exception("No hay caja abierta")
        
        # Act
        resultado = VentaController.realizar_venta(
            self.items, self.fk_cliente, self.fk_usuario
        )
        
        # Assert
        self.assertFalse(resultado['success'])
        self.assertIn("caja", resultado['message'].lower())
    
    @patch('app.controllers.venta_controller.VentaService')
    def test_realizar_venta_un_solo_item(self, mock_venta_service):
        """Test: Venta con un solo item"""
        # Arrange
        items = [{'producto_id': 1, 'cantidad': 5}]
        mock_venta = Mock()
        mock_venta.to_dict.return_value = {'id': 1, 'total': 50.00}
        mock_venta_service.procesar_venta.return_value = mock_venta
        
        # Act
        resultado = VentaController.realizar_venta(items, self.fk_cliente, self.fk_usuario)
        
        # Assert
        self.assertTrue(resultado['success'])
        mock_venta_service.procesar_venta.assert_called_once_with(
            items, self.fk_cliente, self.fk_usuario
        )
    
    @patch('app.controllers.venta_controller.VentaService')
    def test_realizar_venta_multiples_items(self, mock_venta_service):
        """Test: Venta con múltiples items"""
        # Arrange
        items_multiples = [
            {'producto_id': 1, 'cantidad': 2},
            {'producto_id': 2, 'cantidad': 3},
            {'producto_id': 3, 'cantidad': 1}
        ]
        mock_venta = Mock()
        mock_venta.to_dict.return_value = {'id': 1, 'total': 200.00}
        mock_venta_service.procesar_venta.return_value = mock_venta
        
        # Act
        resultado = VentaController.realizar_venta(
            items_multiples, self.fk_cliente, self.fk_usuario
        )
        
        # Assert
        self.assertTrue(resultado['success'])
        self.assertIn('venta', resultado)

    # ==================== TESTS PARA OBTENER VENTA ====================
    
    @patch('app.controllers.venta_controller.VentaService')
    def test_obtener_venta_exitoso(self, mock_venta_service):
        """Test: RF15 - Obtener venta con detalles exitosamente"""
        # Arrange
        venta_completa = {
            'id': self.venta_id,
            'total': 125.50,
            'fecha': '2024-01-15',
            'cliente': {'id': 1, 'nombre': 'Cliente Test'},
            'usuario': {'id': 1, 'nombre': 'Cajero Test'},
            'detalles': [
                {'producto': 'Producto A', 'cantidad': 2, 'precio': 50.00},
                {'producto': 'Producto B', 'cantidad': 1, 'precio': 25.50}
            ]
        }
        mock_venta_service.obtener_venta_completa.return_value = venta_completa
        
        # Act
        resultado = VentaController.obtener_venta(self.venta_id)
        
        # Assert
        self.assertTrue(resultado['success'])
        self.assertIn('data', resultado)
        self.assertEqual(resultado['data']['total'], 125.50)
        self.assertIn('detalles', resultado['data'])
        mock_venta_service.obtener_venta_completa.assert_called_once_with(self.venta_id)
    
    @patch('app.controllers.venta_controller.VentaService')
    def test_obtener_venta_no_encontrada(self, mock_venta_service):
        """Test: Venta no encontrada"""
        # Arrange
        mock_venta_service.obtener_venta_completa.return_value = None
        
        # Act
        resultado = VentaController.obtener_venta(999)
        
        # Assert
        self.assertFalse(resultado['success'])
        self.assertEqual(resultado['message'], 'Venta no encontrada')
    
    @patch('app.controllers.venta_controller.VentaService')
    def test_obtener_venta_con_error(self, mock_venta_service):
        """Test: Error al obtener venta"""
        # Arrange
        mock_venta_service.obtener_venta_completa.side_effect = Exception("Error de base de datos")
        
        # Act
        resultado = VentaController.obtener_venta(self.venta_id)
        
        # Assert
        self.assertFalse(resultado['success'])
        self.assertIn("Error", resultado['message'])
    
    @patch('app.controllers.venta_controller.VentaService')
    def test_obtener_venta_con_detalles_vacios(self, mock_venta_service):
        """Test: Obtener venta con detalles vacíos"""
        # Arrange
        venta_sin_detalles = {
            'id': self.venta_id,
            'total': 0,
            'detalles': []
        }
        mock_venta_service.obtener_venta_completa.return_value = venta_sin_detalles
        
        # Act
        resultado = VentaController.obtener_venta(self.venta_id)
        
        # Assert
        self.assertTrue(resultado['success'])
        self.assertEqual(len(resultado['data']['detalles']), 0)

    # ==================== TESTS PARA LISTAR VENTAS ====================
    
    @patch('app.controllers.venta_controller.VentaService')
    def test_listar_ventas_exitoso(self, mock_venta_service):
        """Test: Listar todas las ventas exitosamente"""
        # Arrange
        ventas = [
            {'id': 1, 'total': 100.00, 'fecha': '2024-01-15'},
            {'id': 2, 'total': 200.00, 'fecha': '2024-01-16'},
            {'id': 3, 'total': 150.00, 'fecha': '2024-01-17'}
        ]
        mock_venta_service.listar_ventas.return_value = ventas
        
        # Act
        resultado = VentaController.listar_ventas()
        
        # Assert
        self.assertTrue(resultado['success'])
        self.assertIn('ventas', resultado)
        self.assertEqual(len(resultado['ventas']), 3)
        mock_venta_service.listar_ventas.assert_called_once()
    
    @patch('app.controllers.venta_controller.VentaService')
    def test_listar_ventas_vacio(self, mock_venta_service):
        """Test: Listar cuando no hay ventas"""
        # Arrange
        mock_venta_service.listar_ventas.return_value = []
        
        # Act
        resultado = VentaController.listar_ventas()
        
        # Assert
        self.assertTrue(resultado['success'])
        self.assertEqual(len(resultado['ventas']), 0)
    
    @patch('app.controllers.venta_controller.VentaService')
    def test_listar_ventas_con_error(self, mock_venta_service):
        """Test: Error al listar ventas"""
        # Arrange
        mock_venta_service.listar_ventas.side_effect = Exception("Error de conexión")
        
        # Act
        resultado = VentaController.listar_ventas()
        
        # Assert
        self.assertFalse(resultado['success'])
        self.assertIn("Error", resultado['message'])


# ==================== TESTS CON PYTEST ====================

@pytest.fixture
def mock_venta():
    """Fixture: Venta de prueba"""
    venta = Mock()
    venta.id = 1
    venta.total = 125.50
    venta.fk_cliente = 1
    venta.fk_usuario = 1
    venta.to_dict.return_value = {
        'id': 1,
        'total': 125.50,
        'fk_cliente': 1,
        'fk_usuario': 1
    }
    return venta


@pytest.fixture
def items_venta():
    """Fixture: Items de venta de prueba"""
    return [
        {'producto_id': 1, 'cantidad': 2},
        {'producto_id': 2, 'cantidad': 3}
    ]


def test_realizar_venta_con_pytest(mock_venta, items_venta):
    """Test con pytest: Realizar venta"""
    with patch('app.controllers.venta_controller.VentaService') as mock_service:
        mock_service.procesar_venta.return_value = mock_venta
        
        resultado = VentaController.realizar_venta(items_venta, 1, 1)
        
        assert resultado['success'] is True
        assert resultado['message'] == 'Venta procesada exitosamente'
        assert 'venta' in resultado


def test_flujo_completo_venta():
    """Test con pytest: Flujo completo de venta"""
    with patch('app.controllers.venta_controller.VentaService') as mock_service:
        # Realizar venta
        mock_venta = Mock()
        mock_venta.id = 1
        mock_venta.to_dict.return_value = {'id': 1, 'total': 100.00}
        mock_service.procesar_venta.return_value = mock_venta
        
        items = [{'producto_id': 1, 'cantidad': 2}]
        resultado_venta = VentaController.realizar_venta(items, 1, 1)
        assert resultado_venta['success'] is True
        
        # Obtener venta
        venta_completa = {
            'id': 1,
            'total': 100.00,
            'detalles': [{'producto': 'Test', 'cantidad': 2}]
        }
        mock_service.obtener_venta_completa.return_value = venta_completa
        
        resultado_obtener = VentaController.obtener_venta(1)
        assert resultado_obtener['success'] is True
        assert resultado_obtener['data']['total'] == 100.00


@pytest.mark.parametrize("items,esperado_exito", [
    ([{'producto_id': 1, 'cantidad': 1}], True),
    ([{'producto_id': 1, 'cantidad': 5}], True),
    ([{'producto_id': 1, 'cantidad': 1}, {'producto_id': 2, 'cantidad': 2}], True),
])
def test_realizar_venta_diferentes_casos(items, esperado_exito):
    """Test con pytest: Diferentes casos de ventas"""
    with patch('app.controllers.venta_controller.VentaService') as mock_service:
        if esperado_exito:
            mock_venta = Mock()
            mock_venta.to_dict.return_value = {'id': 1, 'total': 100.00}
            mock_service.procesar_venta.return_value = mock_venta
        else:
            mock_service.procesar_venta.side_effect = Exception("Error")
        
        resultado = VentaController.realizar_venta(items, 1, 1)
        
        assert resultado['success'] == esperado_exito


def test_obtener_venta_con_pytest():
    """Test con pytest: Obtener venta con detalles"""
    with patch('app.controllers.venta_controller.VentaService') as mock_service:
        venta_completa = {
            'id': 1,
            'total': 150.00,
            'detalles': [
                {'producto': 'A', 'cantidad': 2, 'precio': 50.00},
                {'producto': 'B', 'cantidad': 1, 'precio': 50.00}
            ]
        }
        mock_service.obtener_venta_completa.return_value = venta_completa
        
        resultado = VentaController.obtener_venta(1)
        
        assert resultado['success'] is True
        assert resultado['data']['total'] == 150.00
        assert len(resultado['data']['detalles']) == 2


def test_listar_ventas_con_pytest():
    """Test con pytest: Listar ventas"""
    with patch('app.controllers.venta_controller.VentaService') as mock_service:
        ventas = [
            {'id': 1, 'total': 100.00},
            {'id': 2, 'total': 200.00}
        ]
        mock_service.listar_ventas.return_value = ventas
        
        resultado = VentaController.listar_ventas()
        
        assert resultado['success'] is True
        assert len(resultado['ventas']) == 2


if __name__ == '__main__':
    # Ejecutar tests con unittest
    unittest.main()
