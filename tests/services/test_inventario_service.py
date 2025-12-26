"""
Pruebas unitarias para InventarioService
Utiliza unittest, pytest y mocking
Probando: agregar productos, actualizar stock, alertas de stock bajo
"""
import unittest
from unittest.mock import Mock, patch
import pytest
from app.services.inventario_service import InventarioService
from app.models.producto import Producto


class TestInventarioService(unittest.TestCase):
    """Suite de pruebas para InventarioService"""

    def setUp(self):
        """Configuración inicial para cada test"""
        self.producto_data = {
            'id': 1,
            'nombre': 'Producto Test',
            'precio': 50.00,
            'stock': 100,
            'stock_minimo': 10,
            'fk_proveedor': 1
        }

    def tearDown(self):
        """Limpieza después de cada test"""
        pass

    # ==================== TESTS PARA AGREGAR PRODUCTO ====================

    @patch('app.services.inventario_service.ProductoRepository')
    def test_agregar_producto_exitoso(self, mock_repo):
        """Test: Agregar producto exitosamente"""
        # Arrange
        mock_producto = Mock()
        mock_producto.id = 1
        mock_repo.crear.return_value = mock_producto

        # Act
        resultado = InventarioService.agregar_producto(
            self.producto_data['nombre'],
            self.producto_data['precio'],
            self.producto_data['stock'],
            self.producto_data['stock_minimo'],
            self.producto_data['fk_proveedor']
        )

        # Assert
        mock_repo.crear.assert_called_once()
        self.assertEqual(resultado, mock_producto)

    @patch('app.services.inventario_service.ProductoRepository')
    def test_agregar_producto_precio_negativo(self, mock_repo):
        """Test: No se puede agregar producto con precio negativo"""
        # Act & Assert
        with self.assertRaises(Exception) as context:
            InventarioService.agregar_producto(
                'Producto',
                -50.00,
                100,
                10,
                1
            )
        
        self.assertIn("precio no puede ser negativo", str(context.exception))

    @patch('app.services.inventario_service.ProductoRepository')
    def test_agregar_producto_stock_negativo(self, mock_repo):
        """Test: No se puede agregar producto con stock negativo"""
        # Act & Assert
        with self.assertRaises(Exception) as context:
            InventarioService.agregar_producto(
                'Producto',
                50.00,
                -100,
                10,
                1
            )
        
        self.assertIn("stock no puede ser negativo", str(context.exception))

    @patch('app.services.inventario_service.ProductoRepository')
    def test_agregar_producto_precio_cero(self, mock_repo):
        """Test: Se puede agregar producto con precio 0"""
        # Arrange
        mock_producto = Mock()
        mock_producto.id = 1
        mock_repo.crear.return_value = mock_producto

        # Act
        resultado = InventarioService.agregar_producto(
            'Producto',
            0,
            100,
            10,
            1
        )

        # Assert
        self.assertIsNotNone(resultado)

    @patch('app.services.inventario_service.ProductoRepository')
    def test_agregar_producto_stock_cero(self, mock_repo):
        """Test: Se puede agregar producto con stock 0"""
        # Arrange
        mock_producto = Mock()
        mock_producto.id = 1
        mock_repo.crear.return_value = mock_producto

        # Act
        resultado = InventarioService.agregar_producto(
            'Producto',
            50.00,
            0,
            10,
            1
        )

        # Assert
        self.assertIsNotNone(resultado)

    # ==================== TESTS PARA ACTUALIZAR PRODUCTO ====================

    @patch('app.services.inventario_service.ProductoRepository')
    def test_actualizar_producto_exitoso(self, mock_repo):
        """Test: Actualizar producto exitosamente"""
        # Arrange
        mock_producto = Mock()
        mock_producto.id = 1
        mock_producto.nombre = 'Producto Actualizado'
        mock_producto.precio = 75.00
        mock_producto.stock_minimo = 15
        mock_repo.obtener_por_id.return_value = mock_producto

        # Act
        resultado = InventarioService.actualizar_producto(
            1,
            'Producto Actualizado',
            75.00,
            15
        )

        # Assert
        mock_repo.actualizar.assert_called_once()
        self.assertEqual(resultado, mock_producto)

    @patch('app.services.inventario_service.ProductoRepository')
    def test_actualizar_producto_no_existe(self, mock_repo):
        """Test: No se puede actualizar producto que no existe"""
        # Arrange
        mock_repo.obtener_por_id.return_value = None

        # Act & Assert
        with self.assertRaises(Exception) as context:
            InventarioService.actualizar_producto(999, 'Producto', 50.00, 10)
        
        self.assertIn("Producto no encontrado", str(context.exception))

    @patch('app.services.inventario_service.ProductoRepository')
    def test_actualizar_producto_datos_nuevos(self, mock_repo):
        """Test: Actualizar producto con datos nuevos"""
        # Arrange
        mock_producto = Mock()
        mock_producto.id = 1
        mock_repo.obtener_por_id.return_value = mock_producto

        # Act
        resultado = InventarioService.actualizar_producto(
            1,
            'Nuevo Nombre',
            100.00,
            20
        )

        # Assert
        self.assertEqual(mock_producto.nombre, 'Nuevo Nombre')
        self.assertEqual(mock_producto.precio, 100.00)
        self.assertEqual(mock_producto.stock_minimo, 20)

    # ==================== TESTS PARA AGREGAR STOCK ====================

    @patch('app.services.inventario_service.ProductoRepository')
    def test_agregar_stock_exitoso(self, mock_repo):
        """Test: Agregar stock exitosamente"""
        # Arrange
        mock_producto = Mock()
        mock_producto.id = 1
        mock_producto.stock = 100
        mock_repo.obtener_por_id.side_effect = [mock_producto, mock_producto]

        # Act
        resultado = InventarioService.agregar_stock(1, 50)

        # Assert
        mock_repo.actualizar_stock.assert_called_once_with(1, 50)
        self.assertIsNotNone(resultado)

    @patch('app.services.inventario_service.ProductoRepository')
    def test_agregar_stock_producto_no_existe(self, mock_repo):
        """Test: No se puede agregar stock a producto no existe"""
        # Arrange
        mock_repo.obtener_por_id.return_value = None

        # Act & Assert
        with self.assertRaises(Exception) as context:
            InventarioService.agregar_stock(999, 50)
        
        self.assertIn("Producto no encontrado", str(context.exception))

    @patch('app.services.inventario_service.ProductoRepository')
    def test_agregar_stock_cantidad_cero(self, mock_repo):
        """Test: No se puede agregar stock con cantidad 0"""
        # Arrange
        mock_producto = Mock()
        mock_producto.id = 1
        mock_repo.obtener_por_id.return_value = mock_producto

        # Act & Assert
        with self.assertRaises(Exception) as context:
            InventarioService.agregar_stock(1, 0)
        
        self.assertIn("cantidad debe ser mayor a 0", str(context.exception))

    @patch('app.services.inventario_service.ProductoRepository')
    def test_agregar_stock_cantidad_negativa(self, mock_repo):
        """Test: No se puede agregar stock con cantidad negativa"""
        # Arrange
        mock_producto = Mock()
        mock_producto.id = 1
        mock_repo.obtener_por_id.return_value = mock_producto

        # Act & Assert
        with self.assertRaises(Exception) as context:
            InventarioService.agregar_stock(1, -50)
        
        self.assertIn("cantidad debe ser mayor a 0", str(context.exception))

    @patch('app.services.inventario_service.ProductoRepository')
    def test_agregar_stock_cantidad_grande(self, mock_repo):
        """Test: Agregar cantidad grande de stock"""
        # Arrange
        mock_producto = Mock()
        mock_producto.id = 1
        mock_producto.stock = 100
        mock_repo.obtener_por_id.side_effect = [mock_producto, mock_producto]

        # Act
        resultado = InventarioService.agregar_stock(1, 10000)

        # Assert
        mock_repo.actualizar_stock.assert_called_once_with(1, 10000)

    # ==================== TESTS PARA ALERTAS DE STOCK ====================

    @patch('app.services.inventario_service.ProductoRepository')
    def test_obtener_alertas_stock_exitoso(self, mock_repo):
        """Test: Obtiene alertas de productos con stock bajo"""
        # Arrange
        mock_producto1 = Mock()
        mock_producto1.to_dict.return_value = {'id': 1, 'nombre': 'Producto 1', 'stock': 5}
        mock_producto2 = Mock()
        mock_producto2.to_dict.return_value = {'id': 2, 'nombre': 'Producto 2', 'stock': 8}
        mock_repo.obtener_productos_bajo_stock.return_value = [mock_producto1, mock_producto2]

        # Act
        resultado = InventarioService.obtener_alertas_stock()

        # Assert
        self.assertEqual(len(resultado), 2)
        self.assertEqual(resultado[0]['id'], 1)

    @patch('app.services.inventario_service.ProductoRepository')
    def test_obtener_alertas_stock_ninguno_bajo(self, mock_repo):
        """Test: No hay alertas cuando todo stock está bien"""
        # Arrange
        mock_repo.obtener_productos_bajo_stock.return_value = []

        # Act
        resultado = InventarioService.obtener_alertas_stock()

        # Assert
        self.assertEqual(len(resultado), 0)

    @patch('app.services.inventario_service.ProductoRepository')
    def test_obtener_alertas_stock_multiples(self, mock_repo):
        """Test: Obtiene múltiples alertas de stock"""
        # Arrange
        productos_bajo_stock = []
        for i in range(5):
            mock_producto = Mock()
            mock_producto.to_dict.return_value = {'id': i + 1, 'stock': i + 1}
            productos_bajo_stock.append(mock_producto)
        mock_repo.obtener_productos_bajo_stock.return_value = productos_bajo_stock

        # Act
        resultado = InventarioService.obtener_alertas_stock()

        # Assert
        self.assertEqual(len(resultado), 5)

    # ==================== TESTS PARA LISTAR PRODUCTOS ====================

    @patch('app.services.inventario_service.ProductoRepository')
    def test_listar_productos_exitoso(self, mock_repo):
        """Test: Lista todos los productos"""
        # Arrange
        mock_producto1 = Mock()
        mock_producto1.to_dict.return_value = {'id': 1, 'nombre': 'Producto 1'}
        mock_producto2 = Mock()
        mock_producto2.to_dict.return_value = {'id': 2, 'nombre': 'Producto 2'}
        mock_repo.listar.return_value = [mock_producto1, mock_producto2]

        # Act
        resultado = InventarioService.listar_productos()

        # Assert
        self.assertEqual(len(resultado), 2)

    @patch('app.services.inventario_service.ProductoRepository')
    def test_listar_productos_vacio(self, mock_repo):
        """Test: Lista vacía cuando no hay productos"""
        # Arrange
        mock_repo.listar.return_value = []

        # Act
        resultado = InventarioService.listar_productos()

        # Assert
        self.assertEqual(len(resultado), 0)

    # ==================== TESTS PARA BUSCAR PRODUCTO ====================

    @patch('app.services.inventario_service.ProductoRepository')
    def test_buscar_producto_existe(self, mock_repo):
        """Test: Busca producto existente"""
        # Arrange
        mock_producto = Mock()
        mock_producto.to_dict.return_value = {'id': 1, 'nombre': 'Producto'}
        mock_repo.obtener_por_id.return_value = mock_producto

        # Act
        resultado = InventarioService.buscar_producto(1)

        # Assert
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado['id'], 1)

    @patch('app.services.inventario_service.ProductoRepository')
    def test_buscar_producto_no_existe(self, mock_repo):
        """Test: Busca producto que no existe"""
        # Arrange
        mock_repo.obtener_por_id.return_value = None

        # Act
        resultado = InventarioService.buscar_producto(999)

        # Assert
        self.assertIsNone(resultado)


if __name__ == '__main__':
    unittest.main()
