"""
Pruebas unitarias para ProveedorController
"""
import unittest
from unittest.mock import Mock, patch
from app.controllers.proveedor_controller import ProveedorController

class TestProveedorController(unittest.TestCase):
    """Suite de pruebas para ProveedorController"""

    def setUp(self):
        """Configuración inicial para cada test"""
        self.proveedor_data = {
            'id': 1,
            'nombre': 'Distribuidora Test',
            'telefono': '0991234567',
            'direccion': 'Calle Falsa 123',
            'activo': 1
        }

    @patch('app.controllers.proveedor_controller.ProveedorService')
    def test_agregar_proveedor_exito(self, mock_service):
        """Test: Agregar proveedor exitosamente"""
        # Arrange
        # El controller espera un objeto que tenga método to_dict()
        mock_proveedor_obj = Mock()
        mock_proveedor_obj.to_dict.return_value = self.proveedor_data
        mock_service.agregar_proveedor.return_value = mock_proveedor_obj

        # Act
        resultado = ProveedorController.agregar_proveedor('Distribuidora Test', '0991234567', 'Calle Falsa 123')

        # Assert
        mock_service.agregar_proveedor.assert_called_once_with('Distribuidora Test', '0991234567', 'Calle Falsa 123')
        self.assertTrue(resultado['success'])
        self.assertEqual(resultado['message'], 'Proveedor agregado exitosamente')
        self.assertEqual(resultado['proveedor'], self.proveedor_data)

    @patch('app.controllers.proveedor_controller.ProveedorService')
    def test_agregar_proveedor_error(self, mock_service):
        """Test: Error al agregar proveedor (excepción controlada)"""
        # Arrange
        mock_service.agregar_proveedor.side_effect = Exception("Error de validación")

        # Act
        resultado = ProveedorController.agregar_proveedor('', '', '')

        # Assert
        self.assertFalse(resultado['success'])
        self.assertEqual(resultado['message'], "Error de validación")

    @patch('app.controllers.proveedor_controller.ProveedorService')
    def test_actualizar_proveedor_exito(self, mock_service):
        """Test: Actualizar proveedor exitosamente"""
        # Arrange
        mock_proveedor_obj = Mock()
        mock_proveedor_obj.to_dict.return_value = self.proveedor_data
        mock_service.actualizar_proveedor.return_value = mock_proveedor_obj

        # Act
        resultado = ProveedorController.actualizar_proveedor(1, 'Nuevo Nombre', 'Tel', 'Dir')

        # Assert
        mock_service.actualizar_proveedor.assert_called_once_with(1, 'Nuevo Nombre', 'Tel', 'Dir')
        self.assertTrue(resultado['success'])
        self.assertEqual(resultado['message'], 'Proveedor actualizado exitosamente')

    @patch('app.controllers.proveedor_controller.ProveedorService')
    def test_actualizar_proveedor_error(self, mock_service):
        """Test: Error al actualizar proveedor"""
        # Arrange
        mock_service.actualizar_proveedor.side_effect = Exception("No encontrado")

        # Act
        resultado = ProveedorController.actualizar_proveedor(999, 'A', 'B', 'C')

        # Assert
        self.assertFalse(resultado['success'])
        self.assertEqual(resultado['message'], "No encontrado")

    @patch('app.controllers.proveedor_controller.ProveedorService')
    def test_eliminar_proveedor_exito(self, mock_service):
        """Test: Eliminar proveedor exitosamente"""
        # Arrange
        mock_service.eliminar_proveedor.return_value = True

        # Act
        resultado = ProveedorController.eliminar_proveedor(1)

        # Assert
        mock_service.eliminar_proveedor.assert_called_once_with(1)
        self.assertTrue(resultado['success'])
        self.assertEqual(resultado['message'], 'Proveedor eliminado exitosamente')

    @patch('app.controllers.proveedor_controller.ProveedorService')
    def test_eliminar_proveedor_error(self, mock_service):
        """Test: Error al eliminar proveedor"""
        # Arrange
        mock_service.eliminar_proveedor.side_effect = Exception("No se pudo eliminar")

        # Act
        resultado = ProveedorController.eliminar_proveedor(1)

        # Assert
        self.assertFalse(resultado['success'])
        self.assertEqual(resultado['message'], "No se pudo eliminar")

    @patch('app.controllers.proveedor_controller.ProveedorService')
    def test_listar_proveedores_exito(self, mock_service):
        """Test: Listar proveedores exitosamente"""
        # Arrange
        mock_service.listar_proveedores.return_value = [self.proveedor_data]

        # Act
        resultado = ProveedorController.listar_proveedores()

        # Assert
        mock_service.listar_proveedores.assert_called_once()
        self.assertTrue(resultado['success'])
        self.assertEqual(len(resultado['proveedores']), 1)

    @patch('app.controllers.proveedor_controller.ProveedorService')
    def test_listar_proveedores_error(self, mock_service):
        """Test: Error al listar proveedores"""
        # Arrange
        mock_service.listar_proveedores.side_effect = Exception("Error DB")

        # Act
        resultado = ProveedorController.listar_proveedores()

        # Assert
        self.assertFalse(resultado['success'])
        self.assertEqual(resultado['message'], "Error DB")

    @patch('app.controllers.proveedor_controller.ProveedorService')
    def test_buscar_proveedor_exito(self, mock_service):
        """Test: Buscar proveedor existente"""
        # Arrange
        mock_service.buscar_proveedor.return_value = self.proveedor_data

        # Act
        resultado = ProveedorController.buscar_proveedor(1)

        # Assert
        mock_service.buscar_proveedor.assert_called_once_with(1)
        self.assertTrue(resultado['success'])
        self.assertEqual(resultado['proveedor'], self.proveedor_data)

    @patch('app.controllers.proveedor_controller.ProveedorService')
    def test_buscar_proveedor_no_encontrado(self, mock_service):
        """Test: Buscar proveedor que no existe (retorna None service)"""
        # Arrange
        mock_service.buscar_proveedor.return_value = None

        # Act
        resultado = ProveedorController.buscar_proveedor(999)

        # Assert
        self.assertFalse(resultado['success'])
        self.assertEqual(resultado['message'], 'Proveedor no encontrado')

    @patch('app.controllers.proveedor_controller.ProveedorService')
    def test_buscar_proveedor_error(self, mock_service):
        """Test: Error inesperado al buscar proveedor"""
        # Arrange
        mock_service.buscar_proveedor.side_effect = Exception("Error fatal")

        # Act
        resultado = ProveedorController.buscar_proveedor(1)

        # Assert
        self.assertFalse(resultado['success'])
        self.assertEqual(resultado['message'], "Error fatal")

if __name__ == '__main__':
    unittest.main()