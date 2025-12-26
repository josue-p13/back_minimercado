"""
Pruebas unitarias para ProveedorService
"""
import unittest
from unittest.mock import Mock, patch
from app.services.proveedor_service import ProveedorService
from app.models.proveedor import Proveedor

class TestProveedorService(unittest.TestCase):
    """Suite de pruebas para ProveedorService"""

    def setUp(self):
        """Configuración inicial para cada test"""
        self.proveedor_data = {
            'id': 1,
            'nombre': 'Distribuidora Test',
            'telefono': '0991234567',
            'direccion': 'Calle Falsa 123',
            'activo': 1
        }
        self.proveedor = Proveedor(**self.proveedor_data)

    @patch('app.services.proveedor_service.ProveedorRepository')
    def test_agregar_proveedor_exito(self, mock_repo):
        """Test: Agregar un proveedor correctamente"""
        # Arrange
        mock_repo.crear.return_value = self.proveedor

        # Act
        resultado = ProveedorService.agregar_proveedor('Distribuidora Test', '0991234567', 'Calle Falsa 123')

        # Assert
        mock_repo.crear.assert_called_once()
        self.assertIsInstance(resultado, Proveedor)
        self.assertEqual(resultado.nombre, 'Distribuidora Test')

    def test_agregar_proveedor_error_nombre_vacio(self):
        """Test: Error al agregar proveedor sin nombre"""
        # Act & Assert
        with self.assertRaises(Exception) as context:
            ProveedorService.agregar_proveedor('', '0991234567', 'Calle Falsa 123')
        
        self.assertEqual(str(context.exception), "El nombre del proveedor es obligatorio")

    @patch('app.services.proveedor_service.ProveedorRepository')
    def test_actualizar_proveedor_exito(self, mock_repo):
        """Test: Actualizar un proveedor existente"""
        # Arrange
        mock_repo.obtener_por_id.return_value = self.proveedor

        # Act
        resultado = ProveedorService.actualizar_proveedor(1, 'Nuevo Nombre', '099888', 'Nueva Dir')

        # Assert
        mock_repo.obtener_por_id.assert_called_once_with(1)
        mock_repo.actualizar.assert_called_once()
        self.assertEqual(resultado.nombre, 'Nuevo Nombre')
        self.assertEqual(resultado.telefono, '099888')

    @patch('app.services.proveedor_service.ProveedorRepository')
    def test_actualizar_proveedor_no_existe(self, mock_repo):
        """Test: Error al actualizar un proveedor que no existe"""
        # Arrange
        mock_repo.obtener_por_id.return_value = None

        # Act & Assert
        with self.assertRaises(Exception) as context:
            ProveedorService.actualizar_proveedor(999, 'Nombre', 'Tel', 'Dir')
        
        self.assertEqual(str(context.exception), "Proveedor no encontrado")
        mock_repo.actualizar.assert_not_called()

    @patch('app.services.proveedor_service.ProveedorRepository')
    def test_eliminar_proveedor_exito(self, mock_repo):
        """Test: Eliminar un proveedor existente"""
        # Arrange
        mock_repo.obtener_por_id.return_value = self.proveedor

        # Act
        resultado = ProveedorService.eliminar_proveedor(1)

        # Assert
        mock_repo.obtener_por_id.assert_called_once_with(1)
        mock_repo.eliminar.assert_called_once_with(1)
        self.assertTrue(resultado)

    @patch('app.services.proveedor_service.ProveedorRepository')
    def test_eliminar_proveedor_no_existe(self, mock_repo):
        """Test: Error al eliminar un proveedor que no existe"""
        # Arrange
        mock_repo.obtener_por_id.return_value = None

        # Act & Assert
        with self.assertRaises(Exception) as context:
            ProveedorService.eliminar_proveedor(999)
        
        self.assertEqual(str(context.exception), "Proveedor no encontrado")
        mock_repo.eliminar.assert_not_called()

    @patch('app.services.proveedor_service.ProveedorRepository')
    def test_listar_proveedores(self, mock_repo):
        """Test: Listar todos los proveedores (retorna dicts)"""
        # Arrange
        mock_repo.listar.return_value = [self.proveedor]

        # Act
        resultado = ProveedorService.listar_proveedores()

        # Assert
        mock_repo.listar.assert_called_once()
        self.assertIsInstance(resultado, list)
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0]['nombre'], 'Distribuidora Test') # Verifica que sea dict

    @patch('app.services.proveedor_service.ProveedorRepository')
    def test_buscar_proveedor_exito(self, mock_repo):
        """Test: Buscar proveedor existente (retorna dict)"""
        # Arrange
        mock_repo.obtener_por_id.return_value = self.proveedor

        # Act
        resultado = ProveedorService.buscar_proveedor(1)

        # Assert
        mock_repo.obtener_por_id.assert_called_once_with(1)
        self.assertIsInstance(resultado, dict)
        self.assertEqual(resultado['id'], 1)

    @patch('app.services.proveedor_service.ProveedorRepository')
    def test_buscar_proveedor_no_existe(self, mock_repo):
        """Test: Buscar proveedor inexistente (retorna None)"""
        # Arrange
        mock_repo.obtener_por_id.return_value = None

        # Act
        resultado = ProveedorService.buscar_proveedor(999)

        # Assert
        mock_repo.obtener_por_id.assert_called_once_with(999)
        self.assertIsNone(resultado)

if __name__ == '__main__':
    unittest.main()