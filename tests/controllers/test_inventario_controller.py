"""
Pruebas unitarias para InventarioController
Utiliza unittest, pytest y mocking
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
import pytest
from app.controllers.inventario_controller import InventarioController
from app.models.producto import Producto


class TestInventarioController(unittest.TestCase):
    """Suite de pruebas para InventarioController"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.producto_id = 1
        self.nombre = "Producto Test"
        self.precio = 10.50
        self.stock = 100
        self.stock_minimo = 10
        self.fk_proveedor = 1
        
    def tearDown(self):
        """Limpieza después de cada test"""
        pass

    # ==================== TESTS PARA AGREGAR PRODUCTO ====================
    
    @patch('app.controllers.inventario_controller.InventarioService')
    def test_agregar_producto_exitoso(self, mock_inventario_service):
        """Test: Agregar producto exitosamente"""
        # Arrange
        mock_producto = Mock()
        mock_producto.id = self.producto_id
        mock_producto.nombre = self.nombre
        mock_producto.precio = self.precio
        mock_producto.to_dict.return_value = {
            'id': self.producto_id,
            'nombre': self.nombre,
            'precio': self.precio,
            'stock': self.stock
        }
        
        mock_inventario_service.agregar_producto.return_value = mock_producto
        
        # Act
        resultado = InventarioController.agregar_producto(
            self.nombre, self.precio, self.stock, self.stock_minimo, self.fk_proveedor
        )
        
        # Assert
        self.assertTrue(resultado['success'])
        self.assertEqual(resultado['message'], 'Producto agregado exitosamente')
        self.assertIn('producto', resultado)
        self.assertEqual(resultado['producto']['nombre'], self.nombre)
        mock_inventario_service.agregar_producto.assert_called_once_with(
            self.nombre, self.precio, self.stock, self.stock_minimo, self.fk_proveedor
        )
    
    @patch('app.controllers.inventario_controller.InventarioService')
    def test_agregar_producto_con_error(self, mock_inventario_service):
        """Test: Error al agregar producto"""
        # Arrange
        mock_inventario_service.agregar_producto.side_effect = Exception("Producto duplicado")
        
        # Act
        resultado = InventarioController.agregar_producto(
            self.nombre, self.precio, self.stock, self.stock_minimo, self.fk_proveedor
        )
        
        # Assert
        self.assertFalse(resultado['success'])
        self.assertEqual(resultado['message'], "Producto duplicado")
    
    @patch('app.controllers.inventario_controller.InventarioService')
    def test_agregar_producto_precio_invalido(self, mock_inventario_service):
        """Test: Error con precio inválido"""
        # Arrange
        mock_inventario_service.agregar_producto.side_effect = Exception("Precio debe ser positivo")
        
        # Act
        resultado = InventarioController.agregar_producto(
            self.nombre, -10.00, self.stock, self.stock_minimo, self.fk_proveedor
        )
        
        # Assert
        self.assertFalse(resultado['success'])
        self.assertIn("Precio", resultado['message'])

    # ==================== TESTS PARA ACTUALIZAR PRODUCTO ====================
    
    @patch('app.controllers.inventario_controller.InventarioService')
    def test_actualizar_producto_exitoso(self, mock_inventario_service):
        """Test: Actualizar producto exitosamente"""
        # Arrange
        nuevo_nombre = "Producto Actualizado"
        nuevo_precio = 15.00
        nuevo_stock_minimo = 15
        
        mock_producto = Mock()
        mock_producto.to_dict.return_value = {
            'id': self.producto_id,
            'nombre': nuevo_nombre,
            'precio': nuevo_precio,
            'stock_minimo': nuevo_stock_minimo
        }
        
        mock_inventario_service.actualizar_producto.return_value = mock_producto
        
        # Act
        resultado = InventarioController.actualizar_producto(
            self.producto_id, nuevo_nombre, nuevo_precio, nuevo_stock_minimo
        )
        
        # Assert
        self.assertTrue(resultado['success'])
        self.assertEqual(resultado['message'], 'Producto actualizado exitosamente')
        self.assertIn('producto', resultado)
        mock_inventario_service.actualizar_producto.assert_called_once()
    
    @patch('app.controllers.inventario_controller.InventarioService')
    def test_actualizar_producto_no_encontrado(self, mock_inventario_service):
        """Test: Error al actualizar producto inexistente"""
        # Arrange
        mock_inventario_service.actualizar_producto.side_effect = Exception("Producto no encontrado")
        
        # Act
        resultado = InventarioController.actualizar_producto(999, "Nombre", 10.00, 5)
        
        # Assert
        self.assertFalse(resultado['success'])
        self.assertIn("no encontrado", resultado['message'])

    # ==================== TESTS PARA AGREGAR STOCK ====================
    
    @patch('app.controllers.inventario_controller.InventarioService')
    def test_agregar_stock_exitoso(self, mock_inventario_service):
        """Test: RF10 - Agregar stock exitosamente"""
        # Arrange
        cantidad = 50
        nuevo_stock = self.stock + cantidad
        
        mock_producto = Mock()
        mock_producto.stock = nuevo_stock
        mock_producto.to_dict.return_value = {
            'id': self.producto_id,
            'stock': nuevo_stock
        }
        
        mock_inventario_service.agregar_stock.return_value = mock_producto
        
        # Act
        resultado = InventarioController.agregar_stock(self.producto_id, cantidad)
        
        # Assert
        self.assertTrue(resultado['success'])
        self.assertIn(f'Nuevo stock: {nuevo_stock}', resultado['message'])
        self.assertEqual(resultado['producto']['stock'], nuevo_stock)
        mock_inventario_service.agregar_stock.assert_called_once_with(self.producto_id, cantidad)
    
    @patch('app.controllers.inventario_controller.InventarioService')
    def test_agregar_stock_cantidad_cero(self, mock_inventario_service):
        """Test: Agregar stock con cantidad cero"""
        # Arrange
        mock_producto = Mock()
        mock_producto.stock = self.stock
        mock_producto.to_dict.return_value = {'stock': self.stock}
        mock_inventario_service.agregar_stock.return_value = mock_producto
        
        # Act
        resultado = InventarioController.agregar_stock(self.producto_id, 0)
        
        # Assert
        self.assertTrue(resultado['success'])
    
    @patch('app.controllers.inventario_controller.InventarioService')
    def test_agregar_stock_cantidad_negativa(self, mock_inventario_service):
        """Test: Error al agregar stock negativo"""
        # Arrange
        mock_inventario_service.agregar_stock.side_effect = Exception("Cantidad debe ser positiva")
        
        # Act
        resultado = InventarioController.agregar_stock(self.producto_id, -10)
        
        # Assert
        self.assertFalse(resultado['success'])
        self.assertIn("positiva", resultado['message'])

    # ==================== TESTS PARA OBTENER ALERTAS DE STOCK ====================
    
    @patch('app.controllers.inventario_controller.InventarioService')
    def test_obtener_alertas_stock_exitoso(self, mock_inventario_service):
        """Test: RF11 - Obtener alertas de stock bajo"""
        # Arrange
        productos_alerta = [
            {'id': 1, 'nombre': 'Producto A', 'stock': 5, 'stock_minimo': 10},
            {'id': 2, 'nombre': 'Producto B', 'stock': 2, 'stock_minimo': 15}
        ]
        mock_inventario_service.obtener_alertas_stock.return_value = productos_alerta
        
        # Act
        resultado = InventarioController.obtener_alertas_stock()
        
        # Assert
        self.assertTrue(resultado['success'])
        self.assertIn('alertas', resultado)
        self.assertEqual(resultado['total'], 2)
        self.assertEqual(len(resultado['alertas']), 2)
        mock_inventario_service.obtener_alertas_stock.assert_called_once()
    
    @patch('app.controllers.inventario_controller.InventarioService')
    def test_obtener_alertas_stock_sin_alertas(self, mock_inventario_service):
        """Test: Obtener alertas cuando no hay productos con stock bajo"""
        # Arrange
        mock_inventario_service.obtener_alertas_stock.return_value = []
        
        # Act
        resultado = InventarioController.obtener_alertas_stock()
        
        # Assert
        self.assertTrue(resultado['success'])
        self.assertEqual(resultado['total'], 0)
        self.assertEqual(len(resultado['alertas']), 0)
    
    @patch('app.controllers.inventario_controller.InventarioService')
    def test_obtener_alertas_stock_con_error(self, mock_inventario_service):
        """Test: Error al obtener alertas de stock"""
        # Arrange
        mock_inventario_service.obtener_alertas_stock.side_effect = Exception("Error de conexión")
        
        # Act
        resultado = InventarioController.obtener_alertas_stock()
        
        # Assert
        self.assertFalse(resultado['success'])
        self.assertIn("Error", resultado['message'])

    # ==================== TESTS PARA LISTAR PRODUCTOS ====================
    
    @patch('app.controllers.inventario_controller.InventarioService')
    def test_listar_productos_exitoso(self, mock_inventario_service):
        """Test: Listar todos los productos"""
        # Arrange
        productos = [
            {'id': 1, 'nombre': 'Producto A', 'precio': 10.00},
            {'id': 2, 'nombre': 'Producto B', 'precio': 20.00},
            {'id': 3, 'nombre': 'Producto C', 'precio': 15.00}
        ]
        mock_inventario_service.listar_productos.return_value = productos
        
        # Act
        resultado = InventarioController.listar_productos()
        
        # Assert
        self.assertTrue(resultado['success'])
        self.assertIn('productos', resultado)
        self.assertEqual(len(resultado['productos']), 3)
        mock_inventario_service.listar_productos.assert_called_once()
    
    @patch('app.controllers.inventario_controller.InventarioService')
    def test_listar_productos_vacio(self, mock_inventario_service):
        """Test: Listar cuando no hay productos"""
        # Arrange
        mock_inventario_service.listar_productos.return_value = []
        
        # Act
        resultado = InventarioController.listar_productos()
        
        # Assert
        self.assertTrue(resultado['success'])
        self.assertEqual(len(resultado['productos']), 0)
    
    @patch('app.controllers.inventario_controller.InventarioService')
    def test_listar_productos_con_error(self, mock_inventario_service):
        """Test: Error al listar productos"""
        # Arrange
        mock_inventario_service.listar_productos.side_effect = Exception("Error de base de datos")
        
        # Act
        resultado = InventarioController.listar_productos()
        
        # Assert
        self.assertFalse(resultado['success'])
        self.assertIn("Error", resultado['message'])

    # ==================== TESTS PARA BUSCAR PRODUCTO ====================
    
    @patch('app.controllers.inventario_controller.InventarioService')
    def test_buscar_producto_exitoso(self, mock_inventario_service):
        """Test: Buscar producto por ID exitosamente"""
        # Arrange
        producto = {
            'id': self.producto_id,
            'nombre': self.nombre,
            'precio': self.precio,
            'stock': self.stock
        }
        mock_inventario_service.buscar_producto.return_value = producto
        
        # Act
        resultado = InventarioController.buscar_producto(self.producto_id)
        
        # Assert
        self.assertTrue(resultado['success'])
        self.assertIn('producto', resultado)
        self.assertEqual(resultado['producto']['id'], self.producto_id)
        mock_inventario_service.buscar_producto.assert_called_once_with(self.producto_id)
    
    @patch('app.controllers.inventario_controller.InventarioService')
    def test_buscar_producto_no_encontrado(self, mock_inventario_service):
        """Test: Producto no encontrado"""
        # Arrange
        mock_inventario_service.buscar_producto.return_value = None
        
        # Act
        resultado = InventarioController.buscar_producto(999)
        
        # Assert
        self.assertFalse(resultado['success'])
        self.assertEqual(resultado['message'], 'Producto no encontrado')
    
    @patch('app.controllers.inventario_controller.InventarioService')
    def test_buscar_producto_con_error(self, mock_inventario_service):
        """Test: Error al buscar producto"""
        # Arrange
        mock_inventario_service.buscar_producto.side_effect = Exception("Error de consulta")
        
        # Act
        resultado = InventarioController.buscar_producto(self.producto_id)
        
        # Assert
        self.assertFalse(resultado['success'])
        self.assertIn("Error", resultado['message'])


# ==================== TESTS CON PYTEST ====================

@pytest.fixture
def mock_producto():
    """Fixture: Producto de prueba"""
    producto = Mock()
    producto.id = 1
    producto.nombre = "Producto Test"
    producto.precio = 10.50
    producto.stock = 100
    producto.stock_minimo = 10
    producto.to_dict.return_value = {
        'id': 1,
        'nombre': "Producto Test",
        'precio': 10.50,
        'stock': 100,
        'stock_minimo': 10
    }
    return producto


def test_agregar_producto_con_pytest(mock_producto):
    """Test con pytest: Agregar producto"""
    with patch('app.controllers.inventario_controller.InventarioService') as mock_service:
        mock_service.agregar_producto.return_value = mock_producto
        
        resultado = InventarioController.agregar_producto(
            "Producto Test", 10.50, 100, 10, 1
        )
        
        assert resultado['success'] is True
        assert resultado['message'] == 'Producto agregado exitosamente'
        assert 'producto' in resultado


def test_flujo_completo_inventario():
    """Test con pytest: Flujo completo de gestión de inventario"""
    with patch('app.controllers.inventario_controller.InventarioService') as mock_service:
        # Agregar producto
        mock_producto = Mock()
        mock_producto.to_dict.return_value = {'id': 1, 'stock': 100}
        mock_service.agregar_producto.return_value = mock_producto
        
        resultado_agregar = InventarioController.agregar_producto(
            "Producto", 10.00, 100, 10, 1
        )
        assert resultado_agregar['success'] is True
        
        # Agregar stock
        mock_producto.stock = 150
        mock_service.agregar_stock.return_value = mock_producto
        
        resultado_stock = InventarioController.agregar_stock(1, 50)
        assert resultado_stock['success'] is True
        
        # Buscar producto
        mock_service.buscar_producto.return_value = {'id': 1, 'stock': 150}
        
        resultado_buscar = InventarioController.buscar_producto(1)
        assert resultado_buscar['success'] is True


@pytest.mark.parametrize("stock,stock_minimo,debe_alertar", [
    (5, 10, True),   # Stock bajo
    (10, 10, True),  # Stock en mínimo
    (15, 10, False), # Stock suficiente
    (0, 5, True)     # Stock agotado
])
def test_alertas_stock_diferentes_casos(stock, stock_minimo, debe_alertar):
    """Test con pytest: Diferentes casos de alertas de stock"""
    with patch('app.controllers.inventario_controller.InventarioService') as mock_service:
        if debe_alertar:
            productos = [{'stock': stock, 'stock_minimo': stock_minimo}]
        else:
            productos = []
        
        mock_service.obtener_alertas_stock.return_value = productos
        
        resultado = InventarioController.obtener_alertas_stock()
        
        assert resultado['success'] is True
        if debe_alertar:
            assert resultado['total'] > 0
        else:
            assert resultado['total'] == 0


if __name__ == '__main__':
    # Ejecutar tests con unittest
    unittest.main()
