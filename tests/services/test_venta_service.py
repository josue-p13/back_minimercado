"""
Pruebas unitarias para VentaService
Utiliza unittest, pytest y mocking
Probando: procesamiento de ventas, validación de stock, actualización de inventario
"""
import unittest
from unittest.mock import Mock, patch
import pytest
from app.services.venta_service import VentaService
from app.models.venta import Venta, DetalleVenta


class TestVentaService(unittest.TestCase):
    """Suite de pruebas para VentaService"""

    def setUp(self):
        """Configuración inicial para cada test"""
        self.items_venta = [
            {'producto_id': 1, 'cantidad': 2},
            {'producto_id': 2, 'cantidad': 3}
        ]
        self.fk_cliente = 1
        self.fk_usuario = 1

    def tearDown(self):
        """Limpieza después de cada test"""
        pass

    # ==================== TESTS PARA PROCESAR VENTA ====================

    @patch('app.services.venta_service.CajaRepository')
    @patch('app.services.venta_service.ProductoRepository')
    @patch('app.services.venta_service.VentaRepository')
    def test_procesar_venta_exitoso(self, mock_venta_repo, mock_producto_repo, mock_caja_repo):
        """Test: Procesar venta exitosamente"""
        # Arrange
        mock_caja = Mock()
        mock_caja.id = 1
        mock_caja_repo.obtener_caja_abierta.return_value = mock_caja

        # Productos mock
        mock_producto1 = Mock()
        mock_producto1.id = 1
        mock_producto1.precio = 50.00
        mock_producto1.stock = 100
        
        mock_producto2 = Mock()
        mock_producto2.id = 2
        mock_producto2.precio = 75.00
        mock_producto2.stock = 50

        mock_producto_repo.obtener_por_id.side_effect = [
            mock_producto1, mock_producto1, mock_producto2, mock_producto2,
            mock_producto1, mock_producto2
        ]

        mock_venta = Mock()
        mock_venta.id = 1
        mock_venta_repo.crear.return_value = mock_venta

        # Act
        resultado = VentaService.procesar_venta(
            self.items_venta,
            self.fk_cliente,
            self.fk_usuario
        )

        # Assert
        self.assertEqual(resultado, mock_venta)
        mock_venta_repo.crear.assert_called_once()

    @patch('app.services.venta_service.CajaRepository')
    def test_procesar_venta_sin_caja_abierta(self, mock_caja_repo):
        """Test: No se puede procesar venta sin caja abierta"""
        # Arrange
        mock_caja_repo.obtener_caja_abierta.return_value = None

        # Act & Assert
        with self.assertRaises(Exception) as context:
            VentaService.procesar_venta(self.items_venta, self.fk_cliente, self.fk_usuario)
        
        self.assertIn("No hay caja abierta", str(context.exception))

    @patch('app.services.venta_service.CajaRepository')
    @patch('app.services.venta_service.ProductoRepository')
    def test_procesar_venta_producto_no_existe(self, mock_producto_repo, mock_caja_repo):
        """Test: No se puede procesar venta con producto inexistente"""
        # Arrange
        mock_caja = Mock()
        mock_caja.id = 1
        mock_caja_repo.obtener_caja_abierta.return_value = mock_caja
        mock_producto_repo.obtener_por_id.return_value = None

        # Act & Assert
        with self.assertRaises(Exception) as context:
            VentaService.procesar_venta(self.items_venta, self.fk_cliente, self.fk_usuario)
        
        self.assertIn("no existe", str(context.exception))

    @patch('app.services.venta_service.CajaRepository')
    @patch('app.services.venta_service.ProductoRepository')
    def test_procesar_venta_stock_insuficiente(self, mock_producto_repo, mock_caja_repo):
        """Test: No se puede procesar venta con stock insuficiente"""
        # Arrange
        mock_caja = Mock()
        mock_caja.id = 1
        mock_caja_repo.obtener_caja_abierta.return_value = mock_caja

        mock_producto = Mock()
        mock_producto.id = 1
        mock_producto.nombre = "Producto 1"
        mock_producto.stock = 1  # Solo 1 en stock, pero se piden 2
        mock_producto_repo.obtener_por_id.return_value = mock_producto

        # Act & Assert
        with self.assertRaises(Exception) as context:
            VentaService.procesar_venta(self.items_venta, self.fk_cliente, self.fk_usuario)
        
        self.assertIn("Stock insuficiente", str(context.exception))

    @patch('app.services.venta_service.CajaRepository')
    @patch('app.services.venta_service.ProductoRepository')
    @patch('app.services.venta_service.VentaRepository')
    def test_procesar_venta_calcula_total_correcto(self, mock_venta_repo, mock_producto_repo, mock_caja_repo):
        """Test: Procesar venta calcula el total correctamente"""
        # Arrange
        mock_caja = Mock()
        mock_caja.id = 1
        mock_caja_repo.obtener_caja_abierta.return_value = mock_caja

        mock_producto1 = Mock()
        mock_producto1.id = 1
        mock_producto1.precio = 50.00
        mock_producto1.stock = 100
        
        mock_producto2 = Mock()
        mock_producto2.id = 2
        mock_producto2.precio = 75.00
        mock_producto2.stock = 50

        # Usar side_effect con función para retornar el producto correcto múltiples veces
        def get_producto(id_producto):
            if id_producto == 1:
                return mock_producto1
            elif id_producto == 2:
                return mock_producto2
            return None
        
        mock_producto_repo.obtener_por_id.side_effect = get_producto

        mock_venta = Mock()
        mock_venta.id = 1
        mock_venta_repo.crear.return_value = mock_venta

        # Act
        resultado = VentaService.procesar_venta(
            self.items_venta,
            self.fk_cliente,
            self.fk_usuario
        )

        # Assert
        # Verificar que la venta se creó
        self.assertEqual(resultado, mock_venta)
        mock_venta_repo.crear.assert_called_once()
        # Verificar que se pasó el total correcto
        call_args = mock_venta_repo.crear.call_args[0][0]
        # Total debería ser: (50 * 2) + (75 * 3) = 100 + 225 = 325
        self.assertEqual(call_args.total, 325)

    @patch('app.services.venta_service.CajaRepository')
    @patch('app.services.venta_service.ProductoRepository')
    @patch('app.services.venta_service.VentaRepository')
    def test_procesar_venta_actualiza_stock(self, mock_venta_repo, mock_producto_repo, mock_caja_repo):
        """Test: Procesar venta actualiza el stock correctamente"""
        # Arrange
        mock_caja = Mock()
        mock_caja.id = 1
        mock_caja_repo.obtener_caja_abierta.return_value = mock_caja

        mock_producto1 = Mock()
        mock_producto1.id = 1
        mock_producto1.precio = 50.00
        mock_producto1.stock = 100
        
        mock_producto2 = Mock()
        mock_producto2.id = 2
        mock_producto2.precio = 75.00
        mock_producto2.stock = 50

        def get_producto(id_producto):
            if id_producto == 1:
                return mock_producto1
            elif id_producto == 2:
                return mock_producto2
            return None
        
        mock_producto_repo.obtener_por_id.side_effect = get_producto

        mock_venta = Mock()
        mock_venta.id = 1
        mock_venta_repo.crear.return_value = mock_venta

        # Act
        resultado = VentaService.procesar_venta(
            self.items_venta,
            self.fk_cliente,
            self.fk_usuario
        )

        # Assert
        # Debe actualizar stock: producto 1 en -2 y producto 2 en -3
        calls = mock_producto_repo.actualizar_stock.call_args_list
        self.assertEqual(len(calls), 2)
        # Los llamados pueden estar en cualquier orden, así que verificamos que ambos ocurran
        call_args_list = [(call[0][0], call[0][1]) for call in calls]
        self.assertIn((1, -2), call_args_list)
        self.assertIn((2, -3), call_args_list)

    @patch('app.services.venta_service.CajaRepository')
    @patch('app.services.venta_service.ProductoRepository')
    @patch('app.services.venta_service.VentaRepository')
    def test_procesar_venta_vacia(self, mock_venta_repo, mock_producto_repo, mock_caja_repo):
        """Test: Procesar venta con lista vacía de items"""
        # Arrange
        mock_caja = Mock()
        mock_caja.id = 1
        mock_caja_repo.obtener_caja_abierta.return_value = mock_caja

        mock_venta = Mock()
        mock_venta.id = 1
        mock_venta.total = 0
        mock_venta_repo.crear.return_value = mock_venta

        # Act
        resultado = VentaService.procesar_venta([], self.fk_cliente, self.fk_usuario)

        # Assert
        self.assertIsNotNone(resultado)

    # ==================== TESTS PARA OBTENER VENTA COMPLETA ====================

    @patch('app.services.venta_service.VentaRepository')
    def test_obtener_venta_completa_exitoso(self, mock_repo):
        """Test: Obtiene venta completa con detalles"""
        # Arrange
        mock_venta = Mock()
        mock_venta.to_dict.return_value = {'id': 1, 'total': 325}
        
        mock_detalle1 = Mock()
        mock_detalle1.to_dict.return_value = {'producto_id': 1, 'cantidad': 2}
        mock_detalle2 = Mock()
        mock_detalle2.to_dict.return_value = {'producto_id': 2, 'cantidad': 3}
        
        mock_repo.obtener_por_id.return_value = mock_venta
        mock_repo.obtener_detalles.return_value = [mock_detalle1, mock_detalle2]

        # Act
        resultado = VentaService.obtener_venta_completa(1)

        # Assert
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado['venta']['id'], 1)
        self.assertEqual(len(resultado['detalles']), 2)

    @patch('app.services.venta_service.VentaRepository')
    def test_obtener_venta_completa_no_existe(self, mock_repo):
        """Test: Obtiene None para venta inexistente"""
        # Arrange
        mock_repo.obtener_por_id.return_value = None

        # Act
        resultado = VentaService.obtener_venta_completa(999)

        # Assert
        self.assertIsNone(resultado)

    @patch('app.services.venta_service.VentaRepository')
    def test_obtener_venta_completa_sin_detalles(self, mock_repo):
        """Test: Obtiene venta con detalles vacío"""
        # Arrange
        mock_venta = Mock()
        mock_venta.to_dict.return_value = {'id': 1, 'total': 0}
        
        mock_repo.obtener_por_id.return_value = mock_venta
        mock_repo.obtener_detalles.return_value = []

        # Act
        resultado = VentaService.obtener_venta_completa(1)

        # Assert
        self.assertIsNotNone(resultado)
        self.assertEqual(len(resultado['detalles']), 0)

    # ==================== TESTS PARA LISTAR VENTAS ====================

    @patch('app.services.venta_service.VentaRepository')
    def test_listar_ventas_exitoso(self, mock_repo):
        """Test: Lista todas las ventas"""
        # Arrange
        mock_venta1 = Mock()
        mock_venta1.to_dict.return_value = {'id': 1, 'total': 325}
        mock_venta2 = Mock()
        mock_venta2.to_dict.return_value = {'id': 2, 'total': 150}
        mock_repo.listar.return_value = [mock_venta1, mock_venta2]

        # Act
        resultado = VentaService.listar_ventas()

        # Assert
        self.assertEqual(len(resultado), 2)
        self.assertEqual(resultado[0]['id'], 1)

    @patch('app.services.venta_service.VentaRepository')
    def test_listar_ventas_vacio(self, mock_repo):
        """Test: Lista vacía cuando no hay ventas"""
        # Arrange
        mock_repo.listar.return_value = []

        # Act
        resultado = VentaService.listar_ventas()

        # Assert
        self.assertEqual(len(resultado), 0)

    @patch('app.services.venta_service.VentaRepository')
    def test_listar_ventas_multiples(self, mock_repo):
        """Test: Lista múltiples ventas"""
        # Arrange
        ventas_mock = []
        for i in range(10):
            mock_venta = Mock()
            mock_venta.to_dict.return_value = {'id': i + 1, 'total': (i + 1) * 100}
            ventas_mock.append(mock_venta)
        mock_repo.listar.return_value = ventas_mock

        # Act
        resultado = VentaService.listar_ventas()

        # Assert
        self.assertEqual(len(resultado), 10)


if __name__ == '__main__':
    unittest.main()
